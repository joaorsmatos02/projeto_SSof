import Label
import MultiLabel
class Expr:
    def __init__(self, values_dict, line_number):
        self.values_dict = values_dict
        self.line_number = line_number


    def __repr__(self):
        return f"Expr( {self.values_dict.__repr__()} )"
    
    def eval(self,  policy, multilabelling, vulnerabilities, multilabellingAssigned, implicit_multilabel):
        return self.values_dict.eval(policy, multilabelling, vulnerabilities, multilabellingAssigned, implicit_multilabel)