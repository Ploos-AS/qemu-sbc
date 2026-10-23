# Experimental H2+ registration prototype

The prototype `orangepi-zero-lts-proto` uses the existing QEMU H3 board
initializer. It is **not** an Orange Pi Zero LTS / H2+ emulator.

## Verified source build

Commit `27ba839a752cf0bd3bce90cb06f968a4d72a0035` passed QEMU v10.0.0
source build, machine registration and QMP startup:
https://github.com/Ploos-AS/qemu-sbc/actions/runs/39908681050

The experimental machine inherits the H3 board's fixed **1 GiB RAM**
restriction. The source-build CI also contains a negative test checking
that a 256 MiB configuration is rejected, to prevent accidental claims
of correct H2+ RAM support.

## Local reproduction

```sh
./scripts/bootstrap-qemu.sh
python3 scripts/create-h2-prototype.py --qemu-src _work/qemu --apply
make -C _work/qemu/build -j2 qemu-system-arm
python3 scripts/verify-prototype-qmp.py _work/qemu/build/qemu-system-arm
python3 scripts/verify-prototype-ram.py _work/qemu/build/qemu-system-arm
```

Bootstrap checks out the upstream baseline; apply the generator **after**
bootstrap. Source changes are local to `_work/qemu`.

## Next engineering gates

- [x] QEMU v10.0.0 generator, source build and machine registration
- [x] QMP startup
- [ ] Confirm exact Orange Pi Zero LTS RAM variants from board references
- [ ] Implement dedicated H2+ SoC and board initialization
- [ ] Test actual RAM, MMIO, reset, UART and U-Boot serial boot

**Do not** interpret prototype registration or QMP startup as real H2+
hardware support.
