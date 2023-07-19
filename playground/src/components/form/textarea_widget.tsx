import { useState } from "react";

import { WidgetProps } from "@rjsf/utils";
import { Editor, Monaco } from "@monaco-editor/react";
import { editor } from "monaco-editor";

const TextAreaWidget = ({ id, value, onChange, options }: WidgetProps) => {
  const [height, setHeight] = useState(100);
  const lineNumbers: editor.LineNumbersType = options.showLineNumbers ? "on" : "off";
  const language = options.language as string | undefined || "plaintext";
  const customizeMonaco = options.customizeMonaco as ((monaco: Monaco) => void) | undefined;

  const handleEditorDidMount = (
    editor: editor.IStandaloneCodeEditor,
    monaco: Monaco
  ) => {
    editor.onDidContentSizeChange(() => {
      setHeight(Math.min(1000, editor.getContentHeight()));
      editor.layout();
    });

    if (customizeMonaco) {
      customizeMonaco(monaco);
    }
  };

  return (
    <div id={id} className="border border-gray-300 rounded my-2 py-2">
      <div style={{ height }}>
        <Editor
          options={{
            lineNumbers: lineNumbers,
            lineDecorationsWidth: 0,
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
          defaultLanguage={language}
          onChange={(value) => onChange(value)}
        />
      </div>
    </div>
  );
};

TextAreaWidget.defaultProps = {
  options: {
    showLineNumbers: false,
    customizeMonaco: (monaco: Monaco) => {},
    language: undefined,
  },
};

export default TextAreaWidget;
