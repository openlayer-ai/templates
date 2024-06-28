"""Run all my custom metrics."""

# Import all your custom metrics here
from my_metric import RishabMetric
from answer_correctness import Correctness
from openlayer.lib.core import metrics


if __name__ == "__main__":
    metrics.MetricRunner().run_metrics([RishabMetric(), Correctness()])
