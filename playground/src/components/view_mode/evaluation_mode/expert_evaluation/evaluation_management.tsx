import { useState, useEffect } from "react";
import { v4 as uuidv4 } from "uuid";
import { downloadJSONFile } from "@/helpers/download";
import { twMerge } from "tailwind-merge";
import ExerciseSelect from "@/components/selectors/exercise_select";
import MetricsForm from "@/components/view_mode/evaluation_mode/expert_evaluation/metrics_form";
import {Exercise} from "@/model/exercise";

export type EvaluationConfig = {
  id: string;
  name: string;
  metrics: Metric[];
  exercises: Exercise[];
};

export type EvaluationConfigExport = {
  type: "evaluation_config";
  id: string;
  name: string;
  metrics: Metric[];
  exercises: Exercise[];
};

type DefineEvaluationProps = {
  evaluationConfig: EvaluationConfig | undefined;
  onChangeEvaluationConfig: (evaluationConfig: EvaluationConfig | undefined) => void;
};

export default function EvaluationManagement({
  evaluationConfig,
  onChangeEvaluationConfig,
}: DefineEvaluationProps) {
  const [evaluationConfigs, setEvaluationConfigs] = useState<EvaluationConfig[]>([]);
  const [selectedConfigId, setSelectedConfigId] = useState<string>("new");
  const [name, setName] = useState<string>("");
  const [metrics, setMetrics] = useState<Metric[]>([]);
  const [exercises, setExercises] = useState<Exercise[]>([]);
  const [isImporting, setIsImporting] = useState<boolean>(false);

  // Synchronize with selected evaluation config
  useEffect(() => {
    if (selectedConfigId === "new") {
      setName("");
      setMetrics([]);
      setExercises([]);
    } else {
      const selectedConfig = evaluationConfigs.find((config) => config.id === selectedConfigId);
      if (selectedConfig) {
        setName(selectedConfig.name);
        setMetrics(selectedConfig.metrics);
        setExercises(selectedConfig.exercises);
      }
    }
  }, [selectedConfigId, evaluationConfigs]);

  // Get the currently selected evaluation config
  const getSelectedConfig = (): EvaluationConfig => {
    if (selectedConfigId === "new") {
      return {
        id: uuidv4(),
        name,
        metrics,
        exercises,
      };
    } else {
      return (
        evaluationConfigs.find((config) => config.id === selectedConfigId) || {
          id: uuidv4(),
          name: "",
          metrics: [],
          exercises: [],
        }
      );
    }
  };

  const definedEvaluationConfig = getSelectedConfig();

  // Add or update the current evaluation config
  const saveEvaluationConfig = (newConfig: EvaluationConfig) => {
    setEvaluationConfigs((prevConfigs) => {
      const existingIndex = prevConfigs.findIndex((config) => config.id === newConfig.id);
      if (existingIndex !== -1) {
        const updatedConfigs = [...prevConfigs];
        updatedConfigs[existingIndex] = newConfig;
        return updatedConfigs;
      } else {
        return [...prevConfigs, newConfig];
      }
    });
    setSelectedConfigId(newConfig.id);
  };

  // Export evaluation config
  const handleExport = () => {
    const configToExport = definedEvaluationConfig;
    if (!configToExport) return;
    downloadJSONFile(`evaluation_config_${configToExport.name}_${configToExport.id}`, {
      type: "evaluation_config",
      id: configToExport.id,
      name: configToExport.name,
      metrics: configToExport.metrics,
      exercises: configToExport.exercises,
    });
  };

  // Import evaluation config
  const handleImport = async (fileContent: string) => {
    const importedConfig = JSON.parse(fileContent) as EvaluationConfigExport;
    const { type, id, name, metrics, exercises } = importedConfig;
    if (type !== "evaluation_config") {
      alert("Invalid config type");
      return;
    }

    saveEvaluationConfig({ id, name, metrics, exercises });
  };

  return (
    <div className="bg-white rounded-md p-4 mb-8 space-y-2">
      <div className="flex flex-row justify-between items-center">
        <h3 className="text-2xl font-bold">Manage Evaluations</h3>
        <div className="flex flex-row">
          <button
            disabled={!definedEvaluationConfig}
            className="rounded-md p-2 text-primary-500 hover:text-primary-600 hover:bg-gray-100 disabled:text-gray-500 disabled:cursor-not-allowed"
            onClick={handleExport}
          >
            Export
          </button>
          <label className={twMerge("rounded-md p-2 cursor-pointer", "text-primary-500 hover:text-primary-600 hover:bg-gray-100")}>
            Import
            <input
              className="hidden"
              type="file"
              accept=".json"
              onChange={(e) => {
                if (e.target.files && e.target.files.length > 0) {
                  const file = e.target.files[0];
                  const reader = new FileReader();
                  reader.onload = (e) => {
                    if (e.target && typeof e.target.result === "string") {
                      handleImport(e.target.result);
                    }
                  };
                  reader.readAsText(file);
                }
                e.target.value = ""; // Reset file input
              }}
            />
          </label>
        </div>
      </div>

      {/* Dropdown to switch between evaluation configs */}
      <label className="flex flex-col">
        <span className="text-lg font-bold">Evaluation</span>
        <select
          className="border border-gray-300 rounded-md p-2"
          value={selectedConfigId}
          onChange={(e) => setSelectedConfigId(e.target.value)}
        >
          <option value="new">New Evaluation</option>
          {evaluationConfigs.map((config) => (
            <option key={config.id} value={config.id}>
              {config.name}
            </option>
          ))}
        </select>
      </label>

      {/* Show form for new config or edit existing config */}
      {selectedConfigId === "new" ? (
        <>
          <label className="flex flex-col">
            <span className="text-lg font-bold">Name of the New Evaluation</span>
            <input
              type="text"
              placeholder="Insert Evaluation Name"
              className="border border-gray-300 rounded-md p-2"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
          </label>
          <ExerciseSelect
            exercises={exercises}
            exerciseType="text"
            onChange={setExercises}
            multiple={true}
          />
          <MetricsForm metrics={metrics} setMetrics={setMetrics} />
        </>
      ) : (
        <>
          <h4 className="text-lg font-bold">Editing: {name}</h4>
          <ExerciseSelect
            exercises={exercises}
            exerciseType="text"
            onChange={(newExercises) => {
              setExercises(newExercises);
              saveEvaluationConfig({ ...definedEvaluationConfig, exercises: newExercises });
            }}
            multiple={true}
          />
          <MetricsForm
            metrics={metrics}
            setMetrics={(newMetrics) => {
              setMetrics(newMetrics);
              saveEvaluationConfig({ ...definedEvaluationConfig, metrics: newMetrics });
            }}
          />
        </>
      )}

      <div className="flex flex-row gap-2">
        <button
          className={twMerge(
            "bg-primary-500 text-white rounded-md p-2 mt-2 hover:bg-primary-600",
            !definedEvaluationConfig ? "disabled:text-gray-500 disabled:bg-gray-200 disabled:cursor-not-allowed" : ""
          )}
          onClick={() => {
            if (definedEvaluationConfig) {
              saveEvaluationConfig(definedEvaluationConfig);
            }
          }}
        >
          {selectedConfigId === "new" ? "Define Experiment" : "Save Changes"}
        </button>
        {selectedConfigId !== "new" && (
          <button
            className="bg-red-500 text-white rounded-md p-2 mt-2 hover:bg-red-600"
            onClick={() => {
              if (confirm("Cancel evaluation?")) {
                setEvaluationConfigs((prevConfigs) =>
                  prevConfigs.filter((config) => config.id !== selectedConfigId)
                );
                setSelectedConfigId("new");
              }
            }}
          >
            Cancel
          </button>
        )}
      </div>
    </div>
  );
}
