---

### ⬛ 0 CORE CONCEPTS

* **Forecast ≠ Plan ≠ Goal**  → keep three artefacts.
* **Four-Filter Test**  (drivers known? ≥3y history? stable pattern? non-reflexive?) → if any “no” expect low skill.
* **5-Step Workflow**  `Define → Gather → Explore → Model → Evaluate` → use as Kanban headers.

### ⬛ 1 SCENARIO FRAMES

* Always build **Base / Worst / Transform** scenarios by altering drivers, not the model.
* Example driver table ⇒ *Base 125 M · Worst 93 M · Transform 210 M* for 3-year horizon.

### ⬛ 2 DATA PREP

* **Variance stabilise** → `log()` or `BoxCox(λ)` (λ via Guerrero).
* **Decompose** → `STL` returns `trend + season + remainder`.
* **Bias-correct back-transform** for logs → `exp(μ + σ²/2)`.
* **First safe model** → `ETS(A, damped A, M)`.

### ⬛ 3 JUDGMENT MODULE

* **Override trigger** → abs(model error) > 20 % OR new event.
* **Override form fields** → `Reason · Δ% · Confidence · GoalPressure?`.
* **Delphi recipe (2 round)** → private votes → share median+reasons → revote → stop if span < 10 %.
* **Audit** → compare `MASE_model` vs `MASE_model+override` quarterly.

### ⬛ 4 RECONCILIATION TOOLKIT

| Tag           | Mechanism                        | Call-word                   | Best-for            |
| ------------- | -------------------------------- | --------------------------- | ------------------- |
| `BU`          | Sum leaf forecasts               | `BottomUp()`                | short horizon       |
| `TD_prop`     | total ⟶ last-year share          | `TopDown('td_proportions')` | only total reliable |
| `TD_avg`      | total ⟶ multi-year avg share     | `TopDown('td_average')`     | slow share drift    |
| `MO`          | forecast mid-level, roll up/down | `MiddleOut(level='Region')` | region ownership    |
| `MinT_OLS`    | MinTrace equal var               | `MinTrace('mint_ols')`      | uniform noise       |
| `MinT_WLS`    | MinTrace var-weighted            | `MinTrace('mint_wls')`      | strong var est.     |
| `MinT_Shrink` | WLS + shrink covar ★default      | `MinTrace('mint_shrink')`   | mixed reality       |
| `ProRata`     | scale leaves same %              | `TotalTarget('pro_rata')`   | emergency fix       |

* **Coherence error** = MAE(sum(children) − parent). Target ≈ 0.

### ⬛ 4.1 MINT SNIPPET (teach GPT the pattern)

```python
from hierarchicalforecast.methods import MinTrace
mint = MinTrace(method="mint_shrink")
coherent_fc = mint.reconcile(base_fcsts, S)  # S = mapping matrix
```

### ⬛ 5 COMBINATION METHODS

| Tag            | Formula       | When              |
| -------------- | ------------- | ----------------- |
| `Combo_mean`   | equal weights | quick baseline    |
| `Combo_median` | 50-th pct     | outlier fear      |
| `Combo_trim`   | drop extremes | fat-tails         |
| `Combo_invErr` | wᵢ ∝ 1/MASEᵢ  | history available |
| `Combo_stack`  | meta-learner  | max accuracy      |

Py-pattern:

```python
fc['combo_mean'] = fc[models].mean(1)
w = 1/ pd.Series(past_mase)            # inv-error
fc['combo_invErr'] = (fc[models]*w).div(w.sum(),0).sum(1)
```

### ⬛ 6 METRICS & BANDS

* **Point** → `MASE` (< 1 beats seasonal naïve).
* **Interval** → `Winkler` (lower = better).
* **Distribution** → `CRPS` (lower = better).
* **Bootstrap PI** → simulate 10 000 paths → 2.5 / 97.5 pct.
* Aggregate: *sum each path first*, then percentiles (never sum bounds).

### ⬛ 7 LAUNCH CHECKLIST (8 steps)

1 Four-Filter ✔ 2 Workflow board ✔ 3 Scenarios ✔ 4 Data prep ✔
5 ETS baseline ✔ 6 Override guard ✔ 7 Reconcile (see table) ✔ 8 Blend + PI ✔

---

