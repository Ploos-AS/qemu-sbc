#!/usr/bin/env python3
"""Guard QTest protocol literals against escaped-newline regressions."""
import ast
from pathlib import Path
import unittest


SCRIPT = Path(__file__).with_name("qtest_h2_bootstrap.py")


class QTestProtocolTests(unittest.TestCase):
    def test_commands_have_real_newlines(self):
        tree = ast.parse(SCRIPT.read_text(encoding="utf-8"))
        commands = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
                continue
            if node.func.attr != "write" or not node.args:
                continue
            if isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, bytes):
                commands.append(node.args[0].value)
        self.assertGreaterEqual(len(commands), 5)
        for command in commands:
            with self.subTest(command=command):
                self.assertTrue(command.endswith(b"\n"))
                self.assertNotIn(b"\\n", command)
                self.assertTrue(command.startswith((b"readl ", b"writel ")))


if __name__ == "__main__":
    unittest.main()
