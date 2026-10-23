# Roadmap

## M0 — Bootstrap
- [x] Repository scope, board inventory, licenses and CI
- [x] Mango identified as GL-MT300N-V2 / MT7628NN
- [x] QEMU v10.0.0 selected and full source SHA recorded
- [x] Successful source build and prototype QMP initialization (run 39908681050)
- [ ] Board-revision-specific Orange Pi Zero LTS hardware references

## M1 — Orange Pi Zero LTS
- [x] H2+ research inventory and reference machine-list test
- [x] H3 source inspection and experimental H3-backed machine prototype
- [x] Compile prototype, register machine and initialize QMP
- [x] Define independent H2+ implementation and evidence gates
- [ ] Verify exact H2+ RAM variants, MMIO and IRQ wiring from pinned sources
- [ ] Independent Orange Pi Zero LTS board and H2+ SoC
- [ ] UART0 qtest and U-Boot boot log

## M2 — Orange Pi Zero LTS Linux
- SD/MMC, timers, Ethernet, Linux boot and compatibility evidence

## M3–M4 — TL-WR703N
- AR9331 MIPS, UART, SPI NOR, Ethernet and MikroWrt boot

## M5–M6 — GL-MT300N-V2 Mango
- MT7628NN MIPS, UART, SPI NOR, Ethernet and OpenWrt/MikroWrt/PocketBox boot

## M7+
- USB, GPIO, buttons, LEDs and Wi-Fi feasibility; upstream submissions

**Acceptance:** A real board model and boot tests are required before claiming emulation support.
