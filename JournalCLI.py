import sys
from Journal import Journal
from Entry import Base 
from CLI_static import print_text, get_input, add_and_commit
from SubmissionCLI import SubmissionCLI
from TranscriptCLI import TranscriptCLI
from StatsCLI import StatsCLI

from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker

class JournalCLI():
    def __init__(self):
        self.session = Session()
        self.journal = self.get_journal()
        add_and_commit(self.session, [self.journal])
        self.choices = {
            "add submission": self.submission_driver,
            "check stats": self.stats_driver,
            "fetch transcript": self.transcript_driver,
            "quit": quit,
        }
        
        self.options = ", ".join(self.choices.keys())
        self.curr_person = None
        self.chosen_person = None
    
    def get_journal(self):
        journal = self.session.query(Journal).first()
        if not journal:
            journal = Journal()
        return journal

    def run(self):
        while True:
            self.display_menu()
            choice = input(">")
            action = self.choices.get(choice)
            if action:
                action()
            else:
                print_text("not valid", choice)

    def display_menu(self):
        if not self.journal._name:
            name = get_input("greeting_new")
            self.journal._name = name
        print_text("greeting_old", self.journal._name)
        print(self.options)
            
    def submission_driver(self):
        submissionCLI = SubmissionCLI(self.journal, self.session)
        submissionCLI.run()

    def transcript_driver(self):
        transcriptCLI = TranscriptCLI(self.journal)
        transcriptCLI.run()          
    
    def stats_driver(self):
        statsCLI = StatsCLI(self.journal)
        statsCLI.run()
        
    def quit(self):
        sys.exit(0)

if __name__ == "__main__":
    engine = create_engine(f"sqlite:///journal.db")
    Base.metadata.create_all(engine)

    Session = sessionmaker()
    Session.configure(bind=engine)
    sesh = Session()
    journalCLI = JournalCLI()
    journalCLI.run()