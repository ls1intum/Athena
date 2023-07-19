import { useEffect, useRef, useState } from "react";
import { Allotment } from "allotment";
import { Monaco, Editor, useMonaco } from "@monaco-editor/react";
import { editor } from "monaco-editor";

import { useFetchAndUnzip } from "@/helpers/fetch_and_unzip";
import FileTree from "./file_tree";


type CodeViewProps = {
  repository_url: string;
};

export default function CodeView({ repository_url }: CodeViewProps) {
  const editorRef = useRef<editor.IStandaloneCodeEditor>();
  const monaco = useMonaco();
 
  const repository = useFetchAndUnzip(repository_url);
  const [selectedFile, setSelectedFile] = useState<string | undefined>(undefined);
  const [fileContent, setFileContent] = useState<string | undefined>(undefined);

  useEffect(() => {
    if (selectedFile) {
      repository.zip.file(selectedFile)?.async("string").then(setFileContent);
      // editorRef.current?.setModel(model);
      // const model = monaco.editor.createModel(fileContent, undefined, monaco.Uri.file(fileName));

    }
  }, [selectedFile, repository]);

  useEffect(() => {
    if (monaco) {
      console.log('here is the monaco instance:', monaco);
      console.log('Models', monaco.editor.getModels())
      if (selectedFile) {
        const path = monaco.Uri.parse(selectedFile)
        monaco.editor.getModel(path)?.dispose()
        console.log("Create model")
        const model = monaco.editor.createModel(fileContent || "", undefined, monaco.Uri.parse(selectedFile))
        editorRef.current?.setModel(model);
      }
    }
  }, [monaco, selectedFile, fileContent]);

  const handleEditorDidMount = (editor: editor.IStandaloneCodeEditor, monaco: Monaco) => {
    editorRef.current = editor;
  }

  return (
    <div className="h-[400px]">
      <Allotment vertical={false} defaultSizes={[20, 80]}>
        <FileTree tree={repository.tree} selectedFile={selectedFile} onSelectFile={setSelectedFile} />
        <Editor
          height="80vh"
          options={{
            automaticLayout: true,
            scrollbar: {
              vertical: "hidden",
              horizontal: "hidden",
            },
            minimap: {
              enabled: false,
            },
            readOnly: true,
          }}
          value={fileContent}
          path={selectedFile}
          onMount={handleEditorDidMount}
          // onChange={(value) => onChange(value)}
        />
      </Allotment>
    </div>
  );
}
