import { RJSFSchema, UiSchema, FieldProps, RegistryFieldsType, Registry, toPathSchema, UIOptionsType, ValidatorType, PathSchema } from '@rjsf/utils';
import Form from '@rjsf/core';
import ReactMarkdown from "react-markdown";



export function getUISchema(validator: ValidatorType, schema: RJSFSchema, value: UIOptionsType) {
  const paths = toPathSchema(validator, schema, undefined, schema);
  function recursiveSetValueForPaths(paths: PathSchema) {
    const properties = Object.keys(paths).filter((path) => path !== "$name");
    if (properties.length === 0) {
      return value;
    }
    return {
      ...properties.reduce((acc, property) => {
        acc[property] = recursiveSetValueForPaths(paths[property]); 
        return acc;
      }
      , {}),
    }
  }
  return recursiveSetValueForPaths(paths);
}
  

export default Form;
