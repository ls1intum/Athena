import useImportEvaluationData from "@/hooks/playground/data/import";
import useExercises from "@/hooks/playground/exercises";
import type { DataMode } from "@/model/data_mode";
import { useState } from "react";
import { useQueryClient } from "react-query";

function sanitizeDirectoryName(directory: string): string {
  return directory.replace(/[^a-zA-Z0-9_-]/g, "");
}

export default function DataModeSelect({
  dataMode,
  onChangeDataMode
}: {
  dataMode: DataMode;
  onChangeDataMode: (dataMode: DataMode) => void;
}) {
  const queryClient = useQueryClient();
  const evaluationDataKey = dataMode.startsWith("evaluation-") ? dataMode.slice("evaluation-".length) : undefined;

  const { data: exerciseData, error: exerciseError, isLoading: isLoadingExercises } = useExercises()
  const exerciseTypes = new Map<string, number>();
    exerciseData?.forEach((exercise) => {
    exerciseTypes.set(exercise.type, (exerciseTypes.get(exercise.type) || 0) + 1);
  });
  const exerciseStatistics = Array.from(exerciseTypes.entries())
    .map(([type, count]) => `${count} ${type}`)
    .join(", ") || "No exercises available";

  const { mutate, isLoading: isMutating } = useImportEvaluationData({
    onSuccess: () => {
      alert("Import successful!");
      queryClient.invalidateQueries("exercises");
    },
    onError: () => {
      alert("Import failed!");
    }
  });

  const handleImport = (files: FileList | null) => {
    if (!files) return;

    const formData = new FormData();
    Array.from(files).forEach((file) => {
      formData.append("file", file);
    });

    mutate({ dataMode, formData });
  };  

  return (
    <div className="flex flex-col">
      <span className="text-lg font-bold">Dataset</span>
      <div className="flex flex-row mb-2">
        <button
          className={`p-2 rounded-l-md ${
            dataMode === "example"
              ? "bg-primary-500 text-white hover:bg-primary-600"
              : "bg-gray-200 text-gray-500 hover:bg-gray-300"
          }`}
          onClick={() => onChangeDataMode("example")}
        >
          Example Data
        </button>
        <button
          className={`p-2 rounded-r-md ${
            dataMode.startsWith("evaluation")
              ? "bg-primary-500 text-white hover:bg-primary-600"
              : "bg-gray-200 text-gray-500 hover:bg-gray-300"
          }`}
          onClick={() => onChangeDataMode("evaluation")}
        >
          Evaluation Data
        </button>
      </div>
      <p className="text-gray-500">
        Data in <code className="bg-gray-100 p-1 rounded-sm">data/{dataMode.split("-", 1)[0]}/
          {dataMode.startsWith("evaluation") && evaluationDataKey ? evaluationDataKey + "/" : ""}
          </code>{" "}
        directory will be used.
      </p>
      {dataMode.startsWith("evaluation") && (
        <div className="flex flex-col space-y-2">
          <input
            className="border border-gray-300 rounded-md p-2"
            placeholder="Optional, use custom evaluation data directory"
            value={evaluationDataKey}
            onChange={(e) => onChangeDataMode(e.target.value ? `evaluation-${sanitizeDirectoryName(e.target.value)}` : "evaluation")}
          />
          {exerciseError && <div className="text-red-500">Failed to load exercises</div>}
          {isLoadingExercises && <div className="text-gray-500">Loading exercises...</div>}
          {exerciseData && (<div className="text-gray-500">Available exercises: <span className="font-bold">{exerciseStatistics}</span></div>)}
          { evaluationDataKey && (
            <div className="flex flex-row space-x-2">
              <label
                className={"rounded-md p-2 text-primary-500 bg-gray-100 hover:text-primary-600 hover:bg-primary-100 cursor-pointer"}
              >
                Import
                <input
                  multiple
                  className="hidden"
                  type="file"
                  accept=".json,.zip"
                  onChange={(e) => {
                    handleImport(e.target.files);
                    // Reset the input value so that the onChange event will fire again if the same file is selected
                    e.target.value = '';
                  }}
                  disabled={isMutating}
                />
              </label>
              <button
                className="rounded-md p-2 text-primary-500 hover:text-primary-600 bg-gray-100 hover:bg-primary-100"
                onClick={() => {
                  // handleExport();
                }}
              >
                Export
              </button>
              <button
                className="rounded-md p-2 text-red-500 hover:text-red-600 bg-gray-100 hover:bg-red-100"
                onClick={() => {
                  // handleDelete();
                }}
              >
                Delete
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
