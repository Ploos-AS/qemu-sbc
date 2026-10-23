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
        stdout, stderr = proc.communicate(input="readl 0x40000000\n", timeout=15)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.communicate()
        raise RuntimeError("H2+ QTest startup timed out")
    if "OK " not in stdout:
        raise RuntimeError(f"no RAM MMIO reply; exit={proc.returncode}; stderr={stderr[-1500:]}")
    print("PASS: independent H2+ machine launched; RAM read through QTest")
    print("NOTE: GIC/UART/boot not yet implemented")


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
