class Feature:
    def __init__(self,label,arrFunc):
        self.state=True
        self.label=label
        self.arrFunc=arrFunc

    def toggle(self):
        self.state=not self.state