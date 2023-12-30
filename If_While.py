import copy
from Label import Label
from MultiLabel import MultiLabel
class If:
    def __init__(self, test, body, orelse, line_number):
        self.test = test
        self.body = body
        self.orelse = orelse
        self.line_number = line_number

    def __repr__(self):
        return f"If({self.test.__repr__()}, {[elem.__repr__() for elem in self.body]}, {[elem.__repr__() for elem in self.orelse]})"
    
    def eval(self, policy, multilabelling, vulnerabilities, multilabellingMaster):
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
        
        if_multilabelling = copy.deepcopy(multilabelling)
        else_multilabelling = copy.deepcopy(multilabelling)
        
        
        
        multilabelling_list_body_aux = [if_multilabelling]
        for body_element in self.body:
            for i in range(len(multilabelling_list_body_aux)):
                body_eval = body_element.eval(policy, multilabelling_list_body_aux[i], vulnerabilities, multilabellingMaster)
                
                if isinstance(body_element, If) or isinstance(body_element, While):
                    multilabelling_list_body_aux[i:i+1] = body_eval
                    i += len(body_eval) - 1
        
        multilabelling_list_else_aux = [else_multilabelling]
        for else_element in self.orelse:
            for i in range(len(multilabelling_list_else_aux)):
                else_eval = else_element.eval(policy, multilabelling_list_else_aux[i], vulnerabilities, multilabellingMaster)
                
                if isinstance(else_element, If) or isinstance(else_element, While):
                    multilabelling_list_else_aux[i:i+1] = else_eval
                    i += len(else_eval) - 1
        
        multilabelling_list_body_aux.extend(multilabelling_list_else_aux)
        
        return multilabelling_list_body_aux
    
class While:
    def __init__(self, test, body, line_number):
        self.test = test
        self.body = body
        self.line_number = line_number

    def __repr__(self):
        return f"While({self.test.__repr__()}, {[elem.__repr__() for elem in self.body]})"
    
    def eval(self, policy, multilabelling, vulnerabilities, multilabellingMaster):
        
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

        while_multilabellings = [copy.deepcopy(multilabelling)]
        
        for a in range(len(self.body)): # while é simulado a correr a vezes
            for element in self.body: # cada linha
                for i in range(len(while_multilabellings)): # é simulada em cada fluxo de execução
                    eval_result = element.eval(policy, while_multilabellings[i], vulnerabilities, multilabellingMaster)
                    
                    if isinstance(element, If) or isinstance(element, While):
                        while_multilabellings[i:i+1] = eval_result
                        i += len(eval_result) - 1

        result = [multilabelling]
        result.extend(while_multilabellings)

        return result