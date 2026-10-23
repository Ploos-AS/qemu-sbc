#!/usr/bin/env python3
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "generate-h2-uart0.py"


def plan():
    return {"h2_hardware_verified": False, "qemu_wiring_implemented": False,
            "devices": {"uart0": {"mmio_base": "0x01c28000", "mmio_size": 0x400,
                                  "gic_spi_index": 32, "gic_interrupt_id": 64,
                                  "implementation_status": "not_implemented"}}}


class Uart0ConstantsTests(unittest.TestCase):
    def run_generator(self, value):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "plan.json"
            output = Path(directory) / "uart.h"
            source.write_text(json.dumps(value))
            result = subprocess.run([sys.executable, str(SCRIPT), str(source),
                                     "--output", str(output)], capture_output=True, text=True)
            return result, output.read_text() if output.exists() else None

    def test_generates_expected_uart0_defines(self):
        result, content = self.run_generator(plan())
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("#define H2_UART0_MMIO_BASE 0x01c28000u", content)
        self.assertIn("#define H2_UART0_GIC_INTERRUPT_ID 64u", content)

    def test_rejects_misalignment(self):
        value = plan()
        value["devices"]["uart0"]["mmio_base"] = "0x01c28001"
        self.assertNotEqual(self.run_generator(value)[0].returncode, 0)

    def test_rejects_inconsistent_irq(self):
        value = plan()
        value["devices"]["uart0"]["gic_interrupt_id"] = 65
        self.assertNotEqual(self.run_generator(value)[0].returncode, 0)

    def test_rejects_unverified_claim(self):
        value = plan()
        value["h2_hardware_verified"] = True
        self.assertNotEqual(self.run_generator(value)[0].returncode, 0)


if __name__ == "__main__":
    unittest.main()
