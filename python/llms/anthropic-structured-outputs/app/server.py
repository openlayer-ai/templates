from flask import Flask, render_template, request, jsonify
from model import review_extractor
from dotenv import load_dotenv


load_dotenv(dotenv_path=".env")

app = Flask(__name__)
model = review_extractor.ReviewExtractorModel()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        review_text = request.form["review_text"]
        structured_data = model.extract(review_text)
        return jsonify(structured_data.model_dump())
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
