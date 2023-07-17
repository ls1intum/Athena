import useSWR from "swr";
import HealthResponse, { ModuleMeta } from "@/model/health_response";
import fetcher from "@/helpers/fetcher";
import baseUrl from "@/helpers/base_url";
import { useBaseInfo } from "@/hooks/base_info_context";


export default function ModuleSelect({
  module,
  onChange,
}: {
  module: ModuleMeta | undefined;
  onChange: (module: ModuleMeta) => void;
}) {
  const { athenaUrl } = useBaseInfo();
  const { data, error } = useSWR<HealthResponse>(
    `${baseUrl}/api/health?url=${encodeURIComponent(athenaUrl)}`,
    fetcher
  );
  if (error) return <div className="text-red-500 text-sm">Failed to load</div>;
  if (!data) return <div className="text-gray-500 text-sm">Loading...</div>;
  return (
    <label className="flex flex-col">
      <span className="text-lg font-bold">Module</span>
      <select
        className="border border-gray-300 rounded-md p-2"
        value={module?.name ?? ""}
        onChange={(e) => onChange(data.modules[e.target.value])}
      >
        <option value={""} disabled>
          Select a module
        </option>
        {Object.entries(data.modules).map(([moduleName, { healthy, type }]) => {
          return (
            <option key={moduleName} value={moduleName}>
              {moduleName}
              {healthy ? "" : " (not healthy!)"}
            </option>
          );
        })}
      </select>
    </label>
  );
}
