#!/usr/bin/env python3
"""Inject a minimal independent H2+ machine bootstrap into pinned QEMU.

Only a Cortex-A7 and RAM are instantiated. GIC/UART are future milestones.
"""
import argparse
from pathlib import Path

SOURCE = r'''/*
 * Independent Orange Pi Zero LTS (Allwinner H2+) machine bootstrap.
 * Copyright (c) 2026 Ploos AS
 * SPDX-License-Identifier: MIT
 *
 * Incomplete hardware model: CPU and RAM only, no boot support yet.
 */
#include "qemu/osdep.h"
#include "hw/boards.h"
#include "hw/qdev-properties.h"
#include "hw/core/cpu.h"
#include "hw/sysbus.h"
#include "exec/address-spaces.h"
#include "qapi/error.h"
#include "target/arm/cpu.h"

#define TYPE_H2_ZERO_LTS_MACHINE MACHINE_TYPE_NAME("orangepi-zero-lts-h2")
#define H2_DRAM_BASE 0x40000000

static void h2_zero_lts_init(MachineState *machine)
{
    Object *cpu = object_new(ARM_CPU_TYPE_NAME("cortex-a7"));

    object_property_set_bool(cpu, "realized", true, &error_fatal);
    object_unref(cpu);

    memory_region_add_subregion(get_system_memory(), H2_DRAM_BASE,
                                machine->ram);
}

static void h2_zero_lts_class_init(ObjectClass *oc, void *data)
{
    MachineClass *mc = MACHINE_CLASS(oc);

    mc->desc = "Orange Pi Zero LTS H2+ bootstrap (CPU/RAM only; no boot)";
    mc->init = h2_zero_lts_init;
    mc->default_ram_size = 256 * 1024 * 1024;
    mc->default_cpu_type = ARM_CPU_TYPE_NAME("cortex-a7");
    mc->min_cpus = 1;
    mc->max_cpus = 1;
    mc->default_cpus = 1;
}

static const TypeInfo h2_zero_lts_machine_type = {
    .name = TYPE_H2_ZERO_LTS_MACHINE,
    .parent = TYPE_MACHINE,
    .class_init = h2_zero_lts_class_init,
};

static void h2_zero_lts_machine_register(void)
{
    type_register_static(&h2_zero_lts_machine_type);
}

type_init(h2_zero_lts_machine_register)
'''

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--qemu-src", type=Path, required=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    root = args.qemu_src
    meson = root / "hw/arm/meson.build"
    if not (root / "hw/arm/orangepi.c").is_file() or not meson.is_file():
        parser.error("expected QEMU ARM source checkout")
    target = root / "hw/arm/orangepi-zero-lts-h2.c"
    old = meson.read_text()
    anchor = "arm_ss.add(when: 'CONFIG_ALLWINNER_H3', if_true: files('allwinner-h3.c', 'orangepi.c'))"
    entry = "arm_ss.add(when: 'CONFIG_ALLWINNER_H3', if_true: files('orangepi-zero-lts-h2.c'))"
    if anchor not in old:
        parser.error("pinned QEMU Meson anchor not found")
    if target.exists() and target.read_text() != SOURCE:
        parser.error("refusing to overwrite modified H2+ machine source")
    if entry in old and not target.exists():
        parser.error("Meson references missing H2+ machine source")
    if not args.apply:
        print("DRY RUN: independent H2+ CPU/RAM machine")
        return
    if not target.exists():
        target.write_text(SOURCE)
    if entry not in old:
        meson.write_text(old.replace(anchor, anchor + "\n" + entry, 1))
    print("READY: H2+ CPU/RAM bootstrap registered; GIC/UART/boot not implemented")

if __name__ == "__main__":
    main()
