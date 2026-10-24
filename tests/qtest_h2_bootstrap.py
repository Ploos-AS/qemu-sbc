#!/usr/bin/env python3
"""Smoke-test independent H2+ CPU/RAM bootstrap using QTest.

No H2+ GIC, UART or guest boot is claimed by this test.
"""
import argparse
import select
import subprocess
import os
import sys


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--qemu", required=True)
    args = p.parse_args()
    cmd = [args.qemu, "-machine", "orangepi-zero-lts-h2", "-m", "256M",
           "-qtest", "stdio", "-display", "none", "-monitor", "none",
           "-serial", "none", "-S", "-nodefaults"]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=False, bufsize=0)
    try:
        assert proc.stdin is not None and proc.stdout is not None
        proc.stdin.write(b"writel 0x40000000 0x1234abcd\n")
        proc.stdin.flush()
        # QTest is a long-lived protocol: do not wait for QEMU to exit on EOF.
        # Read one response, then terminate the emulator explicitly.
        ready, _, _ = select.select([proc.stdout], [], [], 15)
        if not ready:
            raise RuntimeError("H2+ QTest RAM read timed out")
        reply = os.read(proc.stdout.fileno(), 256).decode("ascii", errors="replace").strip()
        if reply != "OK":
            raise RuntimeError(f"RAM write failed: {reply!r}")
        proc.stdin.write(b"readl 0x40000000\n")
        proc.stdin.flush()
        ready, _, _ = select.select([proc.stdout], [], [], 15)
        if not ready:
            raise RuntimeError("H2+ QTest RAM read timed out")
        reply = os.read(proc.stdout.fileno(), 256).decode("ascii", errors="replace").strip()
        if not reply.startswith("OK ") or int(reply.split()[1], 0) != 0x1234ABCD:
            raise RuntimeError(f"RAM readback mismatch: {reply!r}")
        # GICv2 distributor ID register: ARM GICv2 returns architecture ID.
        # This probes an actual MMIO device, not just an unmapped zero page.
        proc.stdin.write(b"readl 0x01c81fe8\n")
        proc.stdin.flush()
        ready, _, _ = select.select([proc.stdout], [], [], 15)
        if not ready:
            raise RuntimeError("H2+ GIC distributor ID read timed out")
        reply = proc.stdout.readline().strip()
        if not reply.startswith("OK "):
            raise RuntimeError(f"GIC distributor ID read failed: {reply!r}")
        gic_id = int(reply.split()[1], 0)
        if gic_id == 0:
            raise RuntimeError("GIC distributor ID is zero; device may be unmapped")

    finally:
        if proc.poll() is None:
            proc.terminate()
        try:
            proc.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.communicate()
    print("PASS: independent H2+ machine launched; RAM write/readback through QTest")
    print("PASS: GICv2 distributor ID register accessible")
    print("NOTE: GIC interrupt delivery, UART and guest boot not yet tested")


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
