from apted import APTED, Config
from apted.helpers import Tree
from module_programming_ast.convert_code_to_ast.java_to_ast_distance import java_file_to_ast


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


def serialized_to_apted_string(node):
    # Get the node_type of the current node and include value if it's not null
    if node.get('value') is not None:
        result = f'{{{node["node_type"]}={node["value"]}'
    else:
        result = f'{{{node["node_type"]}'
    # If the node has children, recursively process each child and append to the result
    if 'children' in node and node['children']:
        for child in node['children']:
            result += serialized_to_apted_string(child)
    # Close the curly bracket for the current node
    result += '}'
    # returns following apted format {a{b}{c}}
    return result


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
    java_ast1 = java_file_to_ast("../test_files/test2.java")
    java_ast2 = java_file_to_ast("../test_files/test3.java")

    # Convert AST to APTED-Notation (String)
    apted_tree_string1 = serialized_to_apted_string(java_ast1)
    apted_tree_string2 = serialized_to_apted_string(java_ast2)

    # Convert APTED-Notation (String) to right type
    apted3 = Tree.from_text(apted_tree_string1)
    apted4 = Tree.from_text(apted_tree_string2)

    # Call APTED-algorithm
    compute_ap_ted(apted3, apted4)
