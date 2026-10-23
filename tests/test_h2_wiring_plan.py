#!/usr/bin/env python3
"""Regression tests for the source-derived MMIO/GIC wiring plan."""
import json
import subprocess
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "build-h2-wiring-plan.py"
BASES = {"uart0": 0x01c28000, "mmc0": 0x01c0f000, "emac": 0x01c30000}


def fixtures():
    mmio, gic = {}, {}
    for idx, (name, address) in enumerate(BASES.items()):
        mmio[name] = {"unit_address": hex(address),
                      "reg": {"cells": [[hex(address), "0x400"]]}}
        gic[name] = {"kind": "SPI", "index": idx + 20,
                     "gic_interrupt_id": idx + 52, "flags": 4}
    return {"peripherals": mmio}, {"interrupts": gic}


class WiringPlanTests(unittest.TestCase):
    def check(self, mmio, gic):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            a, b, output = root / "mmio.json", root / "gic.json", root / "out.json"
            a.write_text(json.dumps(mmio))
            b.write_text(json.dumps(gic))
            proc = subprocess.run([sys.executable, str(SCRIPT), str(a), str(b),
                                   "--output", str(output)], capture_output=True, text=True)
            return proc, json.loads(output.read_text()) if output.exists() else None

    def test_valid_plan_marks_unimplemented(self):
        proc, data = self.check(*fixtures())
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertFalse(data["h2_hardware_verified"])
        self.assertFalse(data["qemu_wiring_implemented"])
        self.assertEqual(len(data["devices"]), 3)

    def test_mismatched_register_base_rejected(self):
        mmio, gic = fixtures()
        mmio["peripherals"]["uart0"]["reg"]["cells"][0][0] = "0x01c20000"
        self.assertNotEqual(self.check(mmio, gic)[0].returncode, 0)

    def test_duplicate_irq_rejected(self):
        mmio, gic = fixtures()
        gic["interrupts"]["mmc0"]["index"] = gic["interrupts"]["uart0"]["index"]
        gic["interrupts"]["mmc0"]["gic_interrupt_id"] = gic["interrupts"]["uart0"]["gic_interrupt_id"]
        self.assertNotEqual(self.check(mmio, gic)[0].returncode, 0)

    def test_missing_device_rejected(self):
        mmio, gic = fixtures()
        del mmio["peripherals"]["emac"]
        self.assertNotEqual(self.check(mmio, gic)[0].returncode, 0)

    def test_zero_length_rejected(self):
        mmio, gic = fixtures()
        mmio["peripherals"]["mmc0"]["reg"]["cells"][0][1] = "0"
        self.assertNotEqual(self.check(mmio, gic)[0].returncode, 0)


if __name__ == "__main__":
    unittest.main()
