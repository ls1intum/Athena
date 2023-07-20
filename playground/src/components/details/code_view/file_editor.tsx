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
  const portalNode = useMemo(() => portals.createHtmlPortalNode(), []);

  useEffect(() => {
    editor.changeViewZones((changeAccessor) => {
      if (viewZoneId) {
        changeAccessor.removeZone(viewZoneId);
      }

      const overlayDom = document.createElement("div");
      overlayDom.style.background = '#0000ff';
      overlayDom.style.width = "100%";

      const root = createRoot(overlayDom);
      root.render(<portals.OutPortal node={portalNode} />);

      const overlayWidget = {
        getId: () => widgetId,
        getDomNode: () => overlayDom,
        getPosition: () => null,
      };
      editor.addOverlayWidget(overlayWidget);

      const zoneNode = document.createElement('div');
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
  }, [editor, feedback, portalNode, viewZoneId, widgetId]);

  return (
    <portals.InPortal node={portalNode}>
      <FeedbackView feedback={feedback} />
    </portals.InPortal>
  );
}

type FileEditorProps = {
  content: string;
  filePath?: string;
  feedback?: Feedback[];
  onFeedbackChange: (feedback: Feedback[]) => void;
};

export default function FileEditor({
  content,
  filePath,
  feedback,
  onFeedbackChange,
}: FileEditorProps) {
  const editorRef = useRef<editor.IStandaloneCodeEditor>();
  const handleEditorDidMount = (editor: editor.IStandaloneCodeEditor, monaco: Monaco) => {
    editorRef.current = editor;
  }

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
      {editorRef.current && feedback?.map((feedback, index) => (
        <EditorFeedback key={index} feedback={feedback} editor={editorRef.current!} />
      ))}
    </div>
  );
}
