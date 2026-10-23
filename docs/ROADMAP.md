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

## M8+ — PowerPC evaluation (long-term, not committed support)

These targets are **candidates**, not implemented or promised emulation.
Prioritize only after the ARM/MIPS board milestones and a feasibility review.

1. **bplan Pegasos II** — first PowerPC candidate. Evaluate firmware/OF
   compatibility, Marvell Discovery II system controller, PCI, IDE,
   interrupt routing and reproducible guest boot. Relevant to PPCVM,
   but this repository must not duplicate its implementation blindly.
2. **bplan Pegasos I** — separate Articia S platform; not a trivial
   Pegasos II variant. Assess chipset documentation and firmware
   availability before scheduling.
3. **bplan Efika 5K2** — Freescale MPC5200B based compact PowerPC board.
   Evaluate MPC5200B peripherals, firmware and OS boot independently.

### PowerPC acceptance gates

- Identify exact board revision, SoC/chipset, RAM map and IRQ topology.
- Document redistributable firmware and OS test assets, or require
  user-supplied licensed images; never commit proprietary firmware.
- Build a QEMU machine model and deterministic qtests for UART,
  interrupts and storage.
- Obtain reproducible boot logs from supported guest OSes.
- Coordinate shared components and tests with the PPCVM project.

No PowerPC machine is considered supported until these gates pass.
