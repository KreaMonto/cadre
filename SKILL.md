---
name: cadre
description: >
  CADRE (Contextual Analysis & Documentation with Reproducible Evidence) is a
  modular, open-source plugin for rigorous, reproducible data analysis. Use this
  skill whenever the user wants to analyze data, run statistical analysis,
  document an analytical process, produce a research-grade report, audit
  an existing analysis, or build a data pipeline with structured documentation.
  Trigger even if the user just says "let's analyze this dataset", "help me
  understand this data", "I need a report on X data", or any variant that
  implies working with data in a structured way. CADRE governs the full
  lifecycle from project context through final communication.
compatibility:
  claude_code: true
  claude_ai: true
version: "0.1.0-mvp"
license: "Apache-2.0"
---

# CADRE — Contextual Analysis & Documentation with Reproducible Evidence

> **For contributors and users:** Read `references/philosophy.md` before
> modifying this skill. It contains the epistemic principles that govern all
> design decisions.

---

## 0. Environment Detection

Before doing anything, determine which environment you are in:

**Claude Code** (filesystem available):
- Files, scripts, and the artifact manifest persist on disk between turns.
- Output artifacts are written to `./cadre_workspace/` by default.
- The manifest (`cadre_manifest.json`) is the source of truth for all artifacts.

**Claude.ai** (no persistent filesystem):
- All artifacts are presented as downloadable files the user must save locally.
- At the start of every session, ask the user to re-upload the manifest and any
  artifacts from the previous session before continuing.
- Remind the user to save every artifact produced before the conversation ends.

Announce the detected environment at the start of every CADRE session in one
line, e.g.: `🔍 Environment: Claude Code — workspace at ./cadre_workspace/`

---

## 1. Workflow Overview

CADRE proceeds through **ordered stages**. Each stage has defined inputs,
outputs, and an **exit gate** — a condition that must be satisfied before
advancing. Stages are selected after Stage 1 (see Stage 2: Assessment).

```
Stage 0 → Stage 1 → Stage 2 → [Selected Stages] → Final Stage
  Env       Context   Assessment    (a la carte)     Communication
```

| # | Stage | Mandatory |
|---|-------|-----------|
| 0 | Environment Setup | Always |
| 1 | Project Context | Always |
| 2 | Assessment & Stage Selection | Always |
| 3 | Data Ingestion & Profiling | If data is involved |
| 4 | Data Cleaning & Validation | If raw/dirty data |
| 5 | Exploratory Analysis (EDA) | Usually yes |
| 6 | Statistical Analysis / Modeling | If inferential questions |
| 7 | Robustness & Validation | If modeling was done |
| 8 | Communication & Reporting | Always (final stage) |

---

## 2. Transversal Conventions

These rules apply across **all** stages. Read them before starting Stage 1.

### 2.1 Language
Determine the user's preferred output language at Stage 1. All documents
produced for human readers (reports, dictionaries, changelogs) are written in
that language. All filenames, keys, and code remain in English.

### 2.2 Artifact Manifest
Every artifact produced must be registered in `cadre_manifest.json`.
See `references/manifest_spec.md` for the full schema.

Minimum entry per artifact:
```json
{
  "id": "unique-slug",
  "stage": 3,
  "type": "data_dictionary",
  "path": "./cadre_workspace/stage_03/data_dictionary.md",
  "sha256": "<hash>",
  "produced_at": "ISO-8601 timestamp",
  "language": "es",
  "reviewed_by_human": false
}
```

In Claude.ai, present the updated manifest as a downloadable file after
every stage.

### 2.3 Changelog
Any change to a **previously validated artifact** (dataset, cleaning rule,
assumption, reported result) triggers a changelog entry in `CHANGELOG.md`.
Follow Keep a Changelog format (https://keepachangelog.com). First-pass linear
work does not require changelog entries — only revisions do.

### 2.4 References & Citations
- All methodological claims cite a key from `references/bibliography.bib`.
- The AI must never invent a citation. If a claim needs a source not in the
  bibliography, mark it `[UNVERIFIED — needs DOI]` and flag it to the user.
- Each methodological statement carries an **epistemic status tag**:
  - `[CONSENSUS]` — established in peer-reviewed literature
  - `[CONVENTION]` — standard practice, not always formally justified
  - `[HEURISTIC]` — practical rule with known limitations
  - `[DEBATED]` — active discussion in the literature

### 2.5 Mathematical Formulas
Every formula used in a report must include, in this order:
1. Formula in LaTeX notation
2. Definition of each symbol
3. Assumptions required
4. Plain-language interpretation
5. When the formula breaks down or should not be used
6. Numerical example (small, computed from real data in the project)
7. Implementation: library, function name, version

See `references/formula_template.md` for the standard block.

### 2.6 Reproducibility
- All computations must run from scripts, not manual steps.
- Random seeds must be set and documented.
- Library versions must be recorded in `requirements.txt` or `environment.yml`.
- Input data files must be hashed (SHA-256) and the hash stored in the manifest.
- AI-generated content in reports must be marked with: `[AI-assisted, human
  review: pending/done]`.

---

## 3. Stage Instructions

Read the corresponding section in `references/stages.md` for each active stage.
That file contains the detailed checklist, document templates, and exit gate
for every stage.

---

## 4. Stage Gate Protocol

Before advancing to the next stage, explicitly state:
```
✅ EXIT GATE — Stage [N]: [Stage Name]
Condition: [What was verified]
Artifacts produced: [list with manifest IDs]
Pending human review: [yes/no — which items]
Proceeding to: Stage [N+1]
```

If the exit gate is not satisfied, state what is missing and wait.

---

## 5. File Structure (Claude Code)

```
cadre_workspace/
├── cadre_manifest.json
├── CHANGELOG.md
├── analysis_plan.yaml          ← produced at Stage 2
├── requirements.txt            ← maintained throughout
├── stage_01/
│   └── project_context.md
├── stage_02/
│   └── assessment_report.md
├── stage_03/
│   ├── raw_data_profile.md
│   └── data_dictionary.md
└── ...
```

---

## 6. Reference Files

Load these as needed — do not load all at once:

| File | Load when |
|------|-----------|
| `references/stages.md` | Starting any stage |
| `references/philosophy.md` | Questions arise about methodology or design decisions |
| `references/manifest_spec.md` | Writing or reading the artifact manifest |
| `references/formula_template.md` | Documenting any mathematical formula |
| `references/bibliography.bib` | Adding or verifying a citation |
| `references/glossary.md` | Translating or defining technical terms |

---

## 7. Opening Protocol

At the very start of a CADRE session:
1. Detect and announce environment (Section 0).
2. If Claude Code: check for existing `cadre_manifest.json`. If found, load it
   and summarize the project state. If not found, initialize workspace.
3. If Claude.ai: ask the user to upload `cadre_manifest.json` if this is a
   continuing session. If new session, acknowledge that all files must be saved
   manually.
4. Proceed to Stage 1.
