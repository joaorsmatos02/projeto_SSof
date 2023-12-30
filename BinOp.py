import Label
from MultiLabel import MultiLabel
class BinOp:
    def __init__(self, left, op, right, line_number):
        self.left = left
        self.op = op
        self.right = right
        self.line_number = line_number       

    def __repr__(self):
        return f"BinOp({self.left} , {self.op}, {self.right} )"
    
    def eval(self, policy, multilabelling, vulnerabilities, multilabellingAssigned):
        arguments = []
        print(repr(self))
        
        left_result = self.left.eval(policy, multilabelling, vulnerabilities, multilabellingAssigned)
        
        if isinstance(left_result, list):
            arguments.extend(left_result)
        else:
            arguments.append(left_result)
        
        right_result = self.right.eval(policy, multilabelling, vulnerabilities, multilabellingAssigned)
        
        if isinstance(right_result, list):
            arguments.extend(right_result)
        else:
            arguments.append(right_result)

        return arguments
        
        
        
        