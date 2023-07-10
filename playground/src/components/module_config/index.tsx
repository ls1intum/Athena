import { Dispatch, SetStateAction, useEffect, useRef, useState } from "react";
import useSWR from "swr";
import validator from "@rjsf/validator-ajv8";

import { ModuleMeta } from "@/model/health_response";
import baseUrl from "@/helpers/base_url";

import ModuleExampleConfig from "./module_example";
import Form, { getUISchema } from "@/components/form";
import { UIOptionsType, getDefaultFormState } from "@rjsf/utils";

type SetConfig = Dispatch<SetStateAction<any | undefined>>;

export type ModuleConfigProps = {
  configOptions?: any;
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
  // return Object.keys(moduleConfigComponents).includes(moduleName);
  return true;
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
  const athenaFetcher = (url: string) =>
    fetch(
      `${baseUrl}/api/athena_request?${new URLSearchParams({
        url: url,
      })}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "X-API-Secret": athenaSecret,
          // No X-Module-Config here
        },
      }
    ).then((res) =>
      res.json().then((data) => {
        if (res.status !== 200) {
          throw new Error(data);
        }
        return data.data;
      })
    );

  const selectorExists = moduleConfigSelectorExists(module.name);
  const { data, error, isLoading } = useSWR(
    selectorExists
      ? `${athenaUrl}/modules/${module.type}/${module.name}/config_schema`
      : null,
    athenaFetcher
  );

  const [formKey, setFormKey] = useState(0);

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

  // if (!selectorExists) {
  //   return (
  //     <p className="text-gray-500">
  //       Module config selector for{" "}
  //       <code className="bg-gray-100 p-1 rounded-sm">{module.name}</code> is not
  //       implemented.
  //     </p>
  //   );
  // }

  // const SelectedModule = moduleConfigComponents[module.name as Modules];
  return (
    <>
      {isLoading && <p>Loading...</p>}
      {error && (
        <p className="text-red-500">Failed to get config options from Athena</p>
      )}
      {data && (
        <Form
          key={formKey}
          schema={data}
          validator={validator}
          onSubmit={(props) => {
            onChangeConfig(props.formData);
          }}
          formData={moduleConfig}
          liveValidate
          className="schema-form"
          uiSchema={{
            "ui:label": false,
            ...getUISchema(validator, data, (property) => {
              let config: UIOptionsType = {
                "ui:enableMarkdownInDescription": true,
              };
              if (property.includes("message")) {
                config["ui:widget"] = "textarea"
              }
              return config;
            }),
          }}
        >
          <div>
            <button type="submit" className="btn btn-info">
              Save
            </button>
            <button
              className="text-white bg-gray-500 hover:bg-gray-700 ml-2 btn"
              onClick={() => {
                const defaultFormData = getDefaultFormState(
                  validator,
                  data,
                  {},
                  data
                );
                onChangeConfig(defaultFormData);
                setFormKey(formKey + 1);
              }}
            >
              Reset
            </button>
          </div>
        </Form>
        // <SelectedModule
        //   configOptions={data}
        //   moduleConfig={moduleConfig}
        //   onChangeConfig={onChangeConfig}
        // />
      )}
    </>
  );
}
function createRef<T>() {
  throw new Error("Function not implemented.");
}
