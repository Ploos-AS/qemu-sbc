#!/usr/bin/env python3
"""Add UART0 helper to QEMU 10.0.0 ARM Meson build without machine registration."""
import argparse
from pathlib import Path

ENTRY = "arm_ss.add(when: 'CONFIG_ALLWINNER_H3', if_true: files('allwinner-h3.c', 'orangepi.c'))"
ADDITION = "arm_ss.add(when: 'CONFIG_ALLWINNER_H3', if_true: files('allwinner-h2-uart0.c'))"

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--qemu-src", type=Path, required=True)
    p.add_argument("--apply", action="store_true")
    args = p.parse_args()
    root = args.qemu_src
    meson = root / "hw/arm/meson.build"
    uart = root / "hw/arm/allwinner-h2-uart0.c"
    if not meson.is_file() or not uart.is_file():
        p.error("missing QEMU ARM Meson file or H2+ UART0 helper; inject helper first")
    source = meson.read_text()
    if source.count(ENTRY) != 1:
        p.error("unexpected QEMU ARM Meson layout; refusing to patch")
    if source.count(ADDITION) > 1:
        p.error("duplicate H2+ UART0 build entry")
    if ADDITION in source:
        print("UNCHANGED: H2+ UART0 helper already registered in Meson")
        return
    if args.apply:
        meson.write_text(source.replace(ENTRY, ENTRY + "\n" + ADDITION))
        print("UPDATED:", meson)
    else:
        print("DRY RUN: would add H2+ UART0 helper to", meson)
    print("NOTE: build-only helper; no H2+ machine registration or guest test")

if __name__ == "__main__":
    main()
