class Pattern:
    def __init__(self, pattern: dict):
        self.vulnerability = pattern['vulnerability']
        self.sources = pattern['sources']
        self.sanitizers = pattern['sanitizers']
        self.sinks = pattern['sinks']
        self.implicit = pattern['implicit']

    # Selectors
    def get_vulnerability(self):
        return self.vulnerability

    def get_source(self):
        return self.sources

    def get_sanitizer(self):
        return self.sanitizers

    def get_sink(self):
        return self.sinks
        
    def get_implicit(self):
        return self.implicit

    # Tests for checking whether a given name is a source, sanitizer, or sink for the pattern
    def is_source(self, name):
        return name in self.sources

    def is_sanitizer(self, name):
        return name in self.sanitizers

    def is_sink(self, name):
        return name in self.sinks
    
    def is_implicit(self):
        if self.implicit == "yes":
            return self.vulnerability