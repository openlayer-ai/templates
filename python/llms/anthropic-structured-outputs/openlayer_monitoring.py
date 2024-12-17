"""This is script that simulates running your system in production, to stream
your system's data and metadata to Openlayer.

You can fill in the values for the environment variables in the `.env` file and then
run this script.

The model is imported from the `app.model.review_extractor` module, which is
where we defined our model (the `ReviewExtractorModel` class, which uses Anthropic's
Claude). Since the Anthropic client is wrapped with Openlayer's `trace_anthropic`,
the calls to the model will be traced and sent to Openlayer.
"""

import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

# Check for required environment variables and prompt if missing
required_env_vars = {
    "OPENLAYER_API_KEY": "Enter your Openlayer API key: ",
    "ANTHROPIC_API_KEY": "Enter your Anthropic API key: ",
    "OPENLAYER_INFERENCE_PIPELINE_ID": "Enter your Openlayer inference pipeline ID: ",
}

for var, prompt in required_env_vars.items():
    if not os.getenv(var):
        value = input(prompt)
        os.environ[var] = value

from app.model import review_extractor

if __name__ == "__main__":

    review_text = """This tablet has a nice display, and it's lightweight and easy
    to hold for extended periods. However, I find the price too high for the features
    it offers. It's good, but not great."""
    model = review_extractor.ReviewExtractorModel()
    structured_data = model.extract(review_text)

    print(structured_data.model_dump())
