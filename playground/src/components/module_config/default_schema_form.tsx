import { ModuleConfigProps } from '.';

export default function DefaultSchemaFormModuleConfig({ configOptions, onChangeConfig }: ModuleConfigProps) {
  return (
    <p>
      {JSON.stringify(configOptions, undefined, 2)}
    </p>
  );
};