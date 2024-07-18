# Tabular classification (no model) template

This template shows how to set up Openlayer with a project built around a **tabular classification model**. It demonstrates
how to only upload datasets to Openlayer.

## How to use this template

> Prerequisite: an [Openlayer account](https://app.openlayer.com/).

1. Create a GitHub repo that is a clone of this template.

2. Navigate to the [Openlayer platform](https://app.openlayer.com/) and create a project using your repo.

Now, every commit you push to the repo will be automatically tested by Openlayer.

## How it works

The [`openlayer.json`](/python/tabular-classification/no-model/churn-predictor/openlayer.json) config file allows Openlayer to discover your datasets.

Typically, datasets only have the inputs that run through the model. The outputs are generated using [openlayer batch](https://docs.openlayer.com/development/configuring-output-generation). In this case, however, we show how you can include the outputs in your datasets in case you don't want to use Openlayer to generate outputs.
