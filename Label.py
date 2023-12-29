class Label:
    def __init__(self):
        self.sources = []  # List of tuples (source name, line number)
        self.sanitizers = [[]]  # List of tuples (sanitizer name, line number)

    # Constructors and operations for adding sources and sanitizers
    def add_source(self, source_name, line_number):
        self.sources.append((source_name, line_number))

    def add_sanitizer(self, sanitizer_name, line_number):
        if self.sanitizers != [] and self.sanitizers[0] != []:
            inside = False
            for sanitizer in self.sanitizers:
                if sanitizer[0] == sanitizer_name:
                    inside = True

            if not inside:
                self.sanitizers[len(self.sanitizers) - 1].append([sanitizer_name, line_number])
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
    def combine_labels(self, other_label):
        new_label = Label() 
        new_label.sources = list(self.sources)
        
        #new_label.sources = self.sources
        
        # quando a source é a mesma de uma ja existente, temos de atualizar a linha 
        for source in other_label.sources:
            inside = False
            for i, source1 in enumerate(new_label.sources):
                if source[0] == source1[0]:
                    new_label.sources[i] = (source[0], max(source[1], source1[1]))
                    inside = True
                    
            if not inside:
                new_label.sources.append(source)

        if self.sanitizers != [] and self.sanitizers[0] != [] and other_label.sanitizers != [] and other_label.sanitizers[0] != []:
            new_label.sanitizers = list()
       
            if self.sanitizers != [] and self.sanitizers[0] != []:
                new_label.sanitizers.append(self.sanitizers)
            if other_label.sanitizers != [] and other_label.sanitizers[0] != []:
                if other_label.sanitizers != self.sanitizers:
                    new_label.sanitizers.append(other_label.sanitizers)
        elif  self.sanitizers != [] and self.sanitizers[0] != []:
            new_label.sanitizers = self.sanitizers     
        else :
            new_label.sanitizers = other_label.sanitizers 

        return new_label