# Upstream-first development policy

QEMU's ARM Orange Pi PC reference:
https://www.qemu.org/docs/master/system/arm/orangepi.html

- Develop board models against a **recorded, pinned** upstream QEMU commit or release.
- Keep machine and peripheral patches independently reviewable.
- Follow existing QEMU coding style, SPDX headers and contributor submission rules.
- Include qtests for reset, register maps and device behavior.
- Keep board-specific hardware facts separate from implementation assumptions.
- Do not copy third-party firmware, vendor blobs or calibration data into Git.
- Before claiming firmware-image compatibility, boot an exact legal image and record provenance, hash and logs.

The current M0 bootstrap script tracks upstream HEAD unless `QEMU_REF` is supplied. Therefore builds are **not yet pinned by default**. Pin a tested revision before M1 implementation work.
