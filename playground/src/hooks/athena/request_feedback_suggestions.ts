import { UseMutationOptions, useMutation } from "react-query";
import { AthenaError, useAthenaFetcher } from "@/hooks/athena_fetcher";
import { Exercise } from "@/model/exercise";
import { Submission } from "@/model/submission";
import ModuleResponse from "@/model/module_response";

/**
 * Requests feedback suggestions for an exercise and a submission from an Athena module.
 *
 * @example
 * const { data, isLoading, error, mutate } = useRequestFeedbackSuggestions();
 * mutate({ exercise, submission });
 * 
 * @param options The react-query options.
 */
export default function useRequestFeedbackSuggestions(
  options: Omit<
    UseMutationOptions<ModuleResponse | undefined, AthenaError, { exercise: Exercise; submission: Submission }>, 
    "mutationFn"
  > = {}
) {
  const athenaFetcher = useAthenaFetcher();
  return useMutation({
    mutationFn: async ({ exercise, submission }) => {
      return await athenaFetcher("/feedback_suggestions", { exercise, submission });
    },
    ...options,
  });
}
