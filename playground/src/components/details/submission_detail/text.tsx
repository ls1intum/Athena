import { TextSubmission } from "@/model/submission";
import Feedback from "@/model/feedback";
import Markdown from "@/components/markdown";
import FeedbackDetail from "@/components/details/feedback";
import FileEditor from "../code_view/file_editor";

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
      {/* <Markdown content={submission.content} enablePlainTextSwitcher /> */}
      <div className="h-[50vh]">
        <FileEditor content={submission.content} feedbacks={feedbacks} onFeedbackChange={() => {}} />
      </div>
      {feedbacks && feedbacks.length > 0 && (
        <div className="space-y-1 mt-2">
          {feedbacks.map((feedback) => (
            <FeedbackDetail key={feedback.id} feedback={feedback} />
          ))}
        </div>
      )}
    </>
  );
}
