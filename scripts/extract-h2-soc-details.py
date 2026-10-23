#!/usr/bin/env python3
"""Extract raw reg and interrupts cells from selected inherited Linux DTSI nodes.

Not a full DTS parser: only handles literal numeric cells, no preprocessing.
"""
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
    m = re.search(rf"(?m)^\s*{label}:\s*{kind}@([0-9a-fA-F]+)\s*\{{", text)
    if not m:
        raise SystemExit(f"FAIL: missing {label} node")
    start = m.end()
    depth = 1
    i = start
    while i < len(text) and depth:
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
        i += 1
    if depth:
        raise SystemExit(f"FAIL: unclosed {label} node")
    body = text[start:i-1]
    properties = {}
    for prop in ("reg", "interrupts"):
        match = re.search(rf"(?m)^\s*{prop}\s*=\s*(.*?);", body, re.S)
        if not match:
            properties[prop] = None
            continue
        raw = match.group(1).strip()
        groups = re.findall(r"<([^<>]*)>", raw)
        cells = [group.split() for group in groups]
        properties[prop] = {"raw": raw, "cells": cells}
    peripherals[label] = {"unit_address": f"0x{int(m.group(1),16):08x}", **properties}
    print(f"{label}: reg={properties['reg']} interrupts={properties['interrupts']}")
args.output.write_text(json.dumps({"sources": [str(x) for x in args.sources], "peripherals": peripherals}, indent=2) + "\n")
print("NOTE: raw DTSI cells, not translated GIC IRQ or verified H2+ values")
