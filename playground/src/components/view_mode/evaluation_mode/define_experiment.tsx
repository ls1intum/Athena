import Experiment from "@/model/experiment";
import ExerciseSelect from "@/components/selectors/exercise_select";
import { useState } from "react";
import { Exercise } from "@/model/exercise";
import useSubmissions from "@/hooks/playground/submissions";
import { useBaseInfo } from "@/hooks/base_info_context";
import useSendSubmissions from "@/hooks/athena/send_submissions";

type DefineExperimentProps = {
  onStartExperiment: (experiment: Experiment) => void;
};

export default function DefineExperiment({ onStartExperiment }: DefineExperimentProps) {
  const { module } = useBaseInfo();
  const [exercise, setExercise] = useState<Exercise | undefined>(undefined);
  const { data: submissions, isLoading: isLoadingSubmissions } = useSubmissions(exercise);
  const { mutate: sendSubmissions, isLoading: isLoadingSendSubmissions } = useSendSubmissions(module, {
    onSuccess: (_, { exercise, submissions}) => {
      onStartExperiment({
        exercise,
        submissions,
      });
    },
  })

  if (!module) {
    return null;
  }

  return (
    <div className="bg-white rounded-md p-4 mb-8">
      <h3 className="text-2xl font-bold mb-4">Define Experiment</h3>
      <ExerciseSelect
        exerciseType={module.type}
        exercise={exercise}
        onChange={setExercise}
      />
      <button
        className="bg-primary-500 text-white rounded-md p-2 mt-4 hover:bg-primary-600 disabled:text-gray-500 disabled:bg-gray-200 disabled:cursor-not-allowed"
        onClick={() => {
          if (!exercise) {
            alert("Please select an exercise");
            return;
          }
          if (!submissions) {
            alert("Failed to fetch submissions or no submissions found");
            return;
          }
          sendSubmissions({
            exercise,
            submissions,
          });
        }}
        disabled={!exercise || isLoadingSubmissions || isLoadingSendSubmissions}
      >
        {exercise
          ? (isLoadingSubmissions || isLoadingSendSubmissions)
            ? "Loading..."
            : "Start Experiment"
          : "Please select an exercise"}
      </button>
    </div>
  );
}
