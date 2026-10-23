# QEMU source baseline

The bootstrap script defaults to the **QEMU v10.0.0 release tag** rather than tracking upstream HEAD.

```sh
./scripts/bootstrap-qemu.sh
./scripts/smoke.sh
./scripts/check-m1-baseline.sh
```

To override the source revision for experiments:

```sh
QEMU_REF=v10.0.0 ./scripts/bootstrap-qemu.sh
```

The script prints the full resolved commit SHA for traceability. **The tag is a reproducible release selector, but this repository has not yet recorded and independently verified its commit SHA.** Before machine implementation, record the resolved SHA from a successful build and optionally enforce it in CI.

GitHub Actions currently installs distribution-packaged QEMU for lightweight smoke tests; that does **not** validate a source build of the chosen release tag. Keep those test categories distinct.

The reference `orangepi-pc` machine is Allwinner H3. It is not the target Orange Pi Zero LTS H2+ machine.
