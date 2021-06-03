import sys
from Journal import Journal, People
from Exceptions import IncorrectResponse
from Entry import Base, Entry, InterpersonalConflict
from Submission import Submission
from CLI_static import print_error, print_text, get_input, validate

from sqlalchemy import Column, Integer, String, ForeignKey, Table, MetaData, create_engine
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.session import sessionmaker

from sqlalchemy.types import TypeDecorator
import matplotlib.pyplot as plt


class JournalCLI(Base):
    def __init__(self):
        self._session = Session()
        self._journal = self.get_journal()
        self._choices = {
            "add submission": self._create_submission,
            "check stats": self._check_stats,
            "fetch transcript": self._fetch_transcript,
            "quit": self._quit,
        }
        self._types_of_submissions = {
            "interpersonal conflict": self._conflict_entry_driver,
            "emotional trigger": self._trigger_entry,  # TODO: add functionality          
        }
        self.options = ", ".join(self._choices.keys())
        self.submission_options = "\n".join(self._types_of_submissions.keys())
        self._curr_person = None
        self._chosen_person = None
    
    def get_journal(self):
        journal = self._session.query(Journal).first()
        if not journal:
            journal = Journal()
            self.add_and_commit([self._journal])
        return journal

    def run(self):
        while True:
            self._display_menu()
            choice = input(">")
            action = self._choices.get(choice)
            if action:
                action()
            else:
                print_text("not valid", choice)

    def _display_menu(self):
        if not self._journal._name:
            name = get_input("greeting_new")
            self._journal._name = name
        print_text("greeting_old", self._journal._name)
        print(self.options)
            
    def _create_submission(self):        
        while True:
            print_text("topic")
            print(self.submission_options, "\nreturn to main menu")
            choice = input(">")
            if choice == "return to main menu":
                return
            action = self._types_of_submissions.get(choice)
            self.validate_action(action)
                            
    def validate_action(self, action):
        if action:
                new_submission = Submission()
                self._journal.add_submission(new_submission)
                self.add_and_commit([new_submission])
                action(new_submission)
        else:
            print_text("Not a valid action")

    def _choose_person(self):
        name_ls = self.show_people()
        choice = input(">")
        if choice in name_ls: 
            self._curr_person = choice
        elif choice == "New Person":
            self._new_person(name_ls)
        else:
            raise IncorrectResponse(name_ls)
    
    def show_people(self):
        print_text("select person")
        name_ls = self._journal.get_people()
        for person in name_ls:
            print(person)
        return name_ls
    
    def _new_person(self, name_ls):
        self._chosen_person = get_input("new person")
        self.validate_new_person(name_ls)
        new_person = People(self._chosen_person)
        self._journal.add_person(new_person)
        self.add_and_commit([new_person, self._journal])
        self._curr_person = self._chosen_person
    
    def validate_new_person(self, name_ls):
        if self._chosen_person in name_ls:
            print_text("person exists", self._chosen_person)
            while True:                        
                new_choice = get_input("options/start again", self._chosen_person)
                if new_choice == self._chosen_person or new_choice.lower() == "start again":
                    break
                else:
                    print_text("wrong/start again", self._chosen_person)
            if new_choice == "Start Again":
                self._choose_person()
            else:
                self._curr_person = new_choice     

    def _conflict_entry_driver(self, new_submission):
        discuss = True
        while discuss:
            self.validate_person()   
            new_entry = self._create_conflict_entry()
            new_submission.add_entry(new_entry)
            self.add_and_commit([new_entry, new_submission])
            if not self.validate(new_entry, "another relationship"):
                print_text("not another relationship")
                discuss = False  

    def _create_conflict_entry(self):
        new_entry = InterpersonalConflict(self._curr_person)

        self.respond_to_communal_strength(new_entry)
        validate(new_entry.add_anxiety, "anxiety")

        if not validate(new_entry.yes_or_no, "conflict", self._curr_person):    
            gratitude = get_input("gratitude", self._curr_person)
            new_entry.add_gratitude(gratitude)
        else:
            self.process_conflict(new_entry)
        
        self.add_and_commit([new_entry])
        return new_entry
    
    def respond_to_communal_strength(self, new_entry):
        close = validate(new_entry.add_communal_strength, "closeness")
        print_text("glad to hear", self._curr_person) if close else print_text("sorry to hear", self._curr_person)


    def process_conflict(self, new_entry):
        conflict_description = get_input("conflict description")
        new_entry.add_conflict(conflict_description)
        space = get_input("space")
        if validate(new_entry.yes_or_no, "addressed", self._curr_person):
            self.review_conflict(new_entry)
        else:
            self.prepare_to_address(new_entry)
        self.appreciation_and_support(new_entry)
            
    def review_conflict(self, new_entry):
        self.add_input_to_entry(new_entry.add_addressed, "how addressed")

        validate(new_entry.add_consent, "consent", self._curr_person)
        validate(new_entry.add_self_soothe1, "self soothe1")
        validate(new_entry.add_other_soothe1, "other soothe1", self._curr_person)
        
        display_communication_score = get_input("communication score", new_entry._communication_score)
        conclusion = get_input("effective communication", self._curr_person)

    def prepare_to_address(self, new_entry):
        if validate(new_entry.yes_or_no, "how to begin", self._curr_person):
            self.add_input_to_entry(new_entry.add_how_to_approach, "how to approach", self._curr_person)
            self.add_input_to_entry(new_entry.add_their_side, "their side", self._curr_person)
            print_text("healthy communication", self._curr_person)
            self.add_input_to_entry(new_entry.add_how_to_frame, "how to frame", self._curr_person)
            self.add_input_to_entry(new_entry.intended, "intended", self._curr_person)
        else:
            next_steps = get_input("next steps", self._curr_person)
            new_entry.add_steps_to_secure(next_steps)            

    def add_input_to_entry(self, adder, input_string, input_placeholder):
        toAdd = get_input(input_string, input_placeholder)
        adder(toAdd)

    def appreciation_and_support(new_entry):
        support = get_input("support")
        new_entry.add_support_from_others(support)
        self_compassion = get_input("self compassion", self._curr_person)            
        appreciate_person = get_input("appreciate person", self._curr_person)
        new_entry.add_appreciate_other(appreciate_person)
        appreciate_self = get_input("appreciate self")
        new_entry.add_appreciate_self(appreciate_self)

    def _trigger_entry(self, new_submission):
        pass
    
    def _check_stats(self):
        pass
        
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
    
    def add_and_commit(self, add_list):
        for thingToAdd in add_list:
            self._session.add(thingToAdd)
        self._session.commit()
    
    def validate_person(self):
        while True:
            try: 
                self._choose_person()
                break
            except IncorrectResponse as e:
                print_error(e) 
    
    def _quit(self):
        sys.exit(0)

class Submission(JournalCLI):


if __name__ == "__main__":
    engine = create_engine(f"sqlite:///journal.db")
    Base.metadata.create_all(engine)

    Session = sessionmaker()
    Session.configure(bind=engine)
    sesh = Session()
    JournalCLI().run()
