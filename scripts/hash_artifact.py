#!/usr/bin/env python3
"""Compute an artifact's SHA-256 and register it in the CADRE manifest.

Usage:
    python scripts/hash_artifact.py cadre_workspace/stage_03/data_dictionary.md \\
        --type data_dictionary --stage 3
    python scripts/hash_artifact.py cadre_workspace/stage_03/data_dictionary.md

The first form registers a new artifact. For a registered artifact, only the path
is needed and its entry is updated in place, with two safeguards:
- A changed raw_data file is refused, because raw data must never be modified.
- A changed reviewed artifact loses its review, which applied to the old content.
"""

import argparse
import sys
from pathlib import Path

from cadre_manifest import (
    ARTIFACT_TYPES,
    MANIFEST_NAME,
    NON_DOCUMENT_TYPES,
    CadreError,
    default_artifact_id,
    load_manifest,
    manifest_relative_path,
    new_entry,
    now_iso,
    save_manifest,
    sha256_file,
)


def register_new(args, manifest, relative_path, sha256):
    if args.type is None or args.stage is None:
        raise CadreError(f"'{relative_path}' is not registered yet. Pass --type and --stage.")
    artifact_id = args.id or default_artifact_id(relative_path)
    if any(entry["id"] == artifact_id for entry in manifest["artifacts"]):
        raise CadreError(f"The id '{artifact_id}' is already in use. Pass another with --id.")
    language = args.language
    if language is None and args.type not in NON_DOCUMENT_TYPES:
        language = manifest["output_language"]
    manifest["artifacts"].append(
        new_entry(artifact_id, args.stage, args.type, relative_path, sha256, language, args.notes)
    )
    print(f"Registered {artifact_id}  sha256={sha256}")


def update_existing(args, entry, sha256):
    for field, requested in (("id", args.id), ("type", args.type), ("stage", args.stage)):
        if requested is not None and requested != entry[field]:
            raise CadreError(
                f"'{entry['path']}' is registered with {field} '{entry[field]}', "
                f"not '{requested}'. The entry was not changed."
            )

    if sha256 == entry["sha256"]:
        print(f"Unchanged {entry['id']}  sha256={sha256}")
    else:
        if entry["type"] == "raw_data":
            raise CadreError(
                f"Raw data '{entry['path']}' no longer matches its registered hash.\n"
                f"  registered: {entry['sha256']}\n"
                f"  current:    {sha256}\n"
                "The manifest was not changed. Restore the original file, or set "
                "superseded_by on this entry and register the new version with a new --id."
            )
        entry["sha256"] = sha256
        entry["produced_at"] = now_iso()
        print(f"Updated {entry['id']}  sha256={sha256}")
        if entry["reviewed_by_human"]:
            entry.update(reviewed_by_human=False, reviewed_by=None, reviewed_at=None)
            print(
                f"Warning: {entry['id']} changed after human review, so its review was "
                "cleared. Add a CHANGELOG.md entry.",
                file=sys.stderr,
            )

    if args.language is not None:
        entry["language"] = args.language
    if args.notes is not None:
        entry["notes"] = args.notes


def register(args):
    workspace = Path(args.workspace)
    manifest = load_manifest(workspace)
    path = Path(args.path)
    if not path.is_file():
        raise CadreError(f"File not found: '{path}'.")
    if path.resolve() == (workspace / MANIFEST_NAME).resolve():
        raise CadreError("The manifest cannot record its own hash, because writing it changes it.")

    relative_path = manifest_relative_path(path, workspace)
    sha256 = sha256_file(path)
    current = next(
        (entry for entry in manifest["artifacts"]
         if entry["path"] == relative_path and entry["superseded_by"] is None),
        None,
    )
    if current is None:
        register_new(args, manifest, relative_path, sha256)
    else:
        update_existing(args, current, sha256)
    save_manifest(workspace, manifest)


def main():
    parser = argparse.ArgumentParser(description="Register an artifact's SHA-256 in the manifest.")
    parser.add_argument("path", help="artifact file")
    parser.add_argument("--workspace", default="cadre_workspace",
                        help="workspace directory (default: ./cadre_workspace)")
    parser.add_argument("--type", choices=sorted(ARTIFACT_TYPES),
                        help="artifact type (required for a new artifact)")
    parser.add_argument("--stage", type=int, choices=range(0, 9),
                        help="stage that produced it (required for a new artifact)")
    parser.add_argument("--id", help="artifact id (default: derived from the path)")
    parser.add_argument("--language", help="ISO 639-1 code (default: the project's output language)")
    parser.add_argument("--notes", help="free-text notes")
    try:
        register(parser.parse_args())
    except (CadreError, OSError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
