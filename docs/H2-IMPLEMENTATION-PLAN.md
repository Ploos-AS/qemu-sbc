# Orange Pi Zero LTS H2+ implementation plan

## Scope and naming

The existing `orangepi-zero-lts-proto` is a QEMU v10 H3 alias,
not a model of H2+. Keep it intact as a comparison fixture.

The eventual board name is `orangepi-zero-lts`, with a distinct
board initializer and an H2+ SoC type. Neither exists yet.

## Required evidence before coding hardware constants

| Subsystem | Primary reference | Implementation gate |
|---|---|---|
| Board identity and pinout | Linux `sun8i-h2-plus-orangepi-zero.dts` | Record compatible, console, MMC and Ethernet |
| H2+ SoC peripheral addresses | Linux `sun8i-h3.dtsi` plus H2+ overrides | Verified MMIO base and region sizes |
| Interrupt routing | Linux DTS and interrupt bindings | Verified IRQ numbers, GIC wiring |
| RAM size / DRAM setup | Orange Pi Zero LTS board revision docs, U-Boot defconfig and SPL | Confirm supported 256/512 MiB variants rather than infer |
| UART0 | Linux DTS aliases/pinctrl, U-Boot console config | Serial register smoke + U-Boot banner |
| Clocks and reset | Linux CCU and reset bindings; U-Boot sunxi drivers | Correct reset state and clock inputs |
| SD/MMC0 | Linux DTS + U-Boot sunxi MMC | SPL or U-Boot boot from card image |
| Ethernet | Linux DTS internal PHY, QEMU EMAC | Linux network smoke test |
| SDIO Wi-Fi | Linux DTS XR819 | Deferred; no Wi-Fi claim |

## Suggested implementation sequence

1. Pin Linux and U-Boot source revisions and record exact URLs/SHAs.
2. Produce machine-readable H2+ address/IRQ inventory with citations.
3. Introduce a separate `allwinner-h2-plus` SoC device and dedicated
   board init in QEMU source patch series. Do not alias H3's board init.
4. Add CPU/RAM and UART0 qtests against the real new machine.
5. Bring up U-Boot serial output; preserve the exact boot log.
6. Implement and test MMC boot, timer/CCU, Linux and EMAC incrementally.
7. Evaluate upstreaming once tests and copyright/licensing are clean.

## Acceptance criteria

- Source builds from pinned QEMU v10 baseline
- Machine registers as `orangepi-zero-lts` and is independently initialized
- Actual board RAM configurations accepted and unsupported ones rejected
- MMIO/IRQ values traceable to pinned upstream hardware descriptions
- UART0 boot output from a pinned U-Boot build
- Later: MMC, Linux boot and networking evidence

## Guardrails

Do not mark any H2+ gate complete based on the H3 alias.
Do not copy arbitrary H3 offsets, RAM values, or board assumptions.
No boot success claim without CI artifacts and boot logs.
