#!/usr/bin/env python3
"""QTest UART0 MMIO smoke test against QEMU's existing H3 reference board.

This is NOT a test of a separate H2+ SoC or H2+ UART wiring.
"""
import argparse
import subprocess
import sys


def command(proc, line):
    assert proc.stdin and proc.stdout
    proc.stdin.write(line + "\n")
    proc.stdin.flush()
    reply = proc.stdout.readline().strip()
    if not reply:
        raise RuntimeError(f"QTest returned no reply for {line!r}")
    if not reply.startswith("OK"):
        raise RuntimeError(f"QTest rejected {line!r}: {reply}")
    return reply


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--qemu", required=True)
    args = parser.parse_args()
    argv = [args.qemu, "-machine", "orangepi-pc", "-qtest", "stdio",
            "-display", "none", "-monitor", "none", "-serial", "null",
            "-S", "-nodefaults"]
    proc = subprocess.Popen(argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True, bufsize=1)
    try:
        # 16550 UART0 LSR register offset 5 * register stride 4.
        lsr = command(proc, "readl 0x01c28014")
        parts = lsr.split()
        if len(parts) < 2:
            raise RuntimeError(f"Missing UART0 LSR value: {lsr}")
        value = int(parts[1], 0)
        if value & 0x60 != 0x60:
            raise RuntimeError(f"UART0 transmitter not ready (LSR=0x{value:08x})")
        # UART0 scratch register offset 7 * 4: test writable register path.
        command(proc, "writel 0x01c2801c 0x5a")
        scratch = command(proc, "readl 0x01c2801c")
        returned = int(scratch.split()[1], 0) & 0xff
        if returned != 0x5a:
            raise RuntimeError(f"UART0 scratch register mismatch: 0x{returned:02x}")
        print(f"PASS: QEMU H3 UART0 MMIO LSR=0x{value:08x}, SCR=0x{returned:02x}")
        print("NOTE: H3 reference board only; no H2+ runtime validation")
    finally:
        if proc.poll() is None:
            proc.terminate()
            try:
                proc.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.communicate()


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, ValueError, OSError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        sys.exit(1)
