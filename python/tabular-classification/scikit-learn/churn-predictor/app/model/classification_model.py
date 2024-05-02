import pathlib

import joblib
import pandas as pd

CURRENT_DIR = pathlib.Path(__file__).parent


class ClassificationModel:
    def __init__(self):
        if (
            not CURRENT_DIR.joinpath("model.pkl").exists()
            or not CURRENT_DIR.joinpath("encoders.pkl").exists()
        ):
            raise FileNotFoundError(
                "model.pkl or encoders.pkl not found. Run the `train_model.py`"
                " script first to train and save the model and encoders."
            )
        self.model = joblib.load(CURRENT_DIR / "model.pkl")
        self.encoders = joblib.load(CURRENT_DIR / "encoders.pkl")

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

    def predict_proba(self, df: pd.DataFrame) -> pd.DataFrame:
        """Function that runs the model and returns the class probabilities."""
        df = self._data_encode_one_hot(df)
        return self.model.predict_proba(df)
