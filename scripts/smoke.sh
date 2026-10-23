#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
build="${QEMU_BUILD:-$root/_work/qemu/build}"
arm="$build/qemu-system-arm"
mips="$build/qemu-system-mips"
if [[ ! -x "$arm" || ! -x "$mips" ]]; then
  echo "Build QEMU first using bash scripts/bootstrap-qemu.sh" >&2
  exit 2
fi
"$arm" --version
"$mips" --version
"$arm" -machine help | grep -q 'orangepi-pc'
echo "PASS: upstream ARM orangepi-pc machine listed"
"$mips" -machine help >/dev/null
echo "PASS: upstream MIPS machine list accessible"
echo "M0 smoke tests passed; no custom board emulation is asserted."
