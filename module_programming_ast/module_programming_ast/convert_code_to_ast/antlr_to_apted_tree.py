from antlr4 import FileStream, CommonTokenStream
from antlr4.tree.Tree import TerminalNodeImpl, ParseTreeWalker
from module_programming_ast.convert_code_to_ast.languages.python.Python3Lexer import Python3Lexer
from module_programming_ast.convert_code_to_ast.languages.python.Python3Parser import Python3Parser
from module_programming_ast.convert_code_to_ast.languages.java.JavaLexer import JavaLexer
from module_programming_ast.convert_code_to_ast.languages.java.JavaParser import JavaParser
from module_programming_ast.convert_code_to_ast.languages.python.Python3MethodParserListener import MethodParserListener as PythonMethodParserListener
from module_programming_ast.convert_code_to_ast.languages.java.JavaMethodParserListener import MethodParserListener as JavaMethodParserListener


class ASTNode:
    def __init__(self, name):
        self.name = name
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def __repr__(self):
        return f"{self.name}{self.children}"


def to_ast(node):
    if isinstance(node, TerminalNodeImpl):
        return ASTNode(node.getText())
    ast_node = ASTNode(type(node).__name__.replace('Context', ''))
    for i in range(node.getChildCount()):
        ast_node.add_child(to_ast(node.getChild(i)))
    return ast_node


def parse_java_file(file_path):
    input_stream = FileStream(file_path)
    lexer = JavaLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = JavaParser(stream)
    tree = parser.compilationUnit()

    listener = JavaMethodParserListener(parser)
    walker = ParseTreeWalker()
    walker.walk(listener, tree)

    for method in listener.methods:
        print(f"Method name: {method.name}, Start line: {method.line_start}, End line: {method.line_end}")
        print(f"Source code:\n{method.source_code}\n")
        print(f"AST:\n{method.ast_string}\n")


def parse_python_file(file_path):
    input_stream = FileStream(file_path)
    lexer = Python3Lexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = Python3Parser(stream)
    tree = parser.file_input()
    # return to_ast(tree)

    listener = PythonMethodParserListener(parser)
    walker = ParseTreeWalker()
    walker.walk(listener, tree)

    for method in listener.methods:
        print(f"Method name: {method.name}, Start line: {method.line_start}, End line: {method.line_end}")
        print(f"Source code:\n{method.source_code}\n")
        print(f"AST:\n{method.ast_string}\n")


if __name__ == "__main__":
    #file_path2 = "../test_files/test_java_1.java"
    #parse_java_file(file_path2)

    file_path = "../test_files/test_python_1.py"
    parse_python_file(file_path)
