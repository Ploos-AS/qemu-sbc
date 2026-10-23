#!/usr/bin/env python3
"""Offline safety and idempotence checks for independent H2+ bootstrap injection."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/inject-h2-machine-bootstrap.py"
ANCHOR = "arm_ss.add(when: 'CONFIG_ALLWINNER_H3', if_true: files('allwinner-h3.c', 'orangepi.c'))"


class BootstrapTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "hw/arm").mkdir(parents=True)
        (self.root / "hw/arm/orangepi.c").write_text("/* fixture */\n")
        (self.root / "hw/arm/meson.build").write_text(ANCHOR + "\n")

    def run_script(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), "--qemu-src",
                               str(self.root), *args], capture_output=True, text=True)

    def test_dry_run_is_nonmutating(self):
        self.assertEqual(self.run_script().returncode, 0)
        self.assertFalse((self.root / "hw/arm/orangepi-zero-lts-h2.c").exists())
        self.assertEqual((self.root / "hw/arm/meson.build").read_text(), ANCHOR + "\n")

    def test_apply_is_idempotent(self):
        self.assertEqual(self.run_script("--apply").returncode, 0)
        path = self.root / "hw/arm/orangepi-zero-lts-h2.c"
        first = path.read_text()
        self.assertIn('orangepi-zero-lts-h2', first)
        self.assertIn('H2_DRAM_BASE 0x40000000', first)
        self.assertEqual(self.run_script("--apply").returncode, 0)
        self.assertEqual(path.read_text(), first)
        meson = (self.root / "hw/arm/meson.build").read_text()
        self.assertEqual(meson.count("files('orangepi-zero-lts-h2.c')"), 1)

    def test_refuse_modified_source(self):
        self.assertEqual(self.run_script("--apply").returncode, 0)
        path = self.root / "hw/arm/orangepi-zero-lts-h2.c"
        path.write_text("modified")
        self.assertNotEqual(self.run_script("--apply").returncode, 0)
        self.assertEqual(path.read_text(), "modified")

    def test_refuse_missing_anchor(self):
        (self.root / "hw/arm/meson.build").write_text("different QEMU revision")
        self.assertNotEqual(self.run_script("--apply").returncode, 0)


if __name__ == "__main__":
    unittest.main()
