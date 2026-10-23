#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
dir="${QEMU_SRC:-$root/_work/qemu}"
ref="${QEMU_REF:-v10.0.0}"
if [[ ! -d "$dir/.git" ]]; then
  mkdir -p "$(dirname "$dir")"
  git clone --no-checkout --filter=blob:none https://gitlab.com/qemu-project/qemu.git "$dir"
fi
git -C "$dir" fetch --depth 1 origin "$ref"
git -C "$dir" checkout --detach FETCH_HEAD
sha="$(git -C "$dir" rev-parse HEAD)"
echo "QEMU source reference: $ref"
echo "QEMU source commit: $sha"
if [[ -z "${QEMU_REF:-}" ]]; then
  bash "$root/scripts/verify-qemu-revision.sh" "$dir"
fi
mkdir -p "$dir/build"
cd "$dir/build"
../configure --target-list=arm-softmmu,mips-softmmu --disable-werror
make -j"${JOBS:-2}"
