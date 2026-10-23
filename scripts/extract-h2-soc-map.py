#!/usr/bin/env python3
"""Extract selected MMIO and interrupt tuples from a pinned Linux SoC DTS."""
import argparse
import json
import re
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument("dtsi", type=Path)
p.add_argument("--output", type=Path, default=Path("h2-soc-registers.json"))
a = p.parse_args()
s = re.sub(r"/\*.*?\*/", "", a.dtsi.read_text(), flags=re.S)
wanted = {"uart0": "serial", "mmc0": "mmc", "emac": "ethernet"}
found = {}
for label, prefix in wanted.items():
    matches = re.findall(r"(?m)^\s*([\w-]+):\s*("+prefix+r")@([0-9a-fA-F]+)\s*\{", s)
    candidates = [(node, int(addr, 16)) for node, _, addr in matches if node == label]
    if len(candidates) != 1:
        raise SystemExit(f"FAIL: expected one {label} node, found {len(candidates)}")
    node, address = candidates[0]
    if address < 0x01000000 or address > 0x10000000:
        raise SystemExit(f"FAIL: implausible {label} MMIO address 0x{address:x}")
    found[label] = {"node": node, "base": f"0x{address:08x}"}
    print(f"PASS: {label} base = 0x{address:08x}")
a.output.write_text(json.dumps({"source": str(a.dtsi), "peripherals": found}, indent=2) + "\n")
print("NOTE: extracted from H3-inherited DTSI; H2+ MMIO equivalence still needs validation")
