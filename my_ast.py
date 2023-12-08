import ast
import astexport.export
import json

def extract_ast(filename):
    with open(filename, "r") as fp:
        py_str = fp.read()

    ast_py = ast.parse(py_str)
    ast_dict = astexport.export.export_dict(ast_py)
    
    return ast_dict

# Example usage:
filename = "hello_world.py"
ast_dict = extract_ast(filename)

# Print the JSON representation of the AST
print(json.dumps(ast_dict, indent=2))