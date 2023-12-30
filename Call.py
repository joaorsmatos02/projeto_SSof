from Label import Label
from MultiLabel import MultiLabel
from Attribute import Attribute
from Policy import removeUnwantedChars

class Call:
    def __init__(self, function_dict, arguments_dict, line_number):
        self.function_dict = function_dict
        self.arguments_dict = arguments_dict
        self.line_number = line_number

    def __repr__(self):
        return f"Call({self.function_dict} , {self.arguments_dict} )"
    
    def eval(self,  policy, multilabelling, vulnerabilities, multilabellingAssigned):
        print(repr(self))
        arguments = [] 
        if self.arguments_dict != []:
            for argument in self.arguments_dict:
                argument_eval = argument.eval(policy, multilabelling, vulnerabilities, multilabellingAssigned)
                
                if isinstance(argument_eval, list):
                    arguments.extend(argument_eval)
                else:
                    arguments.append(argument_eval)
                    
                    
            all_patterns = policy.getAllPatterns()
            for pattern in all_patterns:
                 # se algum argumento ainda nao tiver aparecido entao e source
                for argument in arguments:
                   if multilabelling.get_Multilabel(argument) != None and \
                                multilabelling.get_Multilabel(argument).get_label(pattern.get_vulnerability()) == None and \
                                "()" not in argument:
                        policy.addUninstantiatedVars(pattern.get_vulnerability(), argument)
                        new_label = Label()
                        new_label.add_source(argument, self.line_number)
                        multilabelling.get_Multilabel(argument).add_label(pattern.get_vulnerability(), new_label, policy, multilabellingAssigned)
                        
            for argument in arguments:    
                # objetivo: atualizar a linha das variaveis marcadas como source por nunca terem sido instanciadas
                for pattern in all_patterns:
                    uninstantiated_vars = policy.getUninstantiatedVars(pattern.get_vulnerability())
                    if (argument in uninstantiated_vars):
                        if(multilabelling.get_Multilabel(argument) != None and  multilabelling.get_Multilabel(argument).get_label(pattern.get_vulnerability()) != None):
                            sources_list =  multilabelling.get_Multilabel(argument).get_label(pattern.get_vulnerability()).get_sources()
                            if lambda argument, x: any((argument, value) in sources_list for value in [x]):
                                new_updated_line_label = Label()
                                new_updated_line_label.add_source(argument, self.line_number)
                                # for source in sources_list:
                                #     new_updated_line_label.add_source(source[0], self.line_number)
                                
                                updated_multilabel = MultiLabel()
                                updated_multilabel.add_label(pattern.get_vulnerability(), new_updated_line_label, policy, multilabellingAssigned)
                                combined_multilabels = multilabelling.get_Multilabel(argument).combine_multilabels(updated_multilabel, policy, multilabellingAssigned)
                                multilabelling.assign_Multilabel(argument, combined_multilabels)
                     
        
        patterns_where_func_is_sink = policy.get_patterns_where_value_is_sink(self.function_dict.get_name_value())
        patterns_where_func_is_sanitizer = policy.get_patterns_where_value_is_sanitizer(self.function_dict.get_name_value())
        
        arguments = removeUnwantedChars(arguments, "()")
        
        # ver se é sanitizer
        if len(patterns_where_func_is_sanitizer) > 0:
            for pattern in patterns_where_func_is_sanitizer:
                for argument in arguments:
                    if  multilabelling.get_Multilabel(argument) != None and (multilabelling.get_Multilabel(argument).get_label(pattern.get_vulnerability())) != None:
                        argument_label = multilabelling.get_Multilabel(argument).get_label(pattern.get_vulnerability())
                        argument_label.add_sanitizer(self.function_dict.get_name_value(), self.line_number)
                        new_multilabel = MultiLabel()
                        new_multilabel.add_label(pattern.get_vulnerability(), argument_label, policy, multilabellingAssigned)
                        multilabelling.update_Multilabel(argument, new_multilabel, policy, multilabellingAssigned)
                    
                    #caso houvesse necessidade de fazer sanitize de vars novas
                    # if argument in uninstantiated_vars:
                    #     uninstantiated_vars.remove(argument)


        ## ver se é sink
        if len(patterns_where_func_is_sink) > 0:
            for pattern in patterns_where_func_is_sink:
                for argument in arguments:
                    # linhas seguintes 4 sao para unsanitized flow, possivelmente vao sair
                    labels_sanitized_flows = list()
                    for argument1 in arguments:
                        if multilabelling.get_Multilabel(argument1) != None and (multilabelling.get_Multilabel(argument1).get_label(pattern.get_vulnerability())) != None:   
                            labels_sanitized_flows.append(multilabelling.get_Multilabel(argument1).get_label(pattern.get_vulnerability())) 
                    if  multilabelling.get_Multilabel(argument) != None and (multilabelling.get_Multilabel(argument).get_label(pattern.get_vulnerability())) != None and multilabelling.get_Multilabel(argument).get_label(pattern.get_vulnerability()).get_sources() != []:
                        vulnerabilities.create_vulnerability(multilabelling, pattern, self.function_dict.get_name_value(), self.line_number, argument, labels_sanitized_flows)
                        
        # tratar do target
        self.function_dict.eval(policy, multilabelling, vulnerabilities, multilabellingAssigned)
        for argument in arguments:
            multilabelling.update_Multilabel(self.function_dict.get_name_value(), multilabelling.get_Multilabel(argument), policy, multilabellingAssigned)

              
        if isinstance(self.function_dict, Attribute):
            self.function_dict.is_callable()
            return self.function_dict.get_name_value()
        else:
            return str(self.function_dict.get_name_value() + "()")