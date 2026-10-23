#!/usr/bin/env python3
"""Smoke-test independent H2+ CPU/RAM bootstrap using QTest.

No H2+ GIC, UART or guest boot is claimed by this test.
"""
import argparse
import subprocess
import sys


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--qemu", required=True)
    args = p.parse_args()
    cmd = [args.qemu, "-machine", "orangepi-zero-lts-h2", "-m", "256M",
           "-qtest", "stdio", "-display", "none", "-monitor", "none",
           "-serial", "none", "-S", "-nodefaults"]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True)
    try:
        assert proc.stdin is not None and proc.stdout is not None
        proc.stdin.write("readl 0x40000000\n")
        proc.stdin.flush()
        # QTest is a long-lived protocol: do not wait for QEMU to exit on EOF.
        # Read one response, then terminate the emulator explicitly.
        import select
        ready, _, _ = select.select([proc.stdout], [], [], 15)
        if not ready:
            raise RuntimeError("H2+ QTest RAM read timed out")
        reply = proc.stdout.readline().strip()
        if not reply.startswith("OK "):
            raise RuntimeError(f"unexpected RAM reply: {reply!r}")
        int(reply.split()[1], 0)
    finally:
        if proc.poll() is None:
            proc.terminate()
        try:
            proc.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.communicate()
    print("PASS: independent H2+ machine launched; RAM read through QTest")
    print("NOTE: GIC/UART/boot not yet implemented")


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
