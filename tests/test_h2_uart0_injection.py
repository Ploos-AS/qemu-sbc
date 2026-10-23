#!/usr/bin/env python3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/inject-h2-uart0.py"


class InjectTests(unittest.TestCase):
    def test_generates_candidate_helper(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            arm = root / "hw/arm"
            arm.mkdir(parents=True)
            (arm / "orangepi.c").write_text("upstream")
            cmd = [sys.executable, str(SCRIPT), "--qemu-src", str(root), "--apply"]
            self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 0)
            self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 0)
            source = (arm / "allwinner-h2-uart0.c").read_text()
            self.assertIn("serial_mm_init(", source)
            self.assertIn("0x01c28000u", source)
            self.assertNotIn("DEFINE_MACHINE(", source)

    def test_rejects_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            arm = root / "hw/arm"
            arm.mkdir(parents=True)
            (arm / "orangepi.c").write_text("upstream")
            target = arm / "allwinner-h2-uart0.c"
            target.write_text("custom")
            result = subprocess.run([sys.executable, str(SCRIPT), "--qemu-src",
                                     str(root), "--apply"], capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(target.read_text(), "custom")


if __name__ == "__main__":
    unittest.main()
