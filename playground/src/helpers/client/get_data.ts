import useSWR from "swr";

import { Exercise } from "@/model/exercise";
import { Mode } from "@/model/mode";
import { Submission } from "@/model/submission";
import baseUrl from "@/helpers/base_url";
import fetcher from "@/helpers/fetcher";

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
