# Contributing to CADRE

CADRE is a framework whose value depends on being trustworthy. Contributions
are welcome, and they are reviewed above all for whether they keep that trust.

## Before You Start

- **Read [`references/philosophy.md`](references/philosophy.md).** A change that
  contradicts its principles needs explicit justification in the pull request.
- **Write in English.** Code, documentation, keys, filenames, and commit
  messages are in English. Reports that CADRE produces use the user's language.
- **Open an issue first for large changes**, such as a new stage or a change to
  the citation rules, so the design can be discussed before the work is done.

## Development Setup

The scripts need Python 3 and use only the standard library. Adding a dependency
needs a justification in the pull request.

```bash
python -m unittest discover tests
```

All tests must pass before a pull request is merged. New script behavior needs
tests.

Do not remove the `.gitattributes` rules for data files. Data files are hashed
byte for byte, and line-ending conversion would change their hashes.

## References

The bibliography is where errors cost the most, because CADRE's citation rules
depend on it.

- **Never add a reference from memory.** Resolve the DOI and compare the title,
  authors, year, venue, volume, issue, and pages with the registry record:

  ```bash
  curl -sL -H "Accept: application/vnd.citationstyles.csl+json" https://doi.org/<doi>
  ```

- **If a work has no DOI**, check that it really has none, and use a stable URL
  with a `note` field saying so.
- **Check the claim, not only the citation.** A correct entry is not enough: the
  source must support the statement that cites it.
- **Cite only `bibliography.bib` keys** in CADRE's own documents. (In an
  analysis, `research/sources.bib` is also allowed, per
  `references/research_protocol.md`.) State the
  epistemic status of each methodological claim (`[CONSENSUS]`, `[CONVENTION]`,
  `[HEURISTIC]`, or `[DEBATED]`).

## Stages, Formulas, and Glossary

- Every stage template must include an exit gate.
- Every formula follows [`references/formula_template.md`](references/formula_template.md).
- Glossary terms in a new language must be checked against published scientific
  literature in that language.
- A new artifact type must be added both to the table in
  [`references/manifest_spec.md`](references/manifest_spec.md) and to
  `ARTIFACT_TYPES` in [`scripts/cadre_manifest.py`](scripts/cadre_manifest.py).

## Commits and Pull Requests

- Use [Conventional Commits](https://www.conventionalcommits.org/) prefixes:
  `feat:`, `fix:`, `docs:`, and so on.
- In the pull request, describe what changed, why, and which principles or stage
  rules it affects.
- Mark AI-assisted contributions as such. A human must have reviewed them,
  as with any other CADRE output.

## Licensing

By contributing, you agree that code you contribute (`scripts/`, `tests/`) is
licensed under [Apache-2.0](LICENSE), and everything else under
[CC BY 4.0](LICENSE-docs).
