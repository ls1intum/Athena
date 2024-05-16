from antlr4 import FileStream, CommonTokenStream
from antlr4.tree.Tree import TerminalNodeImpl
from module_programming_ast.convert_code_to_ast.languages.python.Python3Lexer import Python3Lexer
from module_programming_ast.convert_code_to_ast.languages.python.Python3Parser import Python3Parser
from module_programming_ast.convert_code_to_ast.languages.java.JavaLexer import JavaLexer
from module_programming_ast.convert_code_to_ast.languages.java.JavaParser import JavaParser


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
    return to_ast(tree)


def parse_python_file(file_path):
    input_stream = FileStream(file_path)
    lexer = Python3Lexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = Python3Parser(stream)
    tree = parser.file_input()
    return to_ast(tree)


if __name__ == "__main__":
    file_path2 = "../test_files/test_java_1.java"
    ast2 = parse_java_file(file_path2)
    print(ast2)
