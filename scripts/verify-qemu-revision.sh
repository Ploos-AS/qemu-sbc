#!/usr/bin/env bash
set -euo pipefail
src="${1:-_work/qemu}"
expected="7c949c53e936aa3a658d84ab53bae5cadaa5d59c"
actual="$(git -C "$src" rev-parse HEAD)"
printf 'Expected QEMU commit: %s\nActual QEMU commit:   %s\n' "$expected" "$actual"
if [[ "$actual" != "$expected" ]]; then
  echo "FAIL: QEMU source revision mismatch" >&2
  exit 1
fi
echo "PASS: exact QEMU v10.0.0 baseline"
