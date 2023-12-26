import Label
import MultiLabel
class Call:
    def __init__(self, function_dict, arguments_dict, line_number):
        self.function_dict = function_dict
        self.arguments_dict = arguments_dict
        self.line_number = line_number

    def __repr__(self):
        return f"Call({self.function_dict} , {self.arguments_dict} )"
    
    def eval(self,  policy, multilabelling, vulnerabilities):
        patterns_where_func_is_source = policy.get_patterns_where_value_is_source(self.function_dict.get_name_value())
        
        arguments = [] 
        if self.arguments_dict != []:
            for argument in self.arguments_dict:
                arguments.append(argument.eval(policy, multilabelling, vulnerabilities))
                
        if patterns_where_func_is_source != None:
            self.function_dict.eval(policy, multilabelling, vulnerabilities)
            for argument in arguments:
                multilabelling.update_Multilabel(self.function_dict.get_name_value(), multilabelling.get_Multilabel(argument))

        patterns_where_func_is_sink = policy.get_patterns_where_value_is_sink(self.function_dict.get_name_value())
        patterns_where_func_is_sanitizer = policy.get_patterns_where_value_is_sanitizer(self.function_dict.get_name_value())
        
        ## ver se é sink

        if len(patterns_where_func_is_sink) > 0:
            for pattern in patterns_where_func_is_sink:
                for argument in arguments:
                    if (multilabelling.get_Multilabel(argument).get_label(pattern.get_vulnerability())) != None:
                        vulnerabilities.create_vulnerability(multilabelling, pattern, self.function_dict.get_name_value(), self.line_number, argument)
         

        # ver se é sanitizer
        if len(patterns_where_func_is_sink) > 0:
            for pattern in patterns_where_func_is_sanitizer:
                for argument in arguments:
                    if (multilabelling.get_Multilabel(argument).get_label(pattern.get_vulnerability())) != None:
                        argument_label = multilabelling.get_Multilabel(argument).get_label(pattern.get_vulnerability())
                        argument_label.add_sanitizer(self.function_dict, self.line_number)
                        new_multilabel = MultiLabel()
                        new_multilabel.add_label(argument_label)
                        multilabelling.update_Multilabel(self.function_dict, new_multilabel)

        return self.function_dict.get_name_value()