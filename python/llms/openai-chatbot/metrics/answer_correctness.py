"""This file is used by Openlayer to create a custom metric for
an LLM project.
"""

from __future__ import annotations

import pandas as pd
from openlayer.lib.core import metrics

from ragas.metrics import answer_correctness
from ragas.llms.base import BaseRagasLLM, LLMResult, PromptValue
from ragas import evaluate
from datasets import Dataset
import typing as t

if t.TYPE_CHECKING:
    from langchain_core.callbacks import Callbacks


class MyLLM(BaseRagasLLM):
    """Custom LLM for evals."""

    def generate_text(
        self,
        prompt: PromptValue,
        n: int = 1,
        temperature: float = 1e-8,
        stop: t.Optional[t.List[str]] = None,
        callbacks: Callbacks = None,
    ) -> LLMResult:

        return LLMResult("")

    async def agenerate_text(
        self,
        prompt: PromptValue,
        n: int = 1,
        temperature: float = 1e-8,
        stop: t.Optional[t.List[str]] = None,
        callbacks: Callbacks = None,
    ) -> LLMResult:
        pass


class Correctness(metrics.BaseMetric):
    """Computes correctness."""

    def __init__(self):
        """Instantiates custom LLM for evals."""
        self.llm = BaseRagasLLM()

    def compute_on_dataset(self, config: dict, df: pd.DataFrame) -> dict:
        """Method that computes a metric given a dataframe and config."""

        question_col = "input_data"
        answer_col = config["outputColumnName"]
        gt_col_name = "ground_truth"

        dataset = Dataset.from_pandas(df[[question_col, answer_col, gt_col_name]])

        result = evaluate(
            dataset=dataset,
            metrics=[
                answer_correctness,
            ],
            llm=self.llm,
            column_map={
                "question": question_col,
                "answer": answer_col,
                "ground_truth": gt_col_name,
            },
        )
        score = result.to_pandas()["answer_correctness"].mean()
        return metrics.MetricReturn(value=score, meta={})
