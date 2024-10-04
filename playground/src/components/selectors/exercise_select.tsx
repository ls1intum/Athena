import type { Exercise } from "@/model/exercise";
import useExercises from "@/hooks/playground/exercises";

type ExerciseSelectProps = {
  exercises?: Exercise[];
  exerciseType: string;
  onChange: (exercises: Exercise[]) => void;
  disabled?: boolean;
  multiple?: boolean;
};

export default function ExerciseSelect({
  exercises,
  exerciseType,
  onChange,
  disabled,
  multiple,
}: ExerciseSelectProps) {
  const { data, error, isLoading } = useExercises()
  if (error) return <div className="text-red-500 text-sm">Failed to load</div>;
  if (isLoading) return <div className="text-gray-500 text-sm">Loading...</div>;
  return (
    <label className="flex flex-col">
      {multiple ? (
        <>
         <span className="text-lg font-bold">Exercises</span>
          {data && data
            .sort((a: Exercise, b: Exercise) => a.id - b.id)
            .map((ex: Exercise) => {
              return ex.type === exerciseType ? (
                <label key={ex.id} className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    value={ex.id}
                    disabled={disabled}
                    onChange={(e) => {
                      if (e.target.checked) {
                        onChange([...(exercises ?? []), data.find((ex: Exercise) => ex.id === parseInt(e.target.value))!]);
                      } else {
                        onChange(exercises!.filter((ex) => ex.id !== parseInt(e.target.value)));
                      }
                    }}
                  />
                  {ex.id} {ex.type}{ex.type === "programming" ? ` (${ex.programming_language})` : ""}: {ex.title}
                </label>
              ) : null;
            })}
          </>
        ) : (
        <>
          <span className="text-lg font-bold">Exercise</span><select
          className="border border-gray-300 rounded-md p-2 disabled:opacity-50"
          value={exercises && exercises.length > 0 ? exercises[0]?.id ?? "" : ""}
          disabled={disabled}
          onChange={(e) => onChange([data!.find((ex: Exercise) => ex.id === parseInt(e.target.value))!])}
        >
          <option value={""} disabled>
            Select an exercise
          </option>
          {data && data
            .sort((a: Exercise, b: Exercise) => a.id - b.id)
            .map((ex: Exercise) => {
              return ex.type === exerciseType ? (
                <option key={ex.id} value={ex.id}>
                  {ex.id} {ex.type}{ex.type === "programming" ? ` (${ex.programming_language})` : ""}: {ex.title}
                </option>
              ) : null;
            })}
        </select>
        </>
      )}
    </label>
  );
}
