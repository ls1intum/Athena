import { useEffect, useState } from "react";

// https://platform.openai.com/docs/models/model-endpoint-compatibility
// /v1/chat/completions	gpt-4, gpt-4-0613, gpt-4-32k, gpt-4-32k-0613, gpt-3.5-turbo, gpt-3.5-turbo-0613, gpt-3.5-turbo-16k, gpt-3.5-turbo-16k-0613
// /v1/completions	text-davinci-003, text-davinci-002, text-curie-001, text-babbage-001, text-ada-001
// We have to keep it manually in sync with the OpenAI API for now

const chatModels = [
  "gpt-4",
  "gpt-4-0613",
  "gpt-4-32k",
  "gpt-4-32k-0613",
  "gpt-3.5-turbo",
  "gpt-3.5-turbo-0613",
  "gpt-3.5-turbo-16k",
  "gpt-3.5-turbo-16k-0613",
];

const textModels = [
  "text-davinci-003",
  "text-davinci-002",
  "text-curie-001",
  "text-babbage-001",
  "text-ada-001",
];

export type OpenAIModelConfig = {
  openai_api_key: string;
  temperature?: number;
  max_tokens?: number;
  top_p?: number;
  frequency_penalty?: number;
  presence_penalty?: number;
} & (OpenAI | AzureOpenAI);

type OpenAI = {
  _type: "openai";
  model_name: string;
};

type AzureOpenAI = {
  _type: "azure";
  deployment_name: string;
  openai_api_type: string;
  openai_api_base: string;
  openai_api_version: string;
};

type OpenAIConfig = {
  useAzure: boolean;
  openAIApiKey: string;
  modelName: string;
  azureOpenAIApiKey: string;
  azureOpenAIApiInstanceName: string;
  azureOpenAIApiDeploymentName: string;
  azureOpenAIApiVersion: string;
  temperature: number;
};

export function OpenAILLMModelConfig({
  setModelConfig,
}: {
  setModelConfig: (config: OpenAIModelConfig) => void;
}) {
  const [config, setConfig] = useState<OpenAIConfig>({
    useAzure: false,
    openAIApiKey: "",
    modelName: "text-davinci-003",
    azureOpenAIApiKey: "",
    azureOpenAIApiInstanceName: "ase-eu01",
    azureOpenAIApiDeploymentName: "gpt-35",
    azureOpenAIApiVersion: "2023-03-15-preview",
    temperature: 0.7,
  });

  useEffect(() => {
    const commonConfig = {
      temperature: config.temperature,
    };

    let modelConfig: OpenAIModelConfig;
    if (config.useAzure) {
      modelConfig = {
        _type: "azure",
        openai_api_key: config.azureOpenAIApiKey,
        deployment_name: config.azureOpenAIApiDeploymentName,
        openai_api_type: "azure",
        openai_api_base: `https://${config.azureOpenAIApiInstanceName}.openai.azure.com/`,
        openai_api_version: config.azureOpenAIApiVersion,
        ...commonConfig,
      };
    } else {
      modelConfig = {
        _type: "openai",
        openai_api_key: config.openAIApiKey,
        model_name: config.modelName,
        ...commonConfig,
      };
    }
    setModelConfig(modelConfig);
  }, [config, setModelConfig]);

  return (
    <div className="flex flex-col space-y-1">
      <label className="flex items-center cursor-pointer">
        <input
          type="checkbox"
          checked={config.useAzure}
          onChange={(e) => setConfig({ ...config, useAzure: e.target.checked })}
        />
        <div className="ml-2 text-gray-700 font-normal">Use Azure</div>
      </label>
      {config.useAzure ? (
        <>
          <label className="flex flex-col">
            <span className="text-md font-medium">Azure OpenAI API Key</span>
            <input
              className="border border-gray-300 rounded-md px-2 py-1"
              value={config.azureOpenAIApiKey}
              onChange={(e) =>
                setConfig({ ...config, azureOpenAIApiKey: e.target.value })
              }
              placeholder="..."
            />
          </label>
          <label className="flex flex-col">
            <span className="text-md font-medium">Azure Instance Name</span>
            <input
              className="border border-gray-300 rounded-md px-2 py-1"
              value={config.azureOpenAIApiInstanceName}
              onChange={(e) =>
                setConfig({
                  ...config,
                  azureOpenAIApiInstanceName: e.target.value,
                })
              }
              placeholder="ase-eu01"
            />
          </label>
          <label className="flex flex-col">
            <span className="text-md font-medium">Azure Deployment Name</span>
            <input
              className="border border-gray-300 rounded-md px-2 py-1"
              value={config.azureOpenAIApiDeploymentName}
              onChange={(e) =>
                setConfig({
                  ...config,
                  azureOpenAIApiDeploymentName: e.target.value,
                })
              }
              placeholder="gpt-35"
            />
          </label>
        </>
      ) : (
        <>
          <label className="flex flex-col">
            <span className="text-md font-medium">OpenAI API Key</span>
            <input
              className="border border-gray-300 rounded-md px-2 py-1"
              value={config.openAIApiKey}
              onChange={(e) =>
                setConfig({ ...config, openAIApiKey: e.target.value })
              }
              placeholder="sk-..."
            />
          </label>
          <label className="flex flex-col">
            <span className="text-md font-medium">Model Name</span>
            <select
              className="border border-gray-300 rounded-md px-2 py-1"
              value={config.modelName}
              onChange={(e) =>
                setConfig({ ...config, modelName: e.target.value })
              }
            >
              <optgroup label="Chat Models">
                {chatModels.map((model) => (
                  <option key={model} value={model}>
                    {model}
                  </option>
                ))}
              </optgroup>
              <optgroup label="Text Models">
                {textModels.map((model) => (
                  <option key={model} value={model}>
                    {model}
                  </option>
                ))}
              </optgroup>
            </select>
          </label>
        </>
      )}
      <div className="flex flex-col max-w-xs">
        <div className="flex items-center justify-between">
          <span className="text-md font-medium">Temperature</span>
          <input
            type="number"
            min="0"
            max="2"
            step="0.01"
            className="rounded-md text-right hover:border hover:border-gray-300 w-20 h-8 px-2 duration-100 ease-in-out [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
            value={config.temperature}
            onChange={(e) =>
              setConfig({ ...config, temperature: Number(e.target.value) })
            }
          />
        </div>
        <div className="w-full pr-2">
          <input
            type="range"
            min="0"
            max="2"
            step="0.01"
            className="slider rounded-full w-full bg-gray-300"
            value={config.temperature}
            onChange={(e) =>
              setConfig({ ...config, temperature: Number(e.target.value) })
            }
          />
        </div>
      </div>
    </div>
  );
}
