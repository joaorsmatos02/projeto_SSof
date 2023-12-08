class Pattern:
    def __init__(self, vulnerability, source, sanitizer, sink, implicit):
        self.vulnerability = vulnerability
        self.source = source
        self.sanitizer = sanitizer
        self.sink = sink
        self.implicit = implicit

    # Selectors
    def get_vulnerability(self):
        return self.vulnerability_name

    def get_source(self):
        return self.source_names

    def get_sanitizer(self):
        return self.sanitizer_names

    def get_sink(self):
        return self.sink_names
    
    def get_implicit(self):
        return self.sink_names

    # Tests for checking whether a given name is a source, sanitizer, or sink for the pattern
    def is_source(self, name):
        return name in self.source_names

    def is_sanitizer(self, name):
        return name in self.sanitizer_names

    def is_sink(self, name):
        return name in self.sink_names