import { getDefaultFormState } from "@rjsf/utils";
import validator from "@rjsf/validator-ajv8";

import Form from "@/components/form";
import { ModuleConfigSelectProps } from ".";

export default function DefaultSchemaFormModuleConfig({
  disabled,
  moduleConfig,
  configOptions,
  onChangeConfig,
}: ModuleConfigSelectProps) {
  return (
    <>
      <Form
        disabled={disabled}
        schema={configOptions}
        validator={validator}
        onChange={(props) => {
          if (onChangeConfig) {
            onChangeConfig(props.formData);
          }
        }}
        formData={moduleConfig}
        liveValidate
        className="schema-form"
        uiSchema={{
          "ui:label": false,
          "ui:submitButtonOptions": {
            norender: true,
          },
        }}
      />
      {!disabled && (
        <button
          className="text-white bg-gray-500 hover:bg-gray-700 rounded-md p-2 border mt-4"
          onClick={() => {
            if (!onChangeConfig) return;

            const defaultFormData = getDefaultFormState(
              validator,
              configOptions,
              {},
              configOptions
            );
            onChangeConfig(defaultFormData);
          }}
        >
          Reset
        </button>
      )}
    </>
  );
}
