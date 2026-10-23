# Independent H2+ QEMU board: implementation contract

## Goal

Replace the current H3-backed `orangepi-zero-lts-proto` research alias
with a **separate** H2+ SoC and Orange Pi Zero LTS board machine.
Do not advertise H2+ emulation until the acceptance gates pass.

## Separation from existing prototype

- Keep the H3-backed alias clearly marked as experimental.
- Add a separate board source (proposed: `hw/arm/orangepi-zero-lts.c`)
  and SoC implementation (proposed: `hw/arm/allwinner-h2.c`).
- Register a **different** QEMU machine type only when the SoC has
  independently modeled initialization. Do not simply call the H3
  Orange Pi machine initializer under a new name.
- Reuse QEMU device implementations when hardware compatibility is
  demonstrated, not merely because Linux DTSI nodes are inherited.

## First hardware slice: serial console

1. Identify exact Orange Pi Zero LTS revision and H2+ memory variants.
2. Resolve H2+ CPU/GIC topology and memory map against board-level
   Linux DTS and technical documentation.
3. Instantiate CPU, RAM, GIC, clock/reset baseline and UART0 MMIO
   using QEMU device models compatible with the H2+.
4. Connect UART0 IRQ to the GIC using the validated, source-derived
   `h2-wiring-plan.json`; check trigger semantics.
5. Add qtest for UART0 MMIO and interrupt delivery.
6. Capture deterministic firmware/U-Boot serial boot evidence.

## Follow-on hardware slices

- MMC0, SD boot, timers, clock/reset controller.
- Ethernet MAC, PHY and network boot.
- USB/GPIO and other peripherals only after the minimal boot path.

## Evidence and release gates

- A pinned upstream QEMU revision builds without untracked patches.
- Machine initialization and QMP are verified in CI.
- UART0 qtest demonstrates read/write and interrupt routing.
- U-Boot output is captured from a legally redistributable image or
  documented user-supplied firmware.
- Linux boot and Ethernet are separate later milestones.
- Test output and source references are retained as CI artifacts.

## Current status

Only an H3-backed research prototype and source-derived MMIO/IRQ
inventory exist. **No independent H2+ machine has been implemented.**
