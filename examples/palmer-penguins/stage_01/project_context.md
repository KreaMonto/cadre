# Project Context — Palmer Penguins: Morphological Differentiation by Species

**CADRE version:** 0.1.0-mvp
**Date:** 2026-11-06
**Analyst:** AI-assisted (Claude / CADRE)
**Output language:** English
**AI assistance:** [AI-assisted, human review: pending]

---

## 1. Central Question

Can morphological measurements (bill dimensions, flipper length, body mass)
reliably differentiate among the three penguin species present in the Palmer
Archipelago (Antarctica), and do these differences vary by island or sex?

## 2. Data Sources

| Source | Format | Size | Collection Method |
|--------|--------|------|-------------------|
| Palmer Penguins dataset (Horst, Hill & Gorman, 2020) | CSV | 344 rows × 8 columns | Field measurements, Palmer Station LTER, Antarctica (2007–2009) |

**Dataset citation:**
Horst AM, Hill AP, Gorman KB (2020). palmerpenguins: Palmer Archipelago
(Antarctica) penguin data. R package version 0.1.0.
https://doi.org/10.5281/zenodo.3960218

**Original data source:**
Gorman KB, Williams TD, Fraser WR (2014). Ecological sexual dimorphism and
environmental variability within a community of Antarctic penguins (genus
Pygoscelis). PLOS ONE 9(3): e90081.
https://doi.org/10.1371/journal.pone.0090081

## 3. Domain & Audience

- **Domain:** Ecology / Morphometrics
- **Primary audience:** Data analysis community evaluating the CADRE plugin
- **Technical level:** Intermediate — familiar with descriptive statistics
  and basic inferential concepts

## 4. Analysis Type

- [x] Exploratory (hypothesis-generating)
- [ ] Confirmatory (hypothesis-testing)
- [x] Descriptive
- [ ] Predictive / Modeling
- [ ] Causal inference

> **Note:** Because this is an example/test run for CADRE validation, the
> analysis is explicitly **exploratory and descriptive**. No pre-specified
> hypotheses are tested. Any patterns observed should be treated as
> hypothesis-generating, not as confirmatory evidence.

## 5. Constraints

- Dataset is publicly available and contains no personally identifiable
  information.
- 2 missing values in `bill_length_mm`, `bill_depth_mm`, `flipper_length_mm`,
  `body_mass_g`; 11 missing in `sex`. Handling strategy to be decided in
  Stage 4 if selected.
- Analysis scope limited to Stages 1–2 for this test run. Stages 3–8 are
  defined in `analysis_plan.yaml` but deferred.

## 6. Success Criteria

For this test run, success is defined as:

1. CADRE Stages 1 and 2 execute correctly and produce well-structured,
   documented artifacts.
2. The stage selection rationale at Stage 2 is coherent and reproducible.
3. The output documents are legible to a human reader unfamiliar with CADRE.

## 7. Known Risks & Assumptions

- **Assumption:** The CSV from the public repository matches the canonical
  dataset described in Gorman et al. (2014). Hash verification deferred to
  Stage 3 if selected.
- **Risk:** Exploratory findings may be over-interpreted as confirmatory
  without the guardrails of Stages 6–7. This is acceptable for a Stage 1–2
  test run; the limitation is explicitly noted here.
- **Known data issue:** 11 missing values in `sex` (3.2% of records). This
  may affect sex-disaggregated analyses if pursued in later stages.
