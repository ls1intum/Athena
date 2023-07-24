import type { Exercise } from "@/model/exercise";

import Disclosure from "@/components/disclosure";

import CommonExerciseDetail from "./common";
import TextExerciseDetail from "./text";
import ProgrammingExerciseDetail from "./programming";

type ExerciseDetailProps = {
  exercise: Exercise;
};

export default function ExerciseDetail({ exercise }: ExerciseDetailProps) {
  const specificExerciseDetail = (() => {
    switch (exercise.type) {
      case "text":
        return <TextExerciseDetail exercise={exercise} />;
      case "programming":
        return <ProgrammingExerciseDetail exercise={exercise} />;
      default:
        return null;
    }
  })();

  return (
    <Disclosure
      title="Exercise Detail"
      className={{ root: "mt-2", content: "space-y-1" }}
    >
      <>
        <CommonExerciseDetail exercise={exercise} />
        {specificExerciseDetail}
      </>
    </Disclosure>
  );
}
