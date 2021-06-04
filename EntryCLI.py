from CLI_static import print_text, print_error, validate, get_input, add_and_commit
from Entry import InterpersonalConflict
from Journal import People
from Exceptions import IncorrectResponse

class EntryCLI():
    def __init__(self, submission, journal, session):
        self.submission = submission
        self._curr_person = None
        self._journal = journal
        self.session = session

    def run(self):
        discuss = True
        while discuss:
            self.validate_person()   
            new_entry = self._create_conflict_entry()
            self.submission.add_entry(new_entry)
            add_and_commit(self.session, [new_entry, self.submission])
            if not validate(new_entry.yes_or_no, "another relationship"):
                print_text("not another relationship")
                discuss = False
    
    def validate_person(self):
        while True:
            try: 
                self._choose_person()
                break
            except IncorrectResponse as e:
                print_error(e)
    
    def _choose_person(self):
        name_ls = self._journal.get_people()
        print_text("select person")
        print('\n'.join(name_ls))
        choice = input(">")
        if choice in name_ls: 
            self._curr_person = choice
        elif choice.lower() == "new person":
            self._curr_person = self._new_person(name_ls)
        else:
            raise IncorrectResponse(name_ls)
    
    def _new_person(self, name_ls):
        self._chosen_person = get_input("new person")
        self.validate_new_person(name_ls)
        new_person = People(self._chosen_person)
        self._journal.add_person(new_person)
        add_and_commit(self.session, [new_person, self._journal])
        return new_person._person
    
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
                return new_choice

    def _create_conflict_entry(self):
        new_entry = InterpersonalConflict(self._curr_person)
        self.respond_to_communal_strength(new_entry)
        validate(new_entry.add_anxiety, "anxiety")

        if not validate(new_entry.yes_or_no, "conflict", self._curr_person): 
            self.add_input_to_entry(new_entry.add_gratitude, "gratitude", self._curr_person)   
        else:
            self.process_conflict(new_entry)  
        add_and_commit(self.session, [new_entry])
        return new_entry 

    def respond_to_communal_strength(self, new_entry):
        close = validate(new_entry.add_communal_strength, "closeness", self._curr_person)
        print_text("glad to hear", self._curr_person) if close else print_text("sorry to hear", self._curr_person)

    def add_input_to_entry(self, adder, input_string, input_placeholder=None):
        toAdd = get_input(input_string, input_placeholder)
        adder(toAdd)

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
        
        display_communication_score = get_input("communication score", str(new_entry._communication_score))
        conclusion = get_input("effective communication", self._curr_person)

    def prepare_to_address(self, new_entry):
        if validate(new_entry.yes_or_no, "how to begin", self._curr_person):
            self.add_input_to_entry(new_entry.add_how_to_approach, "how to approach", self._curr_person)
            self.add_input_to_entry(new_entry.add_their_side, "their side", self._curr_person)
            print_text("healthy communication", self._curr_person)
            self.add_input_to_entry(new_entry.add_how_to_frame, "how to frame", self._curr_person)
            self.add_input_to_entry(new_entry.add_intended, "intended", self._curr_person)
        else:
            next_steps = get_input("next steps", self._curr_person)
            new_entry.add_steps_to_secure(next_steps)            

    def appreciation_and_support(self, new_entry):
        support = get_input("support")
        new_entry.add_support_from_others(support)
        self_compassion = get_input("self compassion", self._curr_person)            
        appreciate_person = get_input("appreciate person", self._curr_person)
        new_entry.add_appreciate_other(appreciate_person)
        appreciate_self = get_input("appreciate self")
        new_entry.add_appreciate_self(appreciate_self)
