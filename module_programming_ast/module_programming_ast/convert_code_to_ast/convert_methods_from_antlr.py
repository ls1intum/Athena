from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker

from module_programming_ast.convert_code_to_ast.languages.java.JavaMethodParserListener import MethodParserListener, \
    ExtendedMethodParserListener, JAVA_METHOD_DECLARATIONS
from module_programming_ast.convert_code_to_ast.languages.java.JavaLexer import JavaLexer
from module_programming_ast.convert_code_to_ast.languages.java.JavaParser import JavaParser

#TODO: This is actually not really needed anymore?

def _get_tree_for(source_code: str):
    input_stream = InputStream(source_code)
    lexer = JavaLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = JavaParser(stream)
    return parser.compilationUnit()


def _get_methods_in_tree(tree):
    listener = MethodParserListener(JAVA_METHOD_DECLARATIONS)
    walker = ParseTreeWalker()
    walker.walk(listener, tree)
    return listener.methods.copy()


def extract_methods(source_code: str):
    tree = _get_tree_for(source_code)
    return _get_methods_in_tree(tree)


def extract_method_trees(source_code: str):
    tree = _get_tree_for(source_code)
    listener = ExtendedMethodParserListener(JAVA_METHOD_DECLARATIONS)
    walker = ParseTreeWalker()
    walker.walk(listener, tree)
    return listener.methods


if __name__ == '__main__':
    from pathlib import Path

    with Path("../test_files/test.java").open("r", encoding="utf-8") as f:
        code = f.read()
        print("Methods: ")
        method_trees = extract_method_trees(code)
        for method in method_trees:
            print(f"Method {method.name}: Start {method.line_start}, End {method.line_end}")
            print(f"Source Code:\n{method.source_code}")
            print(f"AST:\n{method.ast.toStringTree()}")
