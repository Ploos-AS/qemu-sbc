# Source-build verification for experimental prototype

CI source build runs when generator, inspection, QMP verifier or workflow changes,
and may be triggered manually.

## First CI failure and correction

Run 39908574348 fetched QEMU v10.0.0 successfully (resolved SHA
`7c949c53e936aa3a658d84ab53bae5cadaa5d59c`) and passed H3 source
inspection, but the generator rejected `orangepi.c`.

Root cause: the generator assumed a `DEFINE_MACHINE_ARM` macro and an
incorrect initializer signature. Actual QEMU v10.0.0 uses
`DEFINE_MACHINE("orangepi-pc", orangepi_machine_init)` and
`static void orangepi_machine_init(MachineClass *mc)`.

The generator and its unit-test fixture now use the actual upstream
declarations. A successful subsequent source build is required before
claiming prototype registration or QMP initialization.

This remains an H3-backed research prototype, **not** H2+ emulation.
