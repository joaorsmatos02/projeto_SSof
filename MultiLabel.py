#APENAS POR TER - NÃO CONFIAR
class MultiLabel:
    def __init__(self, patterns):
        self.labels = {pattern: Label() for pattern in patterns}

    def add_source(self, pattern, source_name, line_number):
        if pattern in self.labels and pattern.is_source(source_name):
            self.labels[pattern].add_source(source_name, line_number)

    def add_sanitizer(self, pattern, sanitizer_name):
        if pattern in self.labels and pattern.is_sanitizer(sanitizer_name):
            self.labels[pattern].add_sanitizer(sanitizer_name)

    def combine_labels(self, other_multilabel):
        combined_multilabel = MultiLabel(self.labels.keys())
        for pattern in self.labels:
            if pattern in other_multilabel.labels:
                combined_multilabel.labels[pattern] = self.labels[pattern].combine_labels(other_multilabel.labels[pattern])
        return combined_multilabel