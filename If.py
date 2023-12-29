import Label
import MultiLabel
class If:
    def __init__(self, test, body, orelse, line_number):
        self.test = test
        self.body = body
        self.orelse = orelse
        self.line_number = line_number

    def __repr__(self):
        return f"If({self.test.__repr__()}, {[elem.__repr__() for elem in self.body]}, {[elem.__repr__() for elem in self.orelse]})"
    
    def eval(self, policy, multilabelling, vulnerabilities, multilabellingMaster):
        result = []
        
        test_eval = self.test.eval(policy, multilabelling, vulnerabilities, multilabellingMaster)
        
        if isinstance(test_eval, list):
            result.extend(test_eval)
        else:
            result.append(test_eval)
        
        result.extend(self.eval_elements(self.body, policy, multilabelling, vulnerabilities, multilabellingMaster))
        result.extend(self.eval_elements(self.orelse, policy, multilabelling, vulnerabilities, multilabellingMaster))
        return result

    def eval_elements(self, elements, policy, multilabelling, vulnerabilities, multilabellingMaster):
        evaluated_results = []
        
        for element in elements:
            element_eval = element.eval(policy, multilabelling, vulnerabilities, multilabellingMaster)
            
            if isinstance(element_eval, list):
                evaluated_results.extend(element_eval)
            else:
                evaluated_results.append(element_eval)
        
        return evaluated_results
