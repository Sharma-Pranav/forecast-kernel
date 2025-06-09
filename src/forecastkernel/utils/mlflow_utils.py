import os
import mlflow


def log_mlflow_metrics(run_id, df, h, metrics_dict, selected_model, pass_ci, output_path, phase):
    """Log metrics and artifacts for a StatsForecast baseline run.

    Parameters
    ----------
    run_id : str
        Identifier for the MLflow run.
    df : pandas.DataFrame
        Full input dataframe used to train the models.
    h : int
        Forecast horizon.
    metrics_dict : dict
        Mapping of model name to metric dictionary.
    selected_model : str
        Model chosen as the best performer.
    pass_ci : bool
        Whether the CI score threshold was met.
    output_path : str
        Directory containing the run outputs to log as artifacts.
    phase : int
        Current project phase used to tag the run.

    Returns
    -------
    None
    """
    # Route logs to hidden subfolder to avoid root clutter
    tracking_dir = os.getenv("MLFLOW_TRACKING_URI", "file:./.mlflow_logs")
    mlflow.set_tracking_uri(tracking_dir)

    mlflow.set_experiment("forecast-kernel-baselines")

    with mlflow.start_run(run_name=run_id) as run:
        mlflow.log_param("selected_model", selected_model)
        mlflow.log_param("horizon", h)
        mlflow.set_tags({
            "phase": phase,
            "series_id": df["unique_id"].iloc[0],
            "run_id": run_id
        })

        for model, metrics in metrics_dict.items():
            for metric_name, value in metrics.items():
                mlflow.log_metric(f"{model}_{metric_name}", value)

        mlflow.log_metric("pass_ci", int(pass_ci))

        # Defensive path check
        def safe_log(path):
            if os.path.exists(path):
                mlflow.log_artifact(path)

        safe_log(os.path.join(output_path, "baseline_metrics.json"))
        safe_log(os.path.join(output_path, "baseline_forecasts.csv"))
        safe_log(os.path.join(output_path, "run_info.json"))
