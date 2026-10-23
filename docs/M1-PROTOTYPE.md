# Experimental H2+ registration prototype

This milestone adds a **source transformation experiment**, not a usable Orange Pi Zero LTS emulator.

The prototype registers `orangepi-zero-lts-proto` with QEMU's existing H3 `orangepi_machine_init` implementation. It intentionally retains the H3 board's **1 GiB RAM** and all its H3 peripheral behavior. This is *not* a faithful H2+ implementation, and is not the final `orangepi-zero-lts` name.

## Try it locally

```sh
./scripts/bootstrap-qemu.sh
python3 scripts/create-h2-prototype.py --qemu-src _work/qemu
python3 scripts/create-h2-prototype.py --qemu-src _work/qemu --apply
cd _work/qemu/build && make -j2 qemu-system-arm
./qemu-system-arm -machine help | grep orangepi-zero-lts-proto
```

`bootstrap-qemu.sh` resets the QEMU checkout to its baseline ref on each invocation; run the generator **after** bootstrap. The generated change is local to `_work/qemu` and not a patch against upstream. Run a real source build to verify API compatibility.

## Exit criteria

- [ ] Generator works on the pinned QEMU release
- [ ] New prototype machine registers and instantiates in a source build
- [ ] Determine verified H2+ vs H3 SoC differences
- [ ] Replace prototype with an independent H2+ SoC/board model
- [ ] Add MMIO, reset, UART qtests and U-Boot serial boot

Do not interpret registration, instantiation or successful H3 boot as H2+ hardware emulation.
