#!/usr/bin/env python3
"""Validate machine registration and QMP startup of research prototype."""
import argparse
import json
import subprocess
import sys
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument("binary", type=Path)
args = p.parse_args()
binary = str(args.binary.resolve())
machines = subprocess.run([binary, "-machine", "help"], text=True, capture_output=True, check=True, timeout=15).stdout
assert any(line.strip().split()[0] == "orangepi-zero-lts-proto" for line in machines.splitlines() if line.strip()), "prototype machine not registered"
print("PASS: prototype machine registered")
cmd = [binary, "-M", "orangepi-zero-lts-proto", "-accel", "tcg",
       "-display", "none", "-nographic", "-S", "-monitor", "none",
       "-serial", "none", "-nodefaults", "-qmp", "stdio"]
proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
try:
    stdout, stderr = proc.communicate('{"execute":"qmp_capabilities"}\n{"execute":"quit"}\n', timeout=20)
except subprocess.TimeoutExpired:
    proc.kill()
    stdout, stderr = proc.communicate()
    print(stderr, file=sys.stderr)
    raise RuntimeError("prototype QMP startup timed out")
Path("qmp-output.txt").write_text(stdout + "\nSTDERR:\n" + stderr)
if proc.returncode != 0:
    raise RuntimeError(f"QEMU exited {proc.returncode}: {stderr}")
objects = [json.loads(line) for line in stdout.splitlines() if line.startswith("{")]
assert any("QMP" in o for o in objects), f"QMP greeting absent: {stdout}"
assert any(o.get("return") == {} for o in objects), f"QMP command response absent: {stdout}"
print("PASS: prototype machine starts and responds to QMP")
print("NOTE: H3-backed prototype, not H2+ emulation")
