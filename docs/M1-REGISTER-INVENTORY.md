# Orange Pi Zero LTS — H2+ register inventory

**Status: verification worksheet, not a verified hardware register map.**

Reference board: Orange Pi Zero LTS, Allwinner H2+.
Existing QEMU reference: Allwinner H3 on `orangepi-pc`.

## Subsystems to compare before implementation

| Subsystem | Questions to verify | Evidence needed |
|---|---|---|
| ARM CPU and GIC | CPU count, CPU type, interrupt lines | SoC manual, DTS, QEMU source |
| SRAM and DRAM | Physical base, size variants, boot mapping | DTS, schematic, bootloader |
| CCU / reset | Clock gates, resets and UART clock | SoC manual, Linux drivers |
| UART0 | MMIO base, IRQ, pinmux, reset behavior | DTS, serial boot log |
| Timers / watchdog | MMIO, IRQs, reset | SoC manual, Linux drivers |
| MMC0 | Boot card wiring, controller behavior | DTS, U-Boot config |
| Ethernet | MAC/PHY type, IRQ, pin wiring | schematic, DTS |
| SPI / flash | Is SPI flash populated? board revisions | schematic, board inspection |
| USB / Wi-Fi | Controller and external device connections | schematic, DTS |

## Source starting points

- QEMU Orange Pi PC documentation: https://www.qemu.org/docs/master/system/arm/orangepi.html
- Linux device tree source tree: https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/arch/arm/boot/dts
- U-Boot source tree: https://source.denx.de/u-boot/u-boot
- Orange Pi vendor documentation should be checked against the exact physical board revision.

No MMIO address or IRQ number is asserted until cross-checked with source and documented here.

## Next implementation gate

1. Select a fixed upstream QEMU commit and record its full hash.
2. Record exact Linux DTS and U-Boot defconfig paths for the target board.
3. Produce a verified H2+-versus-H3 delta table.
4. Implement dedicated board registration, then qtests and UART boot.

Do not treat a QEMU `orangepi-pc` smoke test as Orange Pi Zero LTS emulation.
