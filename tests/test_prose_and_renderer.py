#!/usr/bin/env python3
"""Exercises the drafts gates: prose gate, identifier sweep, renderer defaults."""
import base64
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROSE = os.path.join(ROOT, "scripts", "protean-drafts", "check-prose.py")
SKILL = os.path.join(ROOT, "skills", "draft-review-html", "SKILL.md")


def run(cmd, cwd=None):
    return subprocess.run(cmd, capture_output=True, text=True, cwd=cwd or ROOT,
                          timeout=120)


class TestProseGate(unittest.TestCase):
    def test_clean_file_passes(self):
        result = run([sys.executable, PROSE, SKILL])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_banned_phrase_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "draft.md")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write("Two things worth stating. The right shape.\n")
            result = run([sys.executable, PROSE, path])
            self.assertEqual(result.returncode, 1)
            self.assertIn("AI tell", result.stdout)

    def test_denylist_pattern_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "draft.md")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write("owner: " + base64.b64decode("b3JkYQ==").decode() + "\n")
            deny = os.path.join(tmp, "patterns.txt")
            with open(deny, "w", encoding="utf-8") as fh:
                fh.write(base64.b64decode("b3JkYQ==").decode() + "\n")
            result = run([sys.executable, PROSE, "--denylist", deny, path])
            self.assertEqual(result.returncode, 1)
            self.assertIn("internal identifier", result.stdout)


class TestRendererDefaults(unittest.TestCase):
    def test_renderer_defaults_gate_passes(self):
        result = run([sys.executable,
                      os.path.join(ROOT, "gates", "protean-drafts",
                                   "check-renderer-defaults.py")])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
