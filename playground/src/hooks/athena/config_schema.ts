import { UseQueryOptions, useQuery } from "react-query";
import { AthenaError, useAthenaFetcher } from "@/hooks/athena_fetcher";
import { useBaseInfo } from "@/hooks/base_info_context";
import ModuleResponse from "@/model/module_response";

/**
 * Fetches the config schema from an Athena module.
 *
 * @example
 * const { data, isLoading, error } = useConfigSchema();
 * 
 * @param options The react-query options.
 */
export default function useConfigSchema(options: Omit<UseQueryOptions<ModuleResponse, Error, ModuleResponse>, 'queryFn'> = {}) {
  const { module } = useBaseInfo();
  const athenaFetcher = useAthenaFetcher();
  return useQuery<ModuleResponse, AthenaError, ModuleResponse, any>({
    queryKey: ["config_schema", module?.name],
    queryFn: async () => {
      return await athenaFetcher("/config_schema");
    },
    ...options,
  });
}
