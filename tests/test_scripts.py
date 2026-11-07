"""Tests for the workspace scripts. Run with: python -m unittest discover tests"""

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"


class ScriptTestCase(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.workspace = self.root / "cadre_workspace"
        self.data = self.root / "data.csv"
        self.data.write_bytes(b"a,b\n1,2\n")

    def run_script(self, script, *args, env=None):
        return subprocess.run(
            [sys.executable, str(SCRIPTS / script), *args],
            cwd=self.root, env=env, capture_output=True, text=True, encoding="utf-8",
        )

    def init(self, *args, env=None):
        return self.run_script(
            "init_workspace.py", "--project", "Test", "--lang", "es", *args, env=env
        )

    def hash(self, *args):
        return self.run_script("hash_artifact.py", *args)

    def manifest(self):
        return json.loads((self.workspace / "cadre_manifest.json").read_text(encoding="utf-8"))

    def entry(self, artifact_id):
        return next(e for e in self.manifest()["artifacts"] if e["id"] == artifact_id)

    def artifact(self, content="first"):
        path = self.workspace / "stage_03" / "notes.md"
        path.write_text(content, encoding="utf-8")
        return str(path)


class InitWorkspaceTests(ScriptTestCase):
    def test_creates_structure_and_hashes_data(self):
        result = self.init("--data", "data.csv", "--environment", "claude_ai")
        self.assertEqual(result.returncode, 0, result.stderr)
        for directory in ["stage_01", "stage_08", "research/snapshots"]:
            self.assertTrue((self.workspace / directory).is_dir(), directory)
        self.assertTrue((self.workspace / "requirements.txt").is_file())
        self.assertTrue((self.workspace / "CHANGELOG.md").is_file())

        manifest = self.manifest()
        self.assertEqual(manifest["output_language"], "es")
        self.assertEqual(manifest["environment"], "claude_ai")
        entry = self.entry("data")
        self.assertEqual(entry["type"], "raw_data")
        self.assertEqual(entry["path"], "../data.csv")
        self.assertEqual(entry["sha256"], hashlib.sha256(self.data.read_bytes()).hexdigest())

    def test_refuses_to_overwrite_manifest(self):
        self.init()
        before = (self.workspace / "cadre_manifest.json").read_bytes()
        self.assertEqual(self.init().returncode, 1)
        self.assertEqual((self.workspace / "cadre_manifest.json").read_bytes(), before)

    def test_missing_data_creates_nothing(self):
        self.assertEqual(self.init("--data", "missing.csv").returncode, 1)
        self.assertFalse(self.workspace.exists())

    def test_rejects_invalid_language(self):
        result = self.run_script("init_workspace.py", "--project", "Test", "--lang", "Spanish")
        self.assertEqual(result.returncode, 1)
        self.assertFalse(self.workspace.exists())

    def test_detects_environment(self):
        env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
        self.init(env=env)
        self.assertEqual(self.manifest()["environment"], "unknown")

    def test_detects_claude_code(self):
        self.init(env={**os.environ, "CLAUDECODE": "1"})
        self.assertEqual(self.manifest()["environment"], "claude_code")

    def test_keeps_non_ascii_project_name(self):
        name = "Pingüinos — Análisis"
        result = self.run_script("init_workspace.py", "--project", name, "--lang", "es")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.manifest()["project_name"], name)

    def test_conda_option(self):
        self.init("--env-file", "conda")
        self.assertTrue((self.workspace / "environment.yml").is_file())
        self.assertFalse((self.workspace / "requirements.txt").exists())
        self.assertEqual(self.manifest()["requirements_path"], "./environment.yml")


class HashArtifactTests(ScriptTestCase):
    def setUp(self):
        super().setUp()
        self.init("--data", "data.csv")

    def test_registers_new_artifact(self):
        result = self.hash(self.artifact(), "--type", "eda_report", "--stage", "5")
        self.assertEqual(result.returncode, 0, result.stderr)
        entry = self.entry("stage-03-notes")
        self.assertEqual(entry["path"], "stage_03/notes.md")
        self.assertEqual(entry["language"], "es")

    def test_new_artifact_needs_type_and_stage(self):
        self.assertEqual(self.hash(self.artifact()).returncode, 1)

    def test_updates_in_place(self):
        path = self.artifact()
        self.hash(path, "--type", "eda_report", "--stage", "5")
        count = len(self.manifest()["artifacts"])
        self.artifact("second")
        self.assertEqual(self.hash(path).returncode, 0)
        self.assertEqual(len(self.manifest()["artifacts"]), count)
        self.assertEqual(
            self.entry("stage-03-notes")["sha256"],
            hashlib.sha256(b"second").hexdigest(),
        )

    def test_change_clears_human_review(self):
        path = self.artifact()
        self.hash(path, "--type", "eda_report", "--stage", "5")
        manifest = self.manifest()
        reviewed = next(e for e in manifest["artifacts"] if e["id"] == "stage-03-notes")
        reviewed.update(reviewed_by_human=True, reviewed_by="SR", reviewed_at="2026-11-06")
        (self.workspace / "cadre_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

        self.hash(path)  # Same content keeps the review.
        self.assertTrue(self.entry("stage-03-notes")["reviewed_by_human"])

        self.artifact("second")
        result = self.hash(path)
        self.assertIn("Warning", result.stderr)
        entry = self.entry("stage-03-notes")
        self.assertFalse(entry["reviewed_by_human"])
        self.assertIsNone(entry["reviewed_by"])

    def test_refuses_changed_raw_data(self):
        before = (self.workspace / "cadre_manifest.json").read_bytes()
        self.data.write_bytes(b"a,b\n1,3\n")
        result = self.hash(str(self.data))
        self.assertEqual(result.returncode, 1)
        self.assertIn("no longer matches", result.stderr)
        self.assertEqual((self.workspace / "cadre_manifest.json").read_bytes(), before)

    def test_unchanged_raw_data_passes(self):
        result = self.hash(str(self.data))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Unchanged", result.stdout)

    def test_refuses_manifest_itself(self):
        path = str(self.workspace / "cadre_manifest.json")
        self.assertEqual(self.hash(path, "--type", "manifest", "--stage", "0").returncode, 1)

    def test_rejects_id_in_use(self):
        result = self.hash(self.artifact(), "--type", "eda_report", "--stage", "5", "--id", "data")
        self.assertEqual(result.returncode, 1)

    def test_superseded_entry_is_not_updated(self):
        path = self.artifact()
        self.hash(path, "--type", "eda_report", "--stage", "5")
        manifest = self.manifest()
        old = next(e for e in manifest["artifacts"] if e["id"] == "stage-03-notes")
        old["superseded_by"] = "stage-03-notes-v2"
        old_hash = old["sha256"]
        (self.workspace / "cadre_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

        self.artifact("second")
        result = self.hash(path, "--type", "eda_report", "--stage", "5", "--id", "stage-03-notes-v2")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.entry("stage-03-notes")["sha256"], old_hash)
        self.assertEqual(
            self.entry("stage-03-notes-v2")["sha256"],
            hashlib.sha256(b"second").hexdigest(),
        )

    def test_missing_manifest(self):
        result = self.hash(str(self.data), "--workspace", "elsewhere")
        self.assertEqual(result.returncode, 1)
        self.assertIn("init_workspace.py", result.stderr)


if __name__ == "__main__":
    unittest.main()
