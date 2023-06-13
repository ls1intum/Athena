import { ModuleMeta } from "@/model/health_response";
import SendSubmissions from "./send_submissions";
import SendFeedback from "./send_feedback";
import RequestFeedbackSuggestions from "./request_feedback_suggestions";
import SelectSubmission from "./submission_select";

export default function NormalMode({
  athenaUrl,
  athenaSecret,
  module,
}: {
  athenaUrl: string;
  athenaSecret: string;
  module: ModuleMeta;
}) {
  return (
    <>
      <SendSubmissions
        athenaUrl={athenaUrl}
        athenaSecret={athenaSecret}
        module={module}
      />
      <SelectSubmission
        athenaUrl={athenaUrl}
        athenaSecret={athenaSecret}
        module={module}
      />
      <SendFeedback
        athenaUrl={athenaUrl}
        athenaSecret={athenaSecret}
        module={module}
      />
      <RequestFeedbackSuggestions
        athenaUrl={athenaUrl}
        athenaSecret={athenaSecret}
        module={module}
      />
    </>
  );
}
