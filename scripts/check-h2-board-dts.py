#!/usr/bin/env python3
"""Check H2+ Orange Pi Zero board facts from an upstream Linux DTS file."""
import argparse
import re
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument("dts", type=Path)
args = p.parse_args()
s = re.sub(r"/\*.*?\*/", "", args.dts.read_text(), flags=re.S)
checks = {
    "H3 SoC DTS inheritance": r'#include\s+"sun8i-h3\.dtsi"',
    "H2+ board identity": r'compatible\s*=\s*"xunlong,orangepi-zero"\s*,\s*"allwinner,sun8i-h2-plus"',
    "UART0 alias": r'serial0\s*=\s*&uart0\s*;',
    "UART0 console": r'stdout-path\s*=\s*"serial0:115200n8"',
    "MMC0 card detect PF6": r'cd-gpios\s*=\s*<&pio\s+5\s+6\s+GPIO_ACTIVE_LOW>',
    "MMC0 four-bit bus": r'&mmc0\s*\{[^}]*bus-width\s*=\s*<4>',
    "Ethernet internal PHY": r'&emac\s*\{[^}]*phy-handle\s*=\s*<&int_mii_phy>',
    "SPI0 disabled by default": r'&spi0\s*\{[^}]*status\s*=\s*"disabled"',
}
for label, pattern in checks.items():
    if not re.search(pattern, s, flags=re.S):
        raise SystemExit(f"FAIL: {label}")
    print(f"PASS: {label}")
print("NOTE: DTS board facts only; no H2+ MMIO/IRQ or QEMU boot verification")
