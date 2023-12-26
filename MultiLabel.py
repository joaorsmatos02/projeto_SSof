import Label

class MultiLabel:
    def __init__(self):
        self.labels = {}

    def add_label(self, pattern_name, label):
        if pattern_name not in self.labels:
            self.labels[pattern_name] = Label()
        self.labels[pattern_name] = self.labels[pattern_name].combine_labels(label)

    def get_label(self, pattern_name):
        return self.labels.get(pattern_name, None)

    def add_source(self, pattern_name, source_name, line_number):
        if pattern_name in self.labels:
            self.labels[pattern_name].add_source(source_name, line_number)

    def add_sanitizer(self, pattern_name, sanitizer_name, line_number):
        if pattern_name in self.labels:
            self.labels[pattern_name].add_sanitizer(sanitizer_name, line_number)

    def combine_multilabels(self, other_multilabel):
        new_multi_label = MultiLabel()
        for pattern_name, label in self.labels.items():
            new_multi_label.add_label(pattern_name, label)
        for pattern_name, label in other_multilabel.labels.items():
            new_multi_label.add_label(pattern_name, label)
        return new_multi_label