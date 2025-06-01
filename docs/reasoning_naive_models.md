## 🌟 Phase 1 Rationale: Control Arm, Not Algorithm Bias

### 🔄 Purpose: CI-Tractable, Structure-Aware Baseline

Phase 1 is not about using only "naive" algorithms or getting best accuracy early. It's about establishing:

1. **Reproducible Performance Floor**

   * Define what a structure-aware, zero-feature model can achieve on Score (MAE + |Bias|)
   * All future models must beat this to be eligible for promotion

2. **Baseline CI Gate**

   * CI Rule: `selected_model.Score <= min(ensemble_naive, holt_winters)`
   * Enforces rigor before adding regressors, features, or cloud cost

3. **Forecastability Classification**

   * Uses ADI, CV², and Spectral Entropy to guide model selection
   * Aligns model type (e.g. Croston, Holt-Winters) to structure type (intermittent, seasonal, random)

4. **Data-Bound Audit Contract**

   * Output: `baseline_metrics.json` includes

     * Forecastability tags
     * All core model metrics (MAE, Bias, Score)
     * Drift monitor metadata
     * CI rule outcome (pass/fail)

---

### 🚫 Misconception: Naive Models Are Favored

Naive models are **tracked** but not **promoted** unless they win on Score.

| Model            | Role       | Promotion Rule                        |
| ---------------- | ---------- | ------------------------------------- |
| `naive`          | Benchmark  | Never promoted unless all others fail |
| `ensemble_naive` | Floor      | Part of CI min() gate                 |
| `holt_winters`   | Floor      | Part of CI min() gate                 |
| `croston_sba`    | Structural | Considered if ADI ≥ 1.32              |

> Phase 1 exists to **prevent hype-based forecasting**. If your advanced model can’t beat a tuned moving average, it’s not ready.

---

### 🚀 Strategic Payoff

* Ensures every forecast has a legitimate fallback
* Builds trust in model uplift via clean comparisons
* Keeps Kernel slim, scalable, and verifiable

---

### 👉 Summary

Phase 1 is your **baseline CI armory**:

* Track all candidates
* Promote only those that beat structure-aware naive models on Score
* Lock in demand regime classification before any feature engineering begins
