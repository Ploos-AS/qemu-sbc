#!/usr/bin/env python3
"""Audit QEMU v10.0.0 H3 CPU/GIC bootstrap as an H2+ design reference.

This does not instantiate or register an H2+ machine.
"""
import argparse
import json
import re
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument("h3_source", type=Path)
p.add_argument("--output", type=Path, default=Path("h2-cpu-gic-reference.json"))
args = p.parse_args()
source = args.h3_source.read_text()
checks = {
    "cortex_a7_cpu": r'ARM_CPU_TYPE_NAME\("cortex-a7"\)',
    "gic_child": r'object_initialize_child\(obj,\s*"gic",',
    "gic_realize": r'sysbus_realize\(SYS_BUS_DEVICE\(&s->gic\)',
    "cpu_irq_to_gic": r'qdev_get_gpio_in\(cpudev,\s*ARM_CPU_IRQ\)',
    "cpu_fiq_to_gic": r'qdev_get_gpio_in\(cpudev,\s*ARM_CPU_FIQ\)',
    "gic_timer_input": r'AW_H3_GIC_PPI_SECTIMER',
    "uart0_gic_input": r'qdev_get_gpio_in\(DEVICE\(&s->gic\),\s*AW_H3_GIC_SPI_UART0\)',
}
missing = [name for name, pattern in checks.items() if not re.search(pattern, source, re.S)]
if missing:
    raise SystemExit("FAIL: pinned H3 CPU/GIC reference changed: " + ", ".join(missing))
report = {
    "reference": "QEMU v10.0.0 hw/arm/allwinner-h3.c",
    "checks": {name: True for name in checks},
    "h2_cpu_gic_implemented": False,
    "h2_machine_registered": False,
    "h2_hardware_verified": False,
    "next_implementation": "independent H2+ CPU, RAM and GIC initialization",
}
args.output.write_text(json.dumps(report, indent=2) + "\n")
print("PASS: H3 CPU/GIC reference patterns identified; H2+ remains unimplemented")
