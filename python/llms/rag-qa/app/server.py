"""Sample Flask app using the RAG pipeline.

The model is imported from the `model.rag_pipeline` module, which is where we wrapped
the OpenAI client with Openlayer's Python SDK `OpenAIMonitor` and decorated the methods
we wanted to trace with `@tracer.trace()`.

This sample app is based on OpenAI's original Python example: https://github.com/openai/openai-quickstart-python.
"""

from dotenv import load_dotenv
from flask import (
    Flask,
    jsonify,
    render_template,
    request,
)
from model.rag_pipeline import RagPipeline

load_dotenv(dotenv_path=".env")


model = RagPipeline()
app = Flask(__name__)

chat_history = [
    {"role": "system", "content": "You are a helpful assistant."},
]


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", chat_history=chat_history)


@app.route("/chat", methods=["POST"])
def chat():
    content = request.json["message"]
    chat_history.append({"role": "user", "content": content})
    return jsonify(success=True)


@app.route("/query", methods=["POST"])
def query():
    user_query = request.json["message"]
    assistant_response = model.query(user_query)
    chat_history.append({"role": "assistant", "content": assistant_response})
    return jsonify(success=True, message=assistant_response)


@app.route("/reset", methods=["POST"])
def reset_chat():
    global chat_history
    chat_history = [{"role": "system", "content": "You are a helpful assistant."}]
    return jsonify(success=True)


if __name__ == "__main__":
    app.run(debug=True)
