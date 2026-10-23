# Architecture and validation

Prefer small upstreamable QEMU patches under hw/arm, hw/mips and hw/* device subsystems with corresponding qtests. Keep this repository as planning, integration, hardware-reference and external test harness rather than maintaining an unbounded QEMU fork.

## Fidelity levels

1. **Discovery:** verified component inventory and relevant upstream source.
2. **Bootloader:** repeatable UART output and boot path.
3. **Kernel:** kernel reaches console and mounts root filesystem.
4. **Peripheral:** deterministic MMIO and functional wired networking/storage tests.
5. **Image compatibility:** unmodified legal, redistributable images with documented hashes.

A serial-console message alone does not imply complete board emulation. Device tree, interrupt routing, GPIO muxing, reset/clock gating and boot ROM details must be validated separately.

## Security

Never embed vendor firmware, Wi-Fi blobs, proprietary boot ROMs, device credentials or third-party copyrighted images. Pin references and hash test assets. Prefer fully redistributable boot artifacts.
