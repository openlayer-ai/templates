"""This file is used by Openlayer to create a custom metric for
an LLM project.
"""

import pandas as pd
import ragas_metrics
from openlayer.lib.core import metrics


class AnswerCorrectness(metrics.BaseMetric):
    """Gets the answer correctness."""

    def __init__(self, ragas_metrics: ragas_metrics.RagasMetrics):
        """Instantiates custom LLM for evals."""
        self.ragas_metrics = ragas_metrics

    def compute_on_dataset(self, config: dict, df: pd.DataFrame) -> dict:
        """Method that computes a metric given a dataframe and config."""
        score = self.ragas_metrics.run(
            df=df, config=config, metric="answer_correctness"
        )
        return metrics.MetricReturn(value=score, meta={})


class AnswerSimilarity(metrics.BaseMetric):
    """Gets the answer similarity."""

    def __init__(self, ragas_metrics: ragas_metrics.RagasMetrics):
        """Instantiates custom LLM for evals."""
        self.ragas_metrics = ragas_metrics

    def compute_on_dataset(self, config: dict, df: pd.DataFrame) -> dict:
        """Method that computes a metric given a dataframe and config."""
        score = self.ragas_metrics.run(df=df, config=config, metric="answer_similarity")
        return metrics.MetricReturn(value=score, meta={})


class Faithfulness(metrics.BaseMetric):
    """Gets the faithfulness."""

    def __init__(self, ragas_metrics: ragas_metrics.RagasMetrics):
        """Instantiates custom LLM for evals."""
        self.ragas_metrics = ragas_metrics

    def compute_on_dataset(self, config: dict, df: pd.DataFrame) -> dict:
        """Method that computes a metric given a dataframe and config."""
        score = self.ragas_metrics.run(df=df, config=config, metric="faithfulness")
        return metrics.MetricReturn(value=score, meta={})


class RishabMetric(metrics.BaseMetric):
    """Computes exact match between the ground truth and output."""

    def compute_on_dataset(self, config: dict, df: pd.DataFrame) -> dict:
        """Method that computes a metric given a dataframe and config."""

        df["score"] = df.apply(lambda x: self.compute_on_row(x, config), axis=1)
        score = df["score"].mean()

        return metrics.MetricReturn(value=score, unit=None, meta=None)

    def compute_on_row(self, data: dict, config: dict) -> float:
        """Method that computes a score on a single row."""

        output = data[config["outputColumnName"]]
        gt = data["ground_truth"]

        # Insert any logic you want here
        score = 1.0
        if output == gt:
            score = 0.0

        return score
