"""Run all my custom metrics."""

# Import all your custom metrics here
from my_metrics import (AnswerCorrectness, AnswerSimilarity, Faithfulness,
                        RishabMetric)
from openlayer.lib.core import metrics
from ragas_metrics import RagasMetrics

if __name__ == "__main__":
    ragas_metrics = RagasMetrics()
    metrics.MetricRunner().run_metrics(
        [
            RishabMetric(),
            AnswerCorrectness(ragas_metrics),
            AnswerSimilarity(ragas_metrics),
            Faithfulness(ragas_metrics),
        ]
    )
