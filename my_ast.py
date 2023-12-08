import ast
import json

def extract_ast(filename):
    with open(filename, "r") as fp:
        py_str = fp.read()

    ast_py = ast.parse(py_str)
    return ast_to_dict(ast_py)

def ast_to_dict(node):
    if isinstance(node, ast.AST):
        node_dict = {'ast_type': type(node).__name__, 'lineno': getattr(node, 'lineno', None)}
        node_dict.update({field: ast_to_dict(getattr(node, field)) for field in node._fields})
        return node_dict
    elif isinstance(node, list):
        return [ast_to_dict(item) for item in node]
    else:
        return node

# Example usage:
filename = "hello_world.py"
ast_dict = extract_ast(filename)

# Print the JSON representation of the AST
print(json.dumps(ast_dict, indent=2))