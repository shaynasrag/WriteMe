class IncorrectResponse(Exception):
    def __init__(self, choices):
        self._choices = choices
        self._show_choices(choices)

    def _show_choices(self, choices):
        for choice in choices:
            print(choice)