#!/usr/bin/env python3
"""Prove actual Cortex-A7 execution using a guest-written RAM mailbox."""
import argparse
import json
import select
import subprocess
import sys
import time
import tempfile
from pathlib import Path

MAILBOX = 0x40001000
IRQ_MAILBOX = 0x40001004
IRQ_MAGIC = 0x48324931
RETURN_MAILBOX = 0x40001008
RETURN_MAGIC = 0x48325231
TIMER_MAILBOX = 0x4000100c
TIMER_MAGIC = 0x48325431
MAGIC = 0x48325031


def response(proc, timeout=10):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        ready, _, _ = select.select([proc.stdout], [], [], min(1, max(0, deadline - time.monotonic())))
        if not ready:
            continue
        line = proc.stdout.readline()
        if not line:
            raise RuntimeError("QEMU QMP closed unexpectedly")
        message = json.loads(line)
        if "return" in message or "error" in message:
            return message
    raise RuntimeError("QMP response timed out")


def command(proc, execute, arguments=None):
    request = {"execute": execute}
    if arguments is not None:
        request["arguments"] = arguments
    proc.stdin.write(json.dumps(request) + "\n")
    proc.stdin.flush()
    result = response(proc)
    if "error" in result:
        raise RuntimeError(f"QMP {execute} failed: {result['error']}")
    return result["return"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--qemu", required=True)
    parser.add_argument("--kernel", required=True)
    args = parser.parse_args()
    serial_dir = tempfile.TemporaryDirectory(prefix="h2-uart-")
    serial_path = Path(serial_dir.name) / "uart0.log"
    proc = subprocess.Popen(
        [args.qemu, "-machine", "orangepi-zero-lts-h2", "-m", "256M",
         "-kernel", args.kernel, "-accel", "tcg", "-display", "none",
         "-serial", f"file:{serial_path}", "-monitor", "none", "-qmp", "stdio", "-nodefaults"],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, bufsize=1,
    )
    try:
        assert proc.stdin is not None and proc.stdout is not None
        greeting = proc.stdout.readline()
        if not greeting or "QMP" not in json.loads(greeting):
            raise RuntimeError("QMP greeting missing")
        command(proc, "qmp_capabilities")
        deadline = time.monotonic() + 10
        last = ""
        while time.monotonic() < deadline:
            last = command(proc, "human-monitor-command", {
                "command-line": f"xp /1wx 0x{MAILBOX:x}"
            })
            if f"{MAGIC:08x}" in last.lower():
                print("PASS: Cortex-A7 executed guest and wrote H2P1 mailbox")
                serial_deadline = time.monotonic() + 5
                while time.monotonic() < serial_deadline:
                    if serial_path.exists() and b"H2 UART OK\\n" in serial_path.read_bytes():
                        print("PASS: Cortex-A7 transmitted UART0 bytes")
                        irq_deadline = time.monotonic() + 5
                        while time.monotonic() < irq_deadline:
                            irq_value = command(proc, "human-monitor-command", {
                                "command-line": f"xp /1wx 0x{IRQ_MAILBOX:x}"
                            })
                            if f"{IRQ_MAGIC:08x}" in irq_value.lower():
                                print("PASS: Cortex-A7 handled UART0 SPI32 IRQ")
                                return_deadline = time.monotonic() + 5
                                while time.monotonic() < return_deadline:
                                    return_value = command(proc, "human-monitor-command", {
                                        "command-line": f"xp /1wx 0x{RETURN_MAILBOX:x}"
                                    })
                                    if f"{RETURN_MAGIC:08x}" in return_value.lower():
                                        print("PASS: Cortex-A7 returned from IRQ and resumed guest")
                                        timer_deadline = time.monotonic() + 5
                                        while time.monotonic() < timer_deadline:
                                            timer_value = command(proc, "human-monitor-command", {
                                                "command-line": f"xp /1wx 0x{TIMER_MAILBOX:x}"
                                            })
                                            if f"{TIMER_MAGIC:08x}" in timer_value.lower():
                                                print("PASS: Cortex-A7 handled physical generic timer PPI30")
                                                return
                                            time.sleep(0.1)
                                        raise RuntimeError(f"timer PPI30 marker missing: {timer_value!r}")
                                    time.sleep(0.1)
                                raise RuntimeError(f"IRQ entered but guest did not resume: {return_value!r}")
                            time.sleep(0.1)
                        raise RuntimeError(f"UART output passed but IRQ marker missing: {irq_value!r}")
                    time.sleep(0.1)
                raise RuntimeError("guest mailbox passed but UART0 output missing")
            time.sleep(0.1)
        raise RuntimeError(f"guest did not write mailbox 0x{MAGIC:08x}: {last!r}")
    finally:
        proc.terminate()
        try:
            proc.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.communicate()
        serial_dir.cleanup()


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
