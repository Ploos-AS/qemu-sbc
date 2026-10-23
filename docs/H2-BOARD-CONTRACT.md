# H2+ Orange Pi Zero board contract

Linux v6.12 source: `arch/arm/boot/dts/allwinner/sun8i-h2-plus-orangepi-zero.dts`.

The board DTS defines H2+ compatible strings, UART0 at 115200n8,
MMC0 four-bit SD with PF6 card detect, internal EMAC PHY and
optional disabled SPI NOR. These are source-backed board requirements,
not proof of emulation.

## CI source retrieval

The first CI attempt (run 39909754694) failed before running the
contract checker because unauthenticated raw.githubusercontent.com
returned HTTP 429. The workflow now uses the authenticated GitHub
Contents API with the job's GITHUB_TOKEN and the pinned v6.12 tag.

The contract checker must still pass in CI before its assertions
can be counted as verified. The next stage is extracting MMIO and IRQ
values from the inherited SoC device trees, not guessing them.

Source: https://github.com/torvalds/linux/blob/v6.12/arch/arm/boot/dts/allwinner/sun8i-h2-plus-orangepi-zero.dts
