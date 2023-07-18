import { useState } from "react";

import { ModuleMeta } from "@/model/health_response";
import Experiment from "@/model/experiment";
import DefineExperiment from "./define_experiment";
import InteractiveExperiment from "./interactive_experiment";

export default function EvaluationMode() {
  const [experiment, setExperiment] = useState<Experiment | undefined>(undefined);

  return (
    <>
      <h2 className="text-4xl font-bold text-white mb-4">Evaluation Mode</h2>
      {!experiment && <DefineExperiment onStartExperiment={setExperiment} />}
      {experiment && <InteractiveExperiment experiment={experiment} />}
    </>
  );
}
