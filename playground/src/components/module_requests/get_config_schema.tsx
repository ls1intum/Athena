import useConfigSchema from "@/hooks/athena/config_schema";
import ModuleResponseView from "@/components/module_response_view";
import { ModuleRequestProps } from ".";


export default function GetConfigSchema({ module }: ModuleRequestProps) {
  const { data, error, isLoading, refetch } = useConfigSchema(module, {
    onError: (error) => {
      alert(`Failed to get config from Athena: ${error.message}.\n\nIs the URL correct?`);
    },
    queryKey: ["config_schema", module.name, "module_requests"],
    retry: false,
    enabled: false
  });

  return (
    <div className="bg-white rounded-md p-4 mb-8">
      <h3 className="text-2xl font-bold mb-4">
        Get Config Schema{" "}
        <span className="text-gray-500 text-sm">(OPTIONAL)</span>
      </h3>
      <p className="text-gray-500 mb-4">
        Get a schema for config options of the module as json schema. The config
        complying to the schema can then be provided in the header of a request
        <code>X-Module-Config</code> to override the default values. The module can
        decorate one pydantic model with <code>@config_schema_provider</code> to provide
        the schema and should have default values set for all fields as default
        configuration. The configuration class can be appended to the function
        signature of all other decorators to provide the configuration to the
        function.
      </p>
      <ModuleResponseView response={data || error?.asModuleResponse()} />
      <button
        className="bg-primary-500 text-white rounded-md p-2 mt-4 hover:bg-primary-600"
        onClick={() => refetch()}
        disabled={isLoading}
      >
        {isLoading ? "Loading..." : "Get Config Schema"}
      </button>
    </div>
  );
}
