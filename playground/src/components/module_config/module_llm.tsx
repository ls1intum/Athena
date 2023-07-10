import validator from "@rjsf/validator-ajv8";

import { ModuleConfigProps } from ".";
import Form, { getUISchema } from "@/components/form";
import { UIOptionsType, getDefaultFormState, WidgetProps } from "@rjsf/utils";
import TextareaAutosize from "react-textarea-autosize";

const AutoResizingTextAreaWidget = ({
  id,
  required,
  value,
  readonly,
  disabled,
  autofocus,
  onChange,
  onBlur,
  onFocus,
}: WidgetProps) => {
  const handleOnChange = (e) => {
    onChange(e.target.value);
  };

  const handleOnBlur = (e) => {
    onBlur(id, e.target.value);
  };

  const handleOnFocus = (e) => {
    onFocus(id, e.target.value);
  };

  return (
    <TextareaAutosize
      id={id}
      required={required}
      value={value}
      disabled={disabled || readonly}
      autoFocus={autofocus}
      onChange={handleOnChange}
      onBlur={handleOnBlur}
      onFocus={handleOnFocus}
      className="form-control" // Make sure this matches the class your form uses
    />
  );
};

export default function ModuleLLMConfig({
  moduleConfig,
  configOptions,
  onChangeConfig,
}: ModuleConfigProps) {
  return (
    <Form
      schema={configOptions}
      validator={validator}
      onSubmit={(props) => {
        onChangeConfig(props.formData);
      }}
      formData={moduleConfig}
      liveValidate
      className="schema-form"
      uiSchema={{
        "ui:label": false,
        ...getUISchema(validator, configOptions, (property) => {
          let config: UIOptionsType = {
            "ui:enableMarkdownInDescription": true,
          };
          if (property.includes("message")) {
            config["ui:widget"] = AutoResizingTextAreaWidget; // "textarea";
            // config["ui:widget"] = ((props: WidgetProps) => {
            //   return (
            //     <input
            //       type='text'
            //       className='custom'
            //       value={props.value}
            //       required={props.required}
            //       onChange={(event) => props.onChange(event.target.value)}
            //     />
            //   );
            // });
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
              configOptions,
              {},
              configOptions
            );
            onChangeConfig(defaultFormData);
          }}
        >
          Reset
        </button>
      </div>
    </Form>
  );
}
