import { UseMutationOptions, useMutation } from "react-query";
import { AthenaError, useAthenaFetcher } from "@/hooks/athena_fetcher";
import { Exercise } from "@/model/exercise";
import { Submission } from "@/model/submission";
import ModuleResponse from "@/model/module_response";

/**
 * Sends submissions for an exercise to an Athena module.
 *
 * @example
 * const { data, isLoading, error, mutate } = useSendSubmissions();
 * mutate({ exercise, submissions });
 * 
 * @param options The react-query options.
 */
export default function useSendSubmissions(
  options: Omit<
    UseMutationOptions<ModuleResponse | undefined, AthenaError, { exercise: Exercise; submissions: Submission[] }>,
    "mutationFn"
  > = {}
) {
  const athenaFetcher = useAthenaFetcher();
  return useMutation({
    mutationFn: async ({ exercise, submissions }) => {
      return await athenaFetcher("/submissions", { exercise, submissions });
    },
    ...options,
  });
}
