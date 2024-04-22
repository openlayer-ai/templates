# OpenAI + Openlayer (TypeScript)

This template shows how to set up Openlayer with a project built with **OpenAI using TypeScript**. It
features Openlayer's:

- **development** mode: used to test your AI system automatically using CI / CD.

## How to use this template

> Prerequisite: an [Openlayer account](https://app.openlayer.com/).

### Development

1. Create a GitHub repo that is a clone of this template.

2. Navigate to the [Openlayer platform](https://app.openlayer.com/) and create a project using your repo.

Now, every commit you push to the repo will be automatically tested by Openlayer.

## How it works

We call OpenAI's `createChatCompletion` method by using the `OpenAIMonitor` from [Openlayer's TypeScript SDK](https://github.com/openlayer-ai/openlayer-ts). This enables tracing for
every chat completion call. You can find the code in [`src/models/myModel.ts`](/typescript/llms/openai-chatbot/src/models/myModel.ts), where our LLM is defined.

### Monitoring

All production requests that go through the code wrapped with the `OpenAIMonitor` are automatically streamed to the Openlayer platform, where our tests and alerts are defined. You just need to add your Openlayer API key and project name as environment variables.

### Development

The [`openlayer.json`](/typescript/llms/openai-chatbot/openlayer.json) config file and the [`src/run.ts`](/typescript/llms/openai-chatbot/src/run.ts) script together allow Openlayer to call your AI system and discover your datasets.

With this, every new commit you push is run against your tests on Openlayer in CI / CD. You can define your tests in the app and update them as your system evolves.
