class Constant:
    def __init__(self, value, line_number):
        self.value = value
        self.line_number

    def __repr__(self):
        return f"Constant({self.value})"
    
    def eval(self, policy, multilabelling, vulnerabilities):

        print(repr(self))
        return None