# CADRE

**Contextual Analysis & Documentation with Reproducible Evidence**

CADRE is an open-source plugin for Claude that provides a structured,
academically grounded framework for data analysis. It guides analysts through
a modular pipeline of stages — from project context to final reporting —
producing human-readable documentation with traceable provenance, curated
citations, and reproducible scripts at every step.

---

## Design Principles

- **Truth first.** Results that cannot be verified are not reported as results.
  Limitations are part of every output, not footnotes.
- **Explicit epistemic status.** Every methodological claim is tagged:
  `[CONSENSUS]`, `[CONVENTION]`, `[HEURISTIC]`, or `[DEBATED]`.
- **No invented citations.** Every citation is traceable to something actually
  opened. Methodological claims need academic sources, from the curated
  `bibliography.bib` or found during the analysis with human review pending.
  Anything else is flagged `[UNVERIFIED — needs DOI]`.
- **Research when it matters.** Research is not a stage: it happens at any point
  where the answer could change a decision, and every search is logged.
- **Separation of exploration and confirmation.** EDA generates questions;
  Stage 6 tests them. The distinction is enforced, not advisory.
- **Modularity over completeness.** Not every project needs every stage.
  Stage selection is documented and justified, not defaulted.
- **Multilingual output.** Reports are produced in the user's preferred
  language. Code, filenames, and keys remain in English.

For the full rationale, read `references/philosophy.md`.

---

## Stages

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

Stages 3–7 are selected "à la carte" at Stage 2. The selection is documented
in `analysis_plan.yaml` and approved by the user before analysis begins.

---

## Environments

CADRE runs in two environments with different persistence strategies:

**Claude Code** — full filesystem access. Artifacts persist on disk.
The manifest and workspace are managed automatically.

**Claude.ai** — no persistent filesystem. All artifacts are presented as
downloadable files. The user maintains the manifest between sessions.

CADRE detects the environment automatically at the start of each session.

---

## File Structure

```
cadre/
├── SKILL.md                        ← Main orchestrator (load this)
├── README.md                       ← This file
├── references/
│   ├── stages.md                   ← Detailed stage instructions
│   ├── philosophy.md               ← Epistemic principles
│   ├── research_protocol.md        ← Transversal research rules and templates
│   ├── manifest_spec.md            ← Artifact manifest schema
│   ├── formula_template.md         ← Formula documentation standard
│   ├── bibliography.bib            ← Curated references (DOI verification pending)
│   └── glossary.md                 ← Technical terms in multiple languages
├── assets/
│   └── CHANGELOG_template.md       ← Changelog template for projects
└── scripts/
    └── (future: hash utility, manifest initializer, etc.)
```

---

## Workspace Structure (Claude Code)

```
cadre_workspace/
├── cadre_manifest.json
├── CHANGELOG.md
├── analysis_plan.yaml
├── requirements.txt
├── research/
├── stage_01/project_context.md
├── stage_02/assessment_report.md
├── stage_03/
├── stage_04/
├── stage_05/
├── stage_06/
├── stage_07/
└── stage_08/
```

---

## Contributing

CADRE is designed for community use. Before contributing:

1. Read `references/philosophy.md` — contributions that contradict the
   epistemic principles require explicit justification.
2. All new references added to `bibliography.bib` must include a verified DOI.
3. All new stage templates must include an exit gate.
4. If you add a formula, use the template in `references/formula_template.md`.
5. If you add a language to the glossary, verify terms against published
   scientific literature in that language.

---

## License

- Code and scripts: [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0)
- Documentation and templates: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

---

## Version

`0.1.0-mvp` — Initial release. Covers Stages 0–2 and conventions.
Stages 3–8 are defined in `references/stages.md` with templates.
Scripted utilities (hashing, manifest init) are planned for `0.2.0`.

---

## Acknowledgements

Methodological foundations draw on the work of Nosek et al. (preregistration),
Sandve et al. and Wilson et al. (reproducibility), Wasserstein & Lazar (p-values),
Wilkinson et al. (FAIR principles), Gebru et al. (data documentation),
and Knuth (literate programming), among others. Full references in
`references/bibliography.bib`.
