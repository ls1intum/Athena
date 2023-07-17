import { UseMutationOptions, useMutation } from "react-query";
import { AthenaError, useAthenaFetcher } from "@/hooks/athena_fetcher";
import { ModuleMeta } from "@/model/health_response";
import { Exercise } from "@/model/exercise";
import { Submission } from "@/model/submission";
import ModuleResponse from "@/model/module_response";

/**
 * Requests feedback suggestions for an exercise and a submission from an Athena module.
 *
 * @example
 * const { data, isLoading, error, mutate } = useRequestFeedbackSuggestions(module);
 * mutate({ exercise, submission });
 * 
 * @param module The module to request the feedback suggestions from.
 * @param options The react-query options.
 */
export default function useRequestFeedbackSuggestions(
  module?: ModuleMeta,
  options: Omit<
    UseMutationOptions<ModuleResponse, AthenaError, { exercise: Exercise; submission: Submission }>,
    "mutationFn"
  > = {}
) {
  const athenaFetcher = useAthenaFetcher(module);
  return useMutation({
    mutationFn: async ({ exercise, submission }) => {
      if (athenaFetcher === undefined) {
        throw new AthenaError("No module set.", 0, undefined);
      }
      return await athenaFetcher("/feedback_suggestions", { exercise, submission });
    },
    ...options,
  });
}
