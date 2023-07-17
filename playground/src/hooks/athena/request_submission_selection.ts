import { UseMutationOptions, useMutation } from "react-query";
import { AthenaError, useAthenaFetcher } from "@/hooks/athena_fetcher";
import { ModuleMeta } from "@/model/health_response";
import { Exercise } from "@/model/exercise";
import { Submission } from "@/model/submission";
import ModuleResponse from "@/model/module_response";

/**
 * Request submission selection for an exercise from an Athena module.
 *
 * @example
 * const { data, isLoading, error, mutate } = useRequestSubmissionSelection(module);
 * mutate({ exercise, submissions });
 * 
 * @param module The module to request the submission selection from.
 * @param options The react-query options.
 */
export default function useRequestSubmissionSelection(
  module?: ModuleMeta,
  options: Omit<
    UseMutationOptions<ModuleResponse, AthenaError, { exercise: Exercise; submissions: Submission[] }>,
    "mutationFn"
  > = {}
) {
  const athenaFetcher = useAthenaFetcher(module);
  return useMutation({
    mutationFn: async ({ exercise, submissions }) => {
      if (athenaFetcher === undefined) {
        throw new AthenaError("No module set.", 0, undefined);
      }
      const submissionIds = submissions.map((submission) => submission.id)
      return await athenaFetcher("/select_submission", { exercise, submission_ids: submissionIds });
    },
    ...options,
  });
}
