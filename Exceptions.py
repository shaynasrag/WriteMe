class IncorrectResponse(Exception):
    def __init__(self, choices):
        for choice in choices:
            print(choice)