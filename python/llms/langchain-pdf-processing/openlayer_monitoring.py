"""This is script that simulates running your system in production, to stream
your system's data and metadata to Openlayer.

You can fill in the values for the environment variables in the `.env` file and then
run this script.

The model is imported from the `app.model.cv_extractor` module, which is
where we defined our model (the `CVExtractorModel` class, which uses LangChain).
Since the Openlayer callback handler is passed to the model and all relevant functions
are decorated with `@trace()`, the model will be traced and data will be sent to
Openlayer.
"""

from app.model import cv_extractor
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

if __name__ == "__main__":

    model = cv_extractor.CVExtractorModel()
    output = model.extract("./data/cv_1.pdf")

    print(output)
