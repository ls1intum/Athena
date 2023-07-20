import Feedback from "@/model/feedback";

import { Monaco, Editor, useMonaco } from "@monaco-editor/react";
import * as portals from "react-reverse-portal";
import { editor } from "monaco-editor";
import { useEffect, useId, useMemo, useRef, useState } from "react";
import { createRoot } from "react-dom/client";


function FeedbackView({ feedback }: { feedback: Feedback }) {
  return (
    <div>
      {feedback.text}
      {feedback.detail_text}
    </div>
  );
}

type EditorFeedbackProps = {
  feedback: Feedback;
  editor: editor.IStandaloneCodeEditor;
};

function EditorFeedback({ feedback, editor }: EditorFeedbackProps) {
  const widgetId = useId();
  const [viewZoneId, setViewZoneId] = useState<string | undefined>(undefined);
  const [portalNode, domNode] = useMemo(() => {
    const portalNode = portals.createHtmlPortalNode();

    const overlayDom = document.createElement("div");
    overlayDom.style.background = '#0000ff';
    overlayDom.style.width = "100%";

    const root = createRoot(overlayDom);
    root.render(<portals.OutPortal node={portalNode} />);
    return [portalNode, overlayDom];
  }, []);

  console.log("rendering EditorFeedback", feedback);
  useEffect(() => {

    editor.changeViewZones((changeAccessor) => {
      if (viewZoneId) {
        changeAccessor.removeZone(viewZoneId);
      }

      const overlayWidget = {
        getId: () => widgetId,
        getDomNode: () => domNode,
        getPosition: () => null,
      };
      editor.addOverlayWidget(overlayWidget);

      const zoneNode = document.createElement('div');
      zoneNode.style.background = '#ff0000';
      zoneNode.id = `feedback-${feedback.id}`
      const zoneId = changeAccessor.addZone({
        afterLineNumber: 3,
        heightInLines: 3,
        domNode: zoneNode,
        onDomNodeTop: top => {
          domNode.style.top = top + "px";
        },
        onComputedHeight: height => {
          domNode.style.height = height + "px";
        }
      });
      setViewZoneId(zoneId);
    });
  }, [editor, feedback, portalNode, widgetId]);

  return (
    <portals.InPortal node={portalNode}>
      <FeedbackView feedback={feedback} />
    </portals.InPortal>
  );
}

type FileEditorProps = {
  content: string;
  filePath?: string;
  feedbacks?: Feedback[];
  onFeedbackChange: (feedback: Feedback[]) => void;
};

export default function FileEditor({
  content,
  filePath,
  feedbacks,
  onFeedbackChange,
}: FileEditorProps) {
  const editorRef = useRef<editor.IStandaloneCodeEditor>();
  const monaco = useMonaco();
  const handleEditorDidMount = (editor: editor.IStandaloneCodeEditor, monaco: Monaco) => {
    editorRef.current = editor;
  }

  useEffect(() => {
    if (!monaco || !filePath || !editorRef.current) return;
    const path = monaco.Uri.parse(filePath)
    monaco.editor.getModel(path)?.dispose()
    const model = monaco.editor.createModel(content, undefined, path)
    editorRef.current.setModel(model);
  }, [monaco, editorRef, content, filePath]);

  return (
    <div className="h-full">
      <Editor
        options={{
          automaticLayout: true,
          minimap: {
            enabled: false,
          },
          readOnly: true,
        }}
        value={content}
        path={filePath}
        defaultValue="Please select a file"
        onMount={handleEditorDidMount}
      />
      {editorRef.current && feedbacks?.map((feedback, index) => (
        <EditorFeedback key={index} feedback={feedback} editor={editorRef.current!} />
      ))}
    </div>
  );
}
