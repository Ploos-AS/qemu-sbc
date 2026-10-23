# H2+ inherited GIC interrupt translation

This stage translates Linux GIC binding interrupt specifiers to
architectural GIC interrupt IDs. For a three-cell specifier
`<type index flags>`, SPI (`type=0`) maps to ID `index+32`,
and PPI (`type=1`) maps to ID `index+16`.

The script rejects unsupported types, unresolved preprocessor macros
and invalid PPI indices. It preserves trigger flags without guessing
their meaning or assigning a QEMU GPIO connection.

The workflow first tests synthetic examples, then extracts raw
specifiers from pinned Linux v6.12 DTSI sources and attempts
translation. A failure means source handling needs refinement;
it does **not** mean the H2+ hardware has been validated.

This is **not** a working H2+ QEMU SoC model.

CI: https://github.com/Ploos-AS/qemu-sbc/actions/workflows/h2-gic.yml
