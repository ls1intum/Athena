import { ProgrammingSubmission } from "@/model/submission";
import Feedback from "@/model/feedback";
import CodeView from "@/components/details/code_view";
import FeedbackDetail from "@/components/details/feedback";

type ProgrammingSubmissionDetailProps = {
  submission: ProgrammingSubmission;
  feedbacks?: Feedback[];
};

export default function ProgrammingSubmissionDetail({
  submission,
  feedbacks,
}: ProgrammingSubmissionDetailProps) {
  return (
    <>
      <CodeView repository_url={submission.repository_url} />
      {feedbacks?.map((feedback) => (
        <FeedbackDetail key={feedback.id} feedback={feedback} />
      ))}
    </>
  );
}
