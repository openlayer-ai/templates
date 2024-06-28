"""This file is used by Openlayer to create a custom metric for
an LLM project.
"""

from __future__ import annotations

import typing as t

import openai
import pandas as pd
from datasets import Dataset
from langchain_core.outputs.generation import Generation
from ragas import evaluate
from ragas.llms.base import BaseRagasLLM, LLMResult
from ragas.llms.prompt import PromptValue
from ragas.metrics import answer_correctness, answer_similarity, faithfulness
from ragas.run_config import RunConfig

if t.TYPE_CHECKING:
    from langchain_core.callbacks import Callbacks


# ------------ Custom LLM implementing the BaseRagasLLM interface ------------ #
class MyLLM(BaseRagasLLM):
    """Custom LLM for evals."""

    def __init__(self, run_config: RunConfig):
        """Instantiates custom LLM for evals."""
        super().__init__(run_config=run_config)
        self.client = openai.Client()

    def generate_text(
        self,
        prompt: PromptValue,
        n: int = 1,
        temperature: float = 1e-8,
        stop: t.Optional[t.List[str]] = None,
        callbacks: Callbacks = None,
    ) -> LLMResult:
        """Generates text with the LLM."""
        # Convert from PromptValue to the OpenAI messages format
        messages = []
        for message in prompt.to_messages():
            if message.type == "human":
                messages.append({"role": "user", "content": message.content})

        # Call the LLM
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            n=n,
            temperature=temperature,
        )

        # Return generations
        return LLMResult(
            generations=[[Generation(text=response.choices[0].message.content)]]
        )

    async def agenerate_text(
        self,
        prompt: PromptValue,
        n: int = 1,
        temperature: float = 1e-8,
        stop: t.Optional[t.List[str]] = None,
        callbacks: Callbacks = None,
    ) -> LLMResult:
        pass


# ------ Computes all the metrics and saves the results to self.results ------ #
class RagasMetrics:

    def __init__(self) -> None:
        """Instantiates custom LLM for evals."""
        self.llm = MyLLM(run_config=RunConfig())
        self.results: t.Optional[dict] = None

    def run(self, df: pd.DataFrame, config: dict, metric: str) -> dict:
        """Method that computes the Ragas metrics."""
        if self.results is not None:
            return self.results.get(metric)

        question_col = "input_data"
        answer_col = config["outputColumnName"]
        context_col = "context"
        gt_col_name = "ground_truth"

        dataset = Dataset.from_pandas(
            df[[question_col, answer_col, context_col, gt_col_name]]
        )

        result = evaluate(
            dataset=dataset,
            metrics=[
                answer_similarity,
                answer_correctness,
                faithfulness,
            ],
            llm=self.llm,
            column_map={
                "question": question_col,
                "answer": answer_col,
                "ground_truth": gt_col_name,
                "contexts": context_col,
            },
            is_async=False,
        )
        self.results = {
            "answer_correctness": result.to_pandas()["answer_correctness"].mean(),
            "answer_similarity": result.to_pandas()["answer_similarity"].mean(),
            "faithfulness": result.to_pandas()["faithfulness"].mean(),
        }
        return self.results.get(metric)
