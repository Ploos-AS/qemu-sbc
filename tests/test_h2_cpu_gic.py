#!/usr/bin/env python3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/audit-h2-cpu-gic.py"
SOURCE = """
object_initialize_child(obj, "cpu[*]", &s->cpus[i], ARM_CPU_TYPE_NAME("cortex-a7"));
object_initialize_child(obj, "gic", &s->gic, TYPE_ARM_GIC);
sysbus_realize(SYS_BUS_DEVICE(&s->gic), &error_fatal);
qdev_get_gpio_in(cpudev, ARM_CPU_IRQ);
qdev_get_gpio_in(cpudev, ARM_CPU_FIQ);
AW_H3_GIC_PPI_SECTIMER
qdev_get_gpio_in(DEVICE(&s->gic), AW_H3_GIC_SPI_UART0);
"""


class CpuGicAuditTests(unittest.TestCase):
    def run_audit(self, source):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "h3.c"
            path.write_text(source)
            return subprocess.run([sys.executable, str(SCRIPT), str(path),
                                   "--output", str(Path(d) / "out.json")],
                                  capture_output=True, text=True)

    def test_reference_passes(self):
        result = self.run_audit(SOURCE)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_missing_gic_fails(self):
        self.assertNotEqual(self.run_audit(SOURCE.replace('"gic"', '"other"')).returncode, 0)

    def test_missing_cpu_irq_fails(self):
        self.assertNotEqual(self.run_audit(SOURCE.replace("ARM_CPU_IRQ", "ARM_CPU_VIRQ")).returncode, 0)


if __name__ == "__main__":
    unittest.main()
