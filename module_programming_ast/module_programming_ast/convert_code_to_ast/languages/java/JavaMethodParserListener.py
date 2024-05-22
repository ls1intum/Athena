# Generated from JavaParser.g4 by ANTLR 4.11.1
from antlr4 import *

from module_programming_ast.convert_code_to_ast.method_node import MethodNode

JAVA_METHOD_DECLARATIONS = ["methodDeclaration", "constructorDeclaration", "genericMethodDeclaration",
                            "genericConstructorDeclaration"]


def capitalize_first_letter(s: str):
    return s[0].upper() + s[1:]


class MethodParserListener(ParseTreeListener):
    def __init__(self, method_declarations):
        self.methods = []
        for method_name in method_declarations:
            name = f"enter{capitalize_first_letter(method_name)}"
            setattr(self, name, self.make_enter(method_name))

    def make_enter(self, name):
        def enter(ctx):
            me = MethodNode(
                line_start=ctx.start.line,
                line_end=ctx.stop.line,
                # need to do it like this so that spaces are included:
                source_code=ctx.start.source[1].getText(ctx.start.start, ctx.stop.stop),
                name=None  # will be written later while parsing
            )
            self.methods.append(me)

        return enter

    def enterIdentifier(self, ctx: ParserRuleContext):
        if self.methods and self.methods[-1].name is None:
            self.methods[-1].name = ctx.getText()


class ExtendedMethodParserListener(MethodParserListener):
    def __init__(self, method_declarations):
        super().__init__(method_declarations)

    def make_enter(self, name):
        def enter(ctx):
            # Erstelle eine Instanz von MethodNode mit dem vollständigen AST
            me = MethodNode(
                line_start=ctx.start.line,
                line_end=ctx.stop.line,
                source_code=ctx.start.source[1].getText(ctx.start.start, ctx.stop.stop),
                name=name,  # Set the name of the method
                ast=ctx  # Save the tree
            )
            self.methods.append(me)

        return enter
