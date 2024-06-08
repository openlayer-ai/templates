"""Sample Flask app using an LLM with LangChain.

The model is imported from the `model.langchain_model` module, which is where we used
the Openlayer callback handler.

This sample app is based on OpenAI's original Python example: https://github.com/openai/openai-quickstart-python.
"""

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from model.langchain_model import LangChainModel

load_dotenv(dotenv_path=".env")


model = LangChainModel()
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
    assistant_response = model.invoke(user_query)
    chat_history.append({"role": "assistant", "content": assistant_response})
    return jsonify(success=True, message=assistant_response)


@app.route("/reset", methods=["POST"])
def reset_chat():
    global chat_history
    chat_history = [{"role": "system", "content": "You are a helpful assistant."}]
    return jsonify(success=True)


if __name__ == "__main__":
    app.run(debug=True)
