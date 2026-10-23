#!/usr/bin/env python3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "create-h2-skeleton.py"


class H2SkeletonTests(unittest.TestCase):
    def test_dry_run_apply_and_idempotence(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            arm = root / "hw" / "arm"
            arm.mkdir(parents=True)
            (arm / "orangepi.c").write_text("upstream")
            cmd = [sys.executable, str(SCRIPT), "--qemu-src", str(root)]
            dry = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(dry.returncode, 0, dry.stderr)
            self.assertFalse((arm / "allwinner-h2.c").exists())
            for _ in range(2):
                result = subprocess.run(cmd + ["--apply"], capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((arm / "orangepi-zero-lts.c").exists())
            self.assertNotIn("DEFINE_MACHINE(", (arm / "orangepi-zero-lts.c").read_text().replace("No DEFINE_MACHINE until", ""))

    def test_never_overwrites_existing_code(self):
        with tempfile.TemporaryDirectory() as directory:
            arm = Path(directory) / "hw" / "arm"
            arm.mkdir(parents=True)
            (arm / "orangepi.c").write_text("upstream")
            (arm / "allwinner-h2.c").write_text("custom implementation")
            proc = subprocess.run([sys.executable, str(SCRIPT), "--qemu-src",
                                   directory, "--apply"], capture_output=True, text=True)
            self.assertNotEqual(proc.returncode, 0)
            self.assertEqual((arm / "allwinner-h2.c").read_text(), "custom implementation")


if __name__ == "__main__":
    unittest.main()
