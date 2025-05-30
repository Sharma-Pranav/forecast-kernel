# Forecastability → Baseline Model Mapping

This guide provides the most robust naive baseline models for each structural type of time series, based on ADI, CV², and Spectral Entropy.

---

## 🔹 Intermittent Demand (ADI ≥ 1.32)

### 1. **Lumpy (High CV² ≥ 0.49)**
- **Best Model:** `CrostonOptimized`
- Notes: Large gaps between non-zero values; highly erratic.
  
### 2. **Intermittent (Low CV² < 0.49)**
- **Best Model:** `CrostonClassic` or `CrostonSBA`
- Notes: More regular than lumpy, still with many zeros.

---

## 🔸 Non-Intermittent Demand (ADI < 1.32)

### 3. **Very High Forecastability (Spectral Entropy 0.0 – 0.3)**
- **Best Model:** `HoltWinters` or `SeasonalNaive`
- Notes: Strong seasonality and/or trend.

### 4. **Moderate Forecastability (Entropy 0.3 – 0.6)**
- **Best Model:** `SimpleExponentialSmoothing (SES)` or `Theta`
- Notes: Weak or irregular seasonal pattern; decaying memory useful.

### 5. **Low Forecastability (Entropy > 0.6)**
- **Best Model:** `HistoricAverage` or `Naive`
- Notes: Near-randomness; few repeatable structures.

---

## 🧠 Recommendation Logic Summary

| Type               | Classifier                      | Best Model(s)               |
|--------------------|----------------------------------|-----------------------------|
| Lumpy              | ADI ≥ 1.32 & CV² ≥ 0.49          | CrostonOptimized            |
| Intermittent       | ADI ≥ 1.32 & CV² < 0.49          | CrostonClassic / SBA        |
| Strongly Seasonal  | Entropy < 0.3                    | HoltWinters / SeasonalNaive |
| Semi-Seasonal      | 0.3 ≤ Entropy < 0.6              | SES / Theta                 |
| Noisy / Random     | Entropy ≥ 0.6                    | HistoricAverage / Naive     |

---

✅ **Use this as your pre-modeling guide to pick smart baselines aligned with series structure.**