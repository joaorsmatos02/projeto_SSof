import MultiLabelling
from Label import Label
from MultiLabel import MultiLabel
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
        targets = self.target.eval(policy, multilabelling, vulnerabilities)
        arguments = []
        args_eval = self.arguments.eval(policy, multilabelling, vulnerabilities)
        if isinstance(args_eval, list):
            arguments.extend(args_eval)
        else:
            arguments.append(args_eval)

        all_patterns = policy.getAllPatterns()
        
        for argument in arguments: 
            # se algum argumento ainda nao tiver aparecido entao e source
            if multilabelling.get_Multilabel(argument) != None and multilabelling.get_Multilabel(argument).get_labels() == {} :
                policy.addUninstantiatedVars(argument)
                for pattern in all_patterns:
                    new_label = Label()
                    new_label.add_source(argument, self.line_number)
                    multilabelling.get_Multilabel(argument).add_label(pattern.get_vulnerability(), new_label)
            
           
            # objetivo: atualizar a linha das variaveis marcadas como source por nunca terem sido instanciadas
            for pattern in all_patterns:
                uninstantiated_vars = policy.getUninstantiatedVars()
                if (argument in uninstantiated_vars):
                    if(multilabelling.get_Multilabel(argument) != None and  multilabelling.get_Multilabel(argument).get_label(pattern.get_vulnerability()) != None):
                        sources_list =  multilabelling.get_Multilabel(argument).get_label(pattern.get_vulnerability()).get_sources()
                        if lambda argument, x: any((argument, value) in sources_list for value in [x]):
                            new_updated_line_label = Label()
                            for source in sources_list:
                                new_updated_line_label.add_source(source[0], self.line_number)
                            
                            updated_multilabel = MultiLabel()
                            updated_multilabel.add_label(pattern.get_vulnerability(), new_updated_line_label)
                            combined_multilabels = multilabelling.get_Multilabel(argument).combine_multilabels(updated_multilabel)
                            multilabelling.assign_Multilabel(argument, combined_multilabels)
                            
                    

        if isinstance(targets, str):
            targets = [targets] 
      
        for target in targets:
            # criação de label sem source apenas para marcar a var como conhecida, para o caso de ser passada a um call
            if multilabelling.get_Multilabel(target) != None and multilabelling.get_Multilabel(target).get_labels() == {}:
                for pattern in all_patterns:
                    new_label = Label()
                    multilabelling.get_Multilabel(target).add_label(pattern.get_vulnerability(), new_label)
        
            for argument in arguments:    
                multilabelling.update_Multilabel(target, multilabelling.get_Multilabel(argument))

            patterns_where_target_is_sink = policy.get_patterns_where_value_is_sink(target)
            
            if len(patterns_where_target_is_sink) > 0:
                target_multilabel = multilabelling.get_Multilabel(target)
                for pattern in patterns_where_target_is_sink:
                    if target_multilabel.get_label(pattern.get_vulnerability()) != None and target_multilabel.get_label(pattern.get_vulnerability()).get_sources() != []:
                        # significa que temos de adicionar uma vulnerabilidade
                        vulnerabilities.create_vulnerability(multilabelling, pattern, target, self.line_number, target) # funçao tem de ir buscar o label do padrao para cada argumento 
                                                                                                                            #e escrever as vulnerabilidades com target é o sink

        return