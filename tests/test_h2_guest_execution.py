#!/usr/bin/env python3
"""Prove actual Cortex-A7 execution using a guest-written RAM mailbox."""
import argparse
import json
import select
import subprocess
import sys
import time

MAILBOX = 0x40001000
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
    proc = subprocess.Popen(
        [args.qemu, "-machine", "orangepi-zero-lts-h2", "-m", "256M",
         "-kernel", args.kernel, "-accel", "tcg", "-display", "none",
         "-serial", "none", "-monitor", "none", "-qmp", "stdio", "-nodefaults"],
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
                return
            time.sleep(0.1)
        raise RuntimeError(f"guest did not write mailbox 0x{MAGIC:08x}: {last!r}")
    finally:
        proc.terminate()
        try:
            proc.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.communicate()


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
