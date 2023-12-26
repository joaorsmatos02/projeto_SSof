import MultiLabelling
import Pattern
class Assign:
    def __init__(self, target, arguments_dict, line_number):
        self.target = target
        self.arguments = arguments_dict 
        self.line_number = line_number

    def __repr__(self):
        return f"Assign(%s, %s)" % (self.target, self.arguments)
    
    def eval(self, policy, multilabelling, vulnerabilities):

        print(repr(self))
        target = self.target.eval(policy, multilabelling, vulnerabilities)
        arguments = [self.arguments.eval(policy, multilabelling, vulnerabilities)]

        for argument in arguments:
           multilabelling.update_Multilabel(target, multilabelling.get_Multilabel(argument))

        patterns_where_target_is_sink = policy.get_patterns_where_value_is_sink(self.target)
        
        if len(patterns_where_target_is_sink) > 0:
            target_multilabel = multilabelling.get_Multilabel(self.target)
            for pattern in patterns_where_target_is_sink:
                if target_multilabel.get_label(pattern.get_vulnerability()).len > 0:
                    # significa que temos de adicionar uma vulnerabilidade
                    vulnerabilities.create_vulnerabilitie_from_assign(multilabelling, pattern, target, arguments) # funçao tem de ir buscar o label do padrao para cada argumento 
                                                                                                                    #e escrever as vulnerabilidades com target é o sink

        return