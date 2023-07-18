import { ViewMode } from "@/model/view_mode";

export default function ViewModeSelect({
  viewMode,
  onChangeViewMode,
}: {
  viewMode: ViewMode;
  onChangeViewMode: (viewMode: ViewMode) => void;
}) {
  return (
    <label className="flex flex-col">
      <span className="text-lg font-bold">Select Mode</span>
      <div className="flex flex-row mb-2">
        <button
          className={`p-2 rounded-l-md ${
            viewMode === "module_requests"
              ? "bg-primary-500 text-white hover:bg-primary-600"
              : "bg-gray-200 text-gray-500 hover:bg-gray-300"
          }`}
          onClick={() => onChangeViewMode("module_requests")}
        >
          Module Requests
        </button>
        <button
          className={`p-2 rounded-r-md ${
            viewMode === "evaluation_mode"
              ? "bg-primary-500 text-white hover:bg-primary-600"
              : "bg-gray-200 text-gray-500 hover:bg-gray-300"
          }`}
          onClick={() => onChangeViewMode("evaluation_mode")}
        >
          Evaluation Mode
        </button>
      </div>
      <p className="text-gray-500">
        {viewMode === "module_requests" ? (
          <>
            <b>Module Requests</b> allows you to test different requests to see
            how the module responds.
          </>
        ) : (
          <>
            <b>Evaluation Mode</b> allows you to assess the module&apos;s
            performance and provide feedback for improvement.
          </>
        )}
      </p>
    </label>
  );
}
