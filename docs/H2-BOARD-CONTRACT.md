# H2+ Orange Pi Zero board contract — first executable checks

This document describes a **Linux device-tree contract**, not a working
QEMU model. Source: Linux
`arch/arm/boot/dts/allwinner/sun8i-h2-plus-orangepi-zero.dts`.

The source identifies the board as
`xunlong,orangepi-zero` / `allwinner,sun8i-h2-plus`.
It includes `sun8i-h3.dtsi`, but inheritance does **not** mean the
H2+ is interchangeable with H3.

Executable assertions in `scripts/check-h2-board-dts.py` cover:

- UART0 console alias and 115200n8 stdout
- MMC0 four-bit bus and PF6 active-low card detection
- EMAC internal MII PHY
- SPI NOR optional/disabled in board DTS
- Board compatible strings and shared H3 DTS inclusion

## Reproduce

```sh
curl -fL https://raw.githubusercontent.com/torvalds/linux/v6.12/arch/arm/boot/dts/allwinner/sun8i-h2-plus-orangepi-zero.dts -o /tmp/sun8i-h2-plus-orangepi-zero.dts
python3 scripts/check-h2-board-dts.py /tmp/sun8i-h2-plus-orangepi-zero.dts
```

The test checks only the named DTS properties. It does not infer RAM
variants, peripheral MMIO addresses, interrupt numbers, clocks or boot
compatibility. Those require additional pinned references and tests.
