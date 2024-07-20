import { ThemeProps, withTheme } from "@rjsf/core";
import TextAreaWidget from "./textareaWidget";
import DescriptionField from "./descriptionField";

const theme: ThemeProps = {
  widgets: { textarea: TextAreaWidget },
  templates: {
    DescriptionFieldTemplate: DescriptionField,
  }
};

const ThemedForm = withTheme(theme);
export default ThemedForm;
