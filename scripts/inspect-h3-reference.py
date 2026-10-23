#!/usr/bin/env python3
"""Inspect the actual checked-out QEMU H3 machine/SoC source.

This is a source-inspection gate, not an Orange Pi Zero LTS emulator.
"""
import argparse
import re
from pathlib import Path

def inspect(root: Path) -> int:
    board = root / "hw/arm/orangepi.c"
    soc = root / "hw/arm/allwinner-h3.c"
    header = root / "include/hw/arm/allwinner-h3.h"
    missing = [str(p) for p in (board, soc, header) if not p.is_file()]
    if missing:
        print("ERROR: missing QEMU source files: " + ", ".join(missing))
        return 2
    b, s, h = (p.read_text(encoding="utf-8") for p in (board, soc, header))
    checks = {
        "upstream orangepi-pc machine registration": bool(re.search(r'orangepi-pc', b)),
        "H3 SoC instantiation": "TYPE_AW_H3" in b,
        "H3 source memory map": "memmap" in s,
        "H3 SoC device header": "AW_H3" in h,
        "ARM kernel loader": "arm_load_kernel" in b,
    }
    for label, ok in checks.items():
        print(f"{'PASS' if ok else 'FAIL'}: {label}")
    print("\nRelevant H3 header symbols (research only):")
    for symbol in sorted(set(re.findall(r"\bAW_H3_[A-Z0-9_]+\b", h))):
        if any(k in symbol for k in ("UART", "SDRAM", "MMC", "EMAC", "GIC", "SRAM", "CCU")):
            print("  " + symbol)
    print("\nNOTE: H3 source inspection does not establish H2+ compatibility.")
    return 0 if all(checks.values()) else 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--qemu-src", type=Path, default=Path("_work/qemu"))
    args = parser.parse_args()
    raise SystemExit(inspect(args.qemu_src))
