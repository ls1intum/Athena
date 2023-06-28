import { Exercise } from "@/model/exercise";
import { Mode } from "@/model/mode";

import CommonExerciseDetail from "./common";
import TextExerciseDetail from "./text";
import ProgrammingExerciseDetail from "./programming";

type ExerciseDetailProps = {
  exercise: Exercise;
  mode: Mode;
};

export default function ExerciseDetail({ exercise, mode }: ExerciseDetailProps) {

  const specificExerciseDetail = (() => {
    switch (exercise.type) {
      case "text":
        return <TextExerciseDetail exercise={exercise}/>;
      case "programming":
        return <ProgrammingExerciseDetail exercise={exercise} mode={mode}/>;
      default:
        return null;
    }
  })();

  return (
    <div className="space-y-1">
      <CommonExerciseDetail exercise={exercise} />
      {specificExerciseDetail}
    </div>
  );
}
