#!/usr/bin/env python3
"""Offline regression tests for the inherited DTSI address extractor."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "extract-h2-soc-map.py"


class ExtractorTests(unittest.TestCase):
    def run_extract(self, shared):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            h3 = root / "sun8i-h3.dtsi"
            h3.write_text('#include "sunxi-h3-h5.dtsi"\n')
            common = root / "sunxi-h3-h5.dtsi"
            common.write_text(shared)
            output = root / "result.json"
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(h3), str(common),
                 "--output", str(output)],
                capture_output=True, text=True)
            return result, json.loads(output.read_text()) if output.exists() else None

    def test_three_addresses(self):
        src = """
        uart0: serial@01c28000 {
        };
        mmc0: mmc@01c0f000 {
        };
        emac: ethernet@01c30000 {
        };
        """
        result, data = self.run_extract(src)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(data["peripherals"]["uart0"]["base"], "0x01c28000")
        self.assertEqual(data["peripherals"]["mmc0"]["base"], "0x01c0f000")
        self.assertEqual(data["peripherals"]["emac"]["base"], "0x01c30000")

    def test_missing_device_rejected(self):
        result, _ = self.run_extract("uart0: serial@01c28000 {}\n")
        self.assertNotEqual(result.returncode, 0)

    def test_duplicate_device_rejected(self):
        result, _ = self.run_extract(
            "uart0: serial@01c28000 {}\n"
            "uart0: serial@01c28000 {}\n"
            "mmc0: mmc@01c0f000 {}\n"
            "emac: ethernet@01c30000 {}\n")
        self.assertNotEqual(result.returncode, 0)

    def test_implausible_address_rejected(self):
        result, _ = self.run_extract(
            "uart0: serial@00000000 {}\n"
            "mmc0: mmc@01c0f000 {}\n"
            "emac: ethernet@01c30000 {}\n")
        self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
