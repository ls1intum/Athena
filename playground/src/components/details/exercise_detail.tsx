import { Exercise } from "@/model/exercise";
import Markdown from "@/components/markdown";
import Disclosure from "@/components/disclosure";

type ExerciseDetailProps = {
  exercise: Exercise;
};

export default function ExerciseDetail({ exercise }: ExerciseDetailProps) {
  return (
    <div className="space-y-2">
      {exercise.problem_statement.length > 0 ? (
        <Disclosure title="Problem Statement" openedInitially>
          <Markdown
            content={exercise.problem_statement}
            enablePlainTextSwitcher
          />
        </Disclosure>
      ) : (
        <span className="text-gray-500">No grading instructions available</span>
      )}
      <Disclosure title="Grading Instructions" openedInitially>
        {exercise.grading_instructions.length > 0 ? (
          <Markdown
            content={exercise.grading_instructions}
            enablePlainTextSwitcher
          />
        ) : (
          <span className="text-gray-500">
            No grading instructions available
          </span>
        )}
      </Disclosure>
      {exercise.type === 'text' && (
        <Disclosure title="Example Solution" openedInitially>
          {exercise.example_solution.length > 0 ? (
            <Markdown
              content={exercise.example_solution}
              enablePlainTextSwitcher
            />
          ) : (
            <span className="text-gray-500">
              No example solution available
            </span>
          )}
        </Disclosure>
      )}
    </div>
  );
}
