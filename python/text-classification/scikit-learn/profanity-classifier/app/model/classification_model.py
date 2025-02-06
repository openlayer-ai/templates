import pathlib

import joblib
import pandas as pd
from sentence_transformers import SentenceTransformer


encode_model = SentenceTransformer("all-MiniLM-L6-v2")

CURRENT_DIR = pathlib.Path(__file__).parent


class ClassificationModel:
    def __init__(self):
        if not CURRENT_DIR.joinpath("model.pkl").exists():
            raise FileNotFoundError(
                "model.pkl not found. Run the `train_model.py`"
                " script first to train and save the model and encoders."
            )
        self.model = joblib.load(CURRENT_DIR / "model.pkl")

    def predict_proba(self, df: pd.DataFrame) -> pd.DataFrame:
        """Function that runs the model and returns the class probabilities."""
        X = encode_model.encode(df["text"])
        return self.model.predict_proba(X)
