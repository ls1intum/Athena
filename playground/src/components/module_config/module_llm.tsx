import { useState } from "react";

import { UIOptionsType, getDefaultFormState, WidgetProps, DescriptionFieldProps, RegistryFieldsType } from "@rjsf/utils";
import validator from "@rjsf/validator-ajv8";
import { Editor, Monaco } from "@monaco-editor/react";
import { editor } from "monaco-editor";

import Form from "@/components/form";
import { getUISchema } from "@/components/form/utils";
import { ModuleConfigProps } from ".";


const CustomDescriptionField = ({id, description}) => {
  return <div id={id}>TEST: {description}</div>;
};

const fields = {
  DescriptionField: CustomDescriptionField
};


export default function ModuleLLMConfig({
  moduleConfig,
  configOptions,
  onChangeConfig,
}: ModuleConfigProps) {
  return (
    <>
      <Form
        schema={configOptions}
        validator={validator}
        onChange={(props) => {
          onChangeConfig(props.formData);
        }}
        formData={moduleConfig}
        liveValidate
        className="schema-form"
        fields={fields}
        uiSchema={{
          "ui:submitButtonOptions": {
            norender: true,
          },
          "ui:label": false,
          ...getUISchema(validator, configOptions, (property) => {
            let config: UIOptionsType = {
              "ui:enableMarkdownInDescription": true,
            };
            if (property.includes("message")) {
              config["ui:widget"] = "textarea";
            }
            return config;
          }),
        }}
      />
      <button
        className="text-white bg-gray-500 hover:bg-gray-700 rounded-md p-2 border mx-1"
        onClick={() => {
          const defaultFormData = getDefaultFormState(
            validator,
            configOptions,
            {},
            configOptions
          );
          onChangeConfig(defaultFormData);
          console.log("Reset");
        }}
      >
        Reset
      </button>
    </>
  );
}
