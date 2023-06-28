import useSWR from "swr";
import { Mode } from "@/model/mode";
import { Exercise } from "@/model/exercise";
import { Submission } from "@/model/submission";
import Feedback from "@/model/feedback";
import baseUrl from "@/helpers/base_url";

export function useSubmissions(
  mode: Mode,
  exercise?: Exercise,
  submissionId?: number
) {
  const { data, error, isLoading } = useSWR(
    () => {
      if (exercise === undefined) {
        return null;
      } else {
        return [exercise.id, mode, submissionId];
      }
    },
    ([exerciseId, mode, submissionId]) => {
      return fetch(
        `${baseUrl}/api/mode/${mode}/exercise/${exerciseId}/submissions`
      ).then((res) => {
        if (submissionId !== undefined) {
          return res
            .json()
            .then((submissions) =>
              submissions.filter(
                (submission: Submission) => submission.id === submissionId
              )
            );
        } else {
          return res.json();
        }
      });
    }
  );

  return {
    submissions: data as Submission[] | undefined,
    isLoading,
    error,
  };
}

export function useFeedback(
  mode: Mode,
  exercise?: Exercise,
  submissionId?: number
) {
  const { data, error, isLoading } = useSWR(
    () => {
      if (exercise === undefined) {
        return null;
      } else {
        return [exercise.id, mode, submissionId];
      }
    },
    ([exerciseId, mode, submissionId]) => {
      return fetch(
        `${baseUrl}/api/mode/${mode}/exercise/${exerciseId}/feedbacks`
      ).then((res) => {
        if (submissionId !== undefined) {
          return res
            .json()
            .then((feedbacks) =>
              feedbacks.filter(
                (feedback: Feedback) => feedback.id === submissionId
              )
            );
        } else {
          return res.json();
        }
      });
    }
  );

  return {
    feedbacks: data as Feedback[] | undefined,
    isLoading,
    error,
  };
}
