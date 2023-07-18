import { useState } from "react";

import { ModuleMeta } from "@/model/health_response";
import { Exercise } from "@/model/exercise";
import ExerciseSelect from "@/components/selectors/exercise_select";


export default function EvaluationMode({ module }: { module: ModuleMeta }) {
  const [exercise, setExercise] = useState<Exercise | undefined>(undefined);

  return (
    <>
      <h2 className="text-4xl font-bold text-white mb-4">Evaluation Mode</h2>
      <div className="bg-white rounded-md p-4 mb-8">
        <h3 className="text-2xl font-bold mb-4">
          Define Experiment
        </h3>
        <ExerciseSelect
          exerciseType={module.type}
          exercise={exercise}
          onChange={setExercise}
          disabled={false}
        />
        <button
          className="bg-primary-500 text-white rounded-md p-2 mt-4 hover:bg-primary-600 disabled:text-gray-500 disabled:bg-gray-200 disabled:cursor-not-allowed"
          onClick={() => {
          }}
          disabled={!exercise}
        >
          {exercise
            ? "Start Experiment"
            : "Please select an exercise"
          }
        </button>
      </div>
    </>
  );
}
