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
        arguments = self.arguments_dict.eval(policy, multilabelling, vulnerabilities)

        patterns_where_fucn_is_sink = policy.get_patterns_where_value_is_sink(self.function_dict)
        patterns_where_fucn_is_sanitizer = policy.get_patterns_where_value_is_sanitizer(self.function_dict)
        
        ## ver se é sink

        # ver se é sanitizer

        return