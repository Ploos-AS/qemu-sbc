#!/usr/bin/env python3
"""Generate checked UART0 implementation constants from inherited wiring evidence."""
import argparse
import json
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument("plan", type=Path)
p.add_argument("--output", type=Path, default=Path("h2-uart0-constants.h"))
args = p.parse_args()
plan = json.loads(args.plan.read_text())
if plan.get("h2_hardware_verified") is not False or plan.get("qemu_wiring_implemented") is not False:
    raise SystemExit("FAIL: input must be an unverified, unimplemented evidence plan")
uart = plan["devices"]["uart0"]
base = int(uart["mmio_base"], 0)
size = uart["mmio_size"]
spi = uart["gic_spi_index"]
gic_id = uart["gic_interrupt_id"]
if not all(isinstance(x, int) and not isinstance(x, bool) for x in (size, spi, gic_id)):
    raise SystemExit("FAIL: UART0 numeric fields must be integers")
if base <= 0 or size <= 0 or size & (size - 1) or base % size:
    raise SystemExit("FAIL: UART0 MMIO alignment or size invalid")
if spi < 0 or gic_id != spi + 32 or uart["implementation_status"] != "not_implemented":
    raise SystemExit("FAIL: UART0 GIC SPI or implementation status invalid")
out = f"""/* Generated from inherited Linux DTSI evidence; NOT hardware-verified. */
/* Not a functional UART device or an assertion of H2+ emulation support. */
#ifndef QEMU_SBC_H2_UART0_CONSTANTS_H
#define QEMU_SBC_H2_UART0_CONSTANTS_H
#define H2_UART0_MMIO_BASE 0x{base:08x}u
#define H2_UART0_MMIO_SIZE 0x{size:x}u
#define H2_UART0_GIC_SPI_INDEX {spi}u
#define H2_UART0_GIC_INTERRUPT_ID {gic_id}u
#endif
"""
args.output.write_text(out)
print(f"PASS: UART0 evidence constants: MMIO=0x{base:08x}, SPI={spi}, GIC ID={gic_id}")
