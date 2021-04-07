import sys
from Journal import Journal, People
from Exceptions import IncorrectResponse
from Entry import Base, Entry, InterpersonalConflict
from Submission import Submission

from sqlalchemy import Column, Integer, String, ForeignKey, Table, MetaData, create_engine
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.session import sessionmaker

from sqlalchemy.types import TypeDecorator
import matplotlib.pyplot as plt

class JournalCLI():
    def __init__(self):
        self._session = Session()
        self._journal = self._session.query(Journal).first()
        if not self._journal:
            self._journal = Journal()
            self._session.add(self._journal)
            self._session.commit()
        self._choices = {
            "add submission": self._create_submission,
            "check stats": self._check_stats,
            "fetch transcript": self._fetch_transcript,
            "quit": self._quit,
        }
        self._types_of_submissions = {
            "interpersonal conflict": self._conflict_entry_driver,
            # TODO: add functionality
            "emotional trigger": self._trigger_entry,            
        }
        self._curr_person = None

    def _display_menu(self):
        if not self._journal._name:
            name = input("Hi! What's your name?\n>")
            self._journal._name = name
            self._session.add(self._journal)
            self._session.commit()
            print("Hi {0}, would you like to do today?".format(self._journal._name))
        else:
            print("Hi {0}, what would you like to do today?".format(self._journal._name))
        options = ", ".join(self._choices.keys())
        print(options)

    def run(self):
        while True:
            self._display_menu()
            choice = input(">")
            action = self._choices.get(choice)
            if action:
                action()
            else:
                print("{0} is not a valid choice".format(choice))
            
    def _create_submission(self):        
        while True:
            print("What best describes what you would like to talk about right now?\nI am experiencing an...")
            options = "\n".join(self._types_of_submissions.keys())
            print(options)
            print("return to main menu")
            choice = input(">")
            if choice == "return to main menu":
                return
            action = self._types_of_submissions.get(choice)
            if action:
                new_submission = Submission()
                self._journal.add_submission(new_submission)
                self._session.add(new_submission)
                self._session.commit()
                action(new_submission)
            else:
                print("{0} is not a valid choice".format(choice))
    
    def _choose_person(self):
        print("Please select who you would like to journal about today (If you would like to add a new person, type 'New Person'):")
        name_ls = []
        for i in self._journal.get_people():
            print(i._person)
            name_ls.append(i._person)

        choice = input(">")
        if choice in name_ls: 
            self._curr_person = choice
        elif choice == "New Person":
            person = input("Please enter the name of the new person you would like to add to your journal:\n>")
            if person in name_ls:
                print("You have written about {0} before. Would you like your submission to be about {0} or would you like to start again?".format(person))
                while True:                        
                    new_choice = input("Options: {0}, Start Again\n>".format(person))
                    if new_choice == person or new_choice.lower() == "start again":
                        break
                    else:
                        print("Please type either {0} or 'Start Again'".format(person))
                if new_choice == "Start Again":
                    self._choose_person()
                else:
                    self._curr_person = new_choice     
            p = People(person)
            self._journal.add_person(p)
            self._session.add(p)
            self._session.add(self._journal)
            self._session.commit()
            self._curr_person = person
        else:
            raise IncorrectResponse(self._journal.get_people())

    def _conflict_entry_driver(self, new_submission):
        discuss = True
        while discuss:   
            while True:
                try: 
                    self._choose_person()
                    break
                except IncorrectResponse as e:   
                    print("Please choose from the following choices: ") 
                    for choice in e._choices:
                        print(choice)
        
            new_entry = self._create_conflict_entry()
            new_submission.add_entry(new_entry)
            self._session.add(new_entry)
            self._session.add(new_submission)
            self._session.commit()

            while True:
                try:
                    cont = input("Would you like to discuss another relationship? Yes or No.\n>")
                    another_relationship = new_entry.yes_or_no(cont)
                    break
                except IncorrectResponse as e:
                    print("Please choose from the following choices: ") 
                    for choice in e._choices:
                        print(choice)
            if not another_relationship:
                discuss = False
                print("It's important to remember that having anxious tendencies doesn't make you a bad person or unworthy of love.\nSecure relationships are possible for you.")
                print("Relationship security is earned through actions and behaviors that build both partners up and bring out the best in them.")
                print("You may just have more challenges in this space to overcome than others.\n")
                next = input("Thank you so much for working to understand yourself better and to work toward healthier and fulfilling relationships with the people in your life. See you next time! Type anything to return to the submission menu.\n>")
    
    def _create_conflict_entry(self):
        new_entry = InterpersonalConflict(self._curr_person)
        self._session.add(new_entry)
        print("Great Choice!")
        while True:
            try:
                communal_strength = input("How close are you feeling to {0} today?\nOptions: Close, Not So Close, Distanced\n>".format(self._curr_person))
                new_entry.add_communal_strength(communal_strength)
                break
            except IncorrectResponse as e:
                print("Please choose from the following choices: ") 
                for choice in e._choices:
                    print(choice)
        if communal_strength.lower() == "Close":
            print("I'm glad to hear things are going well with {0}!".format(self._curr_person))
        else:
            print("I'm sorry to hear that you're feeling this way.")
        while True:
            try:
                anxiety = input("To what extent have you been feeling anxiety in the relationship?\nOptions: High Anxiety, Mid Anxiety, Low Anxiety, No Anxiety\n>")
                new_entry.add_anxiety(anxiety)
                break
            except IncorrectResponse as e:
                print("Please choose from the following choices: ") 
                for choice in e._choices:
                    print(choice)
        while True:
            try:
                talk_conflict = input("Would you like to talk about a conflict you've experienced recently with {0}?\nOptions: Yes or No\n>".format(self._curr_person))
                talk_conflict = new_entry.yes_or_no(talk_conflict)
                break
            except IncorrectResponse as e:
                print("Please choose from the following choices: ") 
                for choice in e._choices:
                    print(choice)
        if talk_conflict:
            conflict_description = input("Conflicts can come in all shapes and sizes.\nPlease describe the conflict you've been experiencing and how it's been making you feel.\n>")
            new_entry.add_conflict(conflict_description)
            space = input("Wow, that sounds like it's been really hard for you.\nI definitely understand why you've been feeling some anxiety in the relationship, and I think it's important that we first take a moment to accept that feeling.\nLet me know when you've taken a moment to give yourself space for this.\n>")
            while True:
                try:
                    addressed = input("Thank you for allowing yourself some space for self-compassion. Have you addressed this conflict with {0}?\nOptions: Yes or No\n>".format(self._curr_person))
                    been_addressed = new_entry.yes_or_no(addressed)
                    break
                except IncorrectResponse as e:
                    print("Please choose from the following choices: ") 
                    for choice in e._choices:
                        print(choice)
            if been_addressed:
                how_addressed = input("I'm glad to hear it! In your own words, how has the conflict been addressed?\n>")
                new_entry.add_addressed(how_addressed)
                while True:
                    try:
                        consent = input("I'm glad you took steps to resolve this conflict. Let's talk about your process in terms of healthy communication.\nDid you ask for consent from {0} before approaching the conflict?\nOptions: Yes or No\n>".format(self._curr_person))
                        new_entry.add_consent(consent)
                        break
                    except IncorrectResponse as e:
                        print("Please choose from the following choices: ") 
                        for choice in e._choices:
                            print(choice)
                while True:
                    try:
                        self_soothe1 = input("Next, did you take steps to physically/emotionally soothe yourself?\nOptions: Yes or No\n>")
                        new_entry.add_self_soothe1(self_soothe1)
                        break
                    except IncorrectResponse as e:
                        print("Please choose from the following choices: ") 
                        for choice in e._choices:
                            print(choice)
                while True:
                    try:
                        other_soothe1 = input("How about {0}. Did you take steps to physically/emotionally soothe each other?\nOptions: Yes or No\n>".format(self._curr_person))
                        new_entry.add_other_soothe1(other_soothe1)
                        break
                    except IncorrectResponse as e:
                        print("Please choose from the following choices: ") 
                        for choice in e._choices:
                            print(choice)
                done = input("Remember, when you are close to someone, what you do or say around that person makes an impact, whether positive or negative.\nYour healthy communication score this time with {0} is {1}/3. Type anything to continue\n>".format(self._curr_person, new_entry._communication_score))
                done = input("Effective, health communication is possible for you, and developing these skills can help you develop and build trust and safety with {0}. Type anything to continue\n>".format(self._curr_person))
            else:
                while True:
                    try:
                        how_to_begin = input("Would you like to brainstorm ways to go about this conflict with {0}?\n>".format(self._curr_person))
                        begin = new_entry.yes_or_no(how_to_begin)
                        break 
                    except IncorrectResponse as e:
                        print("Please choose from the following choices: ") 
                        for choice in e._choices:
                            print(choice)
                if begin:
                    how_to_approach = input("An important aspect of healthy communication is asking consent from {0} and allowing both of you the space to address this conflict in the way that is safe for both of you.\n What is one way you could ask consent from {0} before entering in this conversation?\n>".format(self._curr_person))
                    new_entry.add_how_to_approach(how_to_approach)
                    their_side = input("We've already talked about what your experience of the conflict has been. Let's take a moment to think about {0}'s side of the conflict.\nCan you try to explain what you think is going on with {0} in relation to this conflict?\nPerhaps {0} doesn't know that there is a conflict, or perhaps this has been bothering them as well. Take a moment to describe what their perspective may be.\n>".format(self._curr_person))
                    new_entry.add_their_side(their_side)
                    print("Thank you for taking the time to empathize with {0}'s perspective. Empathy is one of the tools you can use to ensure that this conflict can be resolved in a healthy and safe manner.".format(self._curr_person))
                    print("Before we focus on what exactly you might be able to say, let's remember some healthy communication techniques:")
                    print("1) Use I-language")
                    print("2) Focus on one problem at a time")
                    print("3) Make sure to stay in touch with your physical and emotional responses and make sure you feel safe during the conversation")
                    print("4) Pay attention to {0}'s physical and emotional comfort.".format(self._curr_person))
                    print("Take a temporary break from the conversation if you need to")
                    how_to_frame = input("What is another way you can make sure to have a safe and productive conflict resolution with {0}?\n>".format(self._curr_person))
                    new_entry.add_how_to_frame(how_to_frame)
                    intended = input("Now that we've brainstormed a bit about how to approach {0} about the conflict, what would you like to say to them to resolve it? Keep in mind the empathy and healthy communication practices mentioned previously.\n>".format(self._curr_person))
                    new_entry.add_intended(intended)
                else:
                    next_steps = input("That's okay, you'll get there at whatever time is right for you. What steps can you take to feel more secure with {0}?\n>".format(self._curr_person))
                    new_entry.add_steps_to_secure(next_steps)
            support = input("Experiencing a strain in one relationship can sometimes feel destabilizing. It's important that you exercise self compassion in seeking support from others. Where do you feel like you can get support right now?\n>")
            new_entry.add_support_from_others(support)
            done = input("Let's remember that if you've acted unpleasantly, you're not doing it on purpose. You're just expressing yourself in a way that's familiar to you and trying to get your needs met.\nType anything to continue.\n>")
            print("Self compassion may be unfamiliar because you've learned to condemn, criticize, or judge yourself when you learn something you don't like about yourself.\nLet's zoom in on how you reacted to the conflict between you and {0}.".format(self._curr_person))
            filler = input("Zoom in on yourself during your conflict and repeat one or more of the following phrases:\nI see how you suffer just as anyone else does.\nMay you be happy.\nMay you be free from pain.\nAnything else that the you in the scene needs to hear in order to know that this difficulty is seen and acknowledged.\nType anything to continue.\n>")
            
            appreciate_person = input("When it comes to anxious attachments, sometimes conflicts can overwhelm our sense of stability in the relationship.\nWe can ground ourselves through gratitude. What is one thing you appreciate about {0}?\n>".format(self._curr_person))
            new_entry.add_appreciate_other(appreciate_person)
            appreciate_self = input("We still need to keep in mind self-compassion. What is one thing you appreciate about yourself today?\n>")
            new_entry.add_appreciate_self(appreciate_self)
        else:
            gratitude = input("Finally, sometimes it's important to take the time to focus on the positive. Tell me more about the importance of this relationship in your life and why you're grateful for it.\n>".format(self._curr_person))
            new_entry.add_gratitude(gratitude)
        self._session.add(new_entry)
        self._session.commit()
        return new_entry
    
    def _trigger_entry(self, new_submission):
        pass
    
    def _check_stats(self):
        ls = get_stats(self, obj, filter, session, names=None)
    def _fetch_transcript(self):
        submissions = self._journal.get_submissions()
        while True:
            print("Please select which submission you would like to save as a file.")
            count = 1
            for s in submissions:
                print(count, s._date)
                count += 1
            print("return to main menu")
            sub_num = input(">")
            if sub_num == "return to main menu":
                return
            submission = self._journal.get_submission(int(sub_num) - 1)
            submission.write_submission_to_file(sub_num)
            print("Submission has been written to file.")

    def _quit(self):
        sys.exit(0)

if __name__ == "__main__":
    engine = create_engine(f"sqlite:///journal.db")
    Base.metadata.create_all(engine)

    Session = sessionmaker()
    Session.configure(bind=engine)
    sesh = Session()
    JournalCLI().run()


        