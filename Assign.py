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
        arguments = self.arguments.eval(policy, multilabelling, vulnerabilities)


        for argument in arguments:
            multilabelling.update_Multilabel(self.target, multilabelling.get_Multilabel(argument))

                
        patterns_where_target_is_sink = policy.get_patterns_with_sink(self.target)
        
        if patterns_where_target_is_sink.len > 0:
            target_multilabel = multilabelling.get_Multilabel(self.target)
            for pattern in patterns_where_target_is_sink:
                if target_multilabel.get_label(pattern.get_vulnerability()).len > 0:
                    # significa que temos de adicionar uma vulnerabilidade
                    vulnerabilities.create_vulnerability(multilabelling, pattern, target, self.line_number) # funçao tem de ir buscar o label do padrao para cada argumento 
                                                                                                                    #e escrever as vulnerabilidades com target é o sink

        return