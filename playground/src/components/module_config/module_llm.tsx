import { useState } from "react";

import { UIOptionsType, getDefaultFormState, WidgetProps } from "@rjsf/utils";
import validator from "@rjsf/validator-ajv8";
import { Editor, Monaco } from "@monaco-editor/react";
import { editor } from "monaco-editor";

import Form, { getUISchema } from "@/components/form";
import { ModuleConfigProps } from ".";

const PromptTextAreaWidget = ({ id, value, onChange }: WidgetProps) => {
  const [height, setHeight] = useState(100);

  const handleEditorDidMount = (
    editor: editor.IStandaloneCodeEditor,
    monaco: Monaco
  ) => {
    editor.onDidContentSizeChange(() => {
      setHeight(Math.min(1000, editor.getContentHeight()));
      editor.layout();
    });

    monaco.languages.register({ id: "placeholder" });
    monaco.languages.setMonarchTokensProvider("placeholder", {
      tokenizer: {
        root: [[/{\w*}/, "variable"]],
      },
    });
    monaco.editor.defineTheme("my-theme", {
      base: "vs",
      inherit: true,
      rules: [{ token: "variable", foreground: "0000FF" }],
      colors: {},
    });
    monaco.editor.setTheme("my-theme");
  };

  return (
    <div id={id} className="border border-gray-300 rounded my-2 py-2">
      <div style={{ height }}>
        <Editor
          options={{
            scrollBeyondLastLine: false,
            automaticLayout: true,
            scrollbar: {
              vertical: "hidden",
              horizontal: "hidden",
              alwaysConsumeMouseWheel: false,
            },
            minimap: {
              enabled: false,
            },
          }}
          value={value}
          onMount={handleEditorDidMount}
          defaultLanguage="placeholder"
          onChange={(value) => onChange(value)}
        />
      </div>
    </div>
  );
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
              config["ui:widget"] = PromptTextAreaWidget;
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
