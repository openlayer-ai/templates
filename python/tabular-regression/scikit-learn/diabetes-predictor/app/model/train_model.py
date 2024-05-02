"""Script to train a scikit-learn model on the diabetes dataset
(in ../data/training.csv).

The trained model is saved to model.pkl in /model directory.

To run this script, run:
python train_model.py
"""

import pathlib
from typing import Tuple

import joblib
import pandas as pd
from sklearn import linear_model

CURRENT_DIR = pathlib.Path(__file__).parent


def load_data() -> Tuple[pd.DataFrame, pd.Series]:
    """Loads the diabetes dataset from ../data/training.csv.

    Returns the features (X) and target (y) as a tuple."""
    # Load the diabetes dataset
    data = pd.read_csv(CURRENT_DIR / "../../data/training.csv")
    X = data.drop("target", axis=1)
    y = data["target"]

    return X, y


def train_model(X: pd.DataFrame, y: pd.Series) -> None:
    """Trains a linear regression model on the data (X, y) and saves it to
    model.pkl."""
    # Train a linear regression model
    model = linear_model.LinearRegression()
    model.fit(X, y)

    # Save the model
    joblib.dump(model, CURRENT_DIR / "model.pkl")


if __name__ == "__main__":
    X, y = load_data()
    print(X.loc[0].to_dict())
    train_model(X, y)
