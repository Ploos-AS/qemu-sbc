#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
arm="${QEMU_ARM:-$root/_work/qemu/build/qemu-system-arm}"
if [[ ! -x "$arm" ]]; then
  echo "QEMU ARM binary not found: $arm" >&2
  exit 2
fi
machines="$("$arm" -machine help)"
if ! grep -Eq '^[[:space:]]*orangepi-pc([[:space:]]|$)' <<< "$machines"; then
  echo "FAIL: upstream orangepi-pc reference machine is missing" >&2
  exit 1
fi
echo "PASS: upstream orangepi-pc reference exists"
if grep -Eq '^[[:space:]]*orangepi-zero-lts([[:space:]]|$)' <<< "$machines"; then
  echo "INFO: orangepi-zero-lts registered; dedicated boot/qtests are still required"
else
  echo "EXPECTED: orangepi-zero-lts not implemented yet"
fi
