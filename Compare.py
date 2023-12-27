class Compare:
    def __init__(self, left, ops, comparators, line_number):
        self.left = left
        self.ops = ops
        self.comparators = comparators
        self.line_number = line_number       

    def __repr__(self):
        return f"Compare({self.left} , {self.ops}, {self.comparators} )"
    
    def eval(self, policy, multilabelling, vulnerabilities):
        print(repr(self))
        
        arguments = [self.left.eval(policy, multilabelling, vulnerabilities)]
        for value in self.comparators:
            arguments.append(value.eval(policy, multilabelling, vulnerabilities))
        
        return arguments
        
        
        