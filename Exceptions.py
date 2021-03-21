class IncorrectResponse(Exception):
    def __init__(self, choices):
        self._choices = choices