import {
  Submission,
  isProgrammingSubmission,
  isTextSubmission,
} from "@/model/submission";

import TextSubmissionDetail from "./text";
import ProgrammingSubmissionDetail from "./programming";

type SubmissionDetailProps = {
  submission: Submission;
};

export default function SubmissionDetail({
  submission,
}: SubmissionDetailProps) {
  if (isProgrammingSubmission(submission)) {
    return <ProgrammingSubmissionDetail submission={submission} />;
  } else if (isTextSubmission(submission)) {
    return <TextSubmissionDetail submission={submission} />;
  } else {
    return null;
  }
}
