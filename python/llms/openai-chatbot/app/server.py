"""Sample Flask app using OpenAI's GPT.

The model is imported from the `model.openai_model` module, which is where we wrapped
the OpenAI client with Openlayer's Python SDK `trace_openai` for tracing.

This sample app is based on OpenAI's original Python example: https://github.com/openai/openai-quickstart-python.
"""

from dotenv import load_dotenv
from flask import (
    Flask,
    Response,
    jsonify,
    render_template,
    request,
    stream_with_context,
)
from model.openai_model import OpenAIModel

load_dotenv(dotenv_path=".env")


model = OpenAIModel()
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


@app.route("/stream", methods=["GET"])
def stream():
    def generate():
        assistant_response_content = ""
        for chunk in model.create_chat_completion(messages=chat_history, stream=True):
            if chunk.choices[0].delta and chunk.choices[0].delta.content:
                # Accumulate the content only if it's not None
                assistant_response_content += chunk.choices[0].delta.content
                yield f"data: {chunk.choices[0].delta.content}\n\n"
            if chunk.choices[0].finish_reason == "stop":
                break  # Stop if the finish reason is 'stop'

        # Once the loop is done, append the full message to chat_history
        chat_history.append(
            {"role": "assistant", "content": assistant_response_content}
        )

    return Response(stream_with_context(generate()), mimetype="text/event-stream")


@app.route("/reset", methods=["POST"])
def reset_chat():
    global chat_history
    chat_history = [{"role": "system", "content": "You are a helpful assistant."}]
    return jsonify(success=True)


if __name__ == "__main__":
    app.run(debug=True)
