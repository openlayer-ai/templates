"""This file is used by Openlayer to run the model and get its outputs.

If you go to openlayer.json, you'll see that the `batchCommand` field points here.

The openlayer_run.py must contain 2 things:

1. A class that inherits from OpenlayerModel and implements the `run` method.
2. A `__main__` block that creates an instance of the class and calls the `run_from_cli`
method.

The model is imported from the `.app.model.review_extractor` module, which is
where we defined our model (the `ReviewExtractorModel` class, which uses Anthropic's
Claude).
"""

from openlayer.lib.core.base_model import OpenlayerModel, RunReturn

from app.model import cv_extractor


class CVExtractorModelInterface(OpenlayerModel):
    """Inherits from OpenlayerModel and implements the `run` method."""

    def __init__(self):
        """Make sure you import / instantiate your system here."""
        self.model = cv_extractor.CVExtractorModel()

    def run(
        self,
        file_dir: str,
    ) -> RunReturn:
        """Method that runs the model on a single row of the dataset
        and returns the result (a `RunReturn` object)."""
        response: cv_extractor.CVStructuredData = self.model.extract(file_dir=file_dir)
        output = response.json()
        return RunReturn(output=output, other_fields={})


if __name__ == "__main__":
    model = CVExtractorModelInterface()
    model.run_from_cli()
