import { ModuleConfigProps } from '.';

export default function ModuleExampleConfig({ configOptions, onChangeConfig }: ModuleConfigProps) {

  return (
    <p>
      {JSON.stringify(configOptions, undefined, 2)}
    </p>
  );
};