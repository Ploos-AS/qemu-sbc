#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
dir="${QEMU_SRC:-$root/_work/qemu}"
if [[ ! -d "$dir/.git" ]]; then
  mkdir -p "$(dirname "$dir")"
  git clone --depth 1 https://gitlab.com/qemu-project/qemu.git "$dir"
fi
if [[ -n "${QEMU_REF:-}" ]]; then
  git -C "$dir" fetch --depth 1 origin "$QEMU_REF"
  git -C "$dir" checkout --detach FETCH_HEAD
fi
echo "QEMU revision: $(git -C "$dir" rev-parse HEAD)"
mkdir -p "$dir/build"
cd "$dir/build"
../configure --target-list=arm-softmmu,mips-softmmu --disable-werror
make -j"${JOBS:-2}"
