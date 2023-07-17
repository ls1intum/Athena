import { UseMutationOptions, useMutation } from "react-query";
import { AthenaError, useAthenaFetcher } from "@/hooks/athena_fetcher";
import { ModuleMeta } from "@/model/health_response";
import ModuleResponse from "@/model/module_response";
import { Exercise } from "@/model/exercise";
import { Submission } from "@/model/submission";

/**
 * Sends submissions for an exercise to an Athena module.
 *
 * @example
 * const { data, isLoading, error } = useSendSubmissions(module);
 */
export function useSendSubmissions(
  module?: ModuleMeta,
  options: Omit<UseMutationOptions, 'mutationFn'> = {}
) {
  const athenaFetcher = useAthenaFetcher(module);

  return useMutation({
    mutationKey: ["send_submissions", module?.name],
    mutationFn: async ({ exercise, submissions }: { exercise: Exercise, submissions: Submission[] }) => {
      if (athenaFetcher === undefined) {
        throw new AthenaError("No module set.", 0, undefined);
      }
      return await athenaFetcher("/submissions", { exercise, submissions });
    },
    // ...options,    
  });


  // return useQuery<Data, Error, Data, any>({
  //   queryKey: ["config_schema", module?.name],
  //   queryFn: async () => {
  //     if (athenaFetcher === undefined) {
  //       throw new AthenaError("No module set.", 0, undefined);
  //     }
  //     return await athenaFetcher("/config_schema") as ModuleResponse;
  //   },
  //   ...options,
  // });
}
