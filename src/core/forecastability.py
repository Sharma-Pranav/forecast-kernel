import numpy as np
import pandas as pd
from scipy.stats import variation
from scipy.signal import periodogram


def spectral_entropy(series):
    f, Pxx = periodogram(series)
    Pxx = Pxx[Pxx > 0]
    Pxx /= Pxx.sum()
    return -np.sum(Pxx * np.log(Pxx)) / np.log(len(Pxx))


def compute_forecastability_metrics(df: pd.DataFrame) -> list:
    forecastability = []
    for uid, group in df.groupby("unique_id"):
        y = group["y"].values
        adi = len(y) / np.count_nonzero(y)
        cv2 = variation(y, ddof=1) ** 2
        entropy = spectral_entropy(y)
        forecastability.append({
            "unique_id": uid,
            "ADI": round(adi, 2),
            "CV2": round(cv2, 2),
            "Entropy": round(entropy, 3)
        })
    return forecastability
