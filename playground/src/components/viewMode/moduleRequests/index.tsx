import type { ModuleMeta } from "@/model/healthResponse";

import { useState } from "react";

import { ModuleProvider } from "@/hooks/moduleContext";
import ModuleAndConfigSelect from "@/components/selectors/moduleAndConfigSelect";
import GetConfigSchema from "@/components/viewMode/moduleRequests/getConfigSchema";
import SendSubmissions from "@/components/viewMode/moduleRequests/sendSubmissions";
import SelectSubmission from "@/components/viewMode/moduleRequests/requestSubmissionSelection";
import SendFeedbacks from "@/components/viewMode/moduleRequests/sendFeedbacks";
import RequestFeedbackSuggestions from "@/components/viewMode/moduleRequests/requestFeedbackSuggestions";
import RequestEvaluation from "@/components/viewMode/moduleRequests/requestEvaluation";


export default function ModuleRequests() {
  const [moduleAndConfig, setModuleAndConfig] = useState<{ module: ModuleMeta; moduleConfig: any } | undefined>(undefined);

  return (
    <>
      <h2 className="text-4xl font-bold text-white mb-4">Module Requests</h2>
      <div className="bg-white rounded-md p-4 mb-8">
        <ModuleAndConfigSelect
          showOverrideCheckbox
          collapsibleConfig
          moduleAndConfig={moduleAndConfig}
          onChangeModuleAndConfig={setModuleAndConfig}
        />
      </div>
      {moduleAndConfig && (
        <ModuleProvider
          module={moduleAndConfig.module}
          moduleConfig={moduleAndConfig.moduleConfig}
        >
          <GetConfigSchema />
          <SendSubmissions />
          <SelectSubmission />
          <SendFeedbacks />
          <RequestFeedbackSuggestions />
          <RequestEvaluation />
        </ModuleProvider>
      )}
    </>
  );
}
