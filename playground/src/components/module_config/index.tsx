import { Dispatch, SetStateAction } from "react";
import useSWR from "swr";

import { ModuleMeta } from "@/model/health_response";
import baseUrl from "@/helpers/base_url";

import ModuleExampleConfig from "./module_example";

type SetConfig = Dispatch<SetStateAction<any | undefined>>;

export type ModuleConfigProps = {
  moduleConfig: any | undefined;
  onChangeConfig: SetConfig;
};

type Modules = "module_example";

const moduleConfigComponents: {
  [key in Modules]: React.FC<ModuleConfigProps>;
} = {
  module_example: ModuleExampleConfig,
};

export function moduleConfigSelectorExists(moduleName: string): boolean {
  return Object.keys(moduleConfigComponents).includes(moduleName);
}

type Props = ModuleConfigProps & {
  module: ModuleMeta;
  athenaUrl: string;
  athenaSecret: string;
};

export default function ModuleConfig({
  moduleConfig,
  onChangeConfig,
  module,
  athenaUrl,
  athenaSecret,
}: Props) {
  const athenaFetcher = (url: string) => {
    fetch(
      `${baseUrl}/api/athena_request?${new URLSearchParams({
        url: url,
      })}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "X-API-Secret": athenaSecret,
        },
      }
    ).then((res) => {
      console.log("Hello")
      return res.json()
    });
  };

  const selectorExists = moduleConfigSelectorExists(module.name);
  const { data, error, isLoading } = useSWR(
    selectorExists
      ? `${athenaUrl}/modules/${module.type}/${module.name}/config`
      : null,
    athenaFetcher
  );

  if (!selectorExists) {
    return (
      <p className="text-gray-500">
        Module config selector for{" "}
        <code className="bg-gray-100 p-1 rounded-sm">{module.name}</code> is not
        implemented.
      </p>
    );
  }

  const SelectedModule = moduleConfigComponents[module.name as Modules];
  return (
    <>
      <SelectedModule
        moduleConfig={moduleConfig}
        onChangeConfig={onChangeConfig}
      />
      <div className="bg-white rounded-md p-4 mb-8">
        Test
        {"isLoading: " + isLoading}
        {"error: " + error}
        {"data: " + data}
      </div>
    </>
  );
}
