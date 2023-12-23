class MultiLabelling:
    def __init__(self):
        # Dictionary to store mappings from variable names to MultiLabels
        self.labels_mapping = {}

    def assign_label(self, variable_name, multi_label):
        self.labels_mapping[variable_name] = multi_label

    def get_label(self, variable_name):    
        return self.labels_mapping.get(variable_name, None)

    def update_label(self, variable_name, multi_label):
        if variable_name in self.labels_mapping:
            current_label = self.labels_mapping[variable_name]
            updated_label = current_label.combine_labels(multi_label)
            self.labels_mapping[variable_name] = updated_label
        else:
            # If the variable name doesn't exist, assign the new MultiLabel
            self.labels_mapping[variable_name] = multi_label