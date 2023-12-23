import ast
import astexport.export

def extract_ast(slice):
    ast_py = ast.parse(slice)
    ast_dict = astexport.export.export_dict(ast_py)
    
    return ast_dict