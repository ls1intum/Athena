import { useState } from "react";

import { WidgetProps } from "@rjsf/utils";
import { Editor, Monaco } from "@monaco-editor/react";
import { editor } from "monaco-editor";


const TextAreaWidget = ({ id, value, onChange }: WidgetProps) => {
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

export default TextAreaWidget;