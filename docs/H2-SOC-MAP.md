# H2+ inherited SoC register inventory

Linux v6.12 `sun8i-h3.dtsi` includes `sunxi-h3-h5.dtsi`,
which holds common peripherals. The initial extractor incorrectly
looked only in the first file. CI run 39909973566 failed with
`expected one uart0 node, found 0`.

The corrected workflow downloads **both** pinned source files using
the authenticated GitHub Contents API, preserves their SHA256 sums,
and extracts UART0, MMC0 and EMAC node base addresses.

These are inherited H3/H5 source addresses; H2+ applicability,
interrupts and device functionality still require verification.

CI: https://github.com/Ploos-AS/qemu-sbc/actions/workflows/h2-soc-map.yml
