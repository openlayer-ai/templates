"""This file is used by Openlayer to run the model and get its outputs.

If you go to openlayer.json, you'll see that the `batchCommand` field points here.

The openlayer_run.py must contain 2 things:

1. A class that inherits from OpenlayerModel and implements the `run` method.
2. A `__main__` block that creates an instance of the class and calls the `run_from_cli`
method.

The model is imported from the `.app.model.langchain_model` module, which is
where we used Openlayer's callback handler, for tracing.
"""

from app.model import langchain_model
from openlayer.lib.core.base_model import OpenlayerModel, RunReturn


class LangChainModelInterface(OpenlayerModel):
    """Inherits from OpenlayerModel and implements the `run` method."""

    def __init__(self):
        """Make sure you import / instantiate your system here."""
        self.model = langchain_model.LangChainModel()

    def run(
        self,
        input_data: str,
    ) -> RunReturn:
        """Method that runs the model on a single row of the dataset
        and returns the result (a `RunReturn` object)."""
        output = self.model.invoke(message=input_data)
        return RunReturn(output=output, other_fields={})


if __name__ == "__main__":
    model = LangChainModelInterface()
    model.run_from_cli()
