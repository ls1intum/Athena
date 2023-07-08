import { ThemeProps } from "@rjsf/core";
import widgets from "./widgets"
import templates from "./templates";
import fields from "./fields";


export const CustomTheme: {
   fields: ThemeProps["fields"];
   templates: ThemeProps["templates"];
   widgets: ThemeProps["widgets"];
 } = { // @ts-ignore
   fields, // @ts-ignore
   templates, // @ts-ignore
   widgets, 
};