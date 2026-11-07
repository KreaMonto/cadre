"""Shared helpers for the CADRE workspace scripts. Standard library only."""

import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

MANIFEST_NAME = "cadre_manifest.json"

# Keep in sync with the type table in references/manifest_spec.md.
ARTIFACT_TYPES = frozenset({
    "project_context", "assessment_report", "analysis_plan", "domain_brief",
    "research_log", "source_list", "source_snapshot", "raw_data",
    "data_dictionary", "raw_data_profile", "clean_data", "cleaning_log",
    "eda_report", "figure", "analysis_report", "model", "robustness_report",
    "final_report", "script", "requirements", "changelog", "manifest",
})

# Artifacts that are not prose for a human reader get a null language.
NON_DOCUMENT_TYPES = frozenset({
    "raw_data", "clean_data", "model", "script", "requirements",
    "source_snapshot",
})


class CadreError(Exception):
    """A problem the user can act on, reported without a traceback."""


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def manifest_relative_path(path, workspace):
    """Return `path` relative to the workspace root, with forward slashes."""
    resolved = Path(path).resolve()
    try:
        return Path(os.path.relpath(resolved, Path(workspace).resolve())).as_posix()
    except ValueError:  # Windows: the file is on a different drive.
        return resolved.as_posix()


def default_artifact_id(relative_path):
    """Build a kebab-case id, e.g. stage_03/data_dictionary.md -> stage-03-data-dictionary."""
    parts = [part for part in Path(relative_path).with_suffix("").parts if part != ".."]
    slug = re.sub(r"[^a-z0-9]+", "-", "-".join(parts).lower()).strip("-")
    if not slug:
        raise CadreError(f"Cannot build an id from '{relative_path}'. Pass one with --id.")
    return slug


def new_entry(artifact_id, stage, artifact_type, relative_path, sha256, language, notes=None):
    """Build an artifact entry with the fields in references/manifest_spec.md."""
    return {
        "id": artifact_id,
        "stage": stage,
        "type": artifact_type,
        "path": relative_path,
        "sha256": sha256,
        "produced_at": now_iso(),
        "language": language,
        "reviewed_by_human": False,
        "reviewed_by": None,
        "reviewed_at": None,
        "superseded_by": None,
        "notes": notes,
    }


def load_manifest(workspace):
    path = Path(workspace) / MANIFEST_NAME
    if not path.is_file():
        raise CadreError(f"No manifest at '{path}'. Run init_workspace.py first.")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise CadreError(f"Manifest '{path}' is not valid JSON: {error}") from error


def save_manifest(workspace, manifest):
    """Write the manifest atomically, so a failed write cannot corrupt it."""
    manifest["last_updated"] = now_iso()
    path = Path(workspace) / MANIFEST_NAME
    temporary = path.with_suffix(".json.tmp")
    temporary.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    os.replace(temporary, path)
