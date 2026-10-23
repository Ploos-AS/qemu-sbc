# M1 bring-up: Orange Pi Zero LTS (Allwinner H2+)

Status: **research and test plan**, not implemented machine emulation.

## Reference

QEMU upstream supports `orangepi-pc` (Allwinner H3). Documentation:
https://www.qemu.org/docs/master/system/arm/orangepi.html

That machine is a useful implementation reference, but H3 compatibility with H2+ and the Zero LTS board must be established device by device. Do not rename or alias `orangepi-pc` and claim Zero LTS support.

## Research gates

- [ ] Identify exact Orange Pi Zero LTS hardware revision and RAM variant.
- [ ] Record manufacturer schematic, board documentation and relevant Linux DTS paths.
- [ ] Compare H2+ and H3: CPU configuration, memory map, SRAM/DRAM, GIC, CCU, reset, timers, UART, SD/MMC, EMAC, SID, USB.
- [ ] Establish U-Boot board defconfig, SPL expectations, boot media and serial settings.
- [ ] Identify upstream QEMU source modules that can be reused, and missing peripherals.
- [ ] Record legal and redistributable test firmware source and exact hashes.

## M1 implementation sequence

1. Establish pinned upstream QEMU source revision and reproducible baseline build.
2. Add new H2+ SoC type only where required; avoid duplicating H3 devices without a verified difference.
3. Add dedicated `orangepi-zero-lts` machine registration and board wiring.
4. Implement/reset-test RAM, CPU, interrupt wiring and UART.
5. Boot legally redistributable U-Boot and capture repeatable serial log.
6. Add qtests for identification, reset and key MMIO registers.

## Acceptance

- `qemu-system-arm -M help` lists a **real** new machine, not an alias.
- qtests pass on a documented upstream QEMU revision.
- Bootloader serial log and build provenance committed as text/test metadata.
- Limitations and unimplemented devices explicitly listed.

Linux, SD/MMC and wired Ethernet functional boot are M2 targets; Wi-Fi is not part of M1.
