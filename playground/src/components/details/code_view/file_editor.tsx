import type { Feedback, TextFeedback } from "@/model/feedback";

import { useEffect, useId, useMemo, useRef, useState } from "react";
import { Editor, Monaco, useMonaco } from "@monaco-editor/react";
import { IRange, Position, Selection, editor } from "monaco-editor";
import * as portals from "react-reverse-portal";
import { createRoot } from "react-dom/client";

import { getFeedbackRange } from "@/model/feedback";
import InlineFeedback from "./inline_feedback";

type FileEditorProps = {
  content: string;
  filePath?: string;
  feedbacks?: Feedback[];
  onFeedbacksChange?: (feedback: Feedback[]) => void;
};

export default function FileEditor({
  content,
  filePath,
  feedbacks,
  onFeedbacksChange,
}: FileEditorProps) {
  // Only render feedbacks that are relevant to the current file
  // Unreferenced feedbacks are always shown
  const feedbacksToRender = feedbacks?.filter((feedback) => {
    if ("file_path" in feedback) {
      return feedback.file_path === filePath;
    } else {
      return true;
    }
  });

  const editorRef = useRef<editor.IStandaloneCodeEditor>();
  const monaco = useMonaco();

  const id = useId();
  const portalNodes = useMemo(() => feedbacksToRender?.map(() => portals.createHtmlPortalNode()), [feedbacks]);
  const resizeObservers = useRef<(ResizeObserver | null)[]>([]);
  const [decorationsCollection, setDecorationsCollection] = useState<editor.IEditorDecorationsCollection | undefined>(undefined);
  const [hoverPosition, setHoverPosition] = useState<Position | undefined>(undefined);
  const [selection, setSelection] = useState<Selection | undefined>(undefined);
  const [
    addFeedbackDecorationsCollection,
    setAddFeedbackDecorationsCollection,
  ] = useState<editor.IEditorDecorationsCollection | undefined>(undefined);

  const isAddFeedbackPressed = useRef(false);

  const addFeedbackPressed = () => {
    console.log("Add feedback");
  };

  // Update the model when the content or filePath changes (for syntax highlighting)
  useEffect(() => {
    if (!monaco) return;  
    const path = monaco.Uri.parse(filePath || "");
    monaco.editor.getModel(path)?.dispose();
    const model = monaco.editor.createModel(content, undefined, path);
    editorRef.current?.setModel(model);
  }, [monaco, filePath, content]);

  const handleEditorDidMount = (
    editor: editor.IStandaloneCodeEditor,
    monaco: Monaco
  ) => {
    editorRef.current = editor;

    const feedbackRanges = feedbacksToRender?.map((feedback) =>
      getFeedbackRange(content, feedback)
    );

    let overlayNodes: HTMLDivElement[] = [];
    feedbacksToRender?.forEach((_, index) => {
      const portalNode = portalNodes![index]!;

      const overlayNode = document.createElement("div");
      overlayNode.id = `feedback-${id}-${index}-overlay`;
      overlayNode.style.width = "100%";
      const root = createRoot(overlayNode);
      root.render(<portals.OutPortal node={portalNode} />);

      var overlayWidget = {
        getId: () => `feedback-${id}-${index}-widget`,
        getDomNode: () => overlayNode,
        getPosition: () => null,
      };
      editor.addOverlayWidget(overlayWidget);
      overlayNodes.push(overlayNode);
    });

    editor.changeViewZones(function (changeAccessor) {
      feedbacksToRender?.forEach((_, index) => {
        const overlayNode = overlayNodes[index];
        const zoneNode = document.createElement("div");
        zoneNode.id = `feedback-${id}-${index}-zone`;

        const zoneId = changeAccessor.addZone({
          afterLineNumber: feedbackRanges![index]?.endLineNumber || 0,
          afterColumn: feedbackRanges![index]?.endColumn,
          domNode: zoneNode,
          get heightInPx() {
            return overlayNode.offsetHeight;
          },
          onDomNodeTop: (top) => {
            overlayNode.style.top = top + "px";
          },
        });
        const observer = new ResizeObserver(() => {
          editor.changeViewZones((accessor) => accessor.layoutZone(zoneId));
        });
        observer.observe(overlayNode);
        resizeObservers.current.push(observer);
      });
    });

    if (decorationsCollection) {
      decorationsCollection.clear();
    }
    const newDecorationsCollection = editor.createDecorationsCollection(
      feedbackRanges?.flatMap((range, index) =>
        range
          ? [
              {
                options: {
                  inlineClassName: `inline-feedback-text ${
                    feedbacksToRender![index].credits < 0
                      ? "negative"
                      : feedbacksToRender![index].credits > 0
                      ? "positive"
                      : "neutral"
                  }`,
                },
                range,
              },
            ]
          : []
      ) ?? []
    );
    setDecorationsCollection(newDecorationsCollection);

    editor.onMouseMove(function (e) {
      setHoverPosition(e.target.position ?? undefined);
    });

    editor.onDidChangeCursorSelection(function (e) {
      setSelection(e.selection);
    });

    editor.onMouseDown(function (e) {
      if (e.target.element?.className.includes("comment-range-button")) {
        isAddFeedbackPressed.current = true;
      }
    });

    editor.onMouseUp(function (e) {
      if (e.target.element?.className.includes("comment-range-button")) {
        if (isAddFeedbackPressed.current) {
          addFeedbackPressed();
        }
      }
      isAddFeedbackPressed.current = false;
    });
  };

  useEffect(() => {
    if (!editorRef.current || !monaco) {
      return;
    }

    if (addFeedbackDecorationsCollection) {
      addFeedbackDecorationsCollection.clear();
    }
    if (hoverPosition === undefined && selection === undefined) {
      setAddFeedbackDecorationsCollection(undefined);
      return;
    }

    if (selection && !selection.isEmpty()) {
      const decorations: editor.IModelDeltaDecoration[] = [
        {
          range: new monaco.Range(
            selection.startLineNumber,
            selection.startColumn,
            selection.endLineNumber,
            selection.endColumn
          ),
          options: {
            linesDecorationsClassName: "comment-range",
          },
        },
        {
          range: new monaco.Range(
            selection.endLineNumber,
            selection.endColumn,
            selection.endLineNumber,
            selection.endColumn
          ),
          options: {
            linesDecorationsClassName: "comment-range-button",
          },
        },
      ];
      const newAddFeedbackDecorationsCollection =
        editorRef.current.createDecorationsCollection(decorations);
      setAddFeedbackDecorationsCollection(newAddFeedbackDecorationsCollection);
    } else if (hoverPosition) {
      const decorations: editor.IModelDeltaDecoration[] = [
        {
          range: new monaco.Range(
            hoverPosition.lineNumber,
            1,
            hoverPosition.lineNumber,
            1
          ),
          options: {
            isWholeLine: true,
            linesDecorationsClassName: "comment-range",
          },
        },
        {
          range: new monaco.Range(
            hoverPosition.lineNumber,
            hoverPosition.column,
            hoverPosition.lineNumber,
            hoverPosition.column
          ),
          options: { linesDecorationsClassName: "comment-range-button" },
        },
      ];
      const newAddFeedbackDecorationsCollection =
        editorRef.current.createDecorationsCollection(decorations);
      setAddFeedbackDecorationsCollection(newAddFeedbackDecorationsCollection);
    } else {
      setAddFeedbackDecorationsCollection(undefined);
    }
  }, [hoverPosition, selection]);

  // Cleanup on unmount
  useEffect(() => {
    if (editorRef.current && monaco) {
      handleEditorDidMount(editorRef.current, monaco);
    }
    return () => {
      resizeObservers.current.forEach((observer) => observer?.disconnect());
      resizeObservers.current = [];
    };
  }, []);

  return (
    <div className="h-[50vh]">
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
          lineDecorationsWidth: 20,
          folding: false,
          wordWrap: "on",
        }}
        value={content}
        path={filePath}
        defaultValue="Please select a file"
        onMount={handleEditorDidMount}
      />
      {portalNodes && feedbacks && feedbacksToRender &&
        feedbacksToRender.map((feedback, index) => {
          return (
            portalNodes[index] && (
              <portals.InPortal node={portalNodes[index]} key={feedback.id}>
                <div className="mr-4">
                  <InlineFeedback
                    feedback={feedback}
                    onFeedbackChange={
                      onFeedbacksChange &&
                      ((newFeedback) => {
                        if (newFeedback) {
                          onFeedbacksChange(
                            feedbacks.map((f) =>
                              f.id === feedback.id ? newFeedback : f
                            )
                          );
                        } else {
                          onFeedbacksChange(
                            feedbacks.filter((f) => f.id !== feedback.id)
                          );
                        }
                      })
                    }
                  />
                </div>
              </portals.InPortal>
            )
          );
        })}
    </div>
  );
}
