import sys
import json
import copy
from Attribute import Attribute
from BoolOp import BoolOp
from Compare import Compare
from If import If
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
from While import While


def run_ast_dict(ast_dict):
    if ast_dict['ast_type'] == "Constant":
        return Constant(ast_dict["value"], ast_dict["end_lineno"])
    elif ast_dict['ast_type'] == "Name":    
        return Name(ast_dict["id"], ast_dict["end_lineno"])
    elif ast_dict['ast_type'] == "BinOp": 
        return BinOp(run_ast_dict(ast_dict["left"]), ast_dict["op"]["ast_type"], run_ast_dict(ast_dict["right"]), ast_dict["end_lineno"])
    elif ast_dict['ast_type'] == "UnaryOp":  
        return UnaryOp(ast_dict["op"]["ast_type"], run_ast_dict(ast_dict["operand"]), ast_dict["end_lineno"])
    elif ast_dict['ast_type'] == "BoolOp":
        return BoolOp(ast_dict["op"]["ast_type"], list(map(lambda n: run_ast_dict(n), ast_dict["values"])), ast_dict["end_lineno"])
    elif ast_dict['ast_type'] == "Compare":     
        return Compare(run_ast_dict(ast_dict["left"]), ast_dict["ops"][0]["ast_type"], list(map(lambda n: run_ast_dict(n), ast_dict["comparators"])), ast_dict["end_lineno"])
    elif ast_dict['ast_type'] == "Call":
        function_dict = run_ast_dict(ast_dict["func"])
        arguments_dict = [run_ast_dict(arg) for arg in ast_dict["args"]]
        return Call(function_dict, arguments_dict, ast_dict["end_lineno"])
    elif ast_dict['ast_type'] == "Attribute":
        return Attribute(run_ast_dict(ast_dict["value"]), ast_dict['attr'], ast_dict["end_lineno"])
    elif ast_dict['ast_type'] == "Expr":
        return Expr(run_ast_dict(ast_dict["value"]), ast_dict["end_lineno"])
    elif ast_dict['ast_type'] == "Assign":  
        target = run_ast_dict(ast_dict["targets"][0])
        values_dict = run_ast_dict(ast_dict["value"])
        return Assign(target, values_dict, ast_dict["end_lineno"])
    elif ast_dict['ast_type'] == "If":
        return If(run_ast_dict(ast_dict["test"]), list(map(lambda n: run_ast_dict(n), ast_dict["body"])), list(map(lambda n: run_ast_dict(n), ast_dict["orelse"])), ast_dict["end_lineno"])
    elif ast_dict['ast_type'] == "While":         
        return While(run_ast_dict(ast_dict["test"]), list(map(lambda n: run_ast_dict(n), ast_dict["body"])), ast_dict["end_lineno"])
    

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

    #Policy init
    policy = Policy(pattern_dict)
    multilabellingMaster = MultiLabelling()
    vulnerability = Vulnerability(policy)

    ast_dict = extract_ast(slice_content)
    print(json.dumps(ast_dict, indent=4))
    
    ast_dict_body = ast_dict.get('body', [])
    tree = []
    for node in ast_dict_body :
        tree.append(run_ast_dict(node))
    
    print(tree)
    
    for line in tree:
        multilabelling = MultiLabelling()
        for value, multilabel in multilabellingMaster.multilabels_mapping.items(): 
            copied_multilabel = copy.deepcopy(multilabel)
            multilabelling.assign_Multilabel(value, copied_multilabel)

        line.eval(policy, multilabelling, vulnerability, multilabellingMaster)
    

    print(vulnerability.get_vulnerabilities_print())

# criar multilabel com os padroes do policy, passamos a policy e combinar labels quando temos dois argumentos, retornando, e no fim da linha atualizar multilabelling
# classes com mais de um argumento sem ser name e constant temos de chamar o eval do argumentos        