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
    
    def eval(self,  policy, multilabelling, vulnerabilities, multilabellingMaster):
        print(repr(self))
        arguments = [] 
        if self.arguments_dict != []:
            for argument in self.arguments_dict:
                argument_eval = argument.eval(policy, multilabelling, vulnerabilities, multilabellingMaster)
                
                if isinstance(argument_eval, list):
                    arguments.extend(argument_eval)
                else:
                    arguments.append(argument_eval)
                    
                    
            all_patterns = policy.getAllPatterns()
            for pattern in all_patterns:
                for argument in arguments:
                   if multilabelling.get_Multilabel(argument) != None and \
                                multilabelling.get_Multilabel(argument).get_label(pattern.get_vulnerability()) == None and \
                                "()" not in argument:
                        policy.addUninstantiatedVars(pattern.get_vulnerability(), argument)
                        new_label = Label()
                        new_label.add_source(argument, self.line_number)
                        multilabelling.get_Multilabel(argument).add_label(pattern.get_vulnerability(), new_label)
        
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
                        new_multilabel.add_label(pattern.get_vulnerability(), argument_label)
                        multilabelling.update_Multilabel(argument, new_multilabel)

        ## ver se é sink
        if len(patterns_where_func_is_sink) > 0:
            for pattern in patterns_where_func_is_sink:
                for argument in arguments:
                     if  multilabelling.get_Multilabel(argument) != None and (multilabelling.get_Multilabel(argument).get_label(pattern.get_vulnerability())) != None and multilabelling.get_Multilabel(argument).get_label(pattern.get_vulnerability()).get_sources() != []:
                        vulnerabilities.create_vulnerability(multilabelling, pattern, self.function_dict.get_name_value(), self.line_number, argument)
                        
        # tratar do target
        self.function_dict.eval(policy, multilabelling, vulnerabilities, multilabellingMaster)
        for argument in arguments:
            multilabelling.update_Multilabel(self.function_dict.get_name_value(), multilabelling.get_Multilabel(argument))

              
        if isinstance(self.function_dict, Attribute):
            self.function_dict.is_callable()
            return self.function_dict.get_name_value()
        else:
            return str(self.function_dict.get_name_value() + "()")