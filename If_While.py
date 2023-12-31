import copy
from Constant import Constant
from Label import Label
from MultiLabel import MultiLabel
from Policy import Policy
from MultiLabelling import MultiLabelling
class If:
    def __init__(self, test, body, orelse, line_number):
        self.test = test
        self.body = body
        self.orelse = orelse
        self.line_number = line_number

    def __repr__(self):
        return f"If({self.test.__repr__()}, {[elem.__repr__() for elem in self.body]}, {[elem.__repr__() for elem in self.orelse]})"
    
    def eval(self, policy, multilabelling, vulnerabilities, multilabellingAssigned):
        test_eval = self.test.eval(policy, multilabelling, vulnerabilities, multilabellingAssigned)
        
        #check if some element in test_eval is an unknown var
        all_patterns = policy.getAllPatterns()
        for pattern in all_patterns:
            for test_eval_element in test_eval:
                if multilabelling.get_Multilabel(test_eval_element) != None and \
                            multilabelling.get_Multilabel(test_eval_element).get_label(pattern.get_vulnerability()) == None:
                    policy.addUninstantiatedVars(pattern.get_vulnerability(), test_eval_element)
                    new_label = Label()
                    new_label.add_source(test_eval_element, self.line_number)
                    multilabelling.get_Multilabel(test_eval_element).add_label(pattern.get_vulnerability(), new_label, policy, multilabellingAssigned)
        
        if_multilabelling = copy.deepcopy(multilabelling)
        else_multilabelling = copy.deepcopy(multilabelling)
        if_multilabelling_assigned = copy.deepcopy(multilabellingAssigned)
        else_multilabelling_assigned = copy.deepcopy(multilabellingAssigned)
        
        multilabelling_list_body_aux = [if_multilabelling]
        multilabelling_assigned_list_body_aux = [if_multilabelling_assigned]
        for body_element in self.body:
            for i in range(len(multilabelling_list_body_aux)):
                body_eval = body_element.eval(policy, multilabelling_list_body_aux[i], vulnerabilities, multilabelling_assigned_list_body_aux[i])
                
                if isinstance(body_element, If) or isinstance(body_element, While):
                    multilabelling_list_body_aux[i:i+1] = body_eval[0]
                    multilabelling_assigned_list_body_aux[i:i+1] = body_eval[1]
                    i += len(body_eval) - 1
        
        multilabelling_list_else_aux = [else_multilabelling]
        multilabelling_assigned_list_else_aux = [else_multilabelling_assigned]
        for else_element in self.orelse:
            for i in range(len(multilabelling_list_else_aux)):
                else_eval = else_element.eval(policy, multilabelling_list_else_aux[i], vulnerabilities, multilabelling_assigned_list_else_aux[i])
                
                if isinstance(else_element, If) or isinstance(else_element, While):
                    multilabelling_list_else_aux[i:i+1] = else_eval[0]
                    multilabelling_assigned_list_else_aux = else_eval[1]
                    i += len(else_eval) - 1
        
        multilabelling_list_body_aux.extend(multilabelling_list_else_aux)
        multilabelling_assigned_list_body_aux.extend(multilabelling_assigned_list_else_aux)
        
        return [multilabelling_list_body_aux, multilabelling_assigned_list_body_aux]


class While:
    def __init__(self, test, body, line_number):
        self.test = test
        self.body = body
        self.line_number = line_number

    def __repr__(self):
        return f"While({self.test.__repr__()}, {[elem.__repr__() for elem in self.body]})"
    
    def eval(self, policy, multilabelling, vulnerabilities, multilabellingAssigned):
        if not isinstance(self.test, Constant):
            test_eval = self.test.eval(policy, multilabelling, vulnerabilities, multilabellingAssigned)
            
            #check if some element in test_eval is an unknown var
            all_patterns = policy.getAllPatterns()
            for pattern in all_patterns:
                for test_eval_element in test_eval:
                    if multilabelling.get_Multilabel(test_eval_element) != None and \
                                multilabelling.get_Multilabel(test_eval_element).get_label(pattern.get_vulnerability()) == None:
                        policy.addUninstantiatedVars(pattern.get_vulnerability(), test_eval_element)
                        new_label = Label()
                        new_label.add_source(test_eval_element, self.line_number)
                        multilabelling.get_Multilabel(test_eval_element).add_label(pattern.get_vulnerability(), new_label, policy, multilabellingAssigned)

        while_multilabellings = [copy.deepcopy(multilabelling)]
        while_multilabellings_assigned = [copy.deepcopy(multilabellingAssigned)]
        notLists = True
        for a in range(len(self.body)): # while é simulado a correr a vezes
        #for a in range(1):
            for element in self.body: # cada linha
                for i in range(len(while_multilabellings)): # é simulada em cada fluxo de execução
                    if notLists:
                        multilabelling = MultiLabelling()
                        while_multilabellings = [multilabelling]
                        while_multilabellings_assigned = [multilabellingAssigned]
                        
                        for value, multilabel in multilabellingAssigned.multilabels_mapping.items(): 
                            copied_multilabel = copy.deepcopy(multilabel)
                            multilabelling.assign_Multilabel(value, copied_multilabel)
                        
                        eval_result = element.eval(policy, while_multilabellings[i], vulnerabilities, while_multilabellings_assigned[i])
                    else:
                        eval_result = element.eval(policy, while_multilabellings[i], vulnerabilities, while_multilabellings_assigned[i])
                    
                    if isinstance(element, If) or isinstance(element, While):
                        #while_multilabellings[i:i+1] = eval_result[0]
                        while_multilabellings_assigned[i:i+1] = eval_result[1]
                        while_multilabellings = copy.deepcopy(while_multilabellings_assigned)
                        i += len(eval_result) - 1
                        notLists = False
                        
        
        result_assigned = [multilabellingAssigned]
        result_assigned.extend(while_multilabellings_assigned)

        return [[], result_assigned]