import { TextSubmission } from "@/model/submission";
import Markdown from "@/components/markdown";

type TextSubmissionDetailProps = {
  submission: TextSubmission;
};

export default function TextSubmissionDetail({
  submission,
}: TextSubmissionDetailProps) {
  return <Markdown content={submission.content} enablePlainTextSwitcher />;
}
