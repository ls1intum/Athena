import { useEffect, useState } from "react";
import { v4 as uuidv4 } from "uuid";
import { downloadJSONFile } from "@/helpers/download";
import { twMerge } from "tailwind-merge";
import MetricsForm from "@/components/view_mode/evaluation_mode/expert_evaluation/metrics_form";
import { Exercise } from "@/model/exercise";
import { ExpertEvaluationConfig } from "@/model/expert_evaluation_config";
import { Metric } from "@/model/metric";
import MultipleExercisesSelect from "@/components/selectors/multiple_exercises_select";
import EvaluationConfigSelector from "@/components/selectors/evaluation_config_selector";
import {
  EvaluationManagementExportImport
} from "@/components/view_mode/evaluation_mode/expert_evaluation/evaluation_management_export_import";


export default function EvaluationManagement() {
  const [expertEvaluationConfigs, setExpertEvaluationConfigs] = useState<ExpertEvaluationConfig[]>([]);
  const [selectedConfigId, setSelectedConfigId] = useState<string>("new");
  const [name, setName] = useState<string>("");
  const [started, setStarted] = useState<boolean>(false); // This controls if the experiment is locked or not
  const [creationDate, setCreationDate] = useState<Date | undefined>(undefined);
  const [metrics, setMetrics] = useState<Metric[]>([]);
  const [exercises, setExercises] = useState<Exercise[]>([]);
  const [expertIds, setExpertIds] = useState<string[]>([]);

  useEffect(() => {
    if (selectedConfigId === "new") {
      setName("");
      setStarted(false);
      setCreationDate(new Date());
      setMetrics([]);
      setExercises([]);
    } else {
      const selectedConfig = expertEvaluationConfigs.find((config) => config.id === selectedConfigId);
      if (selectedConfig) {
        setName(selectedConfig.name);
        setStarted(selectedConfig.started);
        setCreationDate(selectedConfig.creationDate);
        setMetrics(selectedConfig.metrics);
        setExercises(selectedConfig.exercises);
      }
    }
  }, [selectedConfigId, expertEvaluationConfigs]);

  const getSelectedConfig = (): ExpertEvaluationConfig => {
    if (selectedConfigId === "new") {
      return {
        started: started,
        creationDate: creationDate || new Date(),
        type: "evaluation_config", id: uuidv4(), name, metrics, exercises, expertIds: []
      };
    } else {
      return (expertEvaluationConfigs.find((config) => config.id === selectedConfigId) || {
        started: false,
        creationDate: new Date(),
        type: "evaluation_config", id: uuidv4(), name: "", metrics: [], exercises: [], expertIds: [],
      });
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

  const startEvaluation = () => {
    if (confirm("Are you sure you want to start the evaluation? Once started, no further changes can be made to the configuration!")) {
      setStarted(true);
      saveExpertEvaluationConfig({ ...definedExpertEvaluationConfig, started: true });
    }
  };

  const inputDisabledStyle = started
    ? "bg-gray-100 text-gray-500 cursor-not-allowed"
    : "";  // Style for disabled input fields

  return (
    <div className="bg-white rounded-md p-4 mb-8 space-y-2">
      <div className="flex flex-row justify-between items-center">
        <h3 className="text-2xl font-bold">Manage Evaluations</h3>
        <EvaluationManagementExportImport
          definedExpertEvaluationConfig={definedExpertEvaluationConfig}
          handleExport={handleExport}
          handleImport={handleImport}
        />
      </div>

      <EvaluationConfigSelector
        selectedConfigId={selectedConfigId}
        setSelectedConfigId={setSelectedConfigId}
        expertEvaluationConfigs={expertEvaluationConfigs}
      />

      <label className="flex flex-col">
        <span className="text-lg font-bold">Evaluation Name</span>
        <input
          type="text"
          placeholder="Insert Evaluation Name"
          className={`border border-gray-300 rounded-md p-2 ${inputDisabledStyle}`}
          value={name}
          onChange={(e) => {
            if (!started) {  // Prevent changes if the experiment has started
              setName(e.target.value);
              if (selectedConfigId !== "new") {
                saveExpertEvaluationConfig({ ...definedExpertEvaluationConfig, name: e.target.value });
              }
            }
          }}
          disabled={started} // Disable if the experiment has started
        />
      </label>

      <MultipleExercisesSelect
        selectedExercises={exercises}
        exerciseType="text"
        onChange={(newExercises) => {
          if (!started) {  // Prevent changes if the experiment has started
            setExercises(newExercises);
            if (selectedConfigId !== "new") {
              saveExpertEvaluationConfig({ ...definedExpertEvaluationConfig, exercises: newExercises });
            }
          }
        }}
        disabled={started} // Disable if the experiment has started
      />

      <MetricsForm
        metrics={metrics}
        setMetrics={(newMetrics) => {
          if (!started) {  // Prevent changes if the experiment has started
            setMetrics(newMetrics);
            if (selectedConfigId !== "new") {
              saveExpertEvaluationConfig({ ...definedExpertEvaluationConfig, metrics: newMetrics });
            }
          }
        }}
        disabled={started} // Disable if the experiment has started
      />

      <div className="flex flex-row gap-2">
        <button
          className={twMerge(
            "bg-primary-500 text-white rounded-md p-2 mt-2 hover:bg-primary-600",
            !definedExpertEvaluationConfig || started ?
              "disabled:text-gray-500 disabled:bg-gray-200 disabled:cursor-not-allowed" : ""
          )}
          onClick={() => {
            if (definedExpertEvaluationConfig) {
              saveExpertEvaluationConfig(definedExpertEvaluationConfig);
            }
          }}
          disabled={started}  // Disable if the experiment has started
        >
          {selectedConfigId === "new" ? "Define Experiment" : "Save Changes"}
        </button>

        {selectedConfigId !== "new" && !started && (
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

        {!started && (
          <button
            className="bg-green-500 text-white rounded-md p-2 mt-2 hover:bg-green-600 disabled:bg-gray-300 disabled:text-gray-600 disabled:cursor-not-allowed"
            onClick={startEvaluation}
            disabled={started}
          >
            Start Evaluation
          </button>
        )}
      </div>
    </div>
  );
}