#!/usr/bin/env python3
"""Inject a minimal independent H2+ machine bootstrap into pinned QEMU.

Cortex-A7, RAM, GICv2, timers and UART0 with experimental -kernel loader.
"""
import argparse
from pathlib import Path

SOURCE = r'''/*
 * Independent Orange Pi Zero LTS (Allwinner H2+) machine bootstrap.
 * Copyright (c) 2026 Ploos AS
 * SPDX-License-Identifier: MIT
 *
 * Incomplete hardware model: CPU, RAM, GICv2 and UART0; no guest boot yet.
 */
#include "qemu/osdep.h"
#include "hw/boards.h"
#include "hw/arm/boot.h"
#include "hw/intc/arm_gic.h"
#include "hw/char/serial-mm.h"
#include "system/system.h"
#include "target/arm/gtimer.h"
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
    DeviceState *gic = qdev_new(TYPE_ARM_GIC);
    SysBusDevice *gic_bus = SYS_BUS_DEVICE(gic);

    object_property_set_bool(cpu, "realized", true, &error_fatal);
    qdev_prop_set_uint32(gic, "num-irq", 160);
    qdev_prop_set_uint32(gic, "revision", 2);
    qdev_prop_set_uint32(gic, "num-cpu", 1);
    qdev_prop_set_bit(gic, "has-security-extensions", false);
    qdev_prop_set_bit(gic, "has-virtualization-extensions", true);
    sysbus_realize_and_unref(gic_bus, &error_fatal);
    sysbus_mmio_map(gic_bus, 0, 0x01c81000);
    sysbus_mmio_map(gic_bus, 1, 0x01c82000);
    sysbus_mmio_map(gic_bus, 2, 0x01c84000);
    sysbus_mmio_map(gic_bus, 3, 0x01c86000);
    sysbus_connect_irq(gic_bus, 0, qdev_get_gpio_in(DEVICE(cpu), ARM_CPU_IRQ));
    sysbus_connect_irq(gic_bus, 1, qdev_get_gpio_in(DEVICE(cpu), ARM_CPU_FIQ));
    /* H3-family reference PPI routing; H2+ hardware validation pending. */
    const int timer_ppi[] = {
        [GTIMER_PHYS] = 14,
        [GTIMER_VIRT] = 11,
        [GTIMER_HYP] = 10,
        [GTIMER_SEC] = 13,
    };
    for (int i = 0; i < ARRAY_SIZE(timer_ppi); i++) {
        qdev_connect_gpio_out(DEVICE(cpu), i,
            qdev_get_gpio_in(gic, 128 + GIC_NR_SGIS + timer_ppi[i]));
    }

    serial_mm_init(get_system_memory(), 0x01c28000, 2,
                   qdev_get_gpio_in(gic, 0), 115200, serial_hd(0),
                   DEVICE_LITTLE_ENDIAN);
    memory_region_add_subregion(get_system_memory(), H2_DRAM_BASE,
                                machine->ram);

    /* Initial direct-kernel loader; guest boot is not yet qualified. */
    if (machine->kernel_filename) {
        static struct arm_boot_info bootinfo;
        bootinfo.loader_start = H2_DRAM_BASE;
        bootinfo.ram_size = machine->ram_size;
        bootinfo.board_id = -1;
        bootinfo.kernel_filename = machine->kernel_filename;
        bootinfo.kernel_cmdline = machine->kernel_cmdline;
        bootinfo.initrd_filename = machine->initrd_filename;
        bootinfo.dtb_filename = machine->dtb;
        arm_load_kernel(ARM_CPU(cpu), machine, &bootinfo);
    }
    object_unref(cpu);
}

static void h2_zero_lts_class_init(ObjectClass *oc, void *data)
{
    MachineClass *mc = MACHINE_CLASS(oc);

    mc->desc = "Orange Pi Zero LTS H2+ bootstrap (CPU/RAM/GICv2/UART0; no boot)";
    mc->init = h2_zero_lts_init;
    mc->default_ram_size = 256 * 1024 * 1024;
    mc->default_ram_id = "orangepi-zero-lts-h2.ram";
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
