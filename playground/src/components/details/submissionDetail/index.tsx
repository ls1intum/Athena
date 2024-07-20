import type { Submission } from "@/model/submission";
import type { Feedback } from "@/model/feedback";
import type { ManualRating } from "@/model/manualRating";

import TextSubmissionDetail from "./text";
import ProgrammingSubmissionDetail from "./programming";
import ModelingSubmissionDetail from "@/components/details/submissionDetail/modeling";

type SubmissionDetailProps = {
  identifier?: string;
  submission: Submission;
  feedbacks?: Feedback[];
  onFeedbacksChange?: (feedback: Feedback[]) => void;
  manualRatings?: ManualRating[];
  onManualRatingsChange?: (manualRatings: ManualRating[]) => void;
};

export default function SubmissionDetail({
  identifier,
  submission,
  feedbacks,
  onFeedbacksChange,
  manualRatings,
  onManualRatingsChange,
}: SubmissionDetailProps) {

  if (submission.type === "programming") {
    return (
      <ProgrammingSubmissionDetail
        identifier={identifier}
        submission={submission}
        feedbacks={feedbacks}
        onFeedbacksChange={onFeedbacksChange}
        manualRatings={manualRatings}
        onManualRatingsChange={onManualRatingsChange}
      />
    );
  } else if (submission.type === "text") {
    return (
      <TextSubmissionDetail
        identifier={identifier}
        submission={submission}
        feedbacks={feedbacks}
        onFeedbacksChange={onFeedbacksChange}
        manualRatings={manualRatings}
        onManualRatingsChange={onManualRatingsChange}
      />
    );
  } else if (submission.type === "modeling") {
    return (
      <ModelingSubmissionDetail
        identifier={identifier}
        submission={submission}
        feedbacks={feedbacks}
        onFeedbacksChange={onFeedbacksChange}
        manualRatings={manualRatings}
        onManualRatingsChange={onManualRatingsChange}
      />
    );
  } else {
    return null;
  }
}
