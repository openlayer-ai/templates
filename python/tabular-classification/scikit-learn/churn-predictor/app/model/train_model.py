"""Script to train a scikit-learn model on the churn dataset
(in ../data/training.csv).

The encoder and trained model are saved to encoders.pkl and model.pkl in /model
directory.

To run this script, run:
python train_model.py
"""

import pathlib
from typing import List, Tuple

import joblib
import pandas as pd
from sklearn import linear_model
from sklearn.preprocessing import OneHotEncoder

CURRENT_DIR = pathlib.Path(__file__).parent


def load_data() -> Tuple[pd.DataFrame, pd.Series]:
    """Loads the churn dataset from ../data/training.csv.

    Returns the features (X) and label (y) as a tuple."""
    # Load the churn dataset
    data = pd.read_csv(CURRENT_DIR / "../../data/training.csv")
    X = data.drop("churn", axis=1)
    y = data["churn"]

    return X, y


def create_encoders_dict(df: pd.DataFrame, categorical_feature_names: List[str]):
    """Creates encoders for each of the categorical features.
    The predict function will need these encoders.
    """
    encoders_dict = {}
    for feature in categorical_feature_names:
        enc = OneHotEncoder(handle_unknown="ignore")
        enc.fit(df[[feature]])
        encoders_dict[feature] = enc

    # Save the encoders
    joblib.dump(encoders_dict, CURRENT_DIR / "encoders.pkl")

    return encoders_dict


def data_encode_one_hot(df: pd.DataFrame, encoders_dict) -> pd.DataFrame:
    """Encodes categorical features using one-hot encoding."""
    df = df.copy(True)
    df.reset_index(drop=True, inplace=True)  # Causes NaNs otherwise
    for feature, enc in encoders_dict.items():
        enc_df = pd.DataFrame(
            enc.transform(df[[feature]]).toarray(),
            columns=enc.get_feature_names_out([feature]),
        )
        df = df.join(enc_df)
        df = df.drop(columns=feature)
    return df


def train_model(X: pd.DataFrame, y: pd.Series) -> None:
    """Trains a logistic regression  model on the data (X, y) and saves it to
    model.pkl."""
    # Train a linear regression model
    model = linear_model.LogisticRegression(random_state=1300, solver="liblinear")
    model.fit(X, y)

    # Save the model
    joblib.dump(model, CURRENT_DIR / "model.pkl")


if __name__ == "__main__":
    X, y = load_data()
    encoders = create_encoders_dict(X, ["Geography", "Gender"])
    X_enc_one_hot = data_encode_one_hot(X, encoders)
    train_model(X_enc_one_hot, y)
