import type { Exercise } from "@/model/exercise";
import type { Submission } from "@/model/submission";
import type ModuleResponse from "@/model/moduleResponse";

import { UseMutationOptions, useMutation } from "react-query";
import { AthenaError, useAthenaFetcher } from "@/hooks/athenaFetcher";
import { Feedback } from "@/model/feedback";

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
      let response = await athenaFetcher("/feedback_suggestions", { exercise, submission });
      if (response?.data) {
        response.data = response.data.map((feedback: Feedback, index: number) => {
          // Change variable names from camel case to snake case (change this in the future, index_start -> indexStart, index_end -> indexEnd)
          feedback = Object.fromEntries(
            Object.entries(feedback).map(([key, value]) => [key.replace(/[A-Z]/g, (letter) => `_${letter.toLowerCase()}`), value])
          ) as Feedback;

          feedback.id = Number(`${Date.now()}${String(index).padStart(3, "0")}`); // Good enough for the playground
          feedback.type = exercise.type;
          feedback.isSuggestion = true;
          return feedback;
        });
      }
      return response;
    },
    ...options,
  });
}
