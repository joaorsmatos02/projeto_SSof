import ast
import astexport.export

def extract_ast(filename):
    with open(filename, "r") as fp:
        py_str = fp.read()

    ast_py = ast.parse(py_str)
    ast_dict = astexport.export.export_dict(ast_py)
    
    return ast_dict