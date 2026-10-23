#!/usr/bin/env python3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/integrate-h2-uart0-meson.py"
ENTRY = "arm_ss.add(when: 'CONFIG_ALLWINNER_H3', if_true: files('allwinner-h3.c', 'orangepi.c'))"


class MesonIntegrationTests(unittest.TestCase):
    def test_apply_idempotent(self):
        with tempfile.TemporaryDirectory() as d:
            arm = Path(d) / "hw/arm"
            arm.mkdir(parents=True)
            (arm / "meson.build").write_text(ENTRY + "\n")
            (arm / "allwinner-h2-uart0.c").write_text("candidate")
            cmd = [sys.executable, str(SCRIPT), "--qemu-src", d]
            self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 0)
            self.assertNotIn("allwinner-h2-uart0.c", (arm / "meson.build").read_text())
            for _ in range(2):
                result = subprocess.run(cmd + ["--apply"], capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual((arm / "meson.build").read_text().count(
                "files('allwinner-h2-uart0.c')"), 1)

    def test_refuse_unexpected_meson(self):
        with tempfile.TemporaryDirectory() as d:
            arm = Path(d) / "hw/arm"
            arm.mkdir(parents=True)
            (arm / "meson.build").write_text("other")
            (arm / "allwinner-h2-uart0.c").write_text("candidate")
            proc = subprocess.run([sys.executable, str(SCRIPT), "--qemu-src",
                                   d, "--apply"], capture_output=True)
            self.assertNotEqual(proc.returncode, 0)


if __name__ == "__main__":
    unittest.main()
