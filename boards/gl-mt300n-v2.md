# GL.iNet Mango — GL-MT300N-V2

**Canonical hardware target:** GL-MT300N-V2 (Mango), as linked by the project owner:
https://www.gl-inet.com/en-eu/products/gl-mt300n-v2?country=NO

Do **not** confuse with the earlier GL-MT300N (MT7620NN, 64 MiB RAM) or any newer device marketed as Mango.

## Manufacturer-confirmed baseline

| Component | GL-MT300N-V2 |
|---|---|
| SoC | MediaTek MT7628NN, 580 MHz |
| Architecture | MIPS |
| RAM | 128 MiB DDR2 |
| Flash | 16 MiB NOR |
| Wired ports | 1 WAN, 1 LAN (10/100 Mbit/s) |
| USB | 1 USB 2.0 host; micro USB power |
| Wireless | 2.4 GHz 802.11 b/g/n |
| Other | UART, GPIO, reset and toggle buttons, LEDs |

References:
- https://docs.gl-inet.com/router/en/3/specification/gl-mt300n-v2/
- https://www.gl-inet.com/en-eu/products/gl-mt300n-v2?country=NO
- https://dl.gl-inet.com/firmware/mt300n-v2/

## Implementation plan (M5–M6)

1. Confirm MT7628 memory map, CPU variant, boot ROM behavior and interrupt routing against open-source driver code and hardware documentation.
2. Implement RAM, reset/clock control, UART and SPI NOR, including flash partitions.
3. Boot redistributable U-Boot and capture deterministic serial output.
4. Add wired Ethernet, timer and GPIO support, then boot a compatible OpenWrt/MikroWrt image.
5. Validate PocketBox services with guest networking and repeatable CI tests.

**Not yet implemented.** Original vendor firmware compatibility, USB and Wi-Fi are not implied by early Linux boot success. Do not commit proprietary vendor firmware images or calibration data.

## Acceptance evidence

- QEMU machine name and source revision
- Bootloader image provenance and checksum
- Serial boot log
- Guest kernel and rootfs provenance and checksum
- MMIO and reset qtests, followed by network tests
