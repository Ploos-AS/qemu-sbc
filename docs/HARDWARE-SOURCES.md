# Hardware sources and identification

Primary target: **Orange Pi Zero LTS** (Allwinner H2+). Gather SoC register maps, boot source priority, UART and clock trees, pinmux, DRAM, MMC and Ethernet documentation before M1.

Reference QEMU model: `orangepi-pc` (Allwinner H3). Similarity does not establish H2+ compatibility.

Second target: **TP-Link TL-WR703N**, Atheros AR9331 (MIPS). Confirm hardware revision and flash layout.

Third target: **GL.iNet GL-MT300N-V2**, MediaTek MT7628NN (MIPS).
- Official product: https://www.gl-inet.com/en-eu/products/gl-mt300n-v2?country=NO
- Official hardware docs: https://docs.gl-inet.com/router/en/3/specification/gl-mt300n-v2/
- Official firmware listings: https://dl.gl-inet.com/firmware/mt300n-v2/
- **GL-MT300N (without V2) is a different machine.**

Research tasks: locate and verify publicly redistributable boot artifacts, register documentation, relevant Linux/OpenWrt DTS and U-Boot sources. Do not upload proprietary firmware, factory flash dumps or unique calibration data.
