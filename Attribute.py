from Label import Label
from MultiLabel import MultiLabel


class Attribute:
    def __init__(self, value, attribute, line_number):
        self.value = value
        self.attribute = attribute 
        self.line_number = line_number

    def __repr__(self):
        return f"Attribute({self.value} , {self.attribute})"
    
    def get_name_value(self):
        return self.attribute
    
    def eval(self, policy, multilabelling, vulnerabilities):
        print(repr(self))
        
        patterns_where_is_source = policy.get_patterns_where_value_is_source(self.attribute)
        multiLabel = MultiLabel()

        for pattern in patterns_where_is_source:
            label = Label()
            label.add_source(self.attribute, self.line_number)
            multiLabel.add_label(pattern.get_vulnerability(), label)

        multilabelling.update_Multilabel(self.attribute, multiLabel)
        
        return [self.value.eval(policy, multilabelling, vulnerabilities), self.attribute]
