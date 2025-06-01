from statsmodels.stats.diagnostic import acorr_ljungbox
from scipy.stats import ttest_rel

def compute_dm_test(forecasts_df, actuals_df, model_1: str, model_2: str):
    f1 = forecasts_df[model_1].values
    f2 = forecasts_df[model_2].values
    true = actuals_df["y"].values

    e1 = abs(f1 - true)
    e2 = abs(f2 - true)
    stat, pval = ttest_rel(e1, e2)
    return {
        "vs": model_2,
        "dm_stat": round(stat, 3),
        "p_value": round(pval, 3)
    }
