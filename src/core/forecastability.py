import numpy as np
import pandas as pd
from scipy.stats import variation
from scipy.signal import periodogram


def spectral_entropy(series):
    f, Pxx = periodogram(series)
    Pxx = Pxx[Pxx > 0]
    Pxx /= Pxx.sum()
    return -np.sum(Pxx * np.log(Pxx)) / np.log(len(Pxx))


def classify_forecastability(adi, cv2, entropy):
    if adi >= 1.32 and cv2 >= 0.49:
        return "Lumpy"
    elif adi >= 1.32:
        return "Intermittent"
    elif entropy > 0.6:
        return "Noisy"
    elif entropy < 0.3:
        return "Strongly Seasonal"
    else:
        return "Moderate"


def compute_forecastability_metrics(df: pd.DataFrame) -> dict:
    assert df["unique_id"].nunique() == 1, "Only one series allowed per baseline run"
    y = df["y"].values

    adi = len(y) / np.count_nonzero(y)
    cv2 = variation(y, ddof=1) ** 2
    entropy = spectral_entropy(y)
    classification = classify_forecastability(adi, cv2, entropy)

    return {
        "ADI": round(adi, 2),
        "CV2": round(cv2, 2),
        "SpectralEntropy": round(entropy, 3),
        "classification": classification
    }
