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
        if self.arguments_dict != []:
            arguments = self.arguments_dict.eval(policy, multilabelling, vulnerabilities)

        patterns_where_fucn_is_sink = policy.get_patterns_where_value_is_sink(self.function_dict)
        patterns_where_fucn_is_sanitizer = policy.get_patterns_where_value_is_sanitizer(self.function_dict)
        
        ## ver se é sink

        if len(patterns_where_fucn_is_sink) > 0:
            for pattern in patterns_where_fucn_is_sink:
                for argument in arguments:
                    if len(multilabelling.get_Multilabel(argument).get_label(pattern.get_vulnerability())) > 0:
                        vulnerabilities.create_vulnerability(multilabelling, pattern, self.function_dict, self.line_number)
         

        # ver se é sanitizer
        if len(patterns_where_fucn_is_sanitizer) > 0:
            for pattern in patterns_where_fucn_is_sanitizer:
                for argument in arguments:
                    if len(multilabelling.get_Multilabel(argument).get_label(pattern.get_vulnerability())) > 0:
                        argument_label = multilabelling.get_Multilabel(argument).get_label(pattern.get_vulnerability())
                        argument_label.add_sanitizer(self.function_dict, self.line_number)
                        new_multilabel = MultiLabel()
                        new_multilabel.add_label(argument_label)
                        multilabelling.update_Multilabel(self.function_dict, new_multilabel)

        return