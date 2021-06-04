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
        self.entry = None

    def run(self):
        discuss = True
        while discuss:
            self.validate_person()   
            new_entry = self.create_conflict_entry()
            self.entry = new_entry
            self.submission.add_entry(self.entry)
            add_and_commit(self.session, [self.entry, self.submission])
            if not validate(self.entry.yes_or_no, "another relationship"):
                print_text("not another relationship")
                discuss = False

    def create_conflict_entry(self):
        self.entry = InterpersonalConflict(self._curr_person)
        self.respond_to_communal_strength()
        validate(self.entry.add_anxiety, "anxiety")

        if not validate(self.entry.yes_or_no, "conflict", self._curr_person): 
            self.add_input_to_entry(self.entry.add_gratitude, "gratitude", self._curr_person)   
        else:
            self.talk_about_conflict()  
        add_and_commit(self.session, [self.entry])
        return self.entry 

    def respond_to_communal_strength(self):
        close = validate(self.entry.add_communal_strength, "closeness", self._curr_person)
        print_text("glad to hear", self._curr_person) if close else print_text("sorry to hear", self._curr_person)

    def talk_about_conflict(self):
        self.add_input_to_entry(self.entry.add_conflict, "conflict description")
        space = get_input("space")
        if validate(self.entry.yes_or_no, "addressed", self._curr_person):
            self.review_conflict()
        else:
            self.brainstorm()
        self.appreciation_and_support()
    
    def review_conflict(self):
        self.add_input_to_entry(self.entry.add_addressed, "how addressed")
        validate(self.entry.add_consent, "consent", self._curr_person)
        validate(self.entry.add_self_soothe1, "self soothe1")
        validate(self.entry.add_other_soothe1, "other soothe1", self._curr_person)
        
        display_communication_score = get_input("communication score", str(self.entry._communication_score))
        conclusion = get_input("effective communication", self._curr_person)

    def brainstorm(self):
        if validate(self.entry.yes_or_no, "how to begin", self._curr_person):
            self.add_input_to_entry(self.entry.add_how_to_approach, "how to approach", self._curr_person)
            self.add_input_to_entry(self.entry.add_their_side, "their side", self._curr_person)
            print_text("healthy communication", self._curr_person)
            self.add_input_to_entry(self.entry.add_how_to_frame, "how to frame", self._curr_person)
            self.add_input_to_entry(self.entry.add_intended, "intended", self._curr_person)
        else:
            self.add_input_to_entry(self.entry.add_steps_to_secure, "next steps", self._curr_person)

    def appreciation_and_support(self):
        self.add_input_to_entry(self.entry.add_support_from_others, "support")
        self_compassion = get_input("self compassion", self._curr_person)   
        self.add_input_to_entry(self.entry.add_appreciate_other, "appreciate person", self._curr_person)         
        self.add_input_to_entry(self.entry.add_appreciate_self, "appreciate self")
    
    def add_input_to_entry(self, adder, input_string, input_placeholder=None):
        toAdd = get_input(input_string, input_placeholder)
        adder(toAdd)
        add_and_commit(self.session, [self.entry])

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