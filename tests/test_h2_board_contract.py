#!/usr/bin/env python3
"""Ensure independent board contract does not claim an H3 alias is H2+."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class H2BoardContractTests(unittest.TestCase):
    def test_prototype_explicitly_disclaims_h2(self):
        source = (ROOT / "scripts/create-h2-prototype.py").read_text()
        self.assertIn("NOT Orange Pi Zero LTS hardware emulation", source)
        self.assertIn("orangepi_machine_init(mc);", source)

    def test_independent_machine_requires_own_soc(self):
        doc = (ROOT / "docs/H2-BOARD-CONTRACT.md").read_text()
        self.assertIn("allwinner-h2.c", doc)
        self.assertIn("UART0 qtest", doc)
        self.assertIn("No independent H2+ machine has been implemented", doc)


if __name__ == "__main__":
    unittest.main()
