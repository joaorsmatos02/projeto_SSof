import sys
import json
from Pattern import Pattern
from AST_parser import extract_ast

if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        slice_content = f.read()

    with open(sys.argv[2], "r") as fp:
        patterns = json.load(fp)

    # Print patterns
    print(json.dumps(patterns, indent=4))

    for p in patterns:
        pattern = Pattern(p)
        # Do something with the pattern if needed

    ast_dict = extract_ast(slice_content)

    print(ast_dict)
