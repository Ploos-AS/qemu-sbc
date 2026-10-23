# M1 implementation gates: Orange Pi Zero LTS

## Baseline source inspection

After `./scripts/bootstrap-qemu.sh`, run:

```sh
python3 scripts/inspect-h3-reference.py --qemu-src _work/qemu
```

This inspects the **actual** checked-out `hw/arm/orangepi.c`, `hw/arm/allwinner-h3.c`, and `include/hw/arm/allwinner-h3.h` rather than relying on remembered QEMU APIs. It reports relevant H3 symbols. It does not create a board or establish H2+ register compatibility.

## First real machine patch

Implement an independent `orangepi-zero-lts` QEMU machine registration, with explicit RAM size, ARM Cortex-A7 CPU configuration and H2+ board wiring. Use the H3 reference only for confirmed compatible subsystems. Do not implement a cosmetic alias to `orangepi-pc` and claim it emulates Zero LTS.

Before adding any new MMIO region, document its base, size, IRQ, reset behavior, reference source and expected Linux DTS binding.

## Evidence required to close M1

- Machine is listed by `qemu-system-arm -machine help`.
- Machine instantiates without fatal errors in a pinned QEMU build.
- qtests validate at least reset, UART MMIO and interrupt behavior.
- A redistributable U-Boot build produces a repeatable UART boot log.
- Tested QEMU source commit, bootloader commit and artifact hashes are recorded.

Reference functional tests for `orangepi-pc`:
https://www.qemu.org/docs/master/system/arm/orangepi.html

These reference tests do **not** validate the new H2+ model.
