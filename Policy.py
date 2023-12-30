class Policy:
    def __init__(self, patterns):
        self.patterns = patterns
        self.uninstantiated_vars = {}
        for pattern in patterns:
            self.uninstantiated_vars[pattern.get_vulnerability()] = []

    def get_vulnerability_names(self):
        return [pattern.name for pattern in self.patterns]

    def get_patterns_where_value_is_source(self, source_name):
        return [pattern for pattern in self.patterns if pattern.is_source(source_name)]

    def get_patterns_where_value_is_sanitizer(self, sanitizer_name):
        return [pattern for pattern in self.patterns if pattern.is_sanitizer(sanitizer_name)]

    def get_patterns_where_value_is_sink(self, sink_name):
        return [pattern for pattern in self.patterns if pattern.is_sink(sink_name)]

    def getAllPatterns(self):
        return self.patterns
    
    def getSourcesFromPattern(self, pattern_name):
        all_patterns = self.getAllPatterns()
        for pattern in all_patterns:
            if pattern_name == pattern.get_vulnerability():
                return pattern.get_source()
    
    def getAllSourcesOfAllPatterns(self):
        all_patterns = self.getAllPatterns()
        sources_list = []
        for pattern in all_patterns:
            sources_list.extend(pattern.get_source())
        return sources_list
    
    def getUninstantiatedVars(self, pattern_name):
        return self.uninstantiated_vars[pattern_name]
    
    def addUninstantiatedVars(self, pattern_name, var_to_add):
        self.uninstantiated_vars[pattern_name].append(var_to_add)
        
def removeUnwantedChars(array, to_remove):
    for i in range(len(array)):
        if isinstance(array[i], str) and to_remove in array[i]:
                    array[i] = array[i][:-2]
    return array
            