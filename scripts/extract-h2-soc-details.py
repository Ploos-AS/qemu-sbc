#!/usr/bin/env python3
"""Extract and validate raw reg/interrupt cells from pinned inherited Linux DTSI."""
import argparse
import json
import re
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("sources", nargs="+", type=Path)
parser.add_argument("--output", type=Path, default=Path("h2-soc-details.json"))
args = parser.parse_args()
text = "\n".join(re.sub(r"/\*.*?\*/", "", p.read_text(), flags=re.S) for p in args.sources)
peripherals = {}
for label, kind in (("uart0", "serial"), ("mmc0", "mmc"), ("emac", "ethernet")):
    nodes = list(re.finditer(rf"(?m)^\s*{label}:\s*{kind}@([0-9a-fA-F]+)\s*\{{", text))
    if len(nodes) != 1:
        raise SystemExit(f"FAIL: expected exactly one {label} node, got {len(nodes)}")
    m = nodes[0]
    depth, i = 1, m.end()
    while i < len(text) and depth:
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
        i += 1
    if depth:
        raise SystemExit(f"FAIL: unclosed {label} node")
    body = text[m.end():i-1]
    properties = {}
    for prop in ("reg", "interrupts"):
        matches = re.findall(rf"(?m)(?:^|;)\s*{prop}\s*=\s*(.*?);", body, re.S)
        if len(matches) != 1:
            raise SystemExit(f"FAIL: expected one {label}.{prop}, got {len(matches)}")
        raw = matches[0].strip()
        groups = re.findall(r"<([^<>]*)>", raw)
        if not groups or not all(g.split() for g in groups):
            raise SystemExit(f"FAIL: empty or non-cell {label}.{prop}")
        if re.sub(r"<[^<>]*>", "", raw).strip().strip(","):
            raise SystemExit(f"FAIL: unexpected syntax in {label}.{prop}: {raw}")
        properties[prop] = {"raw": raw, "cells": [g.split() for g in groups]}
    peripherals[label] = {"unit_address": f"0x{int(m.group(1), 16):08x}", **properties}
    print(f"PASS: {label} reg and interrupts present")
args.output.write_text(json.dumps({"sources": [str(x) for x in args.sources], "peripherals": peripherals}, indent=2) + "\n")
print("NOTE: raw DTSI cells, not translated GIC IRQ or verified H2+ values")
