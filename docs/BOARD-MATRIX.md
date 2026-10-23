# Machine compatibility matrix

The entries below describe **targets**, not implemented QEMU support.

| Board | QEMU target name (proposed) | SoC | First evidence gate | Project phase |
|---|---|---|---|---|
| Orange Pi Zero LTS | `orangepi-zero-lts` | Allwinner H2+ | U-Boot serial boot | M1 |
| TP-Link TL-WR703N | `tl-wr703n` | Atheros AR9331 | U-Boot serial boot | M3 |
| GL.iNet Mango GL-MT300N-V2 | `gl-mt300n-v2` | MediaTek MT7628NN | U-Boot serial boot | M5 |

Mango means **GL-MT300N-V2 only**; not GL-MT300N (MT7620NN). Reference:
https://www.gl-inet.com/en-eu/products/gl-mt300n-v2?country=NO

## Evidence requirements

For each model record:
- exact physical hardware revision and RAM/flash configuration;
- upstream QEMU revision and patch series;
- guest bootloader, kernel and rootfs source hashes;
- UART boot logs and qtests;
- peripherals working, stubbed or not implemented.

An upstream QEMU reference board is not evidence that the proposed new machine already works.
