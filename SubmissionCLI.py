from CLI_static import print_text, print_error, validate, get_input, add_and_commit
from Entry import InterpersonalConflict
from Journal import People
from Exceptions import IncorrectResponse
from EntryCLI import EntryCLI
from Submission import Submission

class SubmissionCLI():
    def __init__(self, journal):
        self.types_of_submissions = {
            "interpersonal conflict": self.conflict_entry_driver      
        }
        self.submission_options = "\n".join(self.types_of_submissions.keys())
        self.journal = journal
         
    def run(self):
        while True:
            print_text("topic")
            print(self.submission_options, "\nreturn to main menu")
            choice = input(">")
            if choice == "return to main menu":
                return
            action = self.types_of_submissions.get(choice)
            self.validate_action(action)
    
    def validate_action(self, action):
        if action:
                new_submission = Submission()
                self.journal.add_submission(new_submission)
                add_and_commit([new_submission])
                action(new_submission)
        else:
            print_text("Not a valid action")
    
    def conflict_entry_driver(self, new_submission):
        entryCLI = EntryCLI(new_submission, self.journal)
        entryCLI.run()