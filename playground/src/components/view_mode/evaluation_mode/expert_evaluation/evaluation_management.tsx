import { useState, useEffect } from "react";
import { v4 as uuidv4 } from "uuid";
import { downloadJSONFile } from "@/helpers/download";
import { twMerge } from "tailwind-merge";
import MetricsForm from "@/components/view_mode/evaluation_mode/expert_evaluation/metrics_form";
import { Exercise } from "@/model/exercise";
import { ExpertEvaluationConfig } from "@/model/expert_evaluation_config";
import { Metric } from "@/model/metric";
import MultipleExercisesSelect from "@/components/selectors/multiple_exercises_select";

type DefineEvaluationProps = {
  expertEvaluationConfig: ExpertEvaluationConfig | undefined;
  onChangeExpertEvaluationConfig: (expertEvaluationConfig: ExpertEvaluationConfig | undefined) => void;
};

export default function EvaluationManagement({
  expertEvaluationConfig,
  onChangeExpertEvaluationConfig,
}: DefineEvaluationProps) {
  const [expertEvaluationConfigs, setExpertEvaluationConfigs] = useState<ExpertEvaluationConfig[]>([]);
  const [selectedConfigId, setSelectedConfigId] = useState<string>("new");
  const [name, setName] = useState<string>("");
  const [metrics, setMetrics] = useState<Metric[]>([]);
  const [exercises, setExercises] = useState<Exercise[]>([]);
  const [expertIds, setExpertIds] = useState<string[]>([]);
  const [isImporting, setIsImporting] = useState<boolean>(false);

  useEffect(() => {
    if (selectedConfigId === "new") {
      setName("");
      setMetrics([]);
      setExercises([]);
    } else {
      const selectedConfig = expertEvaluationConfigs.find((config) => config.id === selectedConfigId);
      if (selectedConfig) {
        setName(selectedConfig.name);
        setMetrics(selectedConfig.metrics);
        setExercises(selectedConfig.exercises);
      }
    }
  }, [selectedConfigId, expertEvaluationConfigs]);

  const getSelectedConfig = (): ExpertEvaluationConfig => {
    if (selectedConfigId === "new") {
      return {
        type: "evaluation_config",
        id: uuidv4(),
        name,
        metrics,
        exercises,
        expertIds: [],
      };
    } else {
      return (
        expertEvaluationConfigs.find((config) => config.id === selectedConfigId) || {
          type: "evaluation_config",
          id: uuidv4(),
          name: "",
          metrics: [],
          exercises: [],
          expertIds: [],
        }
      );
    }
  };

  const definedExpertEvaluationConfig = getSelectedConfig();

  const saveExpertEvaluationConfig = (newConfig: ExpertEvaluationConfig) => {
    setExpertEvaluationConfigs((prevConfigs) => {
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

  const handleExport = () => {
    const configToExport = definedExpertEvaluationConfig;
    if (!configToExport) return;
    downloadJSONFile(`evaluation_config_${configToExport.name}_${configToExport.id}`, configToExport);
  };

  const handleImport = async (fileContent: string) => {
    const importedConfig = JSON.parse(fileContent) as ExpertEvaluationConfig;
    if (importedConfig.type !== "evaluation_config") {
      alert("Invalid config type");
      return;
    }

    saveExpertEvaluationConfig(importedConfig);
  };

  return (
    <div className="bg-white rounded-md p-4 mb-8 space-y-2">
      <div className="flex flex-row justify-between items-center">
        <h3 className="text-2xl font-bold">Manage Evaluations</h3>
        <div className="flex flex-row">
          <button
            disabled={!definedExpertEvaluationConfig}
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

      <label className="flex flex-col">
        <span className="text-lg font-bold">Evaluation</span>
        <select
          className="border border-gray-300 rounded-md p-2"
          value={selectedConfigId}
          onChange={(e) => setSelectedConfigId(e.target.value)}
        >
          <option value="new">New Evaluation</option>
          {expertEvaluationConfigs.map((config) => (
            <option key={config.id} value={config.id}>
              {config.name}
            </option>
          ))}
        </select>
      </label>

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
          <MultipleExercisesSelect
            selectedExercises={exercises}
            exerciseType="text"
            onChange={setExercises}
          />
          <MetricsForm metrics={metrics} setMetrics={setMetrics} />
        </>
      ) : (
        <>
          <h4 className="text-lg font-bold">Editing: {name}</h4>
          <MultipleExercisesSelect
            selectedExercises={exercises}
            exerciseType="text"
            onChange={(newExercises) => {
              setExercises(newExercises);
              saveExpertEvaluationConfig({ ...definedExpertEvaluationConfig, exercises: newExercises });
            }}
          />
          <MetricsForm
            metrics={metrics}
            setMetrics={(newMetrics) => {
              setMetrics(newMetrics);
              saveExpertEvaluationConfig({ ...definedExpertEvaluationConfig, metrics: newMetrics });
            }}
          />
        </>
      )}

      <div className="flex flex-row gap-2">
        <button
          className={twMerge(
            "bg-primary-500 text-white rounded-md p-2 mt-2 hover:bg-primary-600",
            !definedExpertEvaluationConfig ? "disabled:text-gray-500 disabled:bg-gray-200 disabled:cursor-not-allowed" : ""
          )}
          onClick={() => {
            if (definedExpertEvaluationConfig) {
              saveExpertEvaluationConfig(definedExpertEvaluationConfig);
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
                setExpertEvaluationConfigs((prevConfigs) =>
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