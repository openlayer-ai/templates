// src/models/myModel.ts
// Make sure to set the following env vars when using this model:
// OPENAI_API_KEY
// OPENLAYER_API_KEY
// OPENLAYER_INFERENCE_PIPELINE_ID

import { ChatCompletion } from "openai/resources";
import { RunReturn } from "openlayer/lib/core/cli";
import OpenAI from "openai";
import { traceOpenAI } from "openlayer/lib/integrations/openAiTracer";

export class MyModel {
  private client: OpenAI;

  constructor() {
    this.client = traceOpenAI(new OpenAI());
  }

  async run({ userQuery }: { userQuery: string }): Promise<RunReturn> {
    // Implement the model run logic here
    console.log(`Processing query: ${userQuery}`);
    const response = await this.client.chat.completions.create(
      {
        messages: [
          {
            content: userQuery,
            role: "user",
          },
        ],
        model: "gpt-4o",
      },
      undefined
    );
    const result = (response as ChatCompletion).choices[0].message.content;
    return { output: result, otherFields: { model: "gpt-4o" } };
  }
}
