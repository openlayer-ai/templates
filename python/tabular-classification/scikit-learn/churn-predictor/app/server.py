import json
import os

import numpy as np

import openlayer
import pandas as pd
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from openlayer import tasks
from model.classification_model import ClassificationModel

load_dotenv(dotenv_path=".env")

client = openlayer.OpenlayerClient(api_key=os.environ.get("OPENLAYER_API_KEY"))
project = client.create_project(
    name=os.environ.get("OPENLAYER_PROJECT_NAME", "churn-predictor"),
    task_type=tasks.TaskType.TabularClassification,
)
inference_pipeline = project.create_inference_pipeline(
    name=os.environ.get("OPENLAYER_INFERENCE_PIPELINE_NAME", "production")
)

app = Flask(__name__)

# Load the model
model = ClassificationModel()


@app.route("/", methods=["GET"])
def home():
    default_input = {
        "CreditScore": 667,
        "Geography": "Spain",
        "Gender": "Female",
        "Age": 34,
        "Tenure": 5,
        "Balance": 0.0,
        "NumOfProducts": 2,
        "HasCrCard": 1,
        "IsActiveMember": 0,
        "EstimatedSalary": 163830.64,
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
        prediction = np.argmax(model.predict_proba(df))

        # Stream the data to Openlayer
        class_names = ["Retained", "Exited"]
        data = {**input_dict, "prediction": prediction}
        config = {
            "classNames": class_names,
            "featureNames": list(input_dict.keys()),
            "categoricalFeatureNames": ["Geography", "Gender"],
            "predictionsColumnName": "prediction",
        }
        inference_pipeline.stream_data(stream_data=data, stream_config=config)

        # Return the prediction
        return render_template(
            "index.html", request_body=input_json, prediction=class_names[prediction]
        )

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(debug=True)
