#!/usr/bin/env python3
"""Regression guard: H3-backed prototype must not be mistaken for a 256 MiB H2+ board."""
import argparse
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("binary", type=Path)
args = parser.parse_args()
binary = str(args.binary.resolve())
cmd = [binary, "-machine", "orangepi-zero-lts-proto", "-m", "256M",
       "-display", "none", "-nographic", "-nodefaults", "-monitor", "none"]
result = subprocess.run(cmd, text=True, capture_output=True, timeout=15)
if result.returncode == 0:
    raise SystemExit("FAIL: 256 MiB unexpectedly accepted by H3-backed prototype")
if "1GiB of RAM" not in result.stderr:
    raise SystemExit(f"FAIL: unexpected error instead of H3 RAM guard: {result.stderr}")
print("PASS: research prototype rejects 256 MiB; still H3-based")
print("NOTE: this negative test is NOT H2+ RAM support")
