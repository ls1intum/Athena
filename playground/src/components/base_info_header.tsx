import { Mode } from "@/model/mode";
import { ModuleMeta } from "@/model/health_response";

import Health from "@/components/health";
import ModuleSelect from "@/components/selectors/module_select";
import DataSelect from "@/components/selectors/data_select";
import ModuleConfig, {
  moduleConfigSelectorExists,
} from "@/components/module_config";
import Disclosure from "./disclosure";

type BaseInfoHeaderProps = {
  athenaUrl: string;
  onChangeAthenaUrl: (value: string) => void;
  athenaSecret: string;
  onChangeAthenaSecret: (value: string) => void;
  module: ModuleMeta | undefined;
  onChangeModule: (value: ModuleMeta) => void;
  moduleConfig: any | undefined;
  onChangeModuleConfig: (value: any | undefined) => void;
  mode: Mode;
  onChangeMode: (value: Mode) => void;
};

export default function BaseInfoHeader({
  athenaUrl,
  onChangeAthenaUrl,
  athenaSecret,
  onChangeAthenaSecret,
  module,
  onChangeModule,
  moduleConfig,
  onChangeModuleConfig,
  mode,
  onChangeMode,
}: BaseInfoHeaderProps) {
  return (
    <div className="bg-white rounded-md p-4 mb-8">
      <label className="flex flex-col">
        <span className="text-lg font-bold">Athena URL</span>
        <input
          className="border border-gray-300 rounded-md p-2"
          value={athenaUrl}
          onChange={(e) => onChangeAthenaUrl(e.target.value)}
        />
      </label>
      <Health url={athenaUrl} />
      <label className="flex flex-col mt-4">
        <span className="text-lg font-bold">Secret</span>
        <p className="text-gray-500 mb-2">
          This is the secret that you configured in Athena. It&apos;s optional
          for local development, but required for production setups.
        </p>
        <input
          className="border border-gray-300 rounded-md p-2"
          value={athenaSecret}
          placeholder="Optional, only required for production setups"
          onChange={(e) => onChangeAthenaSecret(e.target.value)}
        />
      </label>
      <br />
      <ModuleSelect
        url={athenaUrl}
        module={module}
        onChange={(value) => {
          onChangeModule(value);
          onChangeModuleConfig(undefined);
        }}
      />
      {module && (
        <div className="mt-2 space-y-1">
          {moduleConfigSelectorExists(module.name) ? (
            <>
              <p className="text-gray-500">
                This module has a custom configuration. You can use the default
                configuration or provide your own.
              </p>
              <label className="flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={moduleConfig !== undefined}
                  onChange={(e) => {
                    if (e.target.checked) {
                      onChangeModuleConfig({});
                    } else {
                      onChangeModuleConfig(undefined);
                    }
                  }}
                />
                <div className="ml-2 text-gray-700 font-normal">
                  Use custom module config
                </div>
              </label>
              {moduleConfig !== undefined && (
                <Disclosure title="Configuration" openedInitially>
                  <ModuleConfig
                    module={module}
                    athenaUrl={athenaUrl}
                    athenaSecret={athenaSecret}
                    moduleConfig={moduleConfig}
                    onChangeConfig={onChangeModuleConfig}
                  />
                </Disclosure>
              )}
            </>
          ) : (
            <p className="text-gray-500">
              This module does not have a custom configuration (selector)
              implemented.
            </p>
          )}
        </div>
      )}
      <br />
      <DataSelect mode={mode} onChangeMode={onChangeMode} />
    </div>
  );
}
