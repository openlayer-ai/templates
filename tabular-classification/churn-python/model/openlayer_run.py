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


class SklearnModel(OpenlayerModel):
    """Inherits from OpenlayerModel and implements the `run` method."""

    def __init__(self):
        """This is where the serialized objects needed should
        be loaded as class attributes."""

        with open(PACKAGE_PATH / "model.pkl", "rb") as model_file:
            self.model = pickle.load(model_file)
        with open(PACKAGE_PATH / "encoders.pkl", "rb") as encoders_file:
            self.encoders = pickle.load(encoders_file)

    def _data_encode_one_hot(self, df: pd.DataFrame) -> pd.DataFrame:
        """Pre-processing needed for our particular use case."""

        df = df.copy(True)
        df.reset_index(drop=True, inplace=True)  # Causes NaNs otherwise
        for feature, enc in self.encoders.items():
            enc_df = pd.DataFrame(
                enc.transform(df[[feature]]).toarray(),
                columns=enc.get_feature_names_out([feature]),
            )
            df = df.join(enc_df)
            df = df.drop(columns=feature)
        return df

    def run_batch_from_df(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, dict]:
        """Function that runs the model and returns the result."""
        config = {
            "predictionScoresColumnName": "preds",
            "featureNames": [
                "CreditScore",
                "Geography",
                "Gender",
                "Age",
                "Tenure",
                "Balance",
                "NumOfProducts",
                "HasCrCard",
                "IsActiveMember",
                "EstimatedSalary",
            ],
        }
        encoded_df = self._data_encode_one_hot(df[config["featureNames"]])
        probs = self.model.predict_proba(encoded_df)
        df["preds"] = probs.tolist()
        return df, config

    def run(self, **kwargs) -> RunReturn:
        """Function that runs the model and returns the result."""
        raise NotImplementedError(
            "No need to implement this if overriding run_batch_from_df."
        )


if __name__ == "__main__":
    model = SklearnModel()
    model.run_from_cli()
