# Source-build verification for the experimental prototype

The workflow `.github/workflows/qemu-source-build.yml` now runs on
changes to its source-build scripts **and** supports manual dispatch.

It checks out QEMU v10.0.0, applies the experimental H3-backed
`orangepi-zero-lts-proto` registration, builds ARM QEMU, verifies the
machine list, and checks a QMP greeting and command response.

The workflow uploads the resolved QEMU commit and QMP evidence.
A green workflow is needed before the source-build gate can be marked done.

This is still a **research prototype**, not an H2+ emulator. It uses the
H3 board implementation and does not validate U-Boot, UART, Linux,
H2+ MMIO or realistic Orange Pi Zero LTS RAM.
