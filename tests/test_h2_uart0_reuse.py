#!/usr/bin/env python3
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "audit-h2-uart0-reuse.py"
SOURCE = """
[AW_H3_DEV_UART0] = 0x01c28000,
AW_H3_GIC_SPI_UART0 = 0,
serial_mm_init(get_system_memory(), s->memmap[AW_H3_DEV_UART0], 2,
               qdev_get_gpio_in(DEVICE(&s->gic), AW_H3_GIC_SPI_UART0),
               115200, serial_hd(0), DEVICE_LITTLE_ENDIAN);
"""


class UartReuseTests(unittest.TestCase):
    def run_audit(self, source=SOURCE, base="0x01c28000", spi=0):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "h3.c").write_text(source)
            (root / "plan.json").write_text(json.dumps({"devices": {"uart0": {
                "mmio_base": base, "gic_spi_index": spi}}}))
            result = subprocess.run([sys.executable, str(SCRIPT), str(root / "h3.c"),
                                     str(root / "plan.json"), "--output", str(root / "out.json")],
                                    capture_output=True, text=True)
            output = root / "out.json"
            return result, json.loads(output.read_text()) if output.exists() else None

    def test_matching_source(self):
        result, data = self.run_audit()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(data["h2_uart_implemented"])

    def test_wrong_base(self):
        self.assertNotEqual(self.run_audit(base="0x01c28400")[0].returncode, 0)

    def test_wrong_irq(self):
        self.assertNotEqual(self.run_audit(spi=1)[0].returncode, 0)

    def test_changed_qemu_wiring(self):
        self.assertNotEqual(self.run_audit(source=SOURCE.replace(
            "AW_H3_GIC_SPI_UART0),", "AW_H3_GIC_SPI_UART1),"))[0].returncode, 0)


if __name__ == "__main__":
    unittest.main()
