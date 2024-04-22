// src/models/myModel.ts
import { RunReturn } from "../openlayer-ts/utils";
import { OpenAIMonitor } from 'openlayer';
import { ChatCompletion } from 'openai/resources';

export class MyModel {
    private openaiApiKey: string;
    private openlayerApiKey: string;
    private monitor: OpenAIMonitor;

    constructor() {
        this.openaiApiKey = process.env["OPENAI_API_KEY"] || "";
        this.openlayerApiKey = process.env["OPENLAYER_API_KEY"] || "";
        this.monitor = new OpenAIMonitor({
            openAiApiKey: this.openaiApiKey,
            openlayerApiKey: this.openlayerApiKey,
            // specify an existing inference pipeline ID
            openlayerInferencePipelineId: 'YOUR_OPENLAYER_INFERENCE_PIPELINE_ID',
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
                  role: 'user',
                },
              ],
              model: 'gpt-3.5-turbo',
            },
            undefined,
          );
        const result = (response as ChatCompletion).choices[0].message.content;
        return { output: result, otherFields: { model: 'gpt-3.5-turbo' } };
    }
}
