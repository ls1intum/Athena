import { ThemeProps, withTheme } from "@rjsf/core";
import TextAreaWidget from "./textarea_widget";

const theme: ThemeProps = {
  widgets: { textarea: TextAreaWidget },
};

const ThemedForm = withTheme(theme);
export default ThemedForm;
