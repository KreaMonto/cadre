# CADRE — Artifact Manifest Specification

The manifest (`cadre_manifest.json`) is the single source of truth for all
artifacts in a CADRE project. Every stage reads it to find its inputs and
writes to it after producing outputs. It is the backbone of reproducibility
and provenance.

This design follows FAIR data principles (Wilkinson et al., 2016) and the
W3C PROV model for provenance.

---

## Full Schema

```json
{
  "cadre_version": "0.1.0-mvp",
  "project_name": "string",
  "created_at": "ISO-8601",
  "last_updated": "ISO-8601",
  "output_language": "ISO 639-1 code (e.g. en, es, fr)",
  "environment": "claude_code | claude_ai",
  "analysis_plan": "./analysis_plan.yaml",

  "artifacts": [
    {
      "id": "unique-slug (kebab-case)",
      "stage": 0,
      "type": "see type list below",
      "path": "relative path from workspace root",
      "sha256": "hex string — computed at time of write",
      "produced_at": "ISO-8601",
      "language": "ISO 639-1 code",
      "reviewed_by_human": false,
      "reviewed_by": null,
      "reviewed_at": null,
      "superseded_by": null,
      "notes": "optional free text"
    }
  ],

  "changelog_path": "./CHANGELOG.md",
  "requirements_path": "./requirements.txt"
}
```

---

## Artifact Types

| Type | Description |
|------|-------------|
| `project_context` | Stage 1 context document |
| `assessment_report` | Stage 2 assessment document |
| `analysis_plan` | Stage 2 YAML plan |
| `raw_data` | Input data file (never modified) |
| `data_dictionary` | Variable-level documentation |
| `raw_data_profile` | Statistical profile of raw data |
| `clean_data` | Transformed, analysis-ready dataset |
| `cleaning_log` | Record of all transformations |
| `eda_report` | Exploratory analysis findings |
| `figure` | Any plot or visualization |
| `analysis_report` | Stage 6 results document |
| `model` | A trained model artifact |
| `robustness_report` | Stage 7 sensitivity analysis |
| `final_report` | Stage 8 human-readable report |
| `script` | Any code file |
| `requirements` | Dependency lockfile |
| `changelog` | CHANGELOG.md |
| `manifest` | The manifest itself (self-referential) |

---

## SHA-256 Hashing

**Claude Code:**
```bash
sha256sum path/to/file
# or in Python:
import hashlib
with open(path, 'rb') as f:
    sha256 = hashlib.sha256(f.read()).hexdigest()
```

**Claude.ai:** Ask the user to compute the hash using their local tool and
provide it, or note `"sha256": "unverified — computed by user"` and include
the user-provided value in notes.

---

## Updating the Manifest

1. Read the current manifest.
2. Add or update the artifact entry.
3. Update `last_updated`.
4. Write the manifest back.
5. If in Claude.ai, present the updated manifest to the user for download.

**Never delete entries.** If an artifact is superseded (e.g., a dataset is
re-cleaned), set `superseded_by` to the new artifact's id. This preserves
the full provenance chain.

---

## Claude.ai Session Continuity

Because Claude.ai has no persistent filesystem, the manifest doubles as the
project memory between sessions. At the start of every session:

1. Claude asks: *"Is this a continuing CADRE project? If so, please upload
   your `cadre_manifest.json`."*
2. Claude reads the manifest and summarizes project state.
3. User uploads any artifact files needed for the current stage.
4. At the end of every stage, Claude presents updated manifest + all new
   artifacts for download.

The manifest should be treated as a file the user owns and maintains.
Claude is a collaborator, not the keeper of record.
