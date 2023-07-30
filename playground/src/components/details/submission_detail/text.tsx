import type { TextSubmission } from "@/model/submission";
import type { Feedback } from "@/model/feedback";

import FileEditor from "@/components/details/editor/file_editor";
import InlineFeedback from "@/components/details/editor/inline_feedback";
import { getOnFeedbackChange, getFeedbackReferenceType } from "@/model/feedback";

type TextSubmissionDetailProps = {
  submission: TextSubmission;
  feedbacks?: Feedback[];
  onFeedbacksChange?: (feedback: Feedback[]) => void;
  createNewFeedback: () => Feedback;
};

export default function TextSubmissionDetail({
  submission,
  feedbacks,
  onFeedbacksChange,
  createNewFeedback,
}: TextSubmissionDetailProps) {
  const unreferencedFeedbacks = feedbacks?.filter(
    (feedback) => getFeedbackReferenceType(feedback) === "unreferenced"
  );
  return (
    <>
      <div className="border border-gray-100 rounded-lg overflow-hidden">
        <FileEditor
          key={`submission-${submission.id}`}
          identifier={`submission-${submission.id}`}
          content={submission.content}
          autoHeight
          noFileFeedback
          feedbacks={feedbacks}
          onFeedbacksChange={onFeedbacksChange}
          createNewFeedback={createNewFeedback}
        />
      </div>
      {((unreferencedFeedbacks && unreferencedFeedbacks.length > 0) ||
        onFeedbacksChange) && (
        <div className="space-y-2 mt-5">
          <h3 className="ml-2 text-lg font-medium">Unreferenced Feedback</h3>
          {feedbacks?.map(
            (feedback) =>
              getFeedbackReferenceType(feedback) === "unreferenced" && (
                <InlineFeedback
                  key={feedback.id}
                  feedback={feedback}
                  onFeedbackChange={
                    onFeedbacksChange &&
                    getOnFeedbackChange(feedback, feedbacks, onFeedbacksChange)
                  }
                />
              )
          )}
          {onFeedbacksChange && (
            <button
              className="mx-2 my-1 border-2 border-primary-400 border-dashed text-primary-500 hover:text-primary-600 hover:bg-primary-50 hover:border-primary-500 rounded-lg font-medium max-w-3xl w-full py-2"
              onClick={() =>
                onFeedbacksChange([...(feedbacks ?? []), createNewFeedback()])
              }
            >
              Add feedback
            </button>
          )}
        </div>
      )}
    </>
  );
}
