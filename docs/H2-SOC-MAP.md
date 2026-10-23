# H2+ inherited SoC register inventory

The Orange Pi Zero board DTS includes the H3 SoC DTSI. This stage
extracts UART0, MMC0 and EMAC base addresses from **Linux v6.12**
`sun8i-h3.dtsi`, preserving the source and SHA256 as CI artifacts.

Run:
```sh
python3 scripts/extract-h2-soc-map.py h3-inherited.dtsi --output h2-soc-registers.json
```

The output is a machine-readable inventory of **inherited H3 DTSI
values**. It is not yet a verified H2+ register map: H2+ overrides,
IRQ specifiers, register lengths, clock/reset and QEMU model behavior
remain to be checked before using these values in the emulator.

CI: https://github.com/Ploos-AS/qemu-sbc/actions/workflows/h2-soc-map.yml
