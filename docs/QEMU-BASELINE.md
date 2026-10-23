# QEMU source baseline

The default QEMU source is the v10.0.0 tag, independently resolved by
GitHub Actions to commit
`7c949c53e936aa3a658d84ab53bae5cadaa5d59c`.

The source-build workflow now checks this **exact commit** before
compiling. The default local bootstrap does the same; `QEMU_REF`
permits explicitly overriding the release for experiments.

```sh
./scripts/bootstrap-qemu.sh
./scripts/smoke.sh
./scripts/check-m1-baseline.sh
```

To experiment with a different upstream ref, set `QEMU_REF` and record
the resulting SHA. This does not make that version a supported baseline.

GitHub Actions' packaged-QEMU smoke test is separate from the actual
v10.0.0 source-build workflow.

The `orangepi-zero-lts-proto` research machine uses H3 internals.
It is not the H2+ Orange Pi Zero LTS target.
