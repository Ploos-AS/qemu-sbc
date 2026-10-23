#!/usr/bin/env python3
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "translate-h2-gic.py"


class GicTests(unittest.TestCase):
    def translate(self, cells):
        with tempfile.TemporaryDirectory() as d:
            src, dst = Path(d) / "input.json", Path(d) / "output.json"
            src.write_text(json.dumps({"peripherals": {"uart0": {"interrupts": {"cells": [cells]}}}}))
            proc = subprocess.run([sys.executable, str(SCRIPT), str(src),
                                   "--output", str(dst)], capture_output=True, text=True)
            return proc, json.loads(dst.read_text()) if dst.exists() else None

    def test_spi(self):
        proc, data = self.translate(["0", "49", "4"])
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(data["interrupts"]["uart0"]["gic_interrupt_id"], 81)

    def test_ppi(self):
        proc, data = self.translate(["1", "7", "4"])
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(data["interrupts"]["uart0"]["gic_interrupt_id"], 23)

    def test_bad_type(self):
        self.assertNotEqual(self.translate(["2", "49", "4"])[0].returncode, 0)

    def test_known_gic_macros(self):
        proc, data = self.translate(["GIC_SPI", "49", "IRQ_TYPE_LEVEL_HIGH"])
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(data["interrupts"]["uart0"]["gic_interrupt_id"], 81)

    def test_unresolved_macro(self):
        self.assertNotEqual(self.translate(["UNKNOWN_IRQ_TYPE", "49", "4"])[0].returncode, 0)

    def test_invalid_ppi(self):
        self.assertNotEqual(self.translate(["1", "16", "4"])[0].returncode, 0)


if __name__ == "__main__":
    unittest.main()
