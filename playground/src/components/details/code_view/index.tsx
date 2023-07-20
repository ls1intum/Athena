import { useEffect, useMemo, useRef, useState } from "react";
import { Allotment } from "allotment";
import { Monaco, Editor, useMonaco } from "@monaco-editor/react";
import { editor } from "monaco-editor";
import { createRoot } from "react-dom/client";

import { useFetchAndUnzip } from "@/helpers/fetch_and_unzip";
import FileTree from "./file_tree";
import * as portals from 'react-reverse-portal';
import Feedback from "@/model/feedback";


type CodeViewProps = {
  repository_url: string;
  feedback?: Feedback[]
};

export default function CodeView({ repository_url }: CodeViewProps) {
  const editorRef = useRef<editor.IStandaloneCodeEditor>();
  const monaco = useMonaco();
 
  const repository = useFetchAndUnzip(repository_url);
  const [selectedFile, setSelectedFile] = useState<string | undefined>(undefined);
  const [fileContent, setFileContent] = useState<string | undefined>(undefined);

  const [count, setCount] = useState<number>(0);
  const portalNode = useMemo(() => portals.createHtmlPortalNode(), []);

  const MyComponent = () => <div>
    My first view zone {count}
    <button onClick={() => {
      setCount(count + 1)
      console.log("Click")
    }}>Click me</button>
  </div>;

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
    
    const overlayDom = document.createElement("div");
    overlayDom.id = 'overlayId';
    overlayDom.style.width = '100%';
    // overlayDom.style.background = '#0000ff';
    const root = createRoot(overlayDom);
    root.render(<portals.OutPortal node={portalNode} />);
    
    var overlayWidget = {
      getId: () => "my.overlay.widget",
      getDomNode: () => overlayDom,
      getPosition: () => null,
    };
    editor.addOverlayWidget(overlayWidget);

    let zoneNode = document.createElement('div');
    zoneNode.id = "zoneId";

    editorRef.current?.changeViewZones(function (changeAccessor) {
      changeAccessor.addZone({
        afterLineNumber: 3,
        heightInLines: 3,
        domNode: zoneNode,
        onDomNodeTop: top => {
          overlayDom.style.top = top + "px";
        },
        onComputedHeight: height => {
          overlayDom.style.height = height + "px";
        }
      });
    });
  }

  return (
    <div className="h-[50vh]">
      <Allotment vertical={false} defaultSizes={[1,4]}>
        <Allotment.Pane preferredSize={"20%"}>
          <div className="h-full overflow-y-auto mr-2">
            <FileTree tree={repository.tree} selectedFile={selectedFile} onSelectFile={setSelectedFile} />
          </div>
        </Allotment.Pane>
        <div className="h-full">
          <Editor
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
            defaultValue="Please select a file"
            onMount={handleEditorDidMount}
            // onChange={(value) => onChange(value)}
          />
          <portals.InPortal node={portalNode}><MyComponent /></portals.InPortal>
        </div>
      </Allotment>
    </div>
  );
}
