class BaseAnimation:
    def __init__(self, display):
        self.display = display

    def run(self, params):
        raise NotImplementedError("Subclasses must implement 'run' method")
