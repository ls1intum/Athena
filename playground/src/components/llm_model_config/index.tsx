import { OpenAILLMModelConfig, OpenAIModelConfig } from "./openai";

export type LLMModelConfig = OpenAIModelConfig;

type LLMModelConfigProps = {
  setModelConfig: (config: LLMModelConfig) => void;
};

export default function LLMModelConfig({
  setModelConfig,
}: LLMModelConfigProps) {
  return <OpenAILLMModelConfig setModelConfig={setModelConfig} />;
}
