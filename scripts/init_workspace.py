#!/usr/bin/env python3
"""Create a CADRE workspace and its artifact manifest.

Usage:
    python scripts/init_workspace.py --project "My Project" --lang en
    python scripts/init_workspace.py --project "My Project" --lang es --data raw/sales.csv

Input data files are hashed where they are; they are never copied or modified.
An existing manifest is never overwritten, because it holds the provenance record.
"""

import argparse
import os
import platform
import re
import sys
from pathlib import Path

from cadre_manifest import (
    MANIFEST_NAME,
    CadreError,
    default_artifact_id,
    manifest_relative_path,
    new_entry,
    now_iso,
    save_manifest,
    sha256_file,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
STAGE_DIRECTORIES = [f"stage_{number:02d}" for number in range(1, 9)]


def detect_environment():
    """Return claude_code when detectable, otherwise unknown.

    Claude.ai sets no comparable signal, so it must be passed with --environment.
    """
    return "claude_code" if os.environ.get("CLAUDECODE") == "1" else "unknown"


def read_cadre_version():
    match = re.search(
        r'^version:\s*"([^"]+)"',
        (REPO_ROOT / "SKILL.md").read_text(encoding="utf-8"),
        re.MULTILINE,
    )
    if not match:
        raise CadreError("No version found in SKILL.md.")
    return match.group(1)


def build_data_entries(data_paths, workspace):
    entries = {}
    for data_path in data_paths:
        path = Path(data_path)
        if not path.is_file():
            raise CadreError(f"Input data file not found: '{path}'.")
        relative_path = manifest_relative_path(path, workspace)
        artifact_id = default_artifact_id(relative_path)
        existing = entries.get(artifact_id)
        if existing and existing["path"] != relative_path:
            raise CadreError(
                f"'{existing['path']}' and '{relative_path}' produce the same id "
                f"'{artifact_id}'. Register one with hash_artifact.py --id."
            )
        entries[artifact_id] = new_entry(
            artifact_id, 3, "raw_data", relative_path, sha256_file(path), None
        )
    return list(entries.values())


def write_if_missing(path, content):
    if not path.exists():
        path.write_text(content, encoding="utf-8", newline="\n")


def dependency_file(env_file, project):
    """Return the name and skeleton of the dependency file."""
    python_version = platform.python_version()
    if env_file == "conda":
        name = re.sub(r"[^a-z0-9]+", "-", project.lower()).strip("-") or "cadre-project"
        major_minor = ".".join(python_version.split(".")[:2])
        return "environment.yml", (
            f"name: {name}\n"
            "channels:\n"
            "  - conda-forge\n"
            "dependencies:\n"
            f"  - python={major_minor}\n"
            "  # Pin exact versions of the libraries the analysis uses.\n"
        )
    return "requirements.txt", (
        f"# Created with Python {python_version}.\n"
        "# Pin exact versions of the libraries the analysis uses (name==version).\n"
    )


def initialize(args):
    project = args.project.strip()
    if not project:
        raise CadreError("--project cannot be empty.")
    if not re.fullmatch(r"[a-z]{2}", args.lang):
        raise CadreError(f"--lang must be an ISO 639-1 code such as en or es, not '{args.lang}'.")

    workspace = Path(args.workspace)
    if (workspace / MANIFEST_NAME).exists():
        raise CadreError(f"A manifest already exists in '{workspace}'. It was not changed.")

    # Everything that can fail on bad input runs before anything is created.
    version = read_cadre_version()
    template = (REPO_ROOT / "assets" / "CHANGELOG_template.md").read_text(encoding="utf-8")
    data_entries = build_data_entries(args.data, workspace)

    for directory in STAGE_DIRECTORIES + ["research/snapshots"]:
        (workspace / directory).mkdir(parents=True, exist_ok=True)

    changelog_path = workspace / "CHANGELOG.md"
    write_if_missing(changelog_path, template.replace("[Project Name]", project))
    dependency_name, dependency_content = dependency_file(args.env_file, project)
    dependency_path = workspace / dependency_name
    write_if_missing(dependency_path, dependency_content)

    timestamp = now_iso()
    manifest = {
        "cadre_version": version,
        "project_name": project,
        "created_at": timestamp,
        "last_updated": timestamp,
        "output_language": args.lang,
        "environment": args.environment or detect_environment(),
        "analysis_plan": "./analysis_plan.yaml",
        "artifacts": [
            # The template is in English until the first entry is written.
            new_entry("changelog", 0, "changelog", "CHANGELOG.md",
                      sha256_file(changelog_path), "en"),
            new_entry("requirements", 0, "requirements", dependency_name,
                      sha256_file(dependency_path), None),
            *data_entries,
        ],
        "changelog_path": "./CHANGELOG.md",
        "requirements_path": f"./{dependency_name}",
    }
    save_manifest(workspace, manifest)

    print(f"Workspace ready: {workspace}")
    print(f"Environment: {manifest['environment']}")
    for entry in data_entries:
        print(f"Registered {entry['id']}  sha256={entry['sha256']}")


def main():
    parser = argparse.ArgumentParser(description="Create a CADRE workspace and manifest.")
    parser.add_argument("--project", required=True, help="project name")
    parser.add_argument("--lang", required=True, help="output language (ISO 639-1)")
    parser.add_argument("--workspace", default="cadre_workspace",
                        help="workspace directory (default: ./cadre_workspace)")
    parser.add_argument("--data", nargs="*", default=[], metavar="FILE",
                        help="input data files to hash and register")
    parser.add_argument("--env-file", choices=["requirements", "conda"], default="requirements",
                        help="dependency file to create (default: requirements)")
    parser.add_argument("--environment", choices=["claude_code", "claude_ai", "unknown"],
                        help="override environment detection")
    try:
        initialize(parser.parse_args())
    except (CadreError, OSError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
