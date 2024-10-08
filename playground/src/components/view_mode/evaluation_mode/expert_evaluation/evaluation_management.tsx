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
  const [creationDate, setCreationDate] = useState<Date | undefined>(undefined);
  const [metrics, setMetrics] = useState<Metric[]>([]);
  const [exercises, setExercises] = useState<Exercise[]>([]);
  const [expertIds, setExpertIds] = useState<string[]>([]);

  useEffect(() => {
    if (selectedConfigId === "new") {
      setName("");
      setCreationDate(new Date());
      setMetrics([]);
      setExercises([]);
    } else {
      const selectedConfig = expertEvaluationConfigs.find((config) => config.id === selectedConfigId);
      if (selectedConfig) {
        setName(selectedConfig.name);
        setCreationDate(selectedConfig.creationDate);
        setMetrics(selectedConfig.metrics);
        setExercises(selectedConfig.exercises);
      }
    }
  }, [selectedConfigId, expertEvaluationConfigs]);

  const getSelectedConfig = (): ExpertEvaluationConfig => {
    if (selectedConfigId === "new") {
      return {
        creationDate: creationDate || new Date(),
        type: "evaluation_config", id: uuidv4(), name, metrics, exercises, expertIds: []
      };
    } else {
      return (expertEvaluationConfigs.find((config) => config.id === selectedConfigId) || {
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

  return (<div className="bg-white rounded-md p-4 mb-8 space-y-2">
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
        className="border border-gray-300 rounded-md p-2"
        value={name}
        onChange={(e) => {
          setName(e.target.value);
          if (selectedConfigId !== "new") {
            saveExpertEvaluationConfig({ ...definedExpertEvaluationConfig, name: e.target.value });
          }
        }}
      />
    </label>

    <MultipleExercisesSelect
      selectedExercises={exercises}
      exerciseType="text"
      onChange={(newExercises) => {
        setExercises(newExercises);
        if (selectedConfigId !== "new") {
          saveExpertEvaluationConfig({ ...definedExpertEvaluationConfig, exercises: newExercises });
        }
      }}
    />

    <MetricsForm
      metrics={metrics}
      setMetrics={(newMetrics) => {
        setMetrics(newMetrics);
        if (selectedConfigId !== "new") {
          saveExpertEvaluationConfig({ ...definedExpertEvaluationConfig, metrics: newMetrics });
        }
      }}
    />

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
