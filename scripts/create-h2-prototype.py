#!/usr/bin/env python3
"""Generate an EXPERIMENTAL board registration in a separate QEMU checkout.

This reuses H3 initialization; it is NOT an H2+ implementation and must never
be described as a functional Orange Pi Zero LTS emulator.
"""
import argparse
from pathlib import Path

MARKER = "/* qemu-sbc experimental H2+ board registration"
SNIPPET = '''
/* qemu-sbc experimental H2+ board registration
 * PROTOTYPE ONLY: reuses H3 machine initialization and 1 GiB RAM requirement.
 * NOT an Orange Pi Zero LTS hardware model. Do not boot vendor images.
 */
static void orangepi_zero_lts_proto_machine_init(MachineClass *mc)
{
    orangepi_machine_init(mc);
    mc->desc = "Orange Pi Zero LTS research prototype (H3 internals, NOT H2+)";
}

DEFINE_MACHINE_ARM("orangepi-zero-lts-proto",
                   orangepi_zero_lts_proto_machine_init)
'''

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--qemu-src", required=True, type=Path)
    parser.add_argument("--apply", action="store_true", help="modify QEMU checkout")
    args = parser.parse_args()
    target = args.qemu_src / "hw/arm/orangepi.c"
    if not target.is_file():
        parser.error(f"missing {target}")
    source = target.read_text()
    required = ('orangepi_machine_init(MachineClass *mc)', 'DEFINE_MACHINE_ARM("orangepi-pc"')
    if not all(token in source for token in required):
        parser.error("unexpected upstream orangepi.c; refusing to modify")
    if MARKER in source:
        print("Prototype registration already present; no changes")
        return
    if not args.apply:
        print("DRY RUN: would append experimental orangepi-zero-lts-proto registration to", target)
        return
    target.write_text(source.rstrip() + "\n" + SNIPPET)
    print("Prototype registration added to", target)
    print("WARNING: H3 internals and 1 GiB RAM; NOT H2+ emulation.")

if __name__ == "__main__":
    main()
