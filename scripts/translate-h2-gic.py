#!/usr/bin/env python3
"""Translate Linux GIC three-cell SPI/PPI specifiers, without claiming H2+ validation."""
import argparse
import json
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument("inventory", type=Path)
p.add_argument("--output", type=Path, default=Path("h2-gic-irqs.json"))
args = p.parse_args()
inventory = json.loads(args.inventory.read_text())
translated = {}
for name, entry in inventory["peripherals"].items():
    groups = entry["interrupts"]["cells"]
    if len(groups) != 1 or len(groups[0]) != 3:
        raise SystemExit(f"FAIL: {name} requires one 3-cell GIC interrupt specifier")
    try:
        irq_type, irq_index, flags = (int(x, 0) for x in groups[0])
    except ValueError as exc:
        raise SystemExit(f"FAIL: {name} has unresolved interrupt macros: {exc}")
    if irq_type not in (0, 1) or irq_index < 0 or flags < 0:
        raise SystemExit(f"FAIL: invalid GIC specifier for {name}")
    if irq_type == 0:
        gic_id = irq_index + 32
    else:
        if irq_index > 15:
            raise SystemExit(f"FAIL: {name} PPI index exceeds 15")
        gic_id = irq_index + 16
    translated[name] = {"kind": "SPI" if irq_type == 0 else "PPI",
                        "index": irq_index, "gic_interrupt_id": gic_id,
                        "flags": flags}
    print(f"PASS: {name} GIC interrupt ID {gic_id}")
args.output.write_text(json.dumps({"source": str(args.inventory),
                                   "interrupts": translated}, indent=2) + "\n")
print("NOTE: GIC binding translation only; not proof of H2+ IRQ wiring")
