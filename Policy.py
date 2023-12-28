class Policy:
    def __init__(self, patterns):
        self.patterns = patterns
        self.uninstantiated_vars = []

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
    
    def getAllSourcesOfAllPatterns(self):
        all_patterns = self.getAllPatterns()
        sources_list = []
        for pattern in all_patterns:
            sources_list.extend(pattern.get_source())
        return sources_list
    
    def getUninstantiatedVars(self):
        return self.uninstantiated_vars
    
    def addUninstantiatedVars(self, var_to_add):
        self.uninstantiated_vars.append(var_to_add)
            