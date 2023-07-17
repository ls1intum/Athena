import { UseQueryOptions, useQuery } from "react-query";
import baseUrl from "@/helpers/base_url";
import { Exercise } from "@/model/exercise";
import { Feedback } from "@/model/feedback";
import { useBaseInfo } from "@/hooks/base_info_context";


/**
 * Fetches the feedbacks for an exercise of the playground.
 * 
 * @example
 * const { data, isLoading, error } = useFeedbacks(exercise);
 * 
 * @param exercise The exercise to fetch the feedbacks for.
 * @param options The react-query options.
 */
export function useExercises(
  exercise?: Exercise,
  options: Omit<UseQueryOptions<Feedback[], Error, Feedback[]>, 'queryFn'> = {}
) {
  const { mode } = useBaseInfo();

  return useQuery({
    queryKey: ["feedbacks", mode, exercise?.id],
    queryFn: async () => {
      if (exercise === undefined) {
        throw new Error("No exercise set.");
      }
      const response = await fetch(`${baseUrl}/api/mode/${mode}/exercise/${exercise.id}/feedbacks`);
      return await response.json() as Feedback[];
    },
    ...options
  });
}