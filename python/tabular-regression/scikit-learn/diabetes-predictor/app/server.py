import json
import os
import pathlib

import joblib
import pandas as pd
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from openlayer import Openlayer
from openlayer.types.inference_pipelines import data_stream_params

load_dotenv(dotenv_path=".env")


app = Flask(__name__)

# Load the model
CURRENT_DIR = pathlib.Path(__file__).parent
model = joblib.load(CURRENT_DIR / "model/model.pkl")


@app.route("/", methods=["GET"])
def home():
    default_input = {
        "age": 0.012648137276287,
        "sex": 0.0506801187398186,
        "bmi": 0.0024165424552393,
        "bp": 0.0563008952725293,
        "s1": 0.0273260502020122,
        "s2": 0.0171618818193638,
        "s3": 0.0412768238419747,
        "s4": -0.0394933828740932,
        "s5": 0.0037090603325595,
        "s6": 0.0734802269665542,
    }
    return render_template(
        "index.html", request_body=json.dumps(default_input), prediction=None
    )


@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Run the model
        input_json = request.form["request_body"]
        input_dict = json.loads(input_json)
        df = pd.DataFrame([input_dict])
        prediction = model.predict(df)

        # Stream the data to Openlayer
        rows = {**input_dict, "prediction": prediction[0]}
        config = data_stream_params.ConfigTabularRegressionData(
            feature_names=list(input_dict.keys()), predictions_column_name="prediction"
        )
        client = Openlayer()
        client.inference_pipelines.data.stream(
            inference_pipeline_id=os.environ.get("OPENLAYER_INFERENCE_PIPELINE_ID"),
            rows=rows,
            config=config,
        )

        # Return the prediction
        return render_template(
            "index.html", request_body=input_json, prediction=prediction[0]
        )

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(debug=True)
