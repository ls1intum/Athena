import type { Exercise } from "@/model/exercise";
import type { DataMode } from "@/model/dataMode";

import { UseQueryOptions, useQuery } from "react-query";
import baseUrl from "@/helpers/baseUrl";
import { useBaseInfo } from "@/hooks/baseInfoContext";

export async function fetchExercises(dataMode: DataMode) {
  const response = await fetch(`${baseUrl}/api/data/${dataMode}/exercises`);
  return await response.json() as Promise<Exercise[]>;
}

/**
 * Fetches the exercises of the playground.
 * 
 * @example
 * const { data, isLoading, error } = useExercises();
 * 
 * @param options The react-query options.
 */
export default function useExercises(
  options: Omit<UseQueryOptions<Exercise[], Error, Exercise[]>, 'queryFn'> = {}
) {
  const { dataMode } = useBaseInfo();

  return useQuery({
    queryKey: ["exercises", dataMode],
    queryFn: async () => {
      return await fetchExercises(dataMode);
    },
    ...options
  });
}