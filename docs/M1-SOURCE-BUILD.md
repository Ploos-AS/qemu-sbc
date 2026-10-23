# Source-build verification for experimental prototype

## Verified CI result

GitHub Actions source build run
[39908681050](https://github.com/Ploos-AS/qemu-sbc/actions/runs/39908681050)
completed successfully on commit
`27ba839a752cf0bd3bce90cb06f968a4d72a0035`.

The workflow fetched QEMU v10.0.0, ran H3 source inspection, applied the
`orangepi-zero-lts-proto` registration, compiled `qemu-system-arm`,
checked machine registration and confirmed a QMP greeting and command
response. The accompanying static workflow run 39908681117 passed.

Upstream QEMU v10.0.0 was resolved in the earlier run to
`7c949c53e936aa3a658d84ab53bae5cadaa5d59c`.

## Limits

- H3-backed research prototype, not an H2+ SoC implementation.
- No U-Boot, UART boot log, MMC boot, guest Linux or Ethernet test.
- Current model inherits the H3 board's 1 GiB RAM requirement.

## Next engineering gate

Record actual Orange Pi Zero LTS hardware RAM sizes, implement a separate
board initialization path with verified H2+ behavior, then add qtests and
bootloader evidence. Do not change the final board support status based
solely on the successful prototype source build.
