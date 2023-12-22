import sys
import json

from Pattern import Pattern
from AST_parser import extract_ast


if __name__ == "__main__":
    #if len(sys.argv) < 2:
    #    print("usage: python main.py <slice-path> <pattern-path>")
    #    exit()

    #slicePath = "slices\\basic-flow.py"#sys.argv[1]
    slicePath = "slices\\Specification\\slices\\1a-basic-flow.patterns.json"#sys.argv[1]

    patternPath = "slices\\basic-flow.patterns.json"#sys.argv[2]

    ast = extract_ast(slicePath)
    
    with open(patternPath, 'r') as f:
        pattern = f.read()

    for p in json.loads(pattern):
        pattern = Pattern(p)
        print("aaa")
