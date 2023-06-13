import { ModuleMeta } from "@/model/health_response";
import SendSubmissions from "@/components/normal_mode/send_submissions";
import SendFeedback from "@/components/normal_mode/send_feedback";
import RequestFeedbackSuggestions from "@/components/normal_mode/request_feedback_suggestions";
import SelectSubmission from "@/components/normal_mode/request_submission_selection";

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
