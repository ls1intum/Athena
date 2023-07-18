import { ProgrammingExercise } from "@/model/exercise";
import Disclosure from "@/components/disclosure";
import CodeView from "@/components/details/code_view";

type ProgrammingExerciseDetailProps = {
  exercise: ProgrammingExercise;
  openedInitially?: boolean;
};

export default function ProgrammingExerciseDetail({ exercise, openedInitially }: ProgrammingExerciseDetailProps) {
  return (
    <>
      <Disclosure title="Template Repository" openedInitially={openedInitially}>
        <CodeView repository_url={exercise.template_repository_url} />
      </Disclosure>
      <Disclosure title="Solution Repository" openedInitially={openedInitially}>
        <CodeView repository_url={exercise.solution_repository_url} />
      </Disclosure>
      <Disclosure title="Tests Repository" openedInitially={openedInitially}>
        <CodeView repository_url={exercise.tests_repository_url} />
      </Disclosure>
    </>
  );
}
