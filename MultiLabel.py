from Label import Label
from Policy import Policy

class MultiLabel:
    def __init__(self):
        self.labels = {}

    def add_label(self, pattern_name, label, policy, multilabellingMaster):
        if pattern_name not in self.labels:
            self.labels[pattern_name] = Label()
        self.labels[pattern_name] = self.labels[pattern_name].combine_labels(label, policy, pattern_name, multilabellingMaster)

    def get_label(self, pattern_name):
        return self.labels.get(pattern_name, None)
    
    def get_labels(self):
        return self.labels

    def add_source(self, pattern_name, source_name, line_number):
        if pattern_name in self.labels:
            self.labels[pattern_name].add_source(source_name, line_number)

    def add_sanitizer(self, pattern_name, sanitizer_name, line_number):
        if pattern_name in self.labels:
            self.labels[pattern_name].add_sanitizer(sanitizer_name, line_number)

    def combine_multilabels(self, other_multilabel, policy, multilabellingMaster):
        new_multi_label = MultiLabel()
        for pattern_name, label in self.labels.items():
            new_multi_label.add_label(pattern_name, label, policy, multilabellingMaster)
            
        if (other_multilabel != None) :
            for pattern_name, label in other_multilabel.labels.items():
                new_multi_label.add_label(pattern_name, label, policy, multilabellingMaster)
        
        return new_multi_label