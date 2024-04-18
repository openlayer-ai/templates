"""This file is used by Openlayer to run the model and get its outputs.

If you go to openlayer.json, you'll see that the `batchCommand` field points here.

The openlayer_run.py must contain 2 things:

1. A class that inherits from OpenlayerModel and implements the `run_batch_from_df`
    method.
2. A `__main__` block that creates an instance of the class and calls the `run_from_cli`
method.
"""

import pickle
from pathlib import Path
from typing import Tuple

import pandas as pd
from openlayer.model_runners.base_model import OpenlayerModel, RunReturn

PACKAGE_PATH = Path(__file__).parent


class MyModel(OpenlayerModel):
    """Inherits from OpenlayerModel and implements the `run` method."""

    def __init__(self):
        """This is where the serialized objects needed should
        be loaded as class attributes."""

        with open(PACKAGE_PATH / "model.pkl", "rb") as model_file:
            self.model = pickle.load(model_file)

    def run_batch_from_df(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, dict]:
        """Function that runs the model and returns the result."""
        config = {
            "predictionsColumnName": "preds",
            "featureNames": [
                "age",
                "sex",
                "bmi",
                "bp",
                "s1",
                "s2",
                "s3",
                "s4",
                "s5",
                "s6",
            ],
            "categoricalFeatureNames": [],
        }
        probs = self.model.predict(df[config["featureNames"]])
        df["preds"] = probs.tolist()
        return df, config

    def run(self, **kwargs) -> RunReturn:
        """Function that runs the model and returns the result."""
        raise NotImplementedError(
            "No need to implement this if overriding run_batch_from_df."
        )


if __name__ == "__main__":
    model = MyModel()
    model.run_from_cli()
