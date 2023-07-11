import {
  RJSFSchema,
  toPathSchema,
  UIOptionsType,
  ValidatorType,
  PathSchema,
} from "@rjsf/utils";

export function getUISchema(
  validator: ValidatorType,
  schema: RJSFSchema,
  value: (property: string) => UIOptionsType
) {
  const paths = toPathSchema(validator, schema, undefined, schema);
  function recursiveSetValueForPaths(property: string, paths: PathSchema) {
    const properties = Object.keys(paths).filter((path) => path !== "$name");
    if (properties.length === 0) {
      return value(property);
    }
    return {
      ...properties.reduce((acc, property) => {
        acc[property] = recursiveSetValueForPaths(property, paths[property]!);
        return acc;
      }, {} as UIOptionsType),
    };
  }
  return recursiveSetValueForPaths("__root__", paths);
}
