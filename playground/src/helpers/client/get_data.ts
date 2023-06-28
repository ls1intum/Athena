import useSWR from "swr";

import { Exercise } from "@/model/exercise";
import { Mode } from "@/model/mode";
import { Submission } from "@/model/submission";
import baseUrl from "@/helpers/base_url";
import fetcher from "@/helpers/fetcher";

export async function requestSubmissions(
  exercise: Exercise,
  mode: Mode
): Promise<Submission[]> {
  const response = await fetch(
    `${baseUrl}/api/mode/${mode}/exercise/${exercise.id}/submissions`
  );
  const submissions: Submission[] = await response.json();
  return submissions;
}

export async function requestSubmission(
  exercise: Exercise,
  mode: Mode,
  submissionId: number
): Promise<Submission | undefined> {
  const submissions = await requestSubmissions(exercise, mode);
  const submission = submissions.find((s) => s.id === submissionId);
  return submission;
}

export function useSubmissions(
  mode: Mode,
  exercise?: Exercise,
  submissionId?: number
) {
  const { data, error, isLoading } = useSWR(
    () => {
      if (exercise === undefined) {
        return null;
      } else {
        return [exercise.id, mode, submissionId];
      }
    },
    ([exerciseId, mode, submissionId]) => {
      return fetcher(
        `${baseUrl}/api/mode/${mode}/exercise/${exerciseId}/submissions`
      );
    }
  );

  return {
    submissions: data as Submission[] | undefined,
    isLoading,
    error,
  };
}
