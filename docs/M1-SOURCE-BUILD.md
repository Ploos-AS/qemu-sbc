# Source-build verification for the experimental prototype

A **manual** GitHub Actions workflow is provided at
`.github/workflows/qemu-source-build.yml`.

It checks out the QEMU v10.0.0 release tag, inspects the H3 reference,
applies the research-only `orangepi-zero-lts-proto` registration, compiles
`qemu-system-arm`, checks `-machine help`, and attempts to instantiate
the prototype with QMP.

## What it does not prove

- H2+ hardware compatibility
- Orange Pi Zero LTS RAM, clocks, pinmux, or interrupt wiring
- UART or U-Boot functionality
- Linux boot, networking or SD compatibility

The prototype intentionally reuses the H3 machine implementation.
It is **not** the intended final `orangepi-zero-lts` board.

## Execution

From the repository Actions tab, select **QEMU source prototype build** and
choose **Run workflow**. The run will publish logs and evidence artifacts.
Do not mark the source-build gate complete until the actual workflow succeeds.

## Known caveat

The QMP smoke step only verifies that QEMU starts and exposes QMP. It is not a
board-level functional test. Any API incompatibility in the generator must be
fixed from the pinned source build's compiler output.
