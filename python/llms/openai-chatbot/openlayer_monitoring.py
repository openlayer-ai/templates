"""This is script that simulates running your system in production, to stream
your system's data and metadata to Openlayer.

You can fill in the values for the environment variables in the `.env` file and then
run this script.

The model is imported from the `app.model.openai_model` module, which is
where we defined our model (the `OpenAIModel` class).
Since the OpenAI client is wrapped with Openlayer's `trace_openai` function, all model
calls will be traced and data will be sent to Openlayer.
"""

import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

# Check for required environment variables and prompt if missing
required_env_vars = {
    "OPENLAYER_API_KEY": "Enter your Openlayer API key: ",
    "OPENAI_API_KEY": "Enter your OpenAI API key: ",
    "OPENLAYER_INFERENCE_PIPELINE_ID": "Enter your Openlayer inference pipeline ID: ",
}

for var, prompt in required_env_vars.items():
    if not os.getenv(var):
        value = input(prompt)
        os.environ[var] = value

from app.model import openai_model

if __name__ == "__main__":

    model = openai_model.OpenAIModel()
    output = model.create_chat_completion(
        messages=[{"role": "user", "content": "How is the weather today?!"}]
    )

    print(output)
