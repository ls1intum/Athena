import { ProgrammingSubmission } from "@/model/submission";
import CodeView from "@/components/details/code_view";

type ProgrammingSubmissionDetailProps = {
  submission: ProgrammingSubmission;
};

export default function ProgrammingSubmissionDetail({
  submission,
}: ProgrammingSubmissionDetailProps) {
  return <CodeView repository_url={submission.repository_url} />;
}
