# CADRE — Stage Reference

## Table of Contents
- [Stage 1: Project Context](#stage-1-project-context)
- [Stage 2: Assessment & Stage Selection](#stage-2-assessment--stage-selection)
- [Stage 3: Data Ingestion & Profiling](#stage-3-data-ingestion--profiling)
- [Stage 4: Data Cleaning & Validation](#stage-4-data-cleaning--validation)
- [Stage 5: Exploratory Analysis (EDA)](#stage-5-exploratory-analysis-eda)
- [Stage 6: Statistical Analysis / Modeling](#stage-6-statistical-analysis--modeling)
- [Stage 7: Robustness & Validation](#stage-7-robustness--validation)
- [Stage 8: Communication & Reporting](#stage-8-communication--reporting)

> **Research applies across stages.** Whenever the answer to a question could
> change a decision, search and log it per `references/research_protocol.md`.
> Findings from searches run after the data was examined stay exploratory.

---

## Stage 1: Project Context

**Purpose:** Establish the full analytical context before touching any data.
Equivalent to the problem definition phase in CRISP-DM and the pre-analysis
plan in preregistered research (Nosek et al., 2018).

**Inputs:** Conversation with the user.

**Process:**
1. Ask whether the project is confidential (`research_protocol.md`, Section 2).
2. Take in the context the user provides. Do not examine the data yet.
3. Run the context search and write `research/domain_brief.md`, proposing the
   project's morphology: topic, industry, analysis type, audience, regulation,
   and a free-text note.
4. Use the brief to ask better questions (below), then have the user confirm or
   correct the morphology.
5. Write `stage_01/project_context.md`.

**Questions to ask the user** (adapt to conversation; not all may be needed):

1. What is the central question or decision this analysis should inform?
2. What data is available? (source, format, approximate size, collection method)
3. What is the domain? (business, biology, social science, engineering, etc.)
4. Who is the audience for the final output?
5. Are there known constraints? (time, compute, regulatory, privacy)
6. Is this exploratory or confirmatory? (Are hypotheses pre-specified?)
7. What counts as a successful outcome?
8. Preferred output language for reports?

**Outputs:** `research/domain_brief.md`, `research/research_log.md`,
`research/sources.bib`, and `stage_01/project_context.md`

Template for `project_context.md`:
```markdown
# Project Context — [Project Name]
**Date:** YYYY-MM-DD
**Analyst:** [name or "AI-assisted"]
**Output language:** [language]
**AI assistance:** [AI-assisted, human review: pending]

## 1. Central Question
[The specific analytical question in one or two sentences.]

## 2. Data Sources
| Source | Format | Size (approx.) | Collection Method |
|--------|--------|----------------|-------------------|
| ...    | ...    | ...            | ...               |

## 3. Domain & Audience
- **Topic:** ...
- **Domain:** ...
- **Industry:** ...
- **Primary audience:** ...
- **Technical level of audience:** ...
- **Regulation:** ...
- **Notes:** ...

## 4. Analysis Type
- [ ] Exploratory (hypothesis-generating)
- [ ] Confirmatory (hypothesis-testing — hypotheses must be pre-specified here)
- [ ] Descriptive
- [ ] Predictive / Modeling
- [ ] Causal inference

## 5. Constraints
...

## 6. Success Criteria
...

## 7. Known Risks & Assumptions
...
```

**Exit gate:** User has confirmed the project context document is accurate,
including the morphology. The domain brief exists, or the context document states
that no research was performed and why.

---

## Stage 2: Assessment & Stage Selection

**Purpose:** Decide which CADRE stages are needed for this project. This
decision is documented and becomes part of the analysis record — skipping a
stage is a deliberate, justified choice, not an omission.

This stage functions analogously to a pre-analysis plan or study protocol,
grounding the analytical strategy before results are seen.

**Inputs:** `stage_01/project_context.md`

**Process:**
1. Review the project context.
2. For each optional stage (3–7), state:
   - **Include / Exclude**
   - **Reason** (one or two sentences)
   - **Dependencies:** note if including Stage 6 without Stage 7 requires
     explicit justification.
3. Propose the stage sequence to the user.
4. User approves or modifies.
5. Write `analysis_plan.yaml` and `stage_02/assessment_report.md`.

**Mandatory dependency rules:**
- If Stage 6 (Modeling) is included → Stage 7 (Robustness) is strongly
  recommended. Excluding it requires explicit written justification.
- If confirmatory analysis is declared → hypotheses must be written in Stage 1
  before any data is examined. Post-hoc hypotheses must be clearly labeled
  as exploratory (see [DEBATED] note on HARKing, Kerr 1998).

**Output 1:** `analysis_plan.yaml`
```yaml
cadre_version: "0.1.0-mvp"
project_name: ""
created_at: ""
output_language: ""

stages:
  stage_03_ingestion:
    include: true/false
    reason: ""
  stage_04_cleaning:
    include: true/false
    reason: ""
  stage_05_eda:
    include: true/false
    reason: ""
  stage_06_analysis:
    include: true/false
    reason: ""
  stage_07_robustness:
    include: true/false
    reason: ""
    justification_if_excluded: ""

approved_by_user: false
approved_at: ""
```

**Output 2:** `stage_02/assessment_report.md`

Template:
```markdown
# Assessment Report — [Project Name]
**Date:** YYYY-MM-DD
**AI assistance:** [AI-assisted, human review: pending]

## Stage Selection Rationale

| Stage | Decision | Reason |
|-------|----------|--------|
| 3 — Ingestion | Include/Exclude | ... |
| 4 — Cleaning | Include/Exclude | ... |
| 5 — EDA | Include/Exclude | ... |
| 6 — Analysis | Include/Exclude | ... |
| 7 — Robustness | Include/Exclude | ... |

## Dependency Notes
...

## Analytical Strategy Summary
[Two to three sentences describing the overall analytical approach.]

## User Approval
- [ ] Approved by user on [date]
```

**Exit gate:** `analysis_plan.yaml` has `approved_by_user: true` and
`approved_at` timestamp is set.

---

## Stage 3: Data Ingestion & Profiling

**Purpose:** Understand the structure, quality, and provenance of the data
before any transformation. No cleaning occurs here — only observation and
description. [CONVENTION]

**Inputs:** Raw data files (registered in manifest with SHA-256 hash).

**Checklist:**
- [ ] Hash all input files and register in manifest
- [ ] Document schema: column names, types, units, expected ranges
- [ ] Compute basic profile: row count, null counts, duplicate rows,
      cardinality of categoricals, range/mean/std/quantiles of numerics
- [ ] Identify potential data quality issues (do not fix yet — only flag)
- [ ] Document data provenance: who collected it, when, how, any known biases
- [ ] Record library versions used for ingestion

**Outputs:**
- `stage_03/raw_data_profile.md` — human-readable profile report
- `stage_03/data_dictionary.md` — one row per variable (see template below)
- `stage_03/ingest.py` (Claude Code) — reproducible ingestion script

**Data dictionary template (one entry per variable):**
```markdown
### `column_name`
- **Type:** numeric / categorical / datetime / text / boolean
- **Unit:** (if applicable)
- **Description:** ...
- **Expected range / values:** ...
- **Null count:** N (X%)
- **Notes / anomalies observed:** ...
```

**Exit gate:** All input files are hashed and in manifest. Data dictionary
covers every variable. Quality issues are listed (not yet fixed).

---

## Stage 4: Data Cleaning & Validation

**Purpose:** Transform raw data into an analysis-ready dataset. Every
transformation must be justified. This creates an auditable trail from raw
to clean data. [CONVENTION]

**Principle:** Transformations are made to the data *because the analysis
requires it*, not because the results look better. Any transformation that
could affect results must be declared before the analysis in Stage 6.

**Checklist:**
- [ ] For each transformation: document the rule, the reason, the rows affected,
      and the alternative considered
- [ ] Handle missing values — declare strategy (deletion, imputation, flagging)
      and justify [see bibliography: van Buuren 2018 for imputation methods]
- [ ] Handle duplicates
- [ ] Handle outliers — declare detection method and decision rule
- [ ] Type coercions and format normalization
- [ ] Create the clean dataset as a separate file (never overwrite raw data)
- [ ] Hash the clean dataset and register in manifest
- [ ] Run a post-cleaning validation: re-profile the clean dataset

**Output:** `stage_04/cleaning_log.md`

Template per transformation:
```markdown
### Transformation: [Short name]
- **Applied to:** [column(s) or rows]
- **Rule:** [exact rule, e.g. "rows where age < 0 or age > 120 → removed"]
- **Reason:** [statistical or domain justification]
- **Alternative considered:** [and why it was rejected]
- **Rows affected:** N (X% of dataset)
- **Epistemic status:** [CONSENSUS / CONVENTION / HEURISTIC]
- **Reference:** [bib key if applicable]
```

**Exit gate:** Cleaning log has one entry per transformation. Clean dataset
is hashed and in manifest. Raw data is untouched.

---

## Stage 5: Exploratory Analysis (EDA)

**Purpose:** Develop intuition about the data through visual and numerical
summaries. This stage is explicitly **hypothesis-generating**, not
hypothesis-testing. Findings here do not constitute evidence — they motivate
questions for Stage 6. This distinction is critical to avoid post-hoc
rationalization (HARKing). [DEBATED — Kerr 1998; Simmons et al. 2011]

**Checklist:**
- [ ] Univariate summaries for all relevant variables
- [ ] Bivariate summaries for variable pairs of interest
- [ ] Distribution plots (histograms, density, QQ-plots where relevant)
- [ ] Correlation analysis — with explicit warning that correlation ≠ causation
- [ ] Anomaly/outlier visualization
- [ ] Temporal patterns if data has a time dimension
- [ ] All plots saved as files and registered in manifest

**Output:** `stage_05/eda_report.md`

Each finding must be labeled:
- 🔍 **Observation** — factual description of what was seen
- ❓ **Question** — hypothesis or question this observation raises for Stage 6
- ⚠️ **Caution** — something that may affect interpretation

**Exit gate:** At least one "Question" is formulated for each major variable
or relationship of interest. These questions become the basis for Stage 6.

---

## Stage 6: Statistical Analysis / Modeling

**Purpose:** Answer the questions formulated in prior stages using appropriate
statistical or modeling techniques. All methods, formulas, and assumptions must
be fully documented per the formula template.

**Before any test or model is run:**
- Declare the method and why it is appropriate for this data/question
- State the assumptions of the method and verify them (or document why
  verification is not possible)
- State the decision rule (e.g., significance threshold, evaluation metric)

**Formula documentation is mandatory** for every statistical procedure.
See `references/formula_template.md`.

**Checklist:**
- [ ] For each method: declare before running (confirmatory) or label as
      exploratory (if inspired by EDA)
- [ ] Verify statistical assumptions and document results
- [ ] Run analyses from scripts only — no manual computation
- [ ] Report effect sizes, not just p-values [CONSENSUS — Sullivan & Feinn 2012]
- [ ] Report confidence intervals [CONSENSUS — Cumming 2014]
- [ ] Document all tested models/specifications, not only the best one
      (avoid selective reporting) [DEBATED — Simmons et al. 2011]
- [ ] Record random seeds for any stochastic procedure

**Output:** `stage_06/analysis_report.md`

**Exit gate:** All analyses are scripted and reproducible. Assumptions are
documented. No results are selectively withheld.

---

## Stage 7: Robustness & Validation

**Purpose:** Test whether conclusions hold under alternative reasonable
assumptions. A result that only holds under one specific set of choices
is a fragile result. [CONSENSUS — Leamer 1983; Young & Holsteen 2017]

**Checklist:**
- [ ] Sensitivity analysis: vary key analytical choices, report how results change
- [ ] Check robustness to outlier removal/inclusion
- [ ] Cross-validation if predictive models are used
- [ ] Re-examine assumptions with alternative tests
- [ ] Explicitly state limitations of the analysis

**Output:** `stage_07/robustness_report.md`

**Exit gate:** At least one sensitivity check per main result. Limitations
section is complete.

---

## Stage 8: Communication & Reporting

**Purpose:** Translate the analysis into a clear, honest, human-readable
report calibrated to the stated audience.

**Principles:**
- Distinguish clearly between what the data shows and what it implies
- Limitations are not footnotes — they belong in the main text
- All AI-generated content is labeled
- All figures referenced in the text must be in the manifest

**Output:** `stage_08/final_report.md` (or `.pdf` via Quarto if available)

**Mandatory sections:**
1. Executive summary (audience-appropriate, non-technical)
2. Methods (brief, with references to stage documents for detail)
3. Results (with figures and tables)
4. Limitations (prominent, not buried)
5. Conclusions
6. References (from `bibliography.bib` and `research/sources.bib`, with the tier
   of project-level sources visible — no unverified citations)
7. Appendix: AI assistance log

**Exit gate:** User reviews and marks `reviewed_by_human: true` in the
manifest entry for the final report.
