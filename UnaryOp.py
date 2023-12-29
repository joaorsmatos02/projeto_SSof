class UnaryOp:
    def __init__(self, op, operand, line_number):
        self.op = op
        self.operand = operand
        self.line_number = line_number       

    def __repr__(self):
        return f"UnaryOp({self.op} , {self.operand})"
    
    def eval(self, policy, multilabelling, vulnerabilities, multilabellingMaster):
        print(repr(self))
        
        arguments = []
        operand_result = self.operand.eval(policy, multilabelling, vulnerabilities, multilabellingMaster)
        
        if isinstance(operand_result, list):
            arguments.extend(operand_result)
        else:
            arguments.append(operand_result)
                
        return arguments
        
        
        