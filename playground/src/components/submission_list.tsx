import { Exercise } from "@/model/exercise";
import { Mode } from "@/model/mode";
import Disclosure from "@/components/disclosure";
import SubmissionDetail from "@/components/details/submission_detail";
import { useSubmissions } from "@/helpers/client/get_data";

type SubmissionListProps = {
  exercise: Exercise;
  mode: Mode;
};

export default function SubmissionList({
  exercise,
  mode,
}: SubmissionListProps) {
  const {
    submissions,
    isLoading: isLoadingSubmissions,
    error: submissionsError,
  } = useSubmissions(mode, exercise);

  if (submissions) {
    return (
      <Disclosure
        title={`${submissions.length} Submission${
          submissions.length === 1 ? "" : "s"
        }`}
        className={{ content: "space-y-1" }}
      >
        {submissions.map((submission) => (
          <Disclosure
            title={`Submission ${submission.id}`}
            key={submission.id}
          >
            <SubmissionDetail key={submission.id} submission={submission} />
          </Disclosure>
        ))}
      </Disclosure>
    );
  }

  return (
    <>
      {submissions && (
        <Disclosure title="Submissions" className={{ content: "space-y-1" }}>
          {submissions.map((submission) => (
            <Disclosure
              title={`Submission ${submission.id}`}
              key={submission.id}
            >
              <SubmissionDetail key={submission.id} submission={submission} />
            </Disclosure>
          ))}
        </Disclosure>
      )}
      {submissionsError && (
        <div className="text-gray-500">Failed to load submissions</div>
      )}
      {isLoadingSubmissions && (
        <div className="text-gray-500">Loading submissions...</div>
      )}
    </>
  );
}
