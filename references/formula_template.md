# CADRE — Formula Documentation Template

Every formula used in a CADRE report must be documented using this structure.
Copy the block below and fill in each section. No section may be left blank;
write "N/A — [reason]" if a section genuinely does not apply.

---

## Formula Block Template

```markdown
### [Formula Name]

**Epistemic status:** [CONSENSUS / CONVENTION / HEURISTIC / DEBATED]
**Reference:** [bib key — must exist in bibliography.bib]

#### Formal Definition

$$
[LaTeX formula here]
$$

#### Symbol Definitions

| Symbol | Meaning | Unit / Domain |
|--------|---------|---------------|
| $x$    | ...     | ...           |

#### Assumptions

List every assumption required for this formula to be valid. For each:
- State the assumption explicitly.
- Describe how to test or verify it in this project.
- State what happens when the assumption is violated.

Example:
- **Independence of observations:** Residuals must not be correlated.
  Tested via Durbin-Watson statistic. Violation → standard errors are
  underestimated; use HAC-robust standard errors (Newey & West, 1987).

#### Plain-Language Interpretation

Explain what this formula computes and what the result means, without
mathematical notation. Write at the level of the report's target audience.

#### When This Formula Should NOT Be Used

State the conditions under which this formula gives misleading or invalid
results. Be specific. This section prevents misapplication.

#### Numerical Example

Using actual values from this project (not invented numbers):

```python
# Example using project data
# [insert minimal reproducible snippet]
```

Result: [value with units]
Interpretation: [what this specific result means in context]

#### Implementation

| Item | Value |
|------|-------|
| Library | [e.g., scipy, statsmodels, sklearn] |
| Function | [e.g., `scipy.stats.pearsonr()`] |
| Version | [e.g., scipy==1.11.4] |
| Documentation | [URL] |
```

---

## Example: Pearson Correlation Coefficient

### Pearson Correlation Coefficient

**Epistemic status:** [CONSENSUS]
**Reference:** Pearson1895

#### Formal Definition

$$
r = \frac{\sum_{i=1}^{n}(x_i - \bar{x})(y_i - \bar{y})}
         {\sqrt{\sum_{i=1}^{n}(x_i - \bar{x})^2 \cdot \sum_{i=1}^{n}(y_i - \bar{y})^2}}
$$

#### Symbol Definitions

| Symbol | Meaning | Unit / Domain |
|--------|---------|---------------|
| $r$ | Pearson correlation coefficient | dimensionless, $r \in [-1, 1]$ |
| $x_i$ | $i$-th value of variable $X$ | same unit as $X$ |
| $y_i$ | $i$-th value of variable $Y$ | same unit as $Y$ |
| $\bar{x}$ | Arithmetic mean of $X$ | same unit as $X$ |
| $\bar{y}$ | Arithmetic mean of $Y$ | same unit as $Y$ |
| $n$ | Number of paired observations | dimensionless integer |

#### Assumptions

- **Linearity:** The relationship between $X$ and $Y$ must be linear.
  Verified via scatter plot. Violation → $r$ underestimates a real
  monotonic relationship; use Spearman's $\rho$ instead.
- **Normality (for inference):** Both variables should be approximately
  normally distributed when using $r$ to test significance.
  Verified via Shapiro-Wilk or Q-Q plot. Violation → use permutation test
  or Spearman.
- **No significant outliers:** $r$ is sensitive to outliers.
  Inspect scatter plot; consider robust correlation if outliers are present.
- **Homoscedasticity:** Variance of $Y$ should be constant across $X$.
  Violation → $r$ may be misleading in some ranges of $X$.

#### Plain-Language Interpretation

The Pearson correlation measures how strongly two variables move together
in a linear fashion. A value of $r = 1$ means a perfect positive linear
relationship (when one increases, the other increases proportionally).
$r = -1$ means a perfect negative linear relationship. $r = 0$ means no
linear relationship — though a strong non-linear relationship may still
exist.

**Important:** Correlation does not imply causation. [CONSENSUS]

#### When This Formula Should NOT Be Used

- When the relationship between variables is non-linear (use Spearman's $\rho$
  or Kendall's $\tau$).
- When data contains extreme outliers that cannot be removed on substantive
  grounds (use robust correlation).
- When both variables are ordinal, not continuous.
- When the sample size is very small ($n < 10$): $r$ estimates are unstable.

#### Numerical Example

(Using project data — replace with actual values)

```python
import scipy.stats as stats
r, p_value = stats.pearsonr(df['variable_x'], df['variable_y'])
print(f"r = {r:.4f}, p = {p_value:.4f}")
```

Result: $r = 0.74$, $p < 0.001$, $n = 312$
Interpretation: There is a strong positive linear association between
[variable X] and [variable Y]. With $n = 312$ and $p < 0.001$, this
association is unlikely to be due to chance alone, though effect size
context matters more than the p-value alone [CONSENSUS — Sullivan & Feinn 2012].

#### Implementation

| Item | Value |
|------|-------|
| Library | scipy |
| Function | `scipy.stats.pearsonr()` |
| Version | scipy==1.11.4 |
| Documentation | https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.pearsonr.html |
