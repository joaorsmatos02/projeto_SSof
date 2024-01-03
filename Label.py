from Policy import Policy
class Label:
    def __init__(self):
        self.sources = []  # List of tuples (source name, line number)
        self.sanitizers = []  # List of tuples (sanitizer name, line number)

    # Constructors and operations for adding sources and sanitizers
    def add_source(self, source_name, line_number):
        self.sources.append((source_name, line_number))
    
    #[[["s", 8]]]
    def add_sanitizer(self, sanitizer_name, line_number):
        if self.sanitizers != []:
            inside = False
            for sanitizer in self.sanitizers:
                if sanitizer[0] == [sanitizer_name, line_number]:
                    inside = True

            if not inside:
                self.sanitizers[0].append([sanitizer_name, line_number])
        else:    
            self.sanitizers.append([[sanitizer_name, line_number]])


    # Selectors for components
    def get_sources(self):
        return list(self.sources)
    
    def get_source_with_line(self, source_name):
        matching_sources = [(name, line) for name, line in self.sources if name == source_name]
        return matching_sources

    def get_sanitizers(self):
        return list(self.sanitizers)
    
    def get_sanitizers_line(self, sanitizer_name):
        matching_sources = [(name, line) for name, line in self.sanitizers if name == sanitizer_name]
        return matching_sources

    # Combinor for combining two labels
    def combine_labels(self, other_label, policy, pattern_name, multilabellingAssigned):
        new_label = Label() 
        new_label.sources = list(self.sources)
        new_label.sanitizers = self.sanitizers
        
        # quando a source é a mesma de uma ja existente, temos de atualizar a linha         
        for other_source in other_label.sources:
            inside = False
            for i, self_source in enumerate(new_label.sources):
                # if other_source[0] == self_source[0] and \
                #             multilabellingAssigned.get_Multilabel(other_source[0]) != None and \
                #             multilabellingAssigned.get_Multilabel(other_source[0]).get_label(pattern_name) != None and \
                #             len(multilabellingAssigned.get_Multilabel(other_source[0]).get_label(pattern_name).get_sanitizers()) == 0 and \
                #             other_source[0] not in policy.getSourcesFromPattern(pattern_name):
                
                if other_source[0] == self_source[0]:
                    if  multilabellingAssigned.get_Multilabel(other_source[0]) != None and \
                                other_source[0] in policy.getSourcesFromPattern(pattern_name) and \
                                multilabellingAssigned.get_Multilabel(other_source[0]).get_label(pattern_name) != None and \
                                len(multilabellingAssigned.get_Multilabel(other_source[0]).get_label(pattern_name).get_sanitizers()) == 0:
                        #and multilabellingAssigned.get_Multilabel(other_source[0]) == None:
                        new_label.sources[i] = (other_source[0], max(other_source[1], self_source[1]))
                        inside = True
                    
                    elif other_source[0] in policy.getUninstantiatedVars(pattern_name):
                        new_label.sources[i] = (other_source[0], max(other_source[1], self_source[1]))
                        inside = True
                
            if not inside:
                new_label.sources.append(other_source)

        if other_label.sanitizers != []: 
            for other_san in other_label.sanitizers:
                if other_san not in new_label.sanitizers:
                    new_label.sanitizers.extend(other_label.sanitizers)

        return new_label