import { UseMutationOptions, useMutation } from "react-query";
import { AthenaError, useAthenaFetcher } from "@/hooks/athena_fetcher";
import { Exercise } from "@/model/exercise";
import { Submission } from "@/model/submission";
import ModuleResponse from "@/model/module_response";

/**
 * Request submission selection for an exercise from an Athena module.
 *
 * @example
 * const { data, isLoading, error, mutate } = useRequestSubmissionSelection();
 * mutate({ exercise, submissions });
 * 
 * @param options The react-query options.
 */
export default function useRequestSubmissionSelection(
  options: Omit<
    UseMutationOptions<ModuleResponse | undefined, AthenaError, { exercise: Exercise; submissions: Submission[] }>, 
    "mutationFn"
  > = {}
) {
  const athenaFetcher = useAthenaFetcher();
  return useMutation({
    mutationFn: async ({ exercise, submissions }) => {
      const submissionIds = submissions.map((submission) => submission.id)
      return await athenaFetcher("/select_submission", { exercise, submission_ids: submissionIds });
    },
    ...options,
  });
}
