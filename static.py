from Exceptions import IncorrectResponse
from strings import text_dict

def print_error(e):
    print("Please choose from the following choices: ") 
    for choice in e._choices:
        print(choice)

def print_text(key, toReplace=None):
    string = text_dict[key]
    if toReplace:
        altered = string.replace("REPLACE", toReplace)
        string = altered
    print(string)

def get_input(key, toReplace=None):
    string = text_dict[key]
    if toReplace:
        altered = string.replace("REPLACE", toReplace)
        string = altered
    text = input(string)
    return text

def validate(validator, input_string, input_placeholder=None):
    while True:
        try:
            response = get_input(input_string, input_placeholder)
            valid = validator(response)
            break
        except IncorrectResponse as e:
            print_error(e)

    return valid if valid else None

def add_and_commit(session, add_list):
    for thingToAdd in add_list:
        session.add(thingToAdd)
    session.commit() 
