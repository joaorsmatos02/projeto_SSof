import Label
import MultiLabel
import Policy
class Name:
    def __init__(self, value, line_number):
        self.value = value
        self.line_number

    def __repr__(self):
        return f"Name({self.value})"
    
    def eval(self,  policy, multilabelling, vulnerabilities):

        print(repr(self))

        patterns_where_is_source = policy.get_patterns_where_value_is_source(self.value)
        multiLabel = MultiLabel()

        for pattern in patterns_where_is_source:
            label = Label(pattern)
            label.add_source(self.value, self.line_number)
            multiLabel.add_label(pattern.get_vulnerability(), label)

        multilabelling.update_Multilabel(self.value, multiLabel)

        return self.value