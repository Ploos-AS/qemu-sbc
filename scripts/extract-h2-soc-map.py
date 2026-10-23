#!/usr/bin/env python3
"""Extract selected MMIO bases from Linux's H3 + shared H3/H5 DTSI sources."""
import argparse
import json
import re
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument("dtsi", type=Path, nargs="+")
p.add_argument("--output", type=Path, default=Path("h2-soc-registers.json"))
a = p.parse_args()
if len(a.dtsi) < 2:
    p.error("pass both sun8i-h3.dtsi and sunxi-h3-h5.dtsi")
source_text = "\n".join(path.read_text() for path in a.dtsi)
if '#include "sunxi-h3-h5.dtsi"' not in a.dtsi[0].read_text():
    raise SystemExit("FAIL: unexpected H3 shared-DTSI inclusion")
s = re.sub(r"/\*.*?\*/", "", source_text, flags=re.S)
wanted = {"uart0": "serial", "mmc0": "mmc", "emac": "ethernet"}
found = {}
for label, prefix in wanted.items():
    pattern = rf"(?m)^\s*{label}:\s*{prefix}@([0-9a-fA-F]+)\s*\{{"
    matches = re.findall(pattern, s)
    if len(matches) != 1:
        raise SystemExit(f"FAIL: expected one {label} node, found {len(matches)}")
    address = int(matches[0], 16)
    if not 0x01000000 <= address <= 0x10000000:
        raise SystemExit(f"FAIL: implausible {label} address 0x{address:x}")
    found[label] = {"base": f"0x{address:08x}"}
    print(f"PASS: {label} base = 0x{address:08x}")
a.output.write_text(json.dumps({"sources": [str(x) for x in a.dtsi], "peripherals": found}, indent=2) + "\n")
print("NOTE: inherited DTSI bases only, not verified H2+ hardware behavior")
