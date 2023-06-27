import { useEffect, useState } from "react";
import JSZip from "jszip";

import { ProgrammingExercise } from "@/model/exercise";
import { Mode } from "@/model/mode";

import Disclosure from "@/components/disclosure";
import { useFetchAndUnzip } from "@/helpers/fetch_and_unzip";
import FileTree from "@/components/details/repository/file_tree";

type ProgrammingExerciseDetailProps = {
  exercise: ProgrammingExercise;
  mode: Mode;
};

export default function ProgrammingExerciseDetail({
  exercise,
  mode,
}: ProgrammingExerciseDetailProps) {
  // exercise.solution_repository_url -> http://localhost:3000/playground/api/mode/example/exercise/1/data/solution.zip
  // exercise.template_repository_url -> ...
  // exercise.tests_repository_url -> ...
  const solution = useFetchAndUnzip(exercise.solution_repository_url);
  const template = useFetchAndUnzip(exercise.template_repository_url);
  const tests = useFetchAndUnzip(exercise.tests_repository_url);

  return (
    <>
      <Disclosure title="Template Repository">
        <FileTree tree={template.tree} />
      </Disclosure>
      <Disclosure title="Solution Repository">
        <FileTree tree={solution.tree} />
      </Disclosure>
      <Disclosure title="Tests Repository">
        <FileTree tree={tests.tree} />
      </Disclosure>
    </>
  );
}
