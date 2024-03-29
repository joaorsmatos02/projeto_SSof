import MultiLabel
from Policy import Policy
class MultiLabelling:
    def __init__(self):
        # Dictionary to store mappings from variable names to MultiLabels
        self.multilabels_mapping = {}

    def assign_Multilabel(self, variable_name, multi_label):
        self.multilabels_mapping[variable_name] = multi_label

    def get_Multilabel(self, variable_name):    
        if variable_name in self.multilabels_mapping:
            return self.multilabels_mapping.get(variable_name, None) 
        
        return None


    def update_Multilabel(self, variable_name, multi_label, policy, multilabellingAssigned):
        if variable_name in self.multilabels_mapping:
            current_multilabel = self.multilabels_mapping[variable_name]
            updated_multilabel = current_multilabel.combine_multilabels(multi_label, policy, multilabellingAssigned)
            self.multilabels_mapping[variable_name] = updated_multilabel
        else:
            # If the variable name doesn't exist, assign the new MultiLabel
            self.multilabels_mapping[variable_name] = multi_label