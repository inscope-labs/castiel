#!/usr/bin/env python3
"""Tests for build_release.py. Run: python3 -m unittest discover -s amk/scripts -p 'test_*.py'"""
import json
import tempfile
import unittest
from pathlib import Path

import build_release as br


class BuildReleaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.out = Path(cls.tmp.name)
        cls.release, cls.errors, cls.warnings = br.build(cls.out / "a", strict=False, include_open_items=False)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_builds_and_verifies(self):
        self.assertEqual(self.errors, [])
        self.assertEqual(br.verify(self.release), [])

    def test_manifest_lists_generated_specs(self):
        manifest = json.loads((self.release / "release/MANIFEST.json").read_text())
        outputs = {g["output"] for g in manifest["generated"]}
        self.assertIn("amk/protocols-spec-full.md", outputs)
        self.assertIn("amk/components/amk-controller-spec-full.md", outputs)
        self.assertEqual(manifest["format_version"], 1)

    def test_build_is_deterministic(self):
        other, errs, _ = br.build(self.out / "b", strict=False, include_open_items=False)
        self.assertEqual(errs, [])
        self.assertEqual((self.release / "release/SHA256SUMS").read_text(), (other / "release/SHA256SUMS").read_text())

    def test_archive_is_deterministic(self):
        a1, d1 = br.make_archive(self.release)
        a1.unlink()
        _, d2 = br.make_archive(self.release)
        self.assertEqual(d1, d2)

    def test_tampered_file_fails_verify(self):
        rel, _, _ = br.build(self.out / "c", strict=False, include_open_items=False)
        (rel / "amk/amk-ssot.md").write_text("tampered\n")
        self.assertTrue(any("checksum mismatch" in e for e in br.verify(rel)))

    def test_unlisted_file_fails_verify(self):
        rel, _, _ = br.build(self.out / "d", strict=False, include_open_items=False)
        (rel / "extra.txt").write_text("x")
        self.assertTrue(any("not listed" in e for e in br.verify(rel)))

    def test_version_pattern(self):
        for ok in ("0.1.0", "1.2.3-rc.1", "2.0.0+build.5"):
            self.assertRegex(ok, br.VERSION_RE)
        for bad in ("TODO", "v0.1", "0.1"):
            self.assertNotRegex(bad, br.VERSION_RE)


if __name__ == "__main__":
    unittest.main()
