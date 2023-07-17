import { UseMutationOptions, useMutation } from "react-query";
import { AthenaError, useAthenaFetcher } from "@/hooks/athena_fetcher";
import { ModuleMeta } from "@/model/health_response";
import { Exercise } from "@/model/exercise";
import { Submission } from "@/model/submission";
import ModuleResponse from "@/model/module_response";


/**
 * Sends submissions for an exercise to an Athena module.
 *
 * @example
 * const { data, isLoading, error, mutate } = useSendSubmissions(module);
 * mutate({ exercise, submissions });
 * 
 * @param module The module to send the submissions to.
 * @param options The react-query options.
 */
export default function useSendSubmissions(
  module?: ModuleMeta,
  options: Omit<
    UseMutationOptions<ModuleResponse, AthenaError, { exercise: Exercise; submissions: Submission[] }>,
    "mutationFn"
  > = {}
) {
  const athenaFetcher = useAthenaFetcher(module);
  return useMutation({
    mutationFn: async ({
      exercise,
      submissions,
    }) => {
      if (athenaFetcher === undefined) {
        throw new AthenaError("No module set.", 0, undefined);
      }
      return await athenaFetcher("/submissions", { exercise, submissions });
    },
    ...options,
  });
}
