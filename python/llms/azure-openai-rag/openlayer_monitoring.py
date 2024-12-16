"""This is script that simulates running your system in production, to stream
your system's data and metadata to Openlayer.

You can fill in the values for the environment variables in the `.env` file and then
run this script.

The model is imported from the `app.model.rag_pipeline` module, which is
where we defined our model (the `RagPipeline` class, which uses Azure OpenAI).
Since the Azure OpenAI client is wrapped with Openlayer's `trace_openai` and the
important methods are decorated with `@trace()`, the calls to the model will be
traced and sent to Openlayer.
"""

from app.model import rag_pipeline
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

if __name__ == "__main__":

    question = "Who were the founders of Apple?"
    model = rag_pipeline.RagPipeline()
    answer = model.query(question)

    print(answer)
