from Label import Label
from MultiLabel import MultiLabel
from Policy import Policy
class Name:
    def __init__(self, value, line_number):
        self.value = value
        self.line_number = line_number

    def __repr__(self):
        return f"Name({self.value})"
    
    def get_name_value(self):
        return self.value
    
    def eval(self,  policy, multilabelling, vulnerabilities, multilabellingAssigned):

        print(repr(self))

        patterns_where_is_source = policy.get_patterns_where_value_is_source(self.value)
        multiLabel = MultiLabel()

        for pattern in patterns_where_is_source:
            label = Label()
            label.add_source(self.value, self.line_number)
            multiLabel.add_label(pattern.get_vulnerability(), label, policy, multilabellingAssigned)
            
        
        
        multilabelling.update_Multilabel(self.value, multiLabel, policy, multilabellingAssigned)

        return self.value