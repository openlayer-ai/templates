import json
import os

import numpy as np
import pandas as pd
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from model.classification_model import ClassificationModel
from openlayer import Openlayer
from openlayer.types.inference_pipelines import data_stream_params

load_dotenv(dotenv_path=".env")

app = Flask(__name__)

# Load the model
model = ClassificationModel()


@app.route("/", methods=["GET"])
def home():
    default_input = {"text": "hello world"}
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
        prediction_scores = model.predict_proba(df).tolist()
        prediction = int(np.argmax(prediction_scores))

        # Stream the data to Openlayer
        class_names = ["Yes", "No"]
        rows = [
            {
                **input_dict,
                "prediction": prediction,
                "prediction_scores": prediction_scores[0],
            }
        ]
        config = data_stream_params.ConfigTextClassificationData(
            class_names=class_names,
            text_column_name="text",
            prediction_scores_column_name="prediction_scores",
        )

        client = Openlayer()
        client.inference_pipelines.data.stream(
            inference_pipeline_id=os.environ.get("OPENLAYER_INFERENCE_PIPELINE_ID"),
            rows=rows,
            config=config,
        )

        # Return the prediction
        return render_template(
            "index.html", request_body=input_json, prediction=class_names[prediction]
        )

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(debug=True)
