# H2+ SoC inherited register and interrupt inventory

This next-stage source extractor records **raw** `reg` and
`interrupts` property cell groups from UART0, MMC0 and EMAC in
the Linux v6.12 H3/H5 shared DTSI, which the H2+ board inherits
through `sun8i-h3.dtsi`.

It does not expand C preprocessor macros, translate GIC interrupt
specifiers, or validate H2+-specific hardware differences. Raw
cells are intentionally retained to avoid inventing numeric IRQs.

The GitHub Actions workflow saves the exact Linux source files,
SHA256 hashes and JSON extraction as evidence.

CI: https://github.com/Ploos-AS/qemu-sbc/actions/workflows/h2-soc-details.yml
