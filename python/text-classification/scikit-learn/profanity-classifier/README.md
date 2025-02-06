# Text classification (scikit-learn) template

This template shows how to set up Openlayer with a project built around a **text classification model in Python (scikit-learn)**. It
features Openlayer's:

- **development** mode: used to test your model automatically using CI / CD.
- **monitoring** mode: used to test real-time requests to your model in production.

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

### Development

1. Create a GitHub repo that is a clone of this template.

2. Navigate to the [Openlayer platform](https://app.openlayer.com/) and create a project using your repo.

Now, every commit you push to the repo will be automatically tested by Openlayer.

## How it works

The text classification model is trained in the script [`app/model/train_model.py`](/python/text-classification/scikit-learn/profanity-classifier/app/model/train_model.py). At the end of the training, the model is saved as the `model.pkl` file in the [`app/model`](/python/text-classification/scikit-learn/profanity-classifier/app/model) directory.

### Monitoring

All the production requests made to the `/predict` endpoint are streamed to Openlayer (see [`app/server.py`](/python/text-classification/scikit-learn/profanity-classifier/app/server.py)). The data streaming is done with the `stream` method from [Openlayer's Python SDK](https://www.openlayer.com/docs/api-reference/rest/monitoring/stream-data).

### Development

The [`openlayer.json`](/python/text-classification/scikit-learn/profanity-classifier/openlayer.json) config file and the [`openlayer_run.py`](/python/text-classification/scikit-learn/profanity-classifier/app/model/openlayer_run.py) script together allow Openlayer to call your AI system and discover your datasets.

With this, every new commit you push is run against your tests on Openlayer in CI / CD. You can define your tests in the app and update them as your system evolves.

