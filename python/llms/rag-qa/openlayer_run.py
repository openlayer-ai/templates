"""This file is used by Openlayer to run the model and get its outputs.

If you go to openlayer.json, you'll see that the `batchCommand` field points here.

The openlayer_run.py must contain 2 things:

1. A class that inherits from OpenlayerModel and implements the `run` method.
2. A `__main__` block that creates an instance of the class and calls the `run_from_cli`
method.

The model is imported from the `.app.model.rag_pipeline` module, which is
where we wrapped the OpenAI client with Openlayer's Python SDK `OpenAIMonitor`
and decorated the methods we wanted to trace with `@tracer.trace()`.
"""

from app.model import rag_pipeline
from openlayer.lib.core.base_model import OpenlayerModel, RunReturn


class OpenAIModelInterface(OpenlayerModel):
    """Inherits from OpenlayerModel and implements the `run` method."""

    def __init__(self):
        """Make sure you import / instantiate your system here."""
        self.model = rag_pipeline.RagPipeline()

    def run(self, input_data: str) -> RunReturn:
        """Method that runs the model on a single row of the dataset
        and returns the result (a `RunReturn` object)."""
        answer = self.model.query(input_data)
        return RunReturn(output=answer, other_fields={})


if __name__ == "__main__":
    model = OpenAIModelInterface()
    model.run_from_cli()
