from Objects.Exceptions import IncorrectResponse
from Static.strings import text_dict
from datetime import datetime

def print_error(e):
    print("Please choose from the following choices: ") 
    for choice in e._choices:
        print(choice)

def print_text(key, toReplace=None):
    string = text_dict[key]
    if toReplace:
        string = string.replace("REPLACE", toReplace)
    print(string)

def get_input(key, toReplace=None):
    string = text_dict[key]
    if toReplace:
        string = string.replace("REPLACE", toReplace)
    return input(string + '\n>')

def get_text(key, toReplace=None):
    string = text_dict[key]
    if toReplace:
        string = string.replace("REPLACE", toReplace)
    return string


def validate(validator, input_string, input_placeholder=None):
    while True:
        try:
            response = get_input(input_string, input_placeholder)
            return validator(response)
        except IncorrectResponse as e:
            print_error(e)

def add_and_commit(session, add_list):
    for thingToAdd in add_list:
        session.add(thingToAdd)
    session.commit() 

def get_today():
    today = datetime.today()
    return today.strftime("%m-%d-%Y")

def yes_or_no(answer):
        if answer.lower() == "yes" or answer.lower() == "y":
            return True
        elif answer.lower() == "no" or answer.lower() == "n":
            return False
        else:
            raise IncorrectResponse(["Yes", "No"])