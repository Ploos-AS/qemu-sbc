# H2+ vs H3: verified starting points

Target: Orange Pi Zero LTS (H2+). Reference: QEMU Orange Pi PC (H3).

## Source-grounded observations

| Topic | Evidence | Consequence |
|---|---|---|
| Device tree inheritance | Linux `sun8i-h2-plus-orangepi-zero.dts` includes `sun8i-h3.dtsi` | Reuse H3 subsystem implementations selectively, but validate all differences |
| Machine identity | Linux DTS compatible includes `xunlong,orangepi-zero`, `allwinner,sun8i-h2-plus` | Dedicated machine and correct guest DTB needed |
| Serial console | DTS aliases `serial0 = &uart0` and `stdout-path = "serial0:115200n8"` | Prioritize UART0 console and pinmux |
| Storage | `mmc0` enabled, 4-bit bus and card detect PF6 | SD boot path essential |
| Wi-Fi | `mmc1` SDIO XR819 | Wi-Fi deferred, must not be claimed |
| Wired network | DTS enables EMAC with internal MII PHY | Ethernet required for M2 |
| SPI NOR | DTS says optional and disabled by default | Do not assume populated flash |
| QEMU baseline | Existing `orangepi-pc` is H3 Cortex-A7 with UART, SD, EMAC and CCU | Baseline reference only, not proof of H2+ compatibility |

## Sources

- Linux DTS: https://kunit.googlesource.com/linux/+/refs/heads/torvalds/master/arch/arm/boot/dts/sun8i-h2-plus-orangepi-zero.dts
- QEMU board documentation: https://www.qemu.org/docs/master/system/arm/orangepi.html
- QEMU implementation reference: https://gitlab.com/qemu-project/qemu/-/blob/master/hw/arm/orangepi.c
- QEMU SoC implementation reference: https://gitlab.com/qemu-project/qemu/-/blob/master/hw/arm/allwinner-h3.c

## Still unverified

- H2+ versus H3 MMIO register deltas and IRQ wiring
- H2+ clock, reset, CPU and DRAM initialization differences
- Whether Orange Pi Zero LTS hardware revisions use the same DTS without overrides
- U-Boot SPL boot assumptions and tested firmware build
- Exact resolved commit for QEMU v10.0.0 source baseline

**Do not invent register offsets, IRQ numbers, or claim boot success.** Validate them from pinned Linux/U-Boot/QEMU sources and real tests.
