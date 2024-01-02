import subprocess
import re
args = [
    ["slices\\1a-basic-flow.py", "slices\\1a-basic-flow.patterns.json"],
    ["slices\\1b-basic-flow.py", "slices\\1b-basic-flow.patterns.json"],
    ["slices\\2-expr-binary-ops.py", "slices\\2-expr-binary-ops.patterns.json"],
    ["slices\\3a-expr-func-calls.py", "slices\\3a-expr-func-calls.patterns.json"],
    ["slices\\3b-expr-func-calls.py", "slices\\3b-expr-func-calls.patterns.json"],
    ["slices\\3c-expr-attributes.py", "slices\\3c-expr-attributes.patterns.json"],
    ["slices\\4a-conds-branching.py", "slices\\4a-conds-branching.patterns.json"],
    ["slices\\4b-conds-branching.py", "slices\\4b-conds-branching.patterns.json"],
    ["slices\\5a-loops-unfolding.py", "slices\\5a-loops-unfolding.patterns.json"],
    ["slices\\5b-loops-unfolding.py", "slices\\5b-loops-unfolding.patterns.json"],
    ["slices\\5c-loops-unfolding.py", "slices\\5c-loops-unfolding.patterns.json"],
    ["slices\\6a-sanitization.py", "slices\\6a-sanitization.patterns.json"],
    ["slices\\6b-sanitization.py", "slices\\6b-sanitization.patterns.json"],
    ["slices\\7-conds-implicit.py", "slices\\7-conds-implicit.patterns.json"],
    ["slices\\8-loops-implicit.py", "slices\\8-loops-implicit.patterns.json"],
    ["slices\\9-regions-guards.py", "slices\\9-regions-guards.patterns.json"]
]

results = [
    "slices\\1a-basic-flow.output.json",
    "slices\\1b-basic-flow.output.json",
    "slices\\2-expr-binary-ops.output.json",
    "slices\\3a-expr-func-calls.output.json",
    "slices\\3b-expr-func-calls.output.json",
    "slices\\3c-expr-attributes.output.json",
    "slices\\4a-conds-branching.output.json",
    "slices\\4b-conds-branching.output.json",
    "slices\\5a-loops-unfolding.output.json",
    "slices\\5b-loops-unfolding.output.json",
    "slices\\5c-loops-unfolding.output.json",
    "slices\\6a-sanitization.output.json",
    "slices\\6b-sanitization.output.json",
    "slices\\7-conds-implicit.output.json",
    "slices\\8-loops-implicit.output.json",
    "slices\\9-regions-guards.output.json"
]

def run_test(input_args):
    try:
        process = subprocess.run(
            ["python", "Main.py", input_args[0], input_args[1]],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        output_lines = process.stdout.splitlines()[-1]
        output_json_str = output_lines.strip("[]").strip("'")
        output_json_str = output_json_str.replace("\\\'", "\"")
        pattern = re.compile(r'[^{},]+|{[^}]*}')
        matches = pattern.findall(output_json_str)
        result = [match.strip() for match in matches if match.strip()]
        cleaned_array = [s for s in result if s != "'"]        
        return cleaned_array
    except Exception as e:
        print(f"Error running {input_args}: {e}")
        return None



def compare_results(expected, actual):
    with open(expected, 'r') as file:
        objective = file.readline()

    objective = objective[1:-2]
    pattern = re.compile(r'[^{},]+|{[^}]*}')
    matches = pattern.findall(objective)
    objective = [match.strip() for match in matches if match.strip()]

    #remove check do unsanitized
    objective = [s.replace("\"unsanitized_flows\": \"yes\"", "")
                    .replace("\"unsanitized_flows\": \"no\"", "")
                    for s in objective]
    actual = [s.replace("\"unsanitized_flows\": \"yes\"", "")
                    .replace("\"unsanitized_flows\": \"no\"", "")
                    for s in actual]

    actual = set([s.split('source', 1)[1] if 'source' in s else s for s in actual])
    objective = set([s.split('source', 1)[1] if 'source' in s else s for s in objective])
    if actual == objective:
        print("test passed")
        return True
    else:
        print("test failed.")
        print("elements unique to our run:", actual.difference(objective))
        print("elements unique to objective:", objective.difference(actual))
        return False

def main():
    passed = 0
    for i, arg_set in enumerate(args):
        print("--------------------------------------------------------------------------")
        print(f"Running test {args[i][0]}")
        output_json = run_test(arg_set)
        if output_json is not None and compare_results(results[i], output_json):
            passed += 1
    print("--------------------------------------------------------------------------")
    print("passed " + str(passed) + "/" + str(len(args)) + " tests")
            

if __name__ == "__main__":
    main()
