# Forecast-Kernel: Theoretical Enhancements for CI and Model Rigor

## 1. Diebold-Mariano Test (1995)

### Purpose

Statistical method to compare predictive accuracy of two models over the same dataset.

### Formula

Given loss differential $d_t = L(e_{1,t}) - L(e_{2,t})$, where L is typically squared or absolute error:
$DM = \frac{\bar{d}}{\sqrt{\text{Var}(d_t)/n}}$

* $\bar{d}$: Mean difference in errors
* $\text{Var}(d_t)$: Variance of error differences
* $n$: Number of forecast points

### Kernel Implementation

* Use for all model comparisons post-baseline (Phase 1, Phase 8)
* Attach `dm_stat`, `p_value` to `baseline_metrics.json`
* Promotion rule: only allow model if `p_value < 0.05` vs ensemble\_naive

### Example (using `arch.bootstrap` and `scipy.stats`)

```python
from scipy import stats
import numpy as np

def dm_test(e1, e2):
    d = np.abs(e1) - np.abs(e2)
    dm_stat = d.mean() / (d.std(ddof=1) / np.sqrt(len(d)))
    p_value = 2 * (1 - stats.norm.cdf(np.abs(dm_stat)))
    return dm_stat, p_value
```

### Validation Source

* Diebold & Mariano (1995) — [https://www.sas.upenn.edu/\~fdiebold/papers/paper68/pa.dm.pdf](https://www.sas.upenn.edu/~fdiebold/papers/paper68/pa.dm.pdf)

---

## 2. Confidence Intervals (Shumway & Stoffer)

### Purpose

Quantify uncertainty in forecasts using variance of prediction error.

### Formula

$\hat{y}_{t+h} \pm z_{\alpha} \cdot \sqrt{\text{Var}(y_{t+h})}$

* $\hat{y}_{t+h}$: Forecasted value at horizon $h$
* $z_{\alpha}$: z-score corresponding to desired confidence level (e.g., 1.96 for 95%)
* $\text{Var}(y_{t+h})$: Forecast error variance

### Kernel Implementation

* From Phase 3 onward, attach `upper`, `lower`, `std_error` to forecasts
* Use interval width as a drift-volatility indicator
* Enable dashboard flags for low-confidence outputs

### Example (using `statsmodels`)

```python
import numpy as np
import statsmodels.api as sm

model = sm.tsa.ExponentialSmoothing(series, seasonal='add', seasonal_periods=12).fit()
pred = model.forecast(steps=12)

forecast_mean = pred.values
forecast_var = model.sse / model.nobs
z_alpha = 1.96  # 95% confidence
interval = z_alpha * np.sqrt(forecast_var)
forecast_lower = forecast_mean - interval
forecast_upper = forecast_mean + interval
```

### Validation Source

* Shumway & Stoffer (TSA) — [https://www.stat.ucla.edu/\~frederic/415/S23/tsa4.pdf](https://www.stat.ucla.edu/~frederic/415/S23/tsa4.pdf)

---

## 3. Intermittent Demand Forecasting (Syntetos & Boylan)

### Purpose

Model structure-aware zero-heavy series more effectively.

### Key Metrics

* **ADI (Average Demand Interval)**: Average time between non-zero demands
* **CV² (Squared Coefficient of Variation)**: Variability measure = (std / mean)^2

### Classification Logic

* **Lumpy**: ADI ≥ 1.32 and CV² ≥ 0.49 → Use `CrostonOptimized`
* **Intermittent**: ADI ≥ 1.32 and CV² < 0.49 → Use `CrostonSBA` or `TSB`

### Kernel Implementation

* Enforce model tag: `croston_variant = SBA | TSB | Opt`
* Validate selection logic in `scripts/baseline_sf.py`
* Log intermittency class to `baseline_metrics.json`

### Example (using `statsforecast`)

```python
from statsforecast import StatsForecast
from statsforecast.models import CrostonSBA, CrostonOptimized

model_class = CrostonOptimized if (adi >= 1.32 and cv2 >= 0.49) else CrostonSBA
model = model_class()
sf = StatsForecast(models=[model], freq='D')
forecast = sf.forecast(df, h=28)
```

### Validation Source

* Boylan & Syntetos (2021) — [https://www.researchgate.net/publication/351965958\_Intermittent\_Demand\_Forecasting\_Context\_methods\_and\_applications](https://www.researchgate.net/publication/351965958_Intermittent_Demand_Forecasting_Context_methods_and_applications)

---

## Integration Notes

* These enhancements should not bloat ops time or break Phase 1 bootstrap
* Store metrics with full lineage: source, method, assumptions
* Enforce these CI/logging rules from Phase 1 onward; use as hard gates from Phase 3+

---

## Summary Table

| Theory Element       | Phase(s) Used | Implementation Requirement              |
| -------------------- | ------------- | --------------------------------------- |
| Diebold-Mariano Test | 1, 8          | `dm_stat`, `p_value` in metrics log     |
| Confidence Intervals | 3+            | `upper`, `lower`, `std_error` in output |
| Intermittent Models  | 1             | `croston_variant` tag in metrics log    |
