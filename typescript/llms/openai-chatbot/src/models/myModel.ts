// src/models/myModel.ts
import { ChatCompletion } from "openai/resources";
import Openlayer from "openlayer";
import { RunReturn } from "openlayer/lib/core/cli";
import OpenAIMonitor from "openlayer/lib/core/openai-monitor";

export class MyModel {
  private openaiApiKey: string;
  private openlayerApiKey: string;
  private monitor: OpenAIMonitor;

  constructor() {
    this.openaiApiKey = process.env["OPENAI_API_KEY"] || "";
    this.openlayerApiKey = process.env["OPENLAYER_API_KEY"] || "";

    const openlayerClient = new Openlayer({ apiKey: this.openlayerApiKey });

    this.monitor = new OpenAIMonitor({
      openAiApiKey: this.openaiApiKey,
      openlayerClient,
      openlayerInferencePipelineId: '',
    });
  }

  async run({ userQuery }: { userQuery: string }): Promise<RunReturn> {
    // Implement the model run logic here
    console.log(`Processing query: ${userQuery}`);
    const response = await this.monitor.createChatCompletion(
      {
        messages: [
          {
            content: userQuery,
            role: "user",
          },
        ],
        model: "gpt-3.5-turbo",
      },
      undefined
    );
    const result = (response as ChatCompletion).choices[0].message.content;
    return { output: result, otherFields: { model: "gpt-3.5-turbo" } };
  }
}
