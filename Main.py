import sys
import json
from Pattern import Pattern
from AST_parser import extract_ast
from Constant import Constant
from Policy import Policy
from MultiLabelling import MultiLabelling
from UnaryOp import UnaryOp
from Vulnerability import Vulnerability
from Assign import Assign
from Call import Call
from Expr import Expr
from Name import Name
from BinOp import BinOp

def run_ast_dict(ast_dict):
    if ast_dict['ast_type'] == "Constant":
        return Constant(ast_dict["value"], ast_dict["end_lineno"])
    elif ast_dict['ast_type'] == "Name":    
        return Name(ast_dict["id"], ast_dict["end_lineno"])
    elif ast_dict['ast_type'] == "BinOp": 
        return BinOp(run_ast_dict(ast_dict["left"]), ast_dict["op"], run_ast_dict(ast_dict["right"]), ast_dict["end_lineno"])
    elif ast_dict['ast_type'] == "UnaryOp":  
        return UnaryOp(ast_dict["op"], run_ast_dict(ast_dict["operand"]), ast_dict["end_lineno"])
    elif ast_dict['ast_type'] == "BoolOp":    
        return
    elif ast_dict['ast_type'] == "Compare":     
        return
    elif ast_dict['ast_type'] == "Call":
        function_dict = run_ast_dict(ast_dict["func"])
        arguments_dict = [run_ast_dict(arg) for arg in ast_dict["args"]]
        return Call(function_dict, arguments_dict, ast_dict["end_lineno"])
    elif ast_dict['ast_type'] == "Attribute":    
        return 
    elif ast_dict['ast_type'] == "Expr":
        return Expr(run_ast_dict(ast_dict["value"]), ast_dict["end_lineno"])
    elif ast_dict['ast_type'] == "Assign":  
        target = run_ast_dict(ast_dict["targets"][0])
        values_dict = run_ast_dict(ast_dict["value"])
        return Assign(target, values_dict, ast_dict["end_lineno"])
    elif ast_dict['ast_type'] == "If":
        return
    elif ast_dict['ast_type'] == "While":         
        return
    

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py arg1 arg2")
        sys.exit(1)
        
    with open(sys.argv[1], "r") as f:
        slice_content = f.read()

    with open(sys.argv[2], "r") as fp:
        patterns = json.load(fp)

    pattern_dict = []

    for p in patterns:
        pattern = Pattern(p)
        pattern_dict.append(pattern)
        # Do something with the pattern if needed

    #Policy init
    policy = Policy(pattern_dict)
    multilabelling = MultiLabelling()
    vulnerability = Vulnerability(policy)

    ast_dict = extract_ast(slice_content)
    print(json.dumps(ast_dict, indent=4))
    
    ast_dict_body = ast_dict.get('body', [])
    tree = []
    for node in ast_dict_body :
        tree.append(run_ast_dict(node))
    
    print(tree)
    
    for line in tree:
        line.eval(policy, multilabelling, vulnerability)

    print(vulnerability.get_vulnerabilities_print())

# criar multilabel com os padroes do policy, passamos a policy e combinar labels quando temos dois argumentos, retornando, e no fim da linha atualizar multilabelling
# classes com mais de um argumento sem ser name e constant temos de chamar o eval do argumentos        