from apted import APTED, Config
from module_programming_ast.convert_code_to_ast.antlr_to_apted_tree import parse_java_file, parse_python_file


#TODO Whitespace removing and caching

class FeedbackFocusedConfig(Config):
    def rename(self, node1, node2):
        # Adjusting the renaming costs depending on the node type
        if 'Var' in node1.name and 'Var' in node2.name:
            return 0  # Ignore variable renaming
        elif 'Literal' in node1.name and 'Literal' in node2.name:
            return 0.1  # Low costs for changes in literals
        elif 'Comment' in node1.name and 'Comment' in node2.name:
            return 0  # Ignore commmets
        return 1 if node1.name != node2.name else 0  # Standardkosten für andere Typen

    def insert(self, node):
        # Higher costs for inserting new control structures
        if 'Control' in node.name:
            return 2
        return 1

    def delete(self, node):
        # Higher costs for deleting new control structures
        if 'Control' in node.name:
            return 2
        return 1


def compute_ap_ted(tree1, tree2):
    apted = APTED(tree1, tree2, FeedbackFocusedConfig())
    ted = apted.compute_edit_distance()
    # To display mapping between those two predicates
    mapping = apted.compute_edit_mapping()

    print("MAPPING:")
    for i in mapping[1:]:
        print(i)

    print("\nTREE EDIT DISTANCE: {}".format(ted))
    return ted


if __name__ == "__main__":
    # Java to AST (from prev. JSON)
    java_ast1 = parse_java_file("../test_files/test2.java")
    java_ast2 = parse_java_file("../test_files/test3.java")

    code = """def process_numbers(numbers):
    total = 0
    for number in numbers:
        if number % 2 == 1:
            total += number
        else:
            total -= number
    if total > 0:
        print("Positive total:", total)
    else:
        print("Non-positive total:", total)"""

    code_java = ""

    code1 = parse_java_file(code_java)[0]
    code2 = parse_java_file(code_java)[0]

    # Call APTED-algorithm
    compute_ap_ted(code1, code2)
