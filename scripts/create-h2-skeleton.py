#!/usr/bin/env python3
"""Create isolated H2+ QEMU source skeletons; no machine registration yet."""
import argparse
from pathlib import Path

FILES = {
    "hw/arm/allwinner-h2.c": """/*
 * Allwinner H2+ SoC - research skeleton.
 * Copyright (c) 2026 Ploos AS
 * SPDX-License-Identifier: MIT
 *
 * Not yet built, registered, or a functional H2+ SoC.
 * TODO: model CPU, GIC, clock/reset, RAM and UART0.
 */
""",
    "hw/arm/orangepi-zero-lts.c": """/*
 * Orange Pi Zero LTS H2+ board - research skeleton.
 * Copyright (c) 2026 Ploos AS
 * SPDX-License-Identifier: MIT
 *
 * No DEFINE_MACHINE until independent SoC initialization is ready.
 * TODO: board RAM, serial console, SD/MMC, boot integration.
 */
""",
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--qemu-src", required=True, type=Path)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    arm = args.qemu_src / "hw" / "arm"
    if not (arm / "orangepi.c").is_file():
        parser.error("expected a QEMU checkout containing hw/arm/orangepi.c")
    for relative, content in FILES.items():
        target = args.qemu_src / relative
        if target.exists():
            if target.read_text() != content:
                parser.error(f"refusing to overwrite existing source: {target}")
            print("UNCHANGED:", target)
        elif args.apply:
            target.write_text(content)
            print("CREATED:", target)
        else:
            print("DRY RUN:", target)
    print("NOTE: skeleton only; no H2+ QEMU machine registered")

if __name__ == "__main__":
    main()
