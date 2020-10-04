# Define Annotation Class        
class Annotation:
    def __init__(self, tokens, label):
        self.tokens = tokens
        self.label = label

    def print_annotation(self):
        print(self.tokens)
        print(self.label)
