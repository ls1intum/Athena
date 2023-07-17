import baseUrl from "@/helpers/base_url";
import { useBaseInfo } from "@/hooks/base_info_context";
import { ModuleMeta } from "@/model/health_response";
import ModuleResponse from "@/model/module_response";

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
 * const fetcher = useAthenaFetcher(module);
 * const data = await fetcher("request_feedback_suggestions", body);
 * 
 * @param module The module to fetch data from.
 * @returns A function that can be used to fetch data from the module or undefined if the module is not set.
 */
export function useAthenaFetcher(module?: ModuleMeta) {
  const { athenaUrl, athenaSecret, moduleConfig } = useBaseInfo();  

  if (!module) {
    return undefined;
  }

  return (
    async (moduleRoute: string, body?: any) => {
      const url = `${athenaUrl}/modules/${module.type}/${module.name}` + moduleRoute;
      const response = await fetch(
        `${baseUrl}/api/athena_request?${new URLSearchParams({
          url: url,
        })}`,
        {
          method: body ? "POST" : "GET",
          headers: {
            "Content-Type": "application/json",
            "X-API-Secret": athenaSecret,
            ...(moduleConfig && {
              "X-Module-Config": JSON.stringify(moduleConfig),
            }),
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
