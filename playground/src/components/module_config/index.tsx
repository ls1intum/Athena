import { Dispatch, SetStateAction, useEffect, useRef, useState } from "react";
import useSWR from "swr";
import validator from "@rjsf/validator-ajv8";
import { UIOptionsType, WidgetProps, getDefaultFormState } from "@rjsf/utils";

import { ModuleMeta } from "@/model/health_response";

import DefaultSchemaFormModuleConfig from "./default_schema_form";
import ModuleLLMConfig from "./module_llm";
import athenaFetcher from "@/helpers/athena_fetcher";

// Add custom module config components here
type CustomModuleConfig = "module_text_llm";
const customModuleConfigComponents: {
  [key in CustomModuleConfig]: React.FC<ModuleConfigProps>;
} = {
  module_text_llm: ModuleLLMConfig,
};

type SetConfig = Dispatch<SetStateAction<any | undefined>>;

export type ModuleConfigProps = {
  configOptions?: any;
  moduleConfig: any | undefined;
  onChangeConfig: SetConfig;
};

type ModuleConfigWrapperProps = ModuleConfigProps & {
  module: ModuleMeta;
  athenaUrl: string;
  athenaSecret: string;
};

export default function ModuleConfigWrapper({
  moduleConfig,
  onChangeConfig,
  module,
  athenaUrl,
  athenaSecret,
}: ModuleConfigWrapperProps) {
  const hasCustomModuleConfigComponent =
    module.name in customModuleConfigComponents;
  const CustomModuleConfigComponent =
    customModuleConfigComponents[module.name as CustomModuleConfig];

  const [formKey, setFormKey] = useState(0);
  const { data, error, isLoading } = useSWR(
    `${athenaUrl}/modules/${module.type}/${module.name}/config_schema`,
    athenaFetcher(athenaSecret)
  );

  useEffect(() => {
    if (data) {
      const defaultFormData = getDefaultFormState(validator, data, {}, data);
      if (
        Object.keys(moduleConfig).length === 0 &&
        Object.keys(defaultFormData).length !== 0
      ) {
        onChangeConfig(defaultFormData);
        setFormKey(formKey + 1);
      }
    }
  }, [data, formKey, moduleConfig, onChangeConfig]);

  return (
    <>
      {isLoading && <p>Loading...</p>}
      {error &&
        (error.status !== 404 ? (
          <p className="text-red-500">
            Failed to get config options from Athena
          </p>
        ) : (
          <p className="text-gray-500">
            No config options available, not implemented in the module
          </p>
        ))}
      {data &&
        (hasCustomModuleConfigComponent ? (
          <CustomModuleConfigComponent
            configOptions={data.data}
            moduleConfig={moduleConfig}
            onChangeConfig={onChangeConfig}
          />
        ) : (
          <DefaultSchemaFormModuleConfig
            configOptions={data.data}
            moduleConfig={moduleConfig}
            onChangeConfig={onChangeConfig}
          />
        ))}
    </>
  );
}
