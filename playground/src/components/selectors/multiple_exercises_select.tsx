import type { Exercise } from "@/model/exercise";
import useExercises from "@/hooks/playground/exercises";

type ExpertEvaluationExerciseSelectProps = {
  selectedExercises: Exercise[];
  onChange: (exercises: Exercise[]) => void;
  exerciseType: string;
  disabled?: boolean;
};

export default function MultipleExercisesSelect({
  selectedExercises,
  onChange,
  exerciseType,
  disabled,
}: ExpertEvaluationExerciseSelectProps) {
  const { data, error, isLoading } = useExercises();

  if (error) {
    return <div className="text-red-500 text-sm">Failed to load exercises</div>;
  }

  if (isLoading) {
    return <div className="text-gray-500 text-sm">Loading exercises...</div>;
  }

  const availableExercises = data?.filter((ex: Exercise) => ex.type === exerciseType) ?? [];

  const handleCheckboxChange = (exercise: Exercise, isChecked: boolean) => {
    if (isChecked) {
      onChange([...selectedExercises, exercise]);
    } else {
      onChange(selectedExercises.filter((ex) => ex.id !== exercise.id));
    }
  };

  return (
    <label className="flex flex-col">
      <span className="text-lg font-bold">Exercises</span>
      {availableExercises.map((ex) => (
        <label key={ex.id} className="flex items-center gap-2">
          <input
            type="checkbox"
            checked={selectedExercises.some((selected) => selected.id === ex.id)}
            onChange={(e) => handleCheckboxChange(ex, e.target.checked)}
            disabled={disabled}
          />
          {ex.id} {ex.type}{ex.type === "programming" ? ` (${ex.programming_language})` : ""}: {ex.title}
        </label>
      ))}
    </label>
  );
}
