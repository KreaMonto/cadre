# CADRE — Epistemic Philosophy

This document states the principles behind CADRE's design. Any contributor
modifying the plugin should read this first. Design decisions that contradict
these principles require explicit justification in the PR.

---

## 1. Truth Before Convenience

CADRE is designed for analysts who prioritize accurate conclusions over
efficient-looking outputs. This means:

- A result that cannot be verified is not a result.
- An omission that improves the narrative is a form of distortion.
- Limitations are part of the finding, not obstacles to the report.

This principle follows the standard of scientific communication established
in fields where errors have material consequences (medicine, engineering,
public policy).

---

## 2. Explicit Epistemic Status

Not all methodological claims have the same evidentiary basis. CADRE
distinguishes:

| Tag | Meaning |
|-----|---------|
| `[CONSENSUS]` | Supported by multiple independent peer-reviewed studies |
| `[CONVENTION]` | Standard practice; not always formally justified but widely adopted |
| `[HEURISTIC]` | Practical rule with known limitations; works in common cases |
| `[DEBATED]` | Active methodological debate; reasonable experts disagree |

This system is inspired by the LessWrong epistemic status convention and
adapted for scientific practice.

---

## 3. The Citation Problem

Large language models fabricate references. This is not a minor inconvenience —
it is a fundamental reliability problem for academic and professional work.

CADRE's response:
- Every citation must be traceable: it resolves to a BibTeX key and leads to
  something that was actually opened and that another person can check. Nothing
  is cited from memory.
- `bibliography.bib` is curated by humans and is the standard for methodological
  claims. Entries are verified against their DOI and metadata.
- Sources found during an analysis go in the project's `research/sources.bib`.
  Peer-reviewed work may support methodological claims with its tier visible and
  human review pending. Non-academic sources may support context only, never a
  method. See `research_protocol.md`.
- Any claim requiring a citation that meets none of these is flagged
  `[UNVERIFIED — needs DOI]` and must not be presented as established.
- The AI is an analyst and writer, not an authority. Human review is the
  final verification layer.

Reference: Ji et al. (2023). Survey of Hallucination in Natural Language
Generation. ACM Computing Surveys. DOI: 10.1145/3571730

---

## 4. Separation of Exploration and Confirmation

The most pervasive bias in data analysis is treating exploratory findings
as if they were confirmatory. CADRE enforces the distinction:

- **Exploratory (EDA):** generates questions and hypotheses. No claim of
  statistical evidence. Findings labeled 🔍 Observation or ❓ Question.
- **Confirmatory (Stage 6):** tests pre-specified hypotheses. Any hypothesis
  not declared before data examination is labeled exploratory regardless
  of when the analysis ran.
- **Research:** anything suggested by a literature search run after the data was
  examined stays exploratory, whatever the source says. Such searches must also
  look for evidence against the proposed explanation.

This follows the preregistration movement (Nosek et al., 2018) and addresses
HARKing — Hypothesizing After Results are Known (Kerr, 1998).

---

## 5. Reproducibility as a Non-Negotiable

A result that cannot be independently reproduced is a claim, not a finding.
CADRE implements the minimum standards described in:
- Sandve et al. (2013). Ten Simple Rules for Reproducible Computational
  Research. PLOS Computational Biology.
- Wilson et al. (2017). Good Enough Practices in Scientific Computing.
  PLOS Computational Biology.

Minimum requirements: scripts over manual steps, hashed inputs, pinned
library versions, documented random seeds.

---

## 6. AI Assistance is Not AI Authority

CADRE uses AI to accelerate documentation, structure, and computation.
It does not use AI as a source of methodological truth. Every AI-generated
section in a report carries the label `[AI-assisted, human review: pending]`
until a human verifies it, at which point it becomes `[AI-assisted, human
review: done — [reviewer initials/name]]`.

This distinction matters because:
- The AI may misapply a method to an inappropriate context.
- The AI may describe a formula correctly but implement it incorrectly.
- The AI cannot know domain-specific nuances the analyst holds.

Human review is not optional. It is part of what makes a CADRE report a
CADRE report.

---

## 7. Multilingual Output, Canonical English

Skill instructions, filenames, keys, and code are in English to maximize
community accessibility and model performance. Human-facing reports are
produced in the user's preferred language. Technical terms retain their
source-language citation form (e.g., do not translate "p-value" in a Spanish
report to "valor p" without noting both forms). The glossary in
`references/glossary.md` maintains the canonical term list.

---

## 8. Modularity Over Completeness

Not every project needs every stage. A rigid pipeline that forces unnecessary
work produces bureaucratic compliance, not rigorous analysis. CADRE's
assessment stage exists precisely to make stage selection a documented,
justified decision rather than a default.

Skipping a stage is acceptable. Skipping it without documentation is not.
