import { UseMutationOptions, useMutation } from "react-query";
import { AthenaError, useAthenaFetcher } from "@/hooks/athena_fetcher";
import { ModuleMeta } from "@/model/health_response";
import { Exercise } from "@/model/exercise";
import { Submission } from "@/model/submission";
import Feedback from "@/model/feedback";
import ModuleResponse from "@/model/module_response";

/**
 * Sends feedback for an exercise and a submission to an Athena module.
 *
 * @example
 * const { data, isLoading, error, mutate } = useSendFeedback(module);
 * mutate({ exercise, submission, feedback });
 *
 * @param module The module to send the feedback to.
 * @param options The react-query options.
 */
export function useSendFeedback(
  module?: ModuleMeta,
  options: Omit<
    UseMutationOptions<
      ModuleResponse,
      AthenaError, 
      { exercise: Exercise; submission: Submission; feedback: Feedback; }
    >,
    "mutationFn"
  > = {}
) {
  const athenaFetcher = useAthenaFetcher(module);
  return useMutation({
    mutationFn: async ({ exercise, submission, feedback }) => {
      if (athenaFetcher === undefined) {
        throw new AthenaError("No module set.", 0, undefined);
      }
      return await athenaFetcher("/feedback", { exercise, submission, feedback });
    },
    ...options,
  });
}


/**
 * Sends feedbacks for an exercise and a submission to an Athena module.
 *
 * @example
 * const { data, isLoading, error, mutate } = useSendFeedbacks(module);
 * mutate([{ exercise, submission, feedback }]);
 *
 * @param module The module to send the feedbacks to.
 * @param options The react-query options.
 */
export function useSendFeedbacks(
  module?: ModuleMeta,
  options: Omit<
    UseMutationOptions<
      ModuleResponse[],
      AthenaError,
      { exercise: Exercise; submission: Submission; feedback: Feedback; }[]
    >,
    "mutationFn"
  > = {}
) {
  const athenaFetcher = useAthenaFetcher(module);
  return useMutation({
    mutationFn: async (items) => {
      if (athenaFetcher === undefined) {
        throw new AthenaError("No module set.", 0, undefined);
      }

      return await Promise.all(
        items.map(async ({ exercise, submission, feedback }) =>
          athenaFetcher("/feedback", { exercise, submission, feedback })
        )
      );
    },
    ...options,
  });
}
