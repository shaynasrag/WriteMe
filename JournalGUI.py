from tkinter import *
import sys
from Journal import Journal
from Entry import Base 
from static import print_text, get_input, add_and_commit, get_today, get_text
from ActionGUI import TranscriptGUI, StatsGUI
from EntryGUI import EntryGUI
from strings import text_dict

from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker

class JournalGUI():
    def __init__(self):
        self.session = Session()
        self.journal = self.set_journal()
        add_and_commit(self.session, [self.journal])
        self._myJournal = Tk()
        self._myJournal.title("MY JOURNAL")
        
        self.curr_person = None
        self.chosen_person = None
        self.submission = None
        self.options_frame = Frame(self._myJournal)
        self.start_menu = Frame(self._myJournal)
        self.submission_frame = Frame(self._myJournal)

        self.display_menu()

        self._myJournal.mainloop()
    
    def set_journal(self):
        journal = self.session.query(Journal).first()
        if not journal:
            journal = Journal()
            journal._start_date = get_today()
        return journal

    def display_menu(self):
        if not self.journal._name:
            self.show_start_menu()
        else:
            self.show_main_menu()
    
    def show_start_menu(self):
        self.start_menu.destroy()
        self.start_menu = Frame(self._myJournal)
        self.start_label = Label(self.start_menu, text = get_text("greeting_new")).grid(row=0,column=0)
        self.name_entry = Entry(self.start_menu)
        self.name_entry.grid(row=1, column=0)
        main_button = Button(self.start_menu, text = "Next", command=self.set_name).grid(row=2, column=0)
        self.start_menu.grid()
    
    def set_name(self):
        self.journal._name = self.name_entry.get()
        add_and_commit(self.session, [self.journal])
        self.start_menu.destroy()
        self.show_main_menu()

    def show_main_menu(self):
        self.options_frame.destroy()
        self.submission_frame.destroy()
        self.options_frame = Frame(self._myJournal)
        self.greeting_label = Label(self.options_frame, text = get_text("greeting_old", self.journal._name)).grid(row=0, column=1)
        Button(self.options_frame, text = "add submission", command = self.add_submission).grid(row=1, column=0)
        Button(self.options_frame, text = "view stats", command = StatsGUI(self.journal, self.session, self._myJournal, self.options_frame).run).grid(row=1, column=1)
        Button(self.options_frame, text = "fetch transcript", command = TranscriptGUI(self.journal, self.session, self._myJournal, self.options_frame).run).grid(row=1, column=2)
        self.options_frame.grid(row=1,column=0)
    
    def add_submission(self):
        new_submission = self.journal.add_submission(self.session)
        self.submission = new_submission
        self.options_frame.destroy()
        self.submission_frame.destroy()
        self.submission_frame = Frame(self._myJournal)
        Label(self.submission_frame, text = "Would you like to submit an entry?").grid(row=0, column=0)
        Button(self.submission_frame, text = "Yes", command=self.add_entry).grid(row=1, column=0)
        Button(self.submission_frame, text = "Back to Main Menu", command= self.show_main_menu).grid(row=2, column=0)
        self.submission_frame.grid(row=0, column=0)
    
    def add_entry(self):
        self.submission_frame.destroy()
        EntryGUI(self.submission, self.journal, self.session, self._myJournal, self.submission_frame).run()
        # self.add_submission()

if __name__ == "__main__":
    engine = create_engine(f"sqlite:///journal.db")
    Base.metadata.create_all(engine)

    Session = sessionmaker()
    Session.configure(bind=engine)
    sesh = Session()
    JournalGUI()
