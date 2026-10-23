# QEMU SBC

QEMU machine-model development for real single-board computers and small routers.

**Status:** M0 bootstrap. No new board model is implemented yet.

## Target boards

| Board | SoC | Architecture | Planned milestone |
|---|---|---|---|
| Orange Pi Zero LTS | Allwinner H2+ | ARM Cortex-A7 | M1–M2 |
| TP-Link TL-WR703N | Atheros AR9331 | MIPS 24Kc | M3–M4 |
| GL.iNet GL-MT300N-V2 (Mango) | MediaTek MT7628NN | MIPS | M5–M6 |

We develop contributions against upstream QEMU, avoiding a permanent large fork where possible. Upstream's `orangepi-pc` (H3) machine is a useful reference, **not** a substitute for an H2+ board model.

## M0

- Document scope, acceptance tests, licensing and upstream workflow.
- Provide a reproducible QEMU source checkout/build script.
- Add smoke checks for existing upstream reference machines.
- Run static checks and smoke checks in GitHub Actions.
- Record board-specific hardware unknowns before implementation.

Run locally (Debian/Ubuntu, with QEMU development dependencies installed):

```sh
./scripts/bootstrap-qemu.sh
./scripts/smoke.sh
```

The bootstrap script clones upstream QEMU into `_work/qemu` and builds only `arm-softmmu` and `mips-softmmu`. It does not modify the upstream source or create board support.

## Structure

- `docs/` scope, roadmap, compatibility policy and architecture notes
- `boards/` board specifications and milestones
- `scripts/` reproducible local tooling
- `.github/workflows/` continuous integration

## License

Project-owned software and scripts: MIT (see LICENSE). Documentation: CC BY 4.0 (see docs/LICENSE.md). Any future patches to QEMU itself must follow QEMU's file-specific SPDX licensing and upstream contribution requirements. Do not redistribute vendor firmware or proprietary blobs in this repository.
