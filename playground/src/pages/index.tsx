import React from "react";

import { useBaseInfo } from "@/hooks/baseInfoContext";
import BaseInfoHeader from "@/components/baseInfoHeader";
import ModuleRequests from "@/components/viewMode/moduleRequests";
import EvaluationMode from "@/components/viewMode/evaluationMode";

export default function Playground() {
  const { viewMode } = useBaseInfo();

  return (
    <main className='flex min-h-screen flex-col p-24'>
      <h1 className='text-6xl font-bold text-white mb-8'>Playground</h1>
      <BaseInfoHeader />
      {viewMode === "module_requests" && <ModuleRequests />}
      {viewMode === "evaluation_mode" && <EvaluationMode />}
    </main>
  );
}
