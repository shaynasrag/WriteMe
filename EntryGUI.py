from sqlalchemy.sql.sqltypes import String
from static import print_text, validate, get_input, add_and_commit, yes_or_no, get_text
from Entry import InterpersonalConflict

from tkinter import *

class EntryGUI():
    def __init__(self, submission, journal, session, myJournal, submission_frame):
        self.submission = submission
        self._journal = journal
        self.session = session
        self._myJournal = myJournal
        self.entry = None
        self._curr_person = None
        submission_frame.destroy()

        self.choose_person_frame = Frame(self._myJournal)
        self.new_person_frame = Frame(self._myJournal)
        self.begin_conflict_frame = Frame(self._myJournal)
        self.check_to_talk_frame = Frame(self._myJournal)
        self.has_addressed_frame = Frame(self._myJournal)
        self.eff_comm_frame = Frame(self._myJournal)
        self.conclusion_frame = Frame(self._myJournal)
        self.how_to_begin = Frame(self._myJournal)
        self.appreciate_self_frame = Frame(self._myJournal)

        self.boolVar = StringVar()

    def run(self):
        self.conclusion_frame.destroy()
        self.entry = InterpersonalConflict(self._curr_person)
        self.choose_person(self._journal.get_people())   

    def begin_conflict_entry(self): #done
        self.choose_person_frame.destroy()
        self.begin_conflict_frame.destroy()
        self.begin_conflict_frame = Frame(self._myJournal)
        Label(self.begin_conflict_frame, text = get_text("closeness", self._curr_person)).grid(row=0, column=0)
        self.closeness = StringVar()
        Radiobutton(self.begin_conflict_frame, text = "Close", variable = self.closeness, value= "close").grid(row=1, column=0)
        Radiobutton(self.begin_conflict_frame, text = "Not So Close", variable = self.closeness, value= "not so close").grid(row=2, column=0)
        Radiobutton(self.begin_conflict_frame, text = "Distanced", variable = self.closeness, value= "distanced").grid(row=3, column=0)
        Button(self.begin_conflict_frame, text = "Next", command = self.add_closeness).grid(row=4, column=0)
        self.begin_conflict_frame.grid(row=0, column=0)

    def add_closeness(self): #done
        self.begin_conflict_frame.destroy()
        close = self.entry.add_communal_strength(self.closeness.get())
        add_and_commit(self.session, [self.entry])
        self.close_frame = Frame(self._myJournal)
        if close:
            Label(self.close_frame, text = get_text("glad to hear", self._curr_person)).grid(row=0,column=0)
        else:
            Label(self.close_frame, text = get_text("sorry to hear", self._curr_person)).grid(row=0,column=0)
        Button(self.close_frame, text = "Next", command= self.anxiety).grid(row=1,column=0)
        self.close_frame.grid(row=0, column=0)
    
    def anxiety(self): #done
        self.close_frame.destroy()
        self.anxiety_frame = Frame(self._myJournal)
        self.anxietyVar = StringVar()
        Label(self.anxiety_frame, text = get_text("anxiety")).grid(row=0,column=0)
        Radiobutton(self.anxiety_frame, text = "High Anxiety", variable = self.anxietyVar, value= "high anxiety").grid(row=1, column=0)
        Radiobutton(self.anxiety_frame, text = "Mid Anxiety", variable = self.anxietyVar, value= "mid anxiety").grid(row=2, column=0)
        Radiobutton(self.anxiety_frame, text = "Low Anxiety", variable = self.anxietyVar, value= "low anxiety").grid(row=3, column=0)
        Radiobutton(self.anxiety_frame, text = "No Anxiety", variable = self.anxietyVar, value= "no anxiety").grid(row=4, column=0)
        Button(self.anxiety_frame, text = "Next", command = self.add_anxiety).grid(row=5, column=0)
        self.anxiety_frame.grid(row=0, column=0)

    def add_anxiety(self): #done
        self.anxiety_frame.destroy()
        self.entry.add_anxiety(self.anxietyVar.get())
        add_and_commit(self.session, [self.entry])
        self.check_to_talk()
    
    def check_to_talk(self): #done
        self.check_to_talk_frame = Frame(self._myJournal)
        Label(self.check_to_talk_frame, text = get_text("conflict", self._curr_person)).grid(row=0, column=0)
        Radiobutton(self.check_to_talk_frame, text = "Yes", variable = self.boolVar, value= "yes", command=self.talk_about_conflict).grid(row=1, column=0)
        Radiobutton(self.check_to_talk_frame, text = "No", variable = self.boolVar, value= "no", command=self.gratitude).grid(row=2, column=0)
        self.check_to_talk_frame.grid(row=0,column=0)

    def gratitude(self): #done
        self.check_to_talk_frame.destroy()
        self.gratitude_frame = Frame(self._myJournal)
        self.gratitude_text = Text(self.gratitude_frame)
        Label(self.gratitude_frame, text = get_text("gratitude", self._curr_person)).grid(row=0,column=0)
        self.gratitude_text.grid(row=1,column=0)
        Button(self.gratitude_frame, text = "Next", command=self.add_gratitude).grid(row=2, column=0)
        self.gratitude_frame.grid(row=0,column=0)
    
    def add_gratitude(self): #done
        self.gratitude_frame.destroy()
        gratitude = self.gratitude_text.get("1.0", END)
        self.entry.add_gratitude(gratitude)
        self.conclusion()

    def talk_about_conflict(self): #done
        self.check_to_talk_frame.destroy()
        self.conflict_frame = Frame(self._myJournal)
        Label(self.conflict_frame, text = get_text("conflict description")).grid(row=0,column=0)
        self.conflict_text = Text(self._myJournal)
        self.conflict_text.grid(row=1,column=0)
        Button(self.conflict_frame, text="Next", command=self.add_conflict).grid(row=2,column=0)
        self.conflict_frame.grid(row=0,column=0)

    def add_conflict(self): #done
        self.conflict_frame.destroy()
        self.conflict = self.conflict_text.get("1.0",END)
        self.entry.add_conflict(self.conflict)
        self.take_space()
    
    def take_space(self): #done
        self.space_frame = Frame(self._myJournal)
        Label(self.space_frame, text = get_text("space")).grid(row=0,column=0)
        Button(self.space_frame, text = "Next", command=self.has_addressed).grid(row=1,column=0)
        self.space_frame.grid(row=0,column=0)

    def has_addressed(self): #done
        self.space_frame.destroy()
        self.has_addressed_frame = Frame(self._myJournal)
        Label(self.has_addressed_frame, text = get_text("addressed", self._curr_person)).grid(row=0, column=0)
        Radiobutton(self.has_addressed_frame, text = "Yes", variable = self.boolVar, value= "yes", command=self.review_conflict).grid(row=1, column=0)
        Radiobutton(self.has_addressed_frame, text = "No", variable = self.boolVar, value= "no", command=self.brainstorm_how_to_resolve).grid(row=2, column=0)
        self.has_addressed_frame.destroy()

    def review_conflict(self): #done
        self.has_addressed_frame.destroy()
        self.addressed_frame = Frame(self._myJournal)
        Label(self.addressed_frame, text = get_text("how addressed")).grid(row=0,column=0)
        self.addressed_text = Text(self._myJournal)
        self.addressed_text.grid(row=1,column=0)
        Button(self.addressed_frame, text = "Next", command = self.get_addressed)
        self.addressed_frame.grid(row=0,column=0)
        
    def get_addressed(self): #done
        self.has_addressed_frame.destroy()
        self.addressed = self.addressed_text.get("1.0", END)
        self.entry.add_addressed(self.addressed)
        self.add_consent()

    def check_consent(self): #done
        self.consent_frame = Frame(self._myJournal)
        Label(self.consent_frame, text = get_text("consent", self._curr_person)).grid(row=0, column=1)
        self.consentVar = IntVar()
        Radiobutton(self.consent_frame, text = "Yes", variable = self.consentVar, value= 0, command=self.add_consent).grid(row=1, column=0)
        Radiobutton(self.consent_frame, text = "No", variable = self.consentVar, value= 1, command=self.add_consent).grid(row=2, column=0)
        self.consent_frame.grid(row=0,column=0)

    def add_consent(self): #done
        consent = "yes" if self.consentVar.get() == 0 else "no"
        self.entry.add_consent(consent)
        self.consent_frame.destroy()
        self.check_self_soothe()
    
    def check_self_soothe(self): #done
        self.self_soothe_frame = Frame(self._myJournal)
        Label(self.self_soothe_frame, text = get_text("self soothe1")).grid(row=0, column=1)
        self.self_sootheVar = IntVar()
        Radiobutton(self.self_soothe_frame, text = "Yes", variable = self.self_sootheVar, value= 0, command=self.add_self_soothe).grid(row=1, column=0)
        Radiobutton(self.self_soothe_frame, text = "No", variable = self.self_sootheVar, value= 1, command=self.add_self_soothe).grid(row=2, column=0)
        self.self_soothe_frame.grid(row=0,column=0)

    def add_self_soothe(self): #done
        self_soothe = "yes" if self.self_sootheVar.get() == 0 else "no"
        self.entry.add_self_soothe1(self_soothe)
        self.self_soothe_frame.destroy()
        self.check_other_soothe()
    
    def check_other_soothe(self): #done
        self.other_soothe_frame = Frame(self._myJournal)
        Label(self.other_soothe_frame, text = get_text("other soothe1", self._curr_person)).grid(row=0, column=1)
        self.other_sootheVar = IntVar()
        Radiobutton(self.other_soothe_frame, text = "Yes", variable = self.other_sootheVar, value= 0, command=self.add_other_soothe).grid(row=1, column=0)
        Radiobutton(self.other_soothe_frame, text = "No", variable = self.other_sootheVar, value= 1, command=self.add_other_soothe).grid(row=2, column=0)
        self.other_soothe_frame.grid(row=0,column=0)

    def add_other_soothe(self): #done
        other_soothe = "yes" if self.other_sootheVar.get() == 0 else "no"
        self.entry.add_other_soothe1(other_soothe)
        self.other_soothe_frame.destroy()
        self.display_communication_score()
    
    def display_communication_score(self): #done
        self.comm_score_frame = Frame(self._myJournal)
        Label(self.comm_score_frame, text = get_text("communication score", str(self.entry._communication_score))).grid(row=0, column=0)
        Button(self.comm_score_frame, text = "Next", command= self.effective_communication()).grid(row=1, column=0)
        self.comm_score_frame.grid(row=0,column=0)
    
    def effective_communication(self): #done
        self.eff_comm_frame = Frame(self._myJournal)
        Label(self.eff_comm_frame, text = get_text("effective communication", self._curr_person)).grid(row=0, column=0)
        Button(self.eff_comm_frame, text = "Next", command= self.appreciation_and_support).grid(row=1, column=0)
        self.eff_comm_frame.grid(row=0,column=0)

    def brainstorm_how_to_resolve(self):
        self.how_to_begin_frame = Frame(self._myJournal)
        Label(self.how_to_begin_frame, text=get_text("how to begin", self._curr_person)).grid(row=0,column=1)
        Button(self.how_to_begin_frame, text="Yes", command=self.add_how_to_approach).grid(row=1, column=0)
        Button(self.how_to_begin_frame, text = "No", command=self.add_steps_to_secure).grid(row=2, column=0)
    
    def add_steps_to_secure(self):
        self.how_to_begin_frame.destroy()
        self.steps_frame = Frame(self._myJournal)
        Label(self.steps_frame, text = get_text("next steps", self._curr_person)).grid(row=0,column=0)
        self.steps_text = Text(self._myJournal)
        self.steps_text.grid(row=1,column=0)
        Button(self.steps_frame, text = "Next", command = self.get_steps)
        self.steps_frame.grid(row=0,column=0)
    
    def get_steps(self): #done
        self.steps_frame.destroy()
        self.steps = self.steps_text.get("1.0", END)
        self.entry.add_steps_to_secure(self.steps)
        self.appreciation_and_support()

    def add_how_to_approach(self):
        self.approach_frame = Frame(self._myJournal)
        Label(self.approach_frame, text = get_text("how to approach", self._curr_person)).grid(row=0,column=0)
        self.approach_text = Text(self._myJournal)
        self.approach_text.grid(row=1,column=0)
        Button(self.approach_frame, text = "Next", command = self.get_approach)
        self.approach_frame.grid(row=0,column=0)
    
    def get_approach(self): #done
        self.approach_frame.destroy()
        self.approach = self.approach_text.get("1.0", END)
        self.entry.add_how_to_approach(self.approach)
        self.add_their_side()
    
    def add_their_side(self):
        self.their_side_frame = Frame(self._myJournal)
        Label(self.their_side_frame, text = get_text("their side", self._curr_person)).grid(row=0,column=0)
        self.their_side_text = Text(self._myJournal)
        self.their_side_text.grid(row=1,column=0)
        Button(self.their_side_frame, text = "Next", command = self.get_their_side)
        self.their_side_frame.grid(row=0,column=0)
    
    def get_their_side(self): #done
        self.their_side_frame.destroy()
        self.their_side = self.their_side_text.get("1.0", END)
        self.entry.add_their_side(self.their_side)
        self.healthy_communication()
    
    def healthy_communication(self):
        self.healthy_communication_frame = Frame(self._myJournal)
        Label(self.healthy_communication_frame, text = get_text("healthy communication", self._curr_person)).grid(row=0,column=0)
        Button(self.healthy_communication_frame, text = "Next", command = self.add_how_to_frame)
        self.healthy_communication_frame.grid(row=0,column=0)
    
    def add_how_to_frame(self):
        self.how_to_frame = Frame(self._myJournal)
        Label(self.how_to_frame, text = get_text("their side", self._curr_person)).grid(row=0,column=0)
        self.how_to_frame_text = Text(self._myJournal)
        self.how_to_frame_text.grid(row=1,column=0)
        Button(self.how_to_frame, text = "Next", command = self.get_how_to_frame)
        self.how_to_frame.grid(row=0,column=0)
    
    def get_how_to_frame(self): #done
        self.how_to_frame.destroy()
        self.how_to_fr = self.how_to_frame_text.get("1.0", END)
        self.entry.add_how_to_frame(self.how_to_fr)
        self.add_intended()
    
    def add_intended(self):
        self.intended_frame = Frame(self._myJournal)
        Label(self.intended_frame, text = get_text("intended", self._curr_person)).grid(row=0,column=0)
        self.intended_text = Text(self._myJournal)
        self.intended_text.grid(row=1,column=0)
        Button(self.intended_frame, text = "Next", command = self.get_intended)
        self.intended_frame.grid(row=0,column=0)
    
    def get_intended(self): #done
        self.intended_frame.destroy()
        self.intended = self.intended_text.get("1.0", END)
        self.entry.add_intended(self.intended)
        self.appreciation_and_support()

    def appreciation_and_support(self): #done
        self.eff_comm_frame.destroy()
        #TODO: destroy frame from other path
        self.support_frame = Frame(self._myJournal)
        Label(self.support_frame, text = get_text("support")).grid(row=0,column=0)
        self.support_text = Text(self._myJournal)
        self.support_text.grid(row=1,column=0)
        Button(self.support_frame, text = "Next", command = self.get_support)
        self.support_frame.grid(row=0,column=0)

    def get_support(self): #done
        self.support_frame.destroy()
        self.support = self.addressed_text.get("1.0", END)
        self.entry.add_support_from_others(self.support)
        self.self_compassion()

    def self_compassion(self): #done
        self.self_compassion_frame = Frame(self._myJournal)
        Label(self.self_compassion_frame, text = get_text("self compassion", self._curr_person)).grid(row=0, column=0)
        Button(self.self_compassion_frame, text = "Next", command= self.add_appreciate_other).grid(row=1, column=0)
        self.self_compassion_frame.grid(row=0,column=0)
    
    def add_appreciate_other(self): #done
        self.self_compassion_frame.destroy()
        self.appreciate_other_frame = Frame(self._myJournal)
        Label(self.appreciate_other_frame, text = get_text("appreciate person", self._curr_person)).grid(row=0,column=0)
        self.appreciate_other_text = Text(self._myJournal)
        self.appreciate_other_text.grid(row=1,column=0)
        Button(self.appreciate_other_frame, text = "Next", command = self.get_appreciate_other)
        self.appreciate_other_frame.grid(row=0,column=0)

    def get_appreciate_other(self): #done
        self.appreciate_other_frame.destroy()
        self.appreciate_other = self.appreciate_other_text.get("1.0", END)
        self.entry.add_appreciate_other(self.appreciate_other)
        self.add_appreciate_self()

    def add_appreciate_self(self): #done
        self.appreciate_other_frame.destroy()
        self.appreciate_self_frame = Frame(self._myJournal)
        Label(self.appreciate_self_frame, text = get_text("appreciate self")).grid(row=0,column=0)
        self.appreciate_self_text = Text(self._myJournal)
        self.appreciate_self_text.grid(row=1,column=0)
        Button(self.appreciate_self_frame, text = "Next", command = self.get_appreciate_self)
        self.appreciate_self_frame.grid(row=0,column=0)

    def get_appreciate_self(self): #done
        self.appreciate_self_frame.destroy()
        self.appreciate_self = self.appreciate_other_text.get("1.0", END)
        self.entry.add_appreciate_self(self.appreciate_self)
        self.conclusion() 
    
    def conclusion(self): #done
        self.submission.add_entry(self.entry)
        add_and_commit(self.session, [self.entry, self.submission])
        self.appreciate_self_frame.destroy()
        self.conclusion_frame = Frame(self._myJournal)
        Label(self.conclusion_frame, text=get_text("another relationship")).grid(row=0,column=1)
        Button(self.conclusion_frame, text="Yes", command=self.run).grid(row=1, column=0)
        Button(self.conclusion_frame, text = "No", command=self.exit).grid(row=2, column=0)
        self.conclusion_frame.grid(row=0,column=0)

    def exit(self): #done
        self.conclusion_frame.destroy()
        self.exit_frame = Frame(self._myJournal)
        Label(self.exit_frame, text=get_text("not another relationship")).grid(row=0,column=1)
        Button(self.exit_frame, text="Return to Main Menu", command=self.end).grid(row=1, column=0)

    def end(self): #done
        self.exit_frame.destroy()
        self.JournalGUI.show_main_menu()

    def choose_person(self, name_ls): #done
        self.choose_person_frame = Frame(self._myJournal)
        self.person_var = StringVar()
        Button(self.choose_person_frame, text = "Next", command= self.select_person).grid(row= len(name_ls) + 2, column=0)
        row = 1
        Label(self.choose_person_frame, text="Who would you like to journal about today?").grid(row=0, column=0)
        for person in name_ls:
            Radiobutton(self.choose_person_frame, text = person, variable = self.person_var, value= person).grid(row=row, column = 0)
            row += 1
        Radiobutton(self.choose_person_frame, text = "New Person", variable = self.person_var, value= person).grid(row=row, column=0)
        row += 1
        self.choose_person_frame.grid(row=0, column=0)

    def select_person(self): #done
        name = self.person_var.get()
        self.choose_person_frame.destroy()
        if name not in self._journal.get_people():
            self.add_new_person()
        else:
            self._curr_person = name
            self.begin_conflict_entry()
    
    def add_new_person(self): #done
        self.new_person_frame = Frame(self._myJournal)
        Label(self.new_person_frame, text="Add a new person to your journal by typing their name below and clicking 'Next'").grid(row=0,column=0)
        self.new_person_entry = Entry(self.new_person_frame)
        Button(self.new_person_frame, text = "Next", command = self.add_person).grid(row=2, column=0)
        self.new_person_entry.grid(row=1,column=0)
        self.new_person_frame.grid(row=0,column=0)
    
    def add_person(self): #done
        new_person = self.new_person_entry.get()
        new_name = self._journal.add_person(new_person)
        if new_name:
            add_and_commit(self.session, [new_person, self._journal])
        self._curr_person = new_person
        self.begin_conflict_entry()