#!/usr/bin/env bash
# Build a dependency-free ARM EABI /init archive for Linux handoff.
# SPDX-License-Identifier: MIT
set -euo pipefail
output="${1:?usage: build-h2-initramfs.sh OUTPUT.cpio.gz}"
output="$(realpath -m "$output")"
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT
arm-linux-gnueabihf-gcc -Os -static -nostdlib -ffreestanding -fno-stack-protector -march=armv7-a -mfpu=vfpv3-d16 -mfloat-abi=hard -Wl,-e,_start -Wl,--build-id=none -o "$work/init" tests/guest/h2-linux-init.c
arm-linux-gnueabihf-readelf -h "$work/init" | grep -q 'Machine:.*ARM'
(cd "$work"; printf 'init\n' | cpio --quiet -o -H newc | gzip -n -9) > "$output"
test -s "$output"
echo "Built ARM Linux initramfs: $output"
