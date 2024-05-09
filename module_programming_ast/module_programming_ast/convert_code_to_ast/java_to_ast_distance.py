import javalang

class ASTNode:
    def __init__(self, node_type, role=None, value=None):
        self.node_type = node_type
        self.role = role
        self.value = value
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)


def serialize_node(node, parent=None):
    if isinstance(node, javalang.ast.Node):
        # Create AST node
        ast_node = ASTNode(node_type=type(node).__name__)
        if parent:
            parent.add_child(ast_node)

        # Print node information
        print(f"Node Type: {ast_node.node_type}")
        if ast_node.role:
            print(f"Role: {ast_node.role}")
        if ast_node.value:
            print(f"Value: {ast_node.value}")

        # Convert node to a dictionary including its class name and attributes
        for attr in node.attrs:
            value = getattr(node, attr)
            if isinstance(value, javalang.ast.Node):
                serialize_node(value, parent=ast_node)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, javalang.ast.Node):
                        serialize_node(item, parent=ast_node)
            else:
                setattr(ast_node, attr, value)

        return ast_node
    elif isinstance(node, list):
        for item in node:
            serialize_node(item, parent=parent)
    elif isinstance(node, set):
        for item in node:
            serialize_node(item, parent=parent)


def java_file_to_ast(java_file_path):
    with open(java_file_path, 'r') as java_file:
        java_code = java_file.read()

    tree = javalang.parse.parse(java_code)

    root_node = ASTNode(node_type="CompilationUnit")
    serialize_node(tree, parent=root_node)

    # Convert AST to a dictionary for JSON serialization
    serialized_tree = {
        "node_type": root_node.node_type,
        "children": [serialize_ast_node(child) for child in root_node.children]
    }
    # Returns the serialized AST for Java
    return serialized_tree

def serialize_ast_node(ast_node):
    serialized_node = {
        "node_type": ast_node.node_type,
        "role": ast_node.role,
        "value": ast_node.value,
        "children": [serialize_ast_node(child) for child in ast_node.children]
    }
    return serialized_node


# Conversion from AST Json to APTED-Notation



