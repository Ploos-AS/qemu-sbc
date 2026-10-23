# H2+ inherited SoC register inventory

The Orange Pi Zero board DTS includes the H3 SoC DTSI, which in
turn includes the shared H3/H5 DTSI. The source-inventory workflow
downloads both Linux v6.12 sources, extracts UART0, MMC0 and EMAC
base addresses and preserves the source files, checksums and JSON.

## Verified CI

Run [39910094954](https://github.com/Ploos-AS/qemu-sbc/actions/runs/39910094954)
passed on commit `b1f3a37`. The previous attempt failed because
the parser did not follow the H3-to-shared-H3/H5 DTSI inclusion.

The workflow now also executes offline extractor regression tests for
normal, missing, duplicated and invalid-address cases.

## Limits

These are addresses in an inherited Linux source description, not
a validated H2+ MMIO implementation. Before using the extracted
values in QEMU, validate H2+ overrides, IRQs, register ranges,
clocks, reset behavior and guest boot evidence.
