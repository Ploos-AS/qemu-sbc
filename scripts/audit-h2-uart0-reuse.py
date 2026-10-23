#!/usr/bin/env python3
"""Audit UART0 reuse against pinned QEMU H3 source; do not claim H2+ support."""
import argparse
import json
import re
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument("qemu_h3", type=Path)
p.add_argument("wiring_plan", type=Path)
p.add_argument("--output", type=Path, default=Path("h2-uart0-reuse.json"))
args = p.parse_args()
source = args.qemu_h3.read_text()
plan = json.loads(args.wiring_plan.read_text())
uart = plan["devices"]["uart0"]
base = int(uart["mmio_base"], 0)
# Match the H3 map entry and UART0-specific serial_mm_init call separately.
map_match = re.search(r"\[AW_H3_DEV_UART0\]\s*=\s*(0x[0-9a-fA-F]+)", source)
call = re.search(
    r"serial_mm_init\(get_system_memory\(\),\s*"
    r"s->memmap\[AW_H3_DEV_UART0\],\s*(\d+),\s*"
    r"qdev_get_gpio_in\(DEVICE\(&s->gic\),\s*AW_H3_GIC_SPI_UART0\)",
    source, re.S)
spi_match = re.search(r"AW_H3_GIC_SPI_UART0\s*=\s*(\d+)", source)
if not map_match or not call or not spi_match:
    raise SystemExit("FAIL: pinned QEMU H3 UART0 mapping/wiring pattern changed")
if int(map_match.group(1), 16) != base:
    raise SystemExit("FAIL: Linux-inherited UART0 base differs from QEMU H3")
if int(call.group(1)) != 2:
    raise SystemExit("FAIL: unexpected QEMU serial register access shift")
if int(spi_match.group(1)) != uart["gic_spi_index"]:
    raise SystemExit("FAIL: Linux-inherited UART0 SPI differs from QEMU H3")
result = {"qemu_reference": "QEMU v10.0.0 hw/arm/allwinner-h3.c",
          "linux_evidence": "Linux v6.12 inherited DTSI",
          "uart0_mmio_base": uart["mmio_base"],
          "serial_mm_init_regshift": int(call.group(1)),
          "gic_spi_index": uart["gic_spi_index"],
          "qemu_uart_reuse_candidate": True,
          "h2_hardware_verified": False,
          "h2_uart_implemented": False}
args.output.write_text(json.dumps(result, indent=2) + "\n")
print("PASS: H3 UART0 QEMU source matches inherited Linux MMIO/SPI evidence")
print("NOTE: compatibility candidate only; H2+ UART not implemented")
