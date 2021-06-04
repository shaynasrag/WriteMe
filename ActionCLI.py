from CLI_static import print_text, print_error, validate, get_input, add_and_commit
from Entry import InterpersonalConflict
from Journal import People
from Exceptions import IncorrectResponse
from EntryCLI import EntryCLI
from Submission import Submission

class ActionCLI():
    def __init__(self, journal, session):
        self.journal = journal
        self.session = session
    
    def run(self):
        pass

    def validate_action(self, action):
        pass

    def fetch_transcript(self):
        pass


class SubmissionCLI(ActionCLI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.submission = None
        self.types_of_submissions = {
            "interpersonal conflict": EntryCLI  
        }
        self.submission_options = "\n".join(self.types_of_submissions.keys())

    def run(self):
            while True:
                print_text("topic")
                print(self.submission_options, "\nreturn to main menu")
                choice = input(">")
                if choice == "return to main menu":
                    return
                action = self.types_of_submissions.get(choice)
                self.validate_action(action)
                action(self.submission, self.journal, self.session).run()  
        
    def validate_action(self, action):
        if action:
                new_submission = Submission()
                self.journal.add_submission(new_submission)
                add_and_commit(self.session, [new_submission])
                self.submission = new_submission
        else:
            print_text("Not a valid action")

class TranscriptCLI(ActionCLI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def run(self):
        self.fetch_transcript()

    def fetch_transcript(self):
        submissions = self.journal.get_submissions()
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
            submission = self.journal.get_submission(int(sub_num) - 1)
            submission.write_submission_to_file(sub_num)
            print("Submission has been written to file.")

class StatsCLI(ActionCLI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def run(self):
        pass