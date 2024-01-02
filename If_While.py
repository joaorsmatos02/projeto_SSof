import copy
from Constant import Constant
from Label import Label
from MultiLabel import MultiLabel
from Policy import Policy
from MultiLabelling import MultiLabelling
from Compare import Compare
class If:
    def __init__(self, test, body, orelse, line_number):
        self.test = test
        self.body = body
        self.orelse = orelse
        self.line_number = line_number

    def __repr__(self):
        return f"If({self.test.__repr__()}, {[elem.__repr__() for elem in self.body]}, {[elem.__repr__() for elem in self.orelse]})"
    
    def eval(self, policy, multilabelling, vulnerabilities, multilabellingAssigned, implicit_multilabel):
        if not isinstance(self.test, Constant):
            test_eval = self.test.eval(policy, multilabelling, vulnerabilities, multilabellingAssigned, MultiLabelling())
            
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

                
                for pattern in policy.get_patterns_implicit():
                    for value_in_condition in test_eval:
                        if if_multilabelling.get_Multilabel(value_in_condition) != None and if_multilabelling.get_Multilabel(value_in_condition).get_label(pattern.get_vulnerability()) != None: 
                            value_in_condition_label = copy.deepcopy(if_multilabelling.get_Multilabel(value_in_condition).get_label(pattern.get_vulnerability()))
                            value_multilabel = MultiLabel()
                            value_multilabel.add_label(pattern.get_vulnerability(), value_in_condition_label, policy, if_multilabelling_assigned)
                            implicit_multilabel.update_Multilabel(value_in_condition, value_multilabel, policy, if_multilabelling_assigned)


                body_eval = body_element.eval(policy, multilabelling_list_body_aux[i], vulnerabilities, multilabelling_assigned_list_body_aux[i], implicit_multilabel)
                
                if isinstance(self.test, Compare):
                    for pattern in policy.get_patterns_implicit(): 
                        if "()" not in body_eval[0]:
                            for value_in_condition in test_eval:
                                if if_multilabelling.get_Multilabel(value_in_condition) != None and if_multilabelling.get_Multilabel(value_in_condition).get_label(pattern.get_vulnerability()) != None:
                                    value_in_condition_label = copy.deepcopy(if_multilabelling.get_Multilabel(value_in_condition).get_label(pattern.get_vulnerability()))
                                    body_label = copy.deepcopy(if_multilabelling.get_Multilabel(body_eval[0]).get_label(pattern.get_vulnerability()).combine_labels(value_in_condition_label, policy, pattern.get_vulnerability(), if_multilabelling_assigned))
                                    body_multilabel = MultiLabel()
                                    body_multilabel.add_label(pattern.get_vulnerability(), body_label, policy, if_multilabelling_assigned)
                                    if_multilabelling_assigned.update_Multilabel(body_eval[0], body_multilabel, policy, if_multilabelling_assigned)
                                

                if isinstance(body_element, If) or isinstance(body_element, While):
                    multilabelling_list_body_aux[i:i+1] = body_eval[0]
                    multilabelling_assigned_list_body_aux[i:i+1] = body_eval[1]
                    i += len(body_eval) - 1
        
        multilabelling_list_else_aux = [else_multilabelling]
        multilabelling_assigned_list_else_aux = [else_multilabelling_assigned]
        for else_element in self.orelse:
            for i in range(len(multilabelling_list_else_aux)):
                else_eval = else_element.eval(policy, multilabelling_list_else_aux[i], vulnerabilities, multilabelling_assigned_list_else_aux[i], MultiLabelling())
                
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
    
    def eval(self, policy, multilabelling, vulnerabilities, multilabellingAssigned, implicit_multilabel):
        if not isinstance(self.test, Constant):
            test_eval = self.test.eval(policy, multilabelling, vulnerabilities, multilabellingAssigned, implicit_multilabel)
            
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
        auxBool = True
        for a in range(len(self.body)): # while é simulado a correr a vezes
        #for a in range(1):
            for element in self.body: # cada linha
                for i in range(len(while_multilabellings)): # é simulada em cada fluxo de execução
                    if notLists:
                        if not isinstance(self.test, Constant):
                            for test_eval_element in test_eval:
                               if multilabelling.get_Multilabel(test_eval_element) == None:
                                   auxBool = False
                                       
                        if auxBool:
                            for value, multilabel in while_multilabellings[0].multilabels_mapping.items(): 
                                copied_multilabel = copy.deepcopy(multilabel)
                                multilabelling.assign_Multilabel(value, copied_multilabel)    
                        else:
                            multilabelling = MultiLabelling()
                        while_multilabellings = [multilabelling]
                        while_multilabellings_assigned = [multilabellingAssigned]
                        
                        for value, multilabel in multilabellingAssigned.multilabels_mapping.items(): 
                            copied_multilabel = copy.deepcopy(multilabel)
                            multilabelling.assign_Multilabel(value, copied_multilabel)

                        for pattern in policy.get_patterns_implicit():
                            for value_in_condition in test_eval:
                                if multilabelling.get_Multilabel(value_in_condition) != None and multilabelling.get_Multilabel(value_in_condition).get_label(pattern.get_vulnerability()) != None: 
                                    value_in_condition_label = copy.deepcopy(multilabelling.get_Multilabel(value_in_condition).get_label(pattern.get_vulnerability()))
                                    value_multilabel = MultiLabel()
                                    value_multilabel.add_label(pattern.get_vulnerability(), value_in_condition_label, policy, multilabellingAssigned)
                                    implicit_multilabel.update_Multilabel(value_in_condition, value_multilabel, policy, multilabellingAssigned)

                        eval_result = element.eval(policy, while_multilabellings[i], vulnerabilities, while_multilabellings_assigned[i], implicit_multilabel)
                        if isinstance(self.test, Compare) and not isinstance(element, If):
                            for pattern in policy.get_patterns_implicit(): 
                                if "()" not in eval_result[0]:
                                    for value_in_condition in test_eval:
                                        if multilabelling.get_Multilabel(value_in_condition) != None and multilabelling.get_Multilabel(value_in_condition).get_label(pattern.get_vulnerability()) != None:
                                            value_in_condition_label = copy.deepcopy(multilabelling.get_Multilabel(value_in_condition).get_label(pattern.get_vulnerability()))
                                            body_label = copy.deepcopy(multilabelling.get_Multilabel(eval_result[0]).get_label(pattern.get_vulnerability()).combine_labels(value_in_condition_label, policy, pattern.get_vulnerability(), multilabellingAssigned))
                                            body_multilabel = MultiLabel()
                                            body_multilabel.add_label(pattern.get_vulnerability(), body_label, policy, multilabellingAssigned)
                                            multilabellingAssigned.update_Multilabel(eval_result[0], body_multilabel, policy, multilabellingAssigned)
                       
                    else:
                        
                        for pattern in policy.get_patterns_implicit():
                            for value_in_condition in test_eval:
                                if multilabelling.get_Multilabel(value_in_condition) != None and multilabelling.get_Multilabel(value_in_condition).get_label(pattern.get_vulnerability()) != None: 
                                    value_in_condition_label = copy.deepcopy(multilabelling.get_Multilabel(value_in_condition).get_label(pattern.get_vulnerability()))
                                    value_multilabel = MultiLabel()
                                    value_multilabel.add_label(pattern.get_vulnerability(), value_in_condition_label, policy, multilabellingAssigned)
                                    implicit_multilabel.update_Multilabel(value_in_condition, value_multilabel, policy, multilabellingAssigned)
                        
                        eval_result = element.eval(policy, while_multilabellings[i], vulnerabilities, while_multilabellings_assigned[i], copy.deepcopy(implicit_multilabel))
                    
                    if isinstance(element, If) or isinstance(element, While):
                        #while_multilabellings[i:i+1] = eval_result[0]
                        while_multilabellings_assigned[i:i+1] = eval_result[1]
                        while_multilabellings = copy.deepcopy(while_multilabellings_assigned)
                        i += len(eval_result) - 1
                        notLists = False
                        
        
        result_assigned = [multilabellingAssigned]
        result_assigned.extend(while_multilabellings_assigned)

        return [[], result_assigned]