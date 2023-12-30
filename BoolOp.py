class BoolOp:
    def __init__(self, op, values, line_number):
        self.op = op
        self.values = values
        self.line_number = line_number       

    def __repr__(self):
        return f"BoolOp({self.op}, {self.values})"
    
    def eval(self, policy, multilabelling, vulnerabilities, multilabellingAssigned):
        print(repr(self))
        
        arguments = []
        for value in self.values:
            arguments.append(value.eval(policy, multilabelling, vulnerabilities, multilabellingAssigned))
        
        return arguments
        
        
        
        