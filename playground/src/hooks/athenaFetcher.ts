import type ModuleResponse from "@/model/moduleResponse";
import type { Module } from "@/hooks/moduleContext";

import baseUrl from "@/helpers/baseUrl";
import { useBaseInfo } from "@/hooks/baseInfoContext";
import { useModule } from "@/hooks/moduleContext";
import { useExperimentIdentifiers } from "@/hooks/experimentIdentifiersContext";

export class AthenaError extends Error {
  status: number;
  info: any;

  constructor(message: string, status: number, info: any) {
    super(message);
    this.name = "FetchError";
    this.status = status;
    this.info = info;
  }

  // Convenience method to create a ModuleResponse from this error.
  asModuleResponse(): ModuleResponse {
    return {
      module_name: "Unknown",
      status: this.status,
      data: this.message,
    };
  }
}

/**
 * Fetches data from an Athena module.
 * 
 * @example
 * const fetcher = useAthenaFetcher();
 * const data = await fetcher("request_feedback_suggestions", body);
 * 
 * @returns A function that can be used to fetch data from the module or that returns undefined if the module is not set.
 */
export function useAthenaFetcher() {
  const { module: contextModule, moduleConfig: contextModuleConfig } = useModule();
  const { athenaUrl, athenaSecret } = useBaseInfo();  
  const { experimentId, moduleConfigurationId, runId } = useExperimentIdentifiers();

  return (
    async (moduleRoute: string, body?: any, overrideModule?: Module) => {
      let targetModule = contextModule;
      let targetModuleConfig = contextModuleConfig;
      if (overrideModule) {
        targetModule = overrideModule.module;
        targetModuleConfig = overrideModule.moduleConfig;
      }

      const headers: { [key: string]: string } = {};
      if (targetModuleConfig) {
        headers["X-Module-Config"] = JSON.stringify(targetModuleConfig);
      }
      if (experimentId) {
        headers["X-Experiment-ID"] = experimentId;
      }
      if (moduleConfigurationId) {
        headers["X-Module-Configuration-ID"] = moduleConfigurationId;
      }
      if (runId) {
        headers["X-Run-ID"] = runId;
      }

      const url = `${athenaUrl}/modules/${targetModule.type}/${targetModule.name}${moduleRoute}`;
      const response = await fetch(
        `${baseUrl}/api/athenaRequest?${new URLSearchParams({
          url: url,
        })}`,
        {
          method: body ? "POST" : "GET",
          headers: {
            "Content-Type": "application/json",
            "Authorization": athenaSecret,
            ...headers,
          },
          ...(body && { body: JSON.stringify(body) }),
        }
      )
      if (!response.ok) {
        throw new AthenaError(
          "An error occurred while fetching the data.",
          response.status,
          await response.json()
        );
      }
      return response.json() as Promise<ModuleResponse>;
    }
  );
}
