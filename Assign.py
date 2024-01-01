import MultiLabelling
from Label import Label
from MultiLabel import MultiLabel
import Pattern
from Policy import removeUnwantedChars
from Policy import Policy
class Assign:
    def __init__(self, target, arguments_dict, line_number):
        self.target = target
        self.arguments = arguments_dict 
        self.line_number = line_number

    def __repr__(self):
        return f"Assign(%s, %s)" % (self.target, self.arguments)
    
    def eval(self, policy, multilabelling, vulnerabilities, multilabellingAssigned):

        print(repr(self))
        targets = self.target.eval(policy, multilabelling, vulnerabilities, multilabellingAssigned)
        arguments = []
        args_eval = self.arguments.eval(policy, multilabelling, vulnerabilities, multilabellingAssigned)
        if isinstance(args_eval, list):
            arguments.extend(args_eval)
        else:
            arguments.append(args_eval)

        all_patterns = policy.getAllPatterns()
        
        for pattern in all_patterns:
            for argument in arguments: 
                # se algum argumento ainda nao tiver aparecido entao e source
                if multilabelling.get_Multilabel(argument) != None and \
                            multilabelling.get_Multilabel(argument).get_label(pattern.get_vulnerability()) == None and \
                            "()" not in argument:
                    policy.addUninstantiatedVars(pattern.get_vulnerability(), argument)
                    new_label = Label()
                    new_label.add_source(argument, self.line_number)
                    multilabelling.get_Multilabel(argument).add_label(pattern.get_vulnerability(), new_label, policy, multilabellingAssigned)
                
        arguments = removeUnwantedChars(arguments, "()")
            
        for argument in arguments:    
            # objetivo: atualizar a linha das variaveis marcadas como source por nunca terem sido instanciadas
            for pattern in all_patterns:
                uninstantiated_vars = policy.getUninstantiatedVars(pattern.get_vulnerability())
                if (argument in uninstantiated_vars):
                    if(multilabelling.get_Multilabel(argument) != None and  multilabelling.get_Multilabel(argument).get_label(pattern.get_vulnerability()) != None):
                        sources_list =  multilabelling.get_Multilabel(argument).get_label(pattern.get_vulnerability()).get_sources()
                        if lambda argument, x: any((argument, value) in sources_list for value in [x]):
                            new_updated_line_label = Label()
                            for source in sources_list:
                                new_updated_line_label.add_source(source[0], self.line_number)
                            
                            updated_multilabel = MultiLabel()
                            updated_multilabel.add_label(pattern.get_vulnerability(), new_updated_line_label, policy, multilabellingAssigned)
                            combined_multilabels = multilabelling.get_Multilabel(argument).combine_multilabels(updated_multilabel, policy, multilabellingAssigned)
                            multilabelling.assign_Multilabel(argument, combined_multilabels)
                            
                    

        if isinstance(targets, str):
            targets = [targets] 

        


        for target in targets:
            # criação de label sem source apenas para marcar a var como conhecida, para o caso de ser passada a um call
            if multilabelling.get_Multilabel(target) != None and multilabelling.get_Multilabel(target).get_labels() == {}:
                for pattern in all_patterns:
                    new_label = Label()
                    multilabelling.get_Multilabel(target).add_label(pattern.get_vulnerability(), new_label, policy, multilabellingAssigned)
        
            for argument in arguments:    
                multilabelling.update_Multilabel(target, multilabelling.get_Multilabel(argument), policy, multilabellingAssigned)
                
            multilabellingAssigned.update_Multilabel(target, multilabelling.get_Multilabel(target), policy, multilabellingAssigned)    
            

            
            patterns_where_target_is_sink = policy.get_patterns_where_value_is_sink(target)
            
            if len(patterns_where_target_is_sink) > 0:
                target_multilabel = multilabelling.get_Multilabel(target)
                for pattern in patterns_where_target_is_sink:
                    # linhas seguintes 5 sao para unsanitized flow, possivelmente vao sair
                    for argument in arguments:
                        labels_sanitized_flows = list()
                        for argument1 in arguments:
                            if multilabelling.get_Multilabel(argument1) != None and (multilabelling.get_Multilabel(argument1).get_label(pattern.get_vulnerability())) != None:   
                                labels_sanitized_flows.append(multilabelling.get_Multilabel(argument1).get_label(pattern.get_vulnerability()))  
                        if target_multilabel.get_label(pattern.get_vulnerability()) != None and target_multilabel.get_label(pattern.get_vulnerability()).get_sources() != []:
                        # significa que temos de adicionar uma vulnerabilidade
                            vulnerabilities.create_vulnerability(multilabelling, pattern, target, self.line_number, target, labels_sanitized_flows) # funçao tem de ir buscar o label do padrao para cada argumento 
                                                                                                                            #e escrever as vulnerabilidades com target é o sink

        if len(targets) > 1:
            for key, value in policy.uninstantiated_vars.items():
                if targets[1] in value:
                    policy.uninstantiated_vars[key].remove(target[1])  
        else:
            for key, value in policy.uninstantiated_vars.items():
                if targets[0] in value:
                    policy.uninstantiated_vars[key].remove(target[0]) 

        args = targets

        return args