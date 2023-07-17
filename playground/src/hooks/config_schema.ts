import { UseQueryOptions, useQuery } from "react-query";
import { AthenaError, useAthenaFetcher } from "@/hooks/athena_fetcher";
import { ModuleMeta } from "@/model/health_response";
import ModuleResponse from "@/model/module_response";

/**
 * Fetches the config schema from an Athena module.
 *
 * @example
 * const { data, isLoading, error } = useConfigSchema(module);
 */
export function useConfigSchema<Data = ModuleResponse, Error = AthenaError>(
  module?: ModuleMeta,
  options: Omit<UseQueryOptions<Data, Error, Data>, 'queryFn'> = {}
) {
  const athenaFetcher = useAthenaFetcher(module);
  return useQuery<Data, Error, Data, any>({
    queryKey: ["config_schema", module?.name],
    queryFn: async () => {
      if (athenaFetcher === undefined) {
        throw new AthenaError("No module set.", 0, undefined);
      }
      return await athenaFetcher("/config_schema") as ModuleResponse;
    },
    ...options,
  });
}
