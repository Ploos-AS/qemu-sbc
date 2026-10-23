# Roadmap

## M0 — Bootstrap
- [x] Repository scope and board inventory
- [x] Initial documentation and license policy
- [x] Clone/build/smoke scripts
- [x] CI pipeline definition and successful initial smoke runs
- [x] Clarify Mango identity: **GL-MT300N-V2 / MT7628NN**, not GL-MT300N / MT7620NN
- [ ] Pin upstream QEMU source revision
- [ ] Record Orange Pi Zero LTS hardware references for the exact board revision

## M1 — Orange Pi Zero LTS initial machine
- [x] H2+ subsystem research checklist and reference-machine CI smoke test
- [ ] Verify H2+ vs H3 MMIO map, reset and clock differences
- [ ] Implement actual Orange Pi Zero LTS machine registration
- [ ] Boot ROM / U-Boot execution path and UART
- [ ] QTest coverage for MMIO, reset and basic interrupts

## M2 — Orange Pi Zero LTS Linux
- SD/MMC, timer/interrupts, Ethernet as required
- Mainline Linux + device-tree boot test
- Document unsupported peripherals and fidelity limits

## M3–M4 — TP-Link TL-WR703N
- AR9331 SoC: CPU, UART, SPI NOR, RAM, interrupts
- U-Boot, wired Ethernet and MikroWrt boot validation

## M5–M6 — GL.iNet GL-MT300N-V2 (original Mango target)
- MT7628NN: CPU, UART, SPI NOR, RAM, interrupts
- U-Boot, wired Ethernet, OpenWrt/MikroWrt/PocketBox validation
- Explicitly exclude the older GL-MT300N from this target

## M7+
- GPIO, buttons, LEDs, USB; optional Wi-Fi feasibility
- Upstream patch series, compliance tests and maintenance

**Acceptance rule:** Never mark a machine or guest OS as supported until a real automated boot test demonstrates it.
