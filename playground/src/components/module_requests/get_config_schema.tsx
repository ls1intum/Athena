import { useState } from "react";

import { ModuleMeta } from "@/model/health_response";
import ModuleResponse from "@/model/module_response";
import baseUrl from "@/helpers/base_url";
import ModuleResponseView from "@/components/module_response_view";

import { ModuleRequestProps } from ".";

async function getConfig(
  athenaUrl: string,
  athenaSecret: string,
  module: ModuleMeta
): Promise<ModuleResponse | undefined> {
  try {
    const athenaConfigUrl = `${athenaUrl}/modules/${module.type}/${module.name}/config_schema`;
    const response = await fetch(
      `${baseUrl}/api/athena_request?${new URLSearchParams({
        url: athenaConfigUrl,
      })}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "X-API-Secret": athenaSecret,
          // No X-Module-Config here
        },
      }
    );
    if (response.status !== 200) {
      console.error(response);
      alert(`Athena responded with status code ${response.status}`);
      return {
        module_name: "Unknown",
        status: response.status,
        data: await response.text(),
      };
    }
    return await response.json();
  } catch (e) {
    console.error(e);
    alert(
      "Failed to get config from Athena: Failed to fetch. Is the URL correct?"
    );
  }
}

export default function GetConfigSchema({
  athenaUrl,
  athenaSecret,
  module,
}: ModuleRequestProps) {
  const [loading, setLoading] = useState<boolean>(false);
  const [response, setResponse] = useState<ModuleResponse | undefined>(
    undefined
  );

  return (
    <div className="bg-white rounded-md p-4 mb-8">
      <h3 className="text-2xl font-bold mb-4">
        Get Config Schema{" "}
        <span className="text-gray-500 text-sm">(OPTIONAL)</span>
      </h3>
      <p className="text-gray-500 mb-4">
        Get the module specific config options for the given module. This is
        usually used to get the available configuration options for the module
        which can then be used in the request header <code>X-Module-Config</code> to override the default
        config. The shape of the config and how it is used is specific to the
        module, however using a JSON schema is recommended. The selected
        module&apos;s function annotated with <code>@config_schema_provider</code> will
        be called to get the config.
      </p>
      <ModuleResponseView response={response} />
      <button
        className="bg-primary-500 text-white rounded-md p-2 mt-4 hover:bg-primary-600"
        onClick={() => {
          setLoading(true);
          getConfig(athenaUrl, athenaSecret, module)
            .then(setResponse)
            .finally(() => setLoading(false));
        }}
        disabled={loading}
      >
        {loading ? "Loading..." : "Get Config Schema"}
      </button>
    </div>
  );
}
