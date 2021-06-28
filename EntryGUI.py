from static import add_and_commit, get_text
from Entry import InterpersonalConflict

from tkinter import *

class EntryGUI():
    def __init__(self, submission, journal, session, myJournal, show_main_menu):
        self.submission = submission
        self._journal = journal
        self.session = session
        self._myJournal = myJournal
        self.show_main_menu = show_main_menu

        self.entry = None
        self._curr_person = None

        self.show_people_frame = Frame(self._myJournal)
        self.new_person_frame = Frame(self._myJournal)
        self.bool_adder_frame = Frame(self._myJournal)
        self.label_and_button_frame = Frame(self._myJournal)

        self.boolVar = StringVar()
        self.Var = StringVar()
        self.person_var = StringVar()
        self.done = False

    def run(self):
        self.bool_adder_frame.destroy()
        self.entry = InterpersonalConflict(self._curr_person)
        self.show_people(self._journal.get_people())  
    
    def radio_button(self, text, radiobuttons, func, frames_to_destroy=[]):
        [frame_to_destroy.destroy() for frame_to_destroy in frames_to_destroy]
        self.radio_button_frame = Frame(self._myJournal)
        Label(self.radio_button_frame, text=get_text(text, self._curr_person)).grid(row=0,column=0)
        row = 0  
        for radiobutton in radiobuttons:
            row +=1
            Radiobutton(self.radio_button_frame, text = radiobutton[0], variable = self.Var, value= radiobutton[1]).grid(row=row, column=0)
        Button(self.radio_button_frame, text = "Next", command = func).grid(row = row + 1, column=0)
        self.radio_button_frame.grid(row=0,column=0)

    def bool_adder(self, text, yes_func, no_func, frame_to_destroy=None):
        if frame_to_destroy:
            frame_to_destroy.destroy()
        self.bool_adder_frame.destroy()
        self.bool_adder_frame = Frame(self._myJournal)
        Label(self.bool_adder_frame, text = get_text(text, self._curr_person)).grid(row=0, column=0)
        Radiobutton(self.bool_adder_frame, text = "Yes", variable = self.boolVar, value= "yes", command=yes_func).grid(row=1, column=0)
        Radiobutton(self.bool_adder_frame, text = "No", variable = self.boolVar, value= "no", command=no_func).grid(row=2, column=0)
        self.bool_adder_frame.grid(row=0,column=0)

    def bool_getter(self, func, next_func):
        toAdd = self.boolVar.get()
        func(toAdd)
        self.bool_adder_frame.destroy()
        add_and_commit(self.session, [self.entry, self.submission])
        next_func()

    def adder(self, text, func, next_func, frames_to_destroy=[]):
        [frame_to_destroy.destroy() for frame_to_destroy in frames_to_destroy]
        self.adder_frame = Frame(self._myJournal)
        Label(self.adder_frame, text = get_text(text, self._curr_person)).grid(row=0,column=0)
        self.adder_text = Text(self.adder_frame)
        self.adder_text.grid(row=1,column=0)
        Button(self.adder_frame, text = "Next", command = self.getter).grid(row=2,column=0)
        self.getter_func = func
        self.next_func = next_func
        self.adder_frame.grid(row=0,column=0)

    def getter(self):
        self.toAdd = self.adder_text.get("1.0", "end-1c")
        self.adder_frame.destroy()
        self.getter_func(self.toAdd)
        add_and_commit(self.session, [self.entry, self.submission])
        self.next_func()
    
    def label_and_button(self, text, toReplace, func, frames_to_destroy=[]):
        [frame_to_destroy.destroy() for frame_to_destroy in frames_to_destroy]
        self.label_and_button_frame = Frame(self._myJournal)
        Label(self.label_and_button_frame, text = get_text(text, toReplace)).grid(row=0, column=0)
        Button(self.label_and_button_frame, text= "Next", command = func).grid(row=1, column=0)
        self.label_and_button_frame.grid(row=0,column=0)

    def show_people(self, name_ls): 
        self.show_people_frame = Frame(self._myJournal)
        Button(self.show_people_frame, text = "Next", command= self.select_person).grid(row= len(name_ls) + 2, column=0)
        Label(self.show_people_frame, text="Who would you like to journal about today?").grid(row=0, column=0)
        row = 1
        for person in name_ls:
            Radiobutton(self.show_people_frame, text = person, variable = self.person_var, value= person).grid(row=row, column = 0)
            row += 1
        Radiobutton(self.show_people_frame, text = "New Person", variable = self.person_var, value= "new person").grid(row=row, column=0)
        self.show_people_frame.grid(row=0, column=0)

    def select_person(self): 
        name = self.person_var.get()
        self.show_people_frame.destroy()
        if name == "new person":
            self.get_new_person()
        else:
            self._curr_person = name
            self.begin_conflict_entry()
    
    def get_new_person(self): 
        self.new_person_frame = Frame(self._myJournal)
        Label(self.new_person_frame, text="Add a new person to your journal by typing their name below and clicking 'Next'").grid(row=0,column=0)
        self.new_person_entry = Entry(self.new_person_frame)
        Button(self.new_person_frame, text = "Next", command = self.add_new_person_to_journal).grid(row=2, column=0)
        self.new_person_entry.grid(row=1,column=0)
        self.new_person_frame.grid(row=0,column=0)
    
    def add_new_person_to_journal(self): 
        new_person = self.new_person_entry.get()
        self.new_person_frame.destroy()
        new_name = self._journal.add_person(new_person)
        if new_name:
            add_and_commit(self.session, [new_name, self._journal])
        self._curr_person = new_person
        self.begin_conflict_entry()
    
    def conclusion(self): 
        self.submission.add_entry(self.entry)
        add_and_commit(self.session, [self.entry, self.submission])
        self.bool_adder("another relationship", self.run, self.exit)
    
    def anxiety(self): 
        self.radio_button("anxiety", [["High Anxiety", "high anxiety"], ["Mid Anxiety", "mid anxiety"], ["Low Anxiety", "low anxiety"], ["No Anxiety", "no anxiety"]], self.add_anxiety, [self.label_and_button_frame])

    def begin_conflict_entry(self):
        self.radio_button("closeness", [["Close", "close"], ["Not So Close", "not so close"], ["Distanced", "distanced"]], self.add_closeness)

    def has_addressed(self): 
        self.bool_adder("addressed", self.review_conflict, self.brainstorm_how_to_resolve, self.label_and_button_frame)

    def check_consent(self): 
        self.bool_adder("consent", self.add_consent, self.add_consent)

    def check_self_soothe(self): 
        self.bool_adder("self soothe1", self.add_self_soothe, self.add_self_soothe)
    
    def check_other_soothe(self):
        self.bool_adder("other soothe1", self.add_other_soothe, self.add_other_soothe)
    
    def brainstorm_how_to_resolve(self):
        self.bool_adder("how to begin", self.add_how_to_approach, self.add_steps_to_secure)

    def add_consent(self): 
        self.bool_getter(self.entry.add_consent, self.check_self_soothe)

    def add_self_soothe(self):
        self.bool_getter(self.entry.add_self_soothe1, self.check_other_soothe)

    def add_other_soothe(self):
        self.bool_getter(self.entry.add_other_soothe1, self.display_communication_score)
    
    def add_steps_to_secure(self):
        self.adder("next steps", self.entry.add_steps_to_secure, self.appreciation_and_support, [self.bool_adder_frame])
    
    def gratitude(self):
        self.adder("gratitude", self.entry.add_gratitude, self.conclusion, [self.bool_adder_frame])
    
    def talk_about_conflict(self):
        self.adder("conflict description", self.entry.add_conflict, self.take_space, [self.bool_adder_frame])
    
    def review_conflict(self):
        self.adder("how addressed", self.entry.add_addressed, self.check_consent, [self.bool_adder_frame])
    
    def add_how_to_approach(self):
        self.adder("how to approach", self.entry.add_how_to_approach, self.add_their_side, [self.bool_adder_frame])
    
    def add_their_side(self):
        self.adder("their side", self.entry.add_their_side, self.healthy_communication)

    def add_how_to_frame(self):
        self.adder("how to frame", self.entry.add_how_to_frame, self.add_intended, [self.label_and_button_frame])
    
    def appreciation_and_support(self):
        self.adder("support", self.entry.add_support_from_others, self.self_compassion, [self.bool_adder_frame, self.label_and_button_frame])
    
    def add_appreciate_other(self):
        self.adder("appreciate person", self.entry.add_appreciate_other, self.add_appreciate_self, [self.label_and_button_frame])
    
    def add_intended(self):
        self.adder("intended", self.entry.add_intended, self.appreciation_and_support)
    
    def add_appreciate_self(self):
        self.adder("appreciate self", self.entry.add_appreciate_self, self.conclusion)

    def display_communication_score(self): 
        self.label_and_button("communication score", str(self.entry.get_attribute("total communication score")) ,self.effective_communication)

    def effective_communication(self):
        self.label_and_button("effective communication", self._curr_person, self.appreciation_and_support, [self.label_and_button_frame])

    def take_space(self):
        self.label_and_button("space", self._curr_person, self.has_addressed)
    
    def healthy_communication(self):
        self.label_and_button("healthy communication", self._curr_person, self.add_how_to_frame)
    
    def self_compassion(self):
        self.label_and_button("self compassion", self._curr_person, self.add_appreciate_other)

    def exit(self): 
        self.label_and_button("not another relationship", self._curr_person, self.return_to_main_menu, [self.bool_adder_frame, self.label_and_button_frame])

    def return_to_main_menu(self):
        self.label_and_button_frame.destroy()
        self.show_main_menu()
    
    def add_anxiety(self):
        self.entry.add_anxiety(self.Var.get())
        self.bool_adder("conflict", self.talk_about_conflict, self.gratitude, self.radio_button_frame)
    
    def add_closeness(self):
        close = self.entry.add_communal_strength(self.Var.get())
        text = "glad to hear" if close else "sorry to hear"
        self.label_and_button(text, self._curr_person, self.anxiety, [self.radio_button_frame])