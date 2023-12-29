from Label import Label
from MultiLabel import MultiLabel
class While:
    def __init__(self, test, body, line_number):
        self.test = test
        self.body = body
        self.line_number = line_number

    def __repr__(self):
        return f"While({self.test.__repr__()}, {[elem.__repr__() for elem in self.body]})"
    
    def eval(self, policy, multilabelling, vulnerabilities, multilabellingMaster):
        result = []
        
        test_eval = self.test.eval(policy, multilabelling, vulnerabilities, multilabellingMaster)
        
        #check if some element in test_eval is an unknown var
        all_patterns = policy.getAllPatterns()
        for pattern in all_patterns:
            for test_eval_element in test_eval:
                if multilabelling.get_Multilabel(test_eval_element) != None and \
                            multilabelling.get_Multilabel(test_eval_element).get_label(pattern.get_vulnerability()) == None:
                    policy.addUninstantiatedVars(pattern.get_vulnerability(), test_eval_element)
                    new_label = Label()
                    new_label.add_source(test_eval_element, self.line_number)
                    multilabelling.get_Multilabel(test_eval_element).add_label(pattern.get_vulnerability(), new_label)
        
        if isinstance(test_eval, list):
            result.extend(test_eval)
        else:
            result.append(test_eval)
        
        result.extend(self.eval_elements(self.body, policy, multilabelling, vulnerabilities, multilabellingMaster))
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
