#!/usr/bin/env python3
"""Inject isolated H2+ UART0 helper into a QEMU checkout; no machine registration."""
import argparse
from pathlib import Path

SOURCE = """/*
 * H2+ UART0 candidate wiring helper; not a complete H2+ SoC.
 * Copyright (c) 2026 Ploos AS
 * SPDX-License-Identifier: MIT
 */
#include "qemu/osdep.h"
#include "hw/char/serial-mm.h"
#include "hw/irq.h"
#include "chardev/char.h"
#include "exec/address-spaces.h"

/* Source-derived Linux v6.12 inherited MMIO address. */
#define H2_UART0_BASE 0x01c28000u
#define H2_UART0_GIC_SPI 0u

/*
 * The caller must provide a valid GIC SPI input for H2_UART0_GIC_SPI.
 * Clock/reset, SoC initialization and H2+ validation are still TODO.
 */
void h2_uart0_candidate_init(qemu_irq uart_irq, Chardev *serial_backend)
{
    serial_mm_init(get_system_memory(), H2_UART0_BASE, 2,
                   uart_irq, 115200, serial_backend,
                   DEVICE_LITTLE_ENDIAN);
}
"""
def main():
    p = argparse.ArgumentParser()
    p.add_argument("--qemu-src", required=True, type=Path)
    p.add_argument("--apply", action="store_true")
    args = p.parse_args()
    root = args.qemu_src
    if not (root / "hw/arm/orangepi.c").is_file():
        p.error("expected QEMU source checkout")
    target = root / "hw/arm/allwinner-h2-uart0.c"
    if target.exists():
        if target.read_text() != SOURCE:
            p.error("refusing to overwrite existing H2+ UART source")
        print("UNCHANGED:", target)
    elif args.apply:
        target.write_text(SOURCE)
        print("CREATED:", target)
    else:
        print("DRY RUN:", target)
    print("NOTE: helper is not linked into QEMU or connected to a GIC")

if __name__ == "__main__":
    main()
