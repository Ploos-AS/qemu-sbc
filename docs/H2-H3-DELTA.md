# H2+ vs H3: source-grounded starting points

Target: Orange Pi Zero LTS (H2+). Reference: QEMU Orange Pi PC (H3).

| Topic | Evidence | Consequence |
|---|---|---|
| Device tree inheritance | Linux `sun8i-h2-plus-orangepi-zero.dts` includes `sun8i-h3.dtsi` | Selectively reuse H3 peripherals, validate differences |
| Machine identity | Linux compatible includes `xunlong,orangepi-zero`, `allwinner,sun8i-h2-plus` | Dedicated machine and guest DTB |
| Serial console | DTS aliases `serial0 = &uart0`, stdout 115200n8 | UART0 first |
| Storage | MMC0 enabled, four-bit bus, card-detect PF6 | SD boot |
| Wi-Fi | MMC1 SDIO XR819 | Defer and do not claim support |
| Ethernet | EMAC with internal MII PHY | Required later |
| SPI NOR | Optional, disabled in reference DTS | Do not assume flash |
| QEMU prototype | H3 board with fixed 1 GiB RAM | Research-only baseline |

## Sources

- Linux DTS: https://kunit.googlesource.com/linux/+/refs/heads/torvalds/master/arch/arm/boot/dts/sun8i-h2-plus-orangepi-zero.dts
- QEMU docs: https://www.qemu.org/docs/master/system/arm/orangepi.html
- QEMU v10.0.0 board: https://gitlab.com/qemu-project/qemu/-/blob/v10.0.0/hw/arm/orangepi.c
- QEMU v10.0.0 SoC: https://gitlab.com/qemu-project/qemu/-/blob/v10.0.0/hw/arm/allwinner-h3.c

## Verified baseline

QEMU v10.0.0 commit:
`7c949c53e936aa3a658d84ab53bae5cadaa5d59c`.
Prototype source build, machine registration and QMP startup passed
in run 39908681050.

## Still unverified

- H2+ versus H3 MMIO and IRQ differences
- H2+ clocks, reset, CPU and DRAM initialization
- Orange Pi Zero LTS hardware revisions and RAM variants
- U-Boot SPL boot assumptions and real guest boot

Never invent offsets or claim a boot that has not been tested.
