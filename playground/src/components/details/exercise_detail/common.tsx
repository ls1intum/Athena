import type { Exercise } from "@/model/exercise";

import Markdown from "@/components/markdown";
import Disclosure from "@/components/disclosure";

export default function CommonExerciseDetail({ exercise }: { exercise: Exercise; }) {
  return (
    <>
      <div className="text-gray-500 font-medium">
        {exercise.max_points} Points and {exercise.bonus_points} Bonus Points
      </div>
      {/* Problem Statement */}
      <Disclosure title="Problem Statement">
        {exercise.problem_statement.length > 0 ? (
          <Markdown
            content={exercise.problem_statement}
            enablePlainTextSwitcher
          />
        ) : (
          <span className="text-gray-500">No problem statement available</span>
        )}
      </Disclosure>

      {/* Grading Instructions */}
      <Disclosure title="Grading Instructions">
        {exercise.grading_instructions?.length > 0 ? (
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
    </>
  );
}
