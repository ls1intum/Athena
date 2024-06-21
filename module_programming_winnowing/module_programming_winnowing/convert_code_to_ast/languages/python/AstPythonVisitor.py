import sys
from antlr4 import *
from Python3Lexer import Python3Lexer
from Python3Parser import Python3Parser
from Python3Visitor import Python3Visitor


# Custom visitor to count loops, if statements, and functions
class AstPythonVisitor(Python3Visitor):
    def __init__(self):
        self.loop_count = 0
        self.if_count = 0
        self.function_count = 0
        self.levels = {0: [], 1: [], 2: []}
        self.parents1 = []
        self.parents2 = []
        self.children1 = []
        self.children2 = []

    def visitWhile_stmt(self, ctx):
        self.loop_count += 1
        return self.visitChildren(ctx)

    def visitFor_stmt(self, ctx):
        self.loop_count += 1
        return self.visitChildren(ctx)

    def visitIf_stmt(self, ctx):
        self.if_count += 1
        return self.visitChildren(ctx)

    def visitFuncdef(self, ctx):
        self.function_count += 1
        return self.visitChildren(ctx)

    def visitChildrenWithLevel(self, node, level=0):
        if level <= 2:
            self.levels[level].append(node.getText())
        for child in node.getChildren():
            self.visitChildrenWithLevel(child, level + 1)

    def get_children(self, node):
        parent = node.getText()
        children = [child.getText() for child in node.getChildren()]
        return parent, children

    def get_parent_children_relation(self, node, level=0):
        for child in node.getChildren():
            p, c = self.get_children(child)
            if level == 0:
                self.parents1.append(p)
                self.children1.append(c)
            elif level == 1:
                self.parents2.append(p)
                self.children2.append(c)
            self.get_parent_children_relation(child, level + 1)


def main(filename):
    input_stream = FileStream(filename)
    lexer = Python3Lexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = Python3Parser(stream)
    tree = parser.file_input()

    visitor = AstPythonVisitor()
    visitor.visit(tree)

    # To find levels
    visitor.visitChildrenWithLevel(tree)

    # To find parent-children relationships
    visitor.get_parent_children_relation(tree)

    # Write counts to file
    program_number1 = sys.argv[1]
    filename_prognum = "program" + program_number1
    with open(f"{filename_prognum}_count.txt", "w") as output_file_counts:
        output_file_counts.write(f'{visitor.loop_count}\n')
        output_file_counts.write(f'{visitor.if_count}\n')
        output_file_counts.write(f'{visitor.function_count}\n')

    # Write levels to files
    with open(f"{filename_prognum}_lev0.txt", "w") as output_file_lev0:
        for ele in visitor.levels[0]:
            output_file_lev0.write(ele + '\n')

    with open(f"{filename_prognum}_lev1.txt", "w") as output_file_lev1:
        with open(f"{filename_prognum}_lev2.txt", "w") as output_file_lev2:
            for parent, children in zip(visitor.parents1, visitor.children1):
                output_file_lev1.write(parent + '\n')
                for child in children:
                    output_file_lev2.write(child + '\n')


if __name__ == "__main__":
    filename = sys.argv[2]
    main(filename)
