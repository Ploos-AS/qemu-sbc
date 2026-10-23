#!/usr/bin/env python3
"""Join inherited MMIO and GIC inventories into an auditable QEMU wiring plan."""
import argparse
import json
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument("mmio", type=Path)
p.add_argument("gic", type=Path)
p.add_argument("--output", type=Path, default=Path("h2-wiring-plan.json"))
args = p.parse_args()
mmio = json.loads(args.mmio.read_text())["peripherals"]
gic = json.loads(args.gic.read_text())["interrupts"]
required = ("uart0", "mmc0", "emac")
if set(mmio) != set(required) or set(gic) != set(required):
    raise SystemExit("FAIL: MMIO/GIC inventories must contain exactly uart0, mmc0, emac")
devices = {}
used = set()
for name in required:
    address = int(mmio[name]["unit_address"], 0)
    reg_groups = mmio[name]["reg"]["cells"]
    if len(reg_groups) != 1 or len(reg_groups[0]) != 2:
        raise SystemExit(f"FAIL: {name} requires a two-cell reg tuple")
    base, length = (int(cell, 0) for cell in reg_groups[0])
    if base != address or length <= 0:
        raise SystemExit(f"FAIL: {name} MMIO tuple does not match node address")
    irq = gic[name]
    if irq["kind"] != "SPI" or irq["gic_interrupt_id"] != irq["index"] + 32:
        raise SystemExit(f"FAIL: {name} requires a consistent SPI interrupt")
    if irq["gic_interrupt_id"] in used:
        raise SystemExit(f"FAIL: duplicate GIC interrupt ID {irq['gic_interrupt_id']}")
    used.add(irq["gic_interrupt_id"])
    devices[name] = {"mmio_base": f"0x{base:08x}", "mmio_size": length,
                     "gic_spi_index": irq["index"],
                     "gic_interrupt_id": irq["gic_interrupt_id"],
                     "irq_flags": irq["flags"],
                     "implementation_status": "not_implemented"}
    print(f"PASS: {name} MMIO=0x{base:08x} size=0x{length:x} IRQ={irq['gic_interrupt_id']}")
args.output.write_text(json.dumps({"evidence": "inherited Linux DTSI",
                                   "h2_hardware_verified": False,
                                   "qemu_wiring_implemented": False,
                                   "devices": devices}, indent=2) + "\n")
