import { TextSubmission } from "@/model/submission";
import Feedback from "@/model/feedback";
import Markdown from "@/components/markdown";
import FeedbackDetail from "@/components/details/feedback";

type TextSubmissionDetailProps = {
  submission: TextSubmission;
  feedbacks?: Feedback[];
};

export default function TextSubmissionDetail({
  submission,
  feedbacks,
}: TextSubmissionDetailProps) {
  return (
    <>
      <Markdown content={submission.content} enablePlainTextSwitcher />
      {feedbacks?.map((feedback) => (
        <FeedbackDetail key={feedback.id} feedback={feedback} />
      ))}
    </>
  );
}
