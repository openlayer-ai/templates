"""This file is used by Openlayer to create a custom metric for
an LLM project.
"""

from openlayer.lib.core import metrics
from openlayer.types.inference_pipelines import data_stream_params


class MyMetric(metrics.BaseMetric):
    """Computes exact match between the ground truth and output."""

    def get_key(self) -> str:
        """Return the key of the metric."""
        return "my_metric"

    def compute_on_dataset(self, dataset: metrics.Dataset) -> dict:
        """Method that computes a metric given a dataframe and config."""

        dataset.df["score"] = dataset.df.apply(
            lambda x: self.compute_on_row(x, dataset.config), axis=1
        )
        score = dataset.df["score"].mean()

        return metrics.MetricReturn(
            value=score, unit=None, meta=None, added_cols={"score"}
        )

    def compute_on_row(
        self, data: dict, config: data_stream_params.ConfigLlmData
    ) -> float:
        """Method that computes a score on a single row."""

        output = data[config["outputColumnName"]]
        gt = data[config["groundTruthColumnName"]]

        # Insert any logic you want here
        score = 0.0
        if output != gt:
            score = 1.0

        return score


if __name__ == "__main__":
    MyMetric().run()
