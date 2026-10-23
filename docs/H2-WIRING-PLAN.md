# H2+ QEMU wiring plan (source-derived, not implemented)

The workflow combines raw `reg` tuples from Linux v6.12
inherited H3/H5 DTSI with GIC SPI interrupt IDs. The script checks
node address vs. `reg`, positive region sizes, unique IRQ IDs,
and correct SPI-to-GIC ID arithmetic.

Each device in the generated JSON explicitly carries
`implementation_status: not_implemented`, and the overall document
sets `h2_hardware_verified: false` and
`qemu_wiring_implemented: false`.

This is an engineering plan, not evidence of a working independent
H2+ board. Before implementing the QEMU device wiring, validate
the H2+ specific DTS overlays and actual controller compatibility,
clock/reset handling, interrupt routing, and guest boot.

CI: https://github.com/Ploos-AS/qemu-sbc/actions/workflows/h2-wiring-plan.yml
