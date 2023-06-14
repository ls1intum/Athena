import { ModuleMeta } from "@/model/health_response";
import SendSubmissions from "@/components/module_requests/send_submissions";
import SendFeedback from "@/components/module_requests/send_feedback";
import RequestFeedbackSuggestions from "@/components/module_requests/request_feedback_suggestions";
import SelectSubmission from "@/components/module_requests/request_submission_selection";
import { Mode } from "@/model/mode";

export type ModuleRequestProps = {
  mode: Mode;
  athenaUrl: string;
  athenaSecret: string;
  module: ModuleMeta;
};

export default function ModuleRequests(props: ModuleRequestProps) {
  return (
    <>
      <SendSubmissions {...props} />
      <SelectSubmission {...props} />
      <SendFeedback {...props} />
      <RequestFeedbackSuggestions {...props} />
    </>
  );
}
