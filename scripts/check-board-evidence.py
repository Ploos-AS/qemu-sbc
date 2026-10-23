#!/usr/bin/env python3
"""Offline assertions for board research records; no hardware emulation."""
from pathlib import Path
root = Path(__file__).resolve().parent.parent
delta = (root / "docs/H2-H3-DELTA.md").read_text()
matrix = (root / "docs/BOARD-MATRIX.md").read_text()
required = ["sun8i-h2-plus-orangepi-zero.dts", "sun8i-h3.dtsi", "UART0", "XR819", "SPI NOR", "EMAC"]
missing = [x for x in required if x not in delta]
assert not missing, f"Missing H2+ evidence topics: {missing}"
assert "GL-MT300N-V2" in matrix
assert "orangepi-zero-lts" in matrix
print("PASS: research inventory contains required board topics (not a hardware test)")
