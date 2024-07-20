import type { Experiment } from "./defineExperiment";
import type { ModuleConfiguration } from "./configureModules";

import { useState } from "react";

import DefineExperiment from "./defineExperiment";
import ConfigureModules from "./configureModules";
import ConductExperiment from "./conductExperiment";

export default function EvaluationMode() {
  const [experiment, setExperiment] = useState<Experiment | undefined>(
    undefined
  );
  const [moduleConfigurations, setModuleConfigurations] = useState<
    ModuleConfiguration[] | undefined
  >(undefined);

  return (
    <>
      <h2 className="text-4xl font-bold text-white mb-4">Evaluation Mode</h2>
      <DefineExperiment
        experiment={experiment}
        onChangeExperiment={(experiment) => {
          setExperiment(experiment);
          setModuleConfigurations(undefined);
        }}
      />
      {experiment && (
        <>
          <ConfigureModules
            experiment={experiment}
            moduleConfigurations={moduleConfigurations}
            onChangeModuleConfigurations={setModuleConfigurations}
          />
          {moduleConfigurations && (
            <ConductExperiment
              experiment={experiment}
              moduleConfigurations={moduleConfigurations}
            />
          )}
        </>
      )}
    </>
  );
}
