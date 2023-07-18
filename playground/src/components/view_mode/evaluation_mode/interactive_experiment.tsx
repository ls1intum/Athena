import { useState } from "react";
import SubmissionDetail from "@/components/details/submission_detail";
import useRequestSubmissionSelection from "@/hooks/athena/request_submission_selection";
import { useBaseInfo } from "@/hooks/base_info_context";
import Experiment from "@/model/experiment";
import Feedback from "@/model/feedback";
import { Submission } from "@/model/submission";
import ExerciseDetail from "@/components/details/exercise_detail";
import { Allotment } from "allotment";
import useRequestFeedbackSuggestions from "@/hooks/athena/request_feedback_suggestions";

export default function InteractiveExperiment({
  experiment,
}: {
  experiment: Experiment;
}) {
  const { module } = useBaseInfo();
  const { mutate: selectSubmission, isLoading: isLoadingSubmissionSelection } = useRequestSubmissionSelection(module);
  const { mutate: requestFeedbackSuggestions, isLoading: isLoadingFeedbackSuggestions } = useRequestFeedbackSuggestions(module);
  const [submissionsAndFeedbacks, setSubmissionsAndFeedbacks] = useState<
    { submission: Submission; feedbacks: Feedback[] }[]
  >([]);
  const [currentIndex, setCurrentSubmissionIndex] = useState(-1);

  return (
    <div className="bg-white rounded-md p-4 mb-8 space-y-4">
      <h3 className="text-2xl font-bold">Interactive Experiment</h3>
      <div className="flex flex-row space-x-2">
        <button
          className="bg-primary-500 text-white rounded-md p-2 hover:bg-primary-600 disabled:text-gray-500 disabled:bg-gray-200 disabled:cursor-not-allowed"
          onClick={() => {
            if (currentIndex <= 0) {
              return;
            }
            setCurrentSubmissionIndex(currentIndex - 1);
          }}
        >
          Previous
        </button>
        <button
          className="bg-primary-500 text-white rounded-md p-2 hover:bg-primary-600 disabled:text-gray-500 disabled:bg-gray-200 disabled:cursor-not-allowed"
          onClick={() => {
            const nextIndex = currentIndex + 1;
            if (currentIndex >= submissionsAndFeedbacks.length - 1) {
              if (isLoadingSubmissionSelection) {
                return;
              } else if (
                submissionsAndFeedbacks.length < experiment.submissions.length
              ) {
                const submissionsToSelectFrom = experiment.submissions.filter(
                  (submission) => {
                    return !submissionsAndFeedbacks.some(
                      (submissionAndFeedback) => {
                        return (
                          submissionAndFeedback.submission.id === submission.id
                        );
                      }
                    );
                  }
                );
                selectSubmission(
                  {
                    exercise: experiment.exercise,
                    submissions: submissionsToSelectFrom,
                  },
                  {
                    onSuccess: (reponse) => {
                      const { data: submissionId } = reponse as {
                        data: number;
                      };
                      const submission = submissionsToSelectFrom.find(
                        (submission) => submission.id === submissionId
                      );
                      if (!submission) {
                        throw new Error("Failed to find submission");
                      }
                      requestFeedbackSuggestions({ exercise: experiment.exercise, submission },
                        {
                          onSuccess: (response) => {
                            const { data: feedbacks } = response as { data: Feedback[] };
                            setSubmissionsAndFeedbacks([
                              ...submissionsAndFeedbacks,
                              { submission, feedbacks },
                            ]);
                            setCurrentSubmissionIndex(nextIndex);
                          }
                        }
                      );
                    },
                  }
                );
              }
            } else {
              setCurrentSubmissionIndex(nextIndex);
            }
          }}
        >
          Next
        </button>
      </div>
      <div className="h-screen">
        <Allotment vertical={false} >
        <div className="mr-4">
          {submissionsAndFeedbacks[currentIndex]?.submission ? (
              <SubmissionDetail
                submission={submissionsAndFeedbacks[currentIndex]?.submission}
                feedbacks={submissionsAndFeedbacks[currentIndex]?.feedbacks}
              />
          ) : (
            <p className="text-gray-500">
              No submission selected. Please click next to select a submission.
            </p>
          )
        }
          </div>
          <div className="ml-4">
            <ExerciseDetail exercise={experiment.exercise} hideDisclosure openedInitially />
          </div>
        </Allotment>
      </div>
      {/* 3. Feedback suggestions */}
      {/* 4. Assessment */}
      {/* 5. Send feedback */}
      {/* Go to 2. */}
      {/* <SubmissionDetail submission={selectedSubmission} feedbacks={} /> */}
    </div>
  );
}
