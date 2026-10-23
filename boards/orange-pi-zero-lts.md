# Orange Pi Zero LTS

**Priority:** first implementation target.

- SoC: Allwinner H2+; ARM Cortex-A7
- Related upstream QEMU reference: `orangepi-pc` (Allwinner H3)
- Initial research: H2+ versus H3 address map, CCU, timer, interrupt controller, DRAM, SD/MMC and UART
- M1 criterion: identifiable board option, reproducible U-Boot output through UART
- M2 criterion: repeatable Linux serial-console boot and validated SD/networking

Do not assume the H3 machine is binary-compatible with this board. Verify actual hardware revisions and boot sources.
