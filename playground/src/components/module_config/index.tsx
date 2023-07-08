import { Dispatch, SetStateAction } from "react";
import ModuleExampleConfig from "./module_example";

type SetConfig = Dispatch<SetStateAction<any | undefined>>;

export type ModuleConfigProps = {
  moduleConfig: any | undefined;
  onChangeConfig: SetConfig;
};

type Modules = "module_example";

const moduleConfigComponents: {
  [key in Modules]: React.FC<ModuleConfigProps>;
} = {
  module_example: ModuleExampleConfig,
};

export function moduleConfigSelectorExists(moduleName: string): boolean {
  return Object.keys(moduleConfigComponents).includes(moduleName);
}

type Props = ModuleConfigProps & { moduleName: string };

export default function ModuleConfig({
  moduleConfig,
  onChangeConfig,
  moduleName,
}: Props) {
  const SelectedModule = moduleConfigComponents[moduleName as Modules];
  if (!SelectedModule) {
    return (
      <p className="text-gray-500">
        Module config selector for{" "}
        <code className="bg-gray-100 p-1 rounded-sm">{moduleName}</code> is not
        implemented.
      </p>
    );
  }
  return (
    <SelectedModule
      moduleConfig={moduleConfig}
      onChangeConfig={onChangeConfig}
    />
  );
}
