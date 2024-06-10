"""This file is used by Openlayer to create a custom metric for
an LLM project.
"""

import pandas as pd
from openlayer.lib.core import metrics
from openlayer.types.inference_pipelines.data_stream_params import ConfigLlmData


class MyMetric(metrics.BaseMetric):
    """Computes exact match between the ground truth and output."""

    def compute_on_dataset(self, df: pd.DataFrame, config: ConfigLlmData) -> dict:
        """Method that computes a metric given a dataframe and config."""

        df["score"] = df.apply(lambda x: self.compute_on_row(x, config), axis=1)
        score = df["score"].mean()

        return metrics.MetricReturn(value=score, meta=None)

    def compute_on_row(self, data: dict, config: ConfigLlmData) -> float:
        """Method that computes a score on the ."""

        output = data[config.output_column_name]
        gt = data[config.ground_truth_column_name]

        # Insert any logic you want here
        score = 1.0
        if output == gt:
            score = 0.0

        return score


if __name__ == "__main__":
    metric = MyMetric()
    metric.run_from_cli()
