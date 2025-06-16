
## 🧠 **FIL-∞ Architecture — Live + Dev Modes with Diagnostic Calibration **

```
        ┌────────────────────────────────────────────┐
        │         Raw Time Series Data Sources       │
        │  (Sales, Orders, Price, Promo, Calendar)   │
        └────────────────────────────────────────────┘
                             │
                             ▼
        ┌────────────────────────────────────────────┐
        │        Data Preprocessing & Feature Gen    │
        │  - Calendar enrichment                     │
        │  - Lag/rolling stats                       │
        │  - Promo/price/stockout handling           │
        └────────────────────────────────────────────┘
                             │
                             ▼
        ┌──────────────────────────────┐
        │   Scenario Injection Engine  │   ◄── Manual or scripted
        │  (stockout, cold start, etc) │
        └──────────────────────────────┘
                             │
                             ▼
        ┌────────────────────────────────────────────┐
        │           Forecast Model Layer             │
        │  - TiRex (xLSTM)     ← internal benchmark  │
        │  - TIME-MoE          ← production-grade    │
        │  - Darts / NeuralForecast (SOTA baselines) │
        └────────────────────────────────────────────┘
                             │
           ┌────────────────┴────────────────┐
           ▼                                 ▼
┌──────────────────────────────┐  ┌────────────────────────────────────────────────────────┐
│      📦 Live Forecast Path    │  │   🧪 Development & Calibration Path (via `toto`)        │
│ - No y_true available        │  │ - For backtesting, diagnostics, and model tuning       │
│ - Used in operational flows  │  │ - Evaluate & recalibrate forecast reliability          │
│                              │  │ - Visualize sharpness & coverage                       │
│                              │  │ - Train `Calibrator()` and export to production        │
└──────────────────────────────┘  └────────────────────────────────────────────────────────┘
                             │                                               ▲
                             ▼                                               │
        ┌────────────────────────────────────────────┐             ┌─────────────────────────────┐
        │   🛠️  (Optional) Calibrator Inference Layer  │ ◄──────────┤ Apply `Calibrator.transform` │
        │ - Load pretrained calibrator object         │             └─────────────────────────────┘
        │ - Correct quantile forecasts before output  │
        └────────────────────────────────────────────┘
                             │
                             ▼
        ┌────────────────────────────────────────────┐
        │      Evaluation & Diagnostic Metrics        │
        │  - MAE, Bias, SMAPE                         │
        │  - Score = MAE + |Bias|                     │
        │  - ABC-XYZ Class Accuracy                   │
        │  - Forecast Value Added (FVA)               │
        └────────────────────────────────────────────┘
                             │
                             ▼
        ┌────────────────────────────────────────────┐
        │       Forecast Output + Metadata Layer      │
        │  - Versioning (DVC, MLflow)                 │
        │  - Export to Obsidian, CSV, Gamma slides    │
        │  - For decks, audits, client trust layers   │
        └────────────────────────────────────────────┘
```

---

## 🧪 `toto` Calibration Code (Used in Development Layer Only)

```python
from toto.metrics import coverage, sharpness, reliability_curve
from toto.calibration import Calibrator
from toto.plotting import plot_reliability_diagram

# Inputs:
# y_preds: array of quantile forecasts, shape [n_samples, n_quantiles]
# y_true: actual target values
# quantiles: list of quantile levels (e.g., [0.1, 0.5, 0.9])

# Step 1: Evaluate forecast calibration
coverage_scores = coverage(y_preds, y_true, quantiles)
sharpness_score = sharpness(y_preds)
rel_x, rel_y = reliability_curve(y_preds, y_true, quantiles)

print("Coverage:", dict(zip(quantiles, coverage_scores)))
print("Sharpness Score:", sharpness_score)

# Optional: Visualize reliability diagram
plot_reliability_diagram(rel_x, rel_y, quantiles)

# Step 2: Recalibrate forecast quantiles
calibrator = Calibrator()
calibrator.fit(y_preds, y_true, quantiles)
y_recalibrated = calibrator.transform(y_preds, quantiles)
```

---

## 🔁 Productionizing the Calibrator

Once validated offline, the `Calibrator` can be moved to live production:

### ✅ Save Once in Dev

```python
import joblib
joblib.dump(calibrator, "quantile_calibrator.pkl")
```

### ✅ Apply in Production

```python
calibrator = joblib.load("quantile_calibrator.pkl")
calibrated_preds = calibrator.transform(y_preds_live, quantiles)
```

💡 *This enables real-time correction of quantile forecasts — trust alignment without retraining.*

---

## 📌 Embedded Design Intelligence & Execution Notes

### ⚠ Assumptions

* Forecast model must support **quantile outputs**
* `toto` calibration logic is only valid when **ground truth (`y_true`) is available**
* Quantiles must be consistent between calibration and inference phases

---

### ✅ When to Use `toto`

| Use Case                      | Use `toto`?                             |
| ----------------------------- | --------------------------------------- |
| Live forecasts                | ✅ After calibrator is trained and saved |
| Backtesting loop              | ✅ Yes                                   |
| Quarterly Codex reviews       | ✅ Yes                                   |
| Forecast Value Added analysis | ✅ Yes                                   |
| Client deck or dashboard      | ✅ Yes (plots, insights)                 |

---

### 🔁 Integration Suggestion (Hydra-style)

```yaml
mode: dev
forecast:
  quantiles: [0.1, 0.5, 0.9]
  use_calibration: true
```

Then:

```python
if config.mode == "dev" and config.forecast.use_calibration:
    run_toto_evaluation(...)
```

---

### 💾 Log This in MLflow/DVC

For each run:

* Save `coverage_scores`, `sharpness_score`, and `recalibrator.pkl`
* Export reliability diagram `.png`
* Tag: `model=TIME-MoE_v1.2-calibrated`, `calibrator=p10-p90-v3`

---

## 🧠 Why This Matters

| Layer                    | Role                                       | Output                      |
| ------------------------ | ------------------------------------------ | --------------------------- |
| **Forecast Model Layer** | Generates quantile predictions             | `y_preds`                   |
| **Calibration (toto)**   | Validates and trains post-hoc correction   | Calibration scores          |
| **Recalibration (prod)** | Corrects quantile spread at inference time | `y_calibrated`              |
| **Evaluation Layer**     | Final trust metrics + FVA                  | MAE, Bias, Score            |
| **Codex Layer**          | Feeds forecasts + trust metrics into tools | Strategy-grade intelligence |

---

