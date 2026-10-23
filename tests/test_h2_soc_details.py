#!/usr/bin/env python3
"""Offline negative and positive tests for the raw SoC detail extractor."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "extract-h2-soc-details.py"
NODES = """
uart0: serial@01c28000 { reg = <0x01c28000 0x400>; interrupts = <0 1 4>; };
mmc0: mmc@01c0f000 { reg = <0x01c0f000 0x1000>; interrupts = <0 2 4>; };
emac: ethernet@01c30000 { reg = <0x01c30000 0x10000>; interrupts = <0 3 4>; };
"""


class DetailsTests(unittest.TestCase):
    def check(self, content):
        with tempfile.TemporaryDirectory() as temp:
            src = Path(temp) / "test.dtsi"
            dst = Path(temp) / "out.json"
            src.write_text(content)
            result = subprocess.run([sys.executable, str(SCRIPT), str(src),
                                     "--output", str(dst)], capture_output=True, text=True)
            return result, json.loads(dst.read_text()) if dst.exists() else None

    def test_valid(self):
        result, data = self.check(NODES)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(data["peripherals"]["uart0"]["reg"]["cells"][0][0], "0x01c28000")

    def test_missing_interrupts(self):
        result, _ = self.check(NODES.replace("interrupts = <0 2 4>;", ""))
        self.assertNotEqual(result.returncode, 0)

    def test_empty_register(self):
        result, _ = self.check(NODES.replace("reg = <0x01c30000 0x10000>;", "reg = <>;"))
        self.assertNotEqual(result.returncode, 0)

    def test_nested_ethernet_child_register_is_ignored(self):
        src = NODES.replace(
            "interrupts = <0 3 4>; };",
            """interrupts = <0 3 4>;
                mdio {
                    phy0: ethernet-phy@1 {
                        reg = <1>;
                        interrupts = <0 99 4>;
                    };
                };
            };""")
        result, data = self.check(src)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            data["peripherals"]["emac"]["reg"]["cells"],
            [["0x01c30000", "0x10000"]])
        self.assertEqual(
            data["peripherals"]["emac"]["interrupts"]["cells"],
            [["0", "3", "4"]])

    def test_duplicate_uart(self):
        result, _ = self.check(NODES + NODES.splitlines()[1] + "\n")
        self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
