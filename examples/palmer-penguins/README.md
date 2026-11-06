# CADRE Example — Palmer Penguins (Stages 1–2)

This example demonstrates CADRE Stages 1 (Project Context) and 2 (Assessment
& Stage Selection) using the publicly available Palmer Penguins dataset.

## Dataset

**Palmer Penguins** — morphological measurements of 344 penguins from three
species (Adélie, Chinstrap, Gentoo) across three islands in the Palmer
Archipelago, Antarctica. Collected 2007–2009.

- **Package citation:** Horst AM, Hill AP, Gorman KB (2020). palmerpenguins.
  https://doi.org/10.5281/zenodo.3960218
- **Original data:** Gorman KB, Williams TD, Fraser WR (2014). PLOS ONE 9(3):
  e90081. https://doi.org/10.1371/journal.pone.0090081

## Files

```
palmer-penguins/
├── README.md                        ← this file
├── penguins.csv                     ← raw dataset (public domain)
├── analysis_plan.yaml               ← stage selection (Stage 2 output)
├── stage_01/
│   └── project_context.md           ← project context document
└── stage_02/
    └── assessment_report.md         ← assessment & stage selection report
```

## What This Example Shows

- How CADRE's **Stage 1** structures the analytical context before any data
  is examined: central question, data provenance, analysis type declaration,
  constraints, and known risks.
- How CADRE's **Stage 2** selects stages à la carte with explicit rationale
  for each inclusion/exclusion, documents inter-stage dependencies, and
  declares scope honestly — including deferring stages that are relevant but
  outside the current run's scope.

## What This Example Does NOT Show

Stages 3–8 are assessed in `analysis_plan.yaml` but not executed. This is
intentional: the example validates the planning and documentation framework,
not the full analytical pipeline. A complete example (Stages 1–8) is planned
for a future release.

## Status

- [x] Stage 1 — Project Context
- [x] Stage 2 — Assessment & Stage Selection
- [ ] Stage 3 — Data Ingestion & Profiling *(deferred)*
- [ ] Stage 4 — Data Cleaning & Validation *(deferred)*
- [ ] Stage 5 — EDA *(deferred)*
- [ ] Stage 6 — Statistical Analysis *(deferred)*
- [ ] Stage 7 — Robustness & Validation *(deferred)*
- [ ] Stage 8 — Communication & Reporting *(deferred)*

## AI Assistance Note

All documents in this example were generated with AI assistance (Claude /
CADRE 0.1.0-mvp). Human review is pending. Per CADRE conventions, all
AI-generated content is labeled `[AI-assisted, human review: pending]`
until verified by a human analyst.
