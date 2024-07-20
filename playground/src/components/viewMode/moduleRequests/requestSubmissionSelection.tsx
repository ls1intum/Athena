import type { Exercise } from "@/model/exercise";
import type ModuleResponse from "@/model/moduleResponse";

import { useEffect, useState } from "react";

import { useBaseInfo } from "@/hooks/baseInfoContext";
import { useModule } from "@/hooks/moduleContext";
import useRequestSubmissionSelection from "@/hooks/athena/requestSubmissionSelection";
import useSubmissions from "@/hooks/playground/submissions";

import ExerciseSelect from "@/components/selectors/exerciseSelect";
import ModuleResponseView from "@/components/moduleResponseView";
import ExerciseDetail from "@/components/details/exerciseDetail";
import Disclosure from "@/components/disclosure";
import SubmissionDetail from "@/components/details/submissionDetail";
import SubmissionList from "@/components/submissionList";

export default function SelectSubmission() {
  const { module } = useModule();
  const { dataMode } = useBaseInfo();
  
  const [exercise, setExercise] = useState<Exercise | undefined>(undefined);
  const { data: submissions, isLoading: isLoadingSubmissions, error: errorSubmissions } = useSubmissions(exercise);
  const { data: response, isLoading, error, mutate, reset } = useRequestSubmissionSelection({
    onError: (error) => {
      console.error(error);
      alert(`Failed to request submission selection from Athena: ${error.message}. Is the URL correct?`);
    },
    onSuccess: () => {
      alert("Submission selection requested successfully!");
    },
  });
  
  useEffect(() => reset(), [exercise, reset]);
  useEffect(() => setExercise(undefined), [module, dataMode]);

  const responseSubmissionView = (response: ModuleResponse | undefined) => {
    if (!response || response.status !== 200 || typeof response.data !== "number") {
      return null;
    }
    const submissionId = response.data;
    const submission = submissions?.find(
      (submission) => submission.id === submissionId
    );
    return (
      submission && (
        <Disclosure
          title="Submission"
          openedInitially
          className={{ root: "ml-2" }}
        >
          <SubmissionDetail identifier="submission_selection" submission={submission} />
        </Disclosure>
      )
    );
  };

  return (
    <div className="bg-white rounded-md p-4 mb-8">
      <h3 className="text-2xl font-bold mb-4">
        Request Submission Selection from Athena
      </h3>
      <p className="text-gray-500 mb-4">
        Request the submission to grade next out out of many submissions from
        Athena. The LMS would usually call this right before a tutor can start
        grading a submission. The matching module for the exercise will receive
        the request at the function annotated with{" "}
        <code>@submission_selector</code>. The playground currently only allows
        requesting a choice between all submissions of an exercise, but the LMS
        can also request a choice between a subset of submissions. <br />
        <b>
          This endpoint will only work properly after the submissions have been
          sent to Athena before.
        </b>
      </p>
      <ExerciseSelect
        exerciseType={module.type}
        exercise={exercise}
        onChange={setExercise}
        disabled={isLoading}
      />
      {exercise && (
        <div className="space-y-1 mt-2">
          <ExerciseDetail exercise={exercise} />
          {errorSubmissions && <div className="text-gray-500 text-sm">Failed to load submissions</div>}
          {isLoadingSubmissions && <div className="text-gray-500 text-sm">Loading submissions...</div>}
          {submissions && <SubmissionList submissions={submissions}/>}
        </div>
      )}
      <ModuleResponseView response={response ?? (error?.asModuleResponse ? error.asModuleResponse() : undefined)}>
        {responseSubmissionView(response)}
      </ModuleResponseView>
      <button
        className="bg-primary-500 text-white rounded-md p-2 mt-4 hover:bg-primary-600 disabled:text-gray-500 disabled:bg-gray-200 disabled:cursor-not-allowed"
        onClick={() => {
          if (!exercise) {
            alert("Please select an exercise");
            return;
          }
          if (!submissions) {
            alert("Failed to fetch submissions or no submissions found");
            return;
          }
          mutate({
            exercise,
            submissions,
          });
        }}
        disabled={!exercise || isLoading || isLoadingSubmissions}
      >
        {exercise
          ? isLoading || isLoadingSubmissions
            ? "Loading..."
            : "Request submission selection"
          : "Please select an exercise"}
      </button>
    </div>
  );
}
