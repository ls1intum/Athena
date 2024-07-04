from antlr4 import *
from Python3Lexer import Python3Lexer
from Python3Parser import Python3Parser
from Python3ParserVisitor import Python3ParserVisitor


class RemoveVariableNames(Python3ParserVisitor):
    def visitAtom(self, ctx):
        name_ctx = ctx.name()
        if name_ctx:
            token = name_ctx.getToken(Python3Parser.NAME, 0)
            if token:
                token.text = 'x'
        return self.visitChildren(ctx)


class CustomPythonVisitor(Python3ParserVisitor):
    def __init__(self):
        self.loop_count = 0
        self.if_count = 0
        self.method_count = 0

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
        self.method_count += 1
        return self.visitChildren(ctx)


def mutate(filename):
    input_stream = FileStream(filename)
    lexer = Python3Lexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = Python3Parser(stream)
    tree = parser.file_input()

    # Transform the AST
    transformer = RemoveVariableNames()
    transformer.visit(tree)

    return tree


level0 = []
level1 = []
level2 = []


def find_levels(node, parser, level=0):
    if level == 0:
        level0.append(node.toStringTree(recog=parser))
    elif level == 1:
        level1.append(node.toStringTree(recog=parser))
    elif level == 2:
        level2.append(node.toStringTree(recog=parser))

    for child in node.getChildren():
        if isinstance(child, ParserRuleContext):
            find_levels(child, parser, level=level + 1)


def get_children(node, parser):
    parent = node.toStringTree(recog=parser)
    children = [child.toStringTree(recog=parser) if isinstance(child, ParserRuleContext) else child.getText() for child
                in node.getChildren()]
    return parent, children


parents1 = []
parents2 = []
children1 = []
children2 = []


def get_parent_children_relation(root, parser, level=0):
    for child in root.getChildren():
        if isinstance(child, ParserRuleContext):
            p, c = get_children(child, parser)
            if level == 0:
                parents1.append(p)
                children1.append(c)
            elif level == 1:
                parents2.append(p)
                children2.append(c)
            get_parent_children_relation(child, parser, level + 1)


def analyze(filename, program_number="1"):
    input_tree = mutate(filename)

    parser = Python3Parser(CommonTokenStream(Python3Lexer(FileStream(filename))))

    visitor = CustomPythonVisitor()
    visitor.visit(input_tree)
    count_l = visitor.loop_count
    count_if = visitor.if_count
    count_f = visitor.method_count

    # Finden der Ebenen
    find_levels(input_tree, parser)

    # Eltern-Kind-Beziehungen finden
    get_parent_children_relation(input_tree, parser)

    counts = [count_l, count_if, count_f]
    levels = [level0, level1, level2]

    return counts, levels


if __name__ == "__main__":
    file_path = "../../../test_codes/test1a.py"
    counts, levels = analyze(file_path)
