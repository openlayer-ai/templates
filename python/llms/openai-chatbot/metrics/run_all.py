"""Run all my custom metrics."""

# Import all your custom metrics here
from my_metric import RishabMetric
from openlayer.lib.core import metrics


if __name__ == "__main__":
    metrics.MetricRunner().run_metrics([RishabMetric()])
