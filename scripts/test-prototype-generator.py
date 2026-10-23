#!/usr/bin/env python3
"""Unit test prototype source transformation without QEMU build."""
import subprocess
import sys
import tempfile
from pathlib import Path

script = Path(__file__).with_name("create-h2-prototype.py")
with tempfile.TemporaryDirectory() as d:
    root = Path(d)
    board = root / "hw/arm/orangepi.c"
    board.parent.mkdir(parents=True)
    board.write_text('static void orangepi_machine_init(MachineClass *mc) {}\n'
                     'DEFINE_MACHINE_ARM("orangepi-pc", orangepi_machine_init)\n')
    def run(*args):
        subprocess.run([sys.executable, str(script), "--qemu-src", str(root), *args], check=True)
    run()
    assert "proto" not in board.read_text(), "dry run modified source"
    run("--apply")
    assert board.read_text().count('DEFINE_MACHINE_ARM("orangepi-zero-lts-proto"') == 1
    run("--apply")
    assert board.read_text().count('DEFINE_MACHINE_ARM("orangepi-zero-lts-proto"') == 1
print("PASS: dry run, registration and idempotence")
