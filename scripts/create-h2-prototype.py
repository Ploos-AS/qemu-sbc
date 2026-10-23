#!/usr/bin/env python3
"""Register an explicitly H3-backed research machine in a local QEMU checkout."""
import argparse
from pathlib import Path

MARKER = "/* qemu-sbc experimental H2+ board registration"
SNIPPET = '''
/* qemu-sbc experimental H2+ board registration
 * PROTOTYPE ONLY: uses the H3 board and its 1 GiB RAM configuration.
 * NOT Orange Pi Zero LTS hardware emulation.
 */
static void orangepi_zero_lts_proto_machine_init(MachineClass *mc)
{
    orangepi_machine_init(mc);
    mc->desc = "Orange Pi Zero LTS research prototype (H3 internals, NOT H2+)";
}

DEFINE_MACHINE("orangepi-zero-lts-proto",
               orangepi_zero_lts_proto_machine_init)
'''

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--qemu-src", required=True, type=Path)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    target = args.qemu_src / "hw/arm/orangepi.c"
    if not target.is_file():
        parser.error(f"missing {target}")
    source = target.read_text(encoding="utf-8")
    required = ('static void orangepi_machine_init(MachineClass *mc)',
                'DEFINE_MACHINE("orangepi-pc", orangepi_machine_init)')
    if not all(token in source for token in required):
        parser.error("unexpected upstream orangepi.c; refusing to modify")
    if MARKER in source:
        print("Prototype already registered; no changes")
        return
    if not args.apply:
        print("DRY RUN: would add research prototype to", target)
        return
    target.write_text(source.rstrip() + "\n" + SNIPPET, encoding="utf-8")
    print("Registered H3-backed prototype in", target)
    print("WARNING: NOT a functional H2+ model")

if __name__ == "__main__":
    main()
