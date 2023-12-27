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
        
        eval = self.value.eval(policy, multilabelling, vulnerabilities)
        
        #check if the left part of the attributte is uninstatiated
        all_patterns = policy.getAllPatterns()
        if multilabelling.get_Multilabel(self.value.value) != None and multilabelling.get_Multilabel(self.value.value).get_labels() == {} :
            for pattern in all_patterns:
                new_label = Label()
                new_label.add_source(self.value.value, self.line_number)
                multilabelling.get_Multilabel(self.value.value).add_label(pattern.get_vulnerability(), new_label)
            multilabelling.update_Multilabel(self.attribute,  multilabelling.get_Multilabel(self.value.value))
        
        
        patterns_where_is_source = policy.get_patterns_where_value_is_source(self.attribute)
        multiLabel = MultiLabel()

        for pattern in patterns_where_is_source:
            label = Label()
            label.add_source(self.attribute, self.line_number)
            multiLabel.add_label(pattern.get_vulnerability(), label)

        multilabelling.update_Multilabel(self.attribute, multiLabel)
        
        return self.attribute
