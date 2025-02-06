"""Script to train a scikit-learn model on a profanity classification dataset
(in ../data/training.csv).

The encoder and trained model are saved to encoders.pkl and model.pkl in /model
directory.

To run this script, run:
python train_model.py
"""

import pathlib
from typing import Tuple

import joblib
import pandas as pd
from sklearn.ensemble import AdaBoostClassifier
from sentence_transformers import SentenceTransformer


encode_model = SentenceTransformer("all-MiniLM-L6-v2")

CURRENT_DIR = pathlib.Path(__file__).parent


def load_data() -> Tuple[pd.DataFrame, pd.Series]:
    """Loads the dataset from ../data/training.csv.

    Returns the features (X) and label (y) as a tuple."""
    # Load the  dataset
    data = pd.read_csv(CURRENT_DIR / "../../data/training.csv")
    X = encode_model.encode(data["text"])
    y = data["actual_target"]
    return X, y


def train_model(X: pd.DataFrame, y: pd.Series) -> None:
    """Trains a text classification model on the data (X, y) and saves it to
    model.pkl."""
    # Train a text classification model
    model = AdaBoostClassifier(n_estimators=100, random_state=0).fit(X, y)

    # Save the model
    joblib.dump(model, CURRENT_DIR / "model.pkl")


if __name__ == "__main__":
    X, y = load_data()
    train_model(X, y)
