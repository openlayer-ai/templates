# PDF processing with LangChain

This template shows how Openlayer can be used with a project built with **LangChain** to extract structured data from a PDF. It
features Openlayer's:

- **development** mode: used to test your AI system automatically using CI / CD.
- **monitoring** mode: used to test real-time requests to your AI system in production.

## How to use this template

> Prerequisite: an [Openlayer account](https://app.openlayer.com/).

### Monitoring

1. Install the requirements and add your env vars from your [Openlayer project](https://app.openlayer.com/):

```bash
pip install -r requirements.txt
cp .env.example .env # copy your env vars over
```

2. Run the app, which serves the model on `localhost:5000`.

```bash
python app/server.py
```

Navigate to `localhost:5000` and send a few requests to the model. You should see these appear in the monitoring mode of your [Openlayer project](https://app.openlayer.com/).

Alternatively, you can run the [`openlayer_monitoring.py`](/python/llms/langchain-pdf-processing/openlayer_monitoring.py) script to simulate running your system in production, to stream your system's data and metadata to Openlayer.

### Development

1. Create a GitHub repo that is a clone of this template.

2. Navigate to the [Openlayer platform](https://app.openlayer.com/) and create a project using your repo.

Now, every commit you push to the repo will be automatically tested by Openlayer.

## How it works

Passing in Openlayer's callback handler from [Openlayer's Python SDK](https://www.openlayer.com/docs/api-reference/sdk/libraries/python) enables tracing for
every chat completion call. This is done in [`app/model/cv_extractor.py`](/python/llms/langchain-pdf-processing/app/model/cv_extractor.py), where our LLM is defined.

### Monitoring

All production requests that go through the code that uses the `OpenlayerHandler` are automatically streamed to the Openlayer platform, where our tests and alerts are defined. You just need to add your Openlayer API key and inference pipeline id as environment variables.

### Development

The [`openlayer.json`](/python/llms/langchain-pdf-processing/openlayer.json) config file and the [`openlayer_run.py`](/python/llms/langchain-pdf-processing/openlayer_run.py) script together allow Openlayer to call your AI system and discover your datasets.

With this, every new commit you push is run against your tests on Openlayer in CI / CD. You can define your tests in the app and update them as your system evolves.

Note that using the `OpenlayerHandler` enables tracing, tokens, and cost tracking in development mode as well.