import os
import uuid

from dotenv import load_dotenv
from flask import Flask, render_template, request, send_file
from model import cv_extractor

load_dotenv(dotenv_path=".env")

app = Flask(__name__)
model = cv_extractor.CVExtractorModel()

# Folder to store uploaded files temporarily
UPLOAD_FOLDER = "./uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create the uploads folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def process_cv(pdf_path):
    return model.extract(pdf_path).dict()


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # Check if a file was uploaded
        if "file" in request.files:
            file = request.files["file"]
            if file.filename != "":
                # Save the file with a unique name
                filename = str(uuid.uuid4()) + ".pdf"
                file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(file_path)

                # Process the uploaded CV
                cv_details = process_cv(file_path)

                return render_template("result.html", **cv_details, filename=filename)

        # If a sample CV was selected
        if "sample_cv" in request.form:
            sample_cv = request.form["sample_cv"]

            # Process the selected sample CV
            cv_details = process_cv(sample_cv)

            return render_template("result.html", **cv_details, filename=sample_cv)

    return render_template("upload.html")


@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    if not os.path.exists(file_path):
        return "File not found", 404

    return send_file(
        file_path,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=filename,
    )


if __name__ == "__main__":
    app.run(debug=True)
