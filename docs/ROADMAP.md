# Roadmap

## M0 — Bootstrap
- [x] Repository scope, board inventory, licenses and initial CI
- [x] Mango identified as GL-MT300N-V2 / MT7628NN
- [x] Select QEMU v10.0.0 as default source release
- [ ] Verify source build and record exact upstream commit SHA
- [ ] Record board-revision-specific Orange Pi Zero LTS hardware references

## M1 — Orange Pi Zero LTS
- [x] H2+ research inventory and reference machine-list CI test
- [x] H3 reference source inspection script and implementation acceptance gates
- [ ] Verified H2+ vs H3 register and IRQ delta table
- [ ] Dedicated Orange Pi Zero LTS QEMU machine implementation
- [ ] Bootloader UART output
- [ ] qtests for MMIO, reset and interrupts

## M2 — Orange Pi Zero LTS Linux
- SD/MMC, timers, Ethernet, Linux boot and compatibility evidence

## M3–M4 — TL-WR703N
- AR9331 MIPS, UART, SPI NOR, Ethernet and MikroWrt boot

## M5–M6 — GL-MT300N-V2 Mango
- MT7628NN MIPS, UART, SPI NOR, Ethernet and OpenWrt/MikroWrt/PocketBox boot

## M7+
- USB, GPIO, buttons, LEDs and Wi-Fi feasibility; upstream submissions

**Acceptance:** A real board model and boot tests are required before claiming emulation support.
