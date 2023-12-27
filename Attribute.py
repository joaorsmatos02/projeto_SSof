class Attribute:
    def __init__(self, value, attribute, line_number):
        self.value = value
        self.attribute = attribute 
        self.line_number = line_number

    def __repr__(self):
        return f"Attribute({self.value} , {self.attribute})"
    
    def eval(self, policy, multilabelling, vulnerabilities):
        print(repr(self))
        
        arguments = [self.value.eval(policy, multilabelling, vulnerabilities)]
        arguments.append(self.attribute.eval(policy, multilabelling, vulnerabilities))
        
        return self.attribute.eval(policy, multilabelling, vulnerabilities)
