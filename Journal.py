from Submission import Submission

class Journal():
    def __init__(self):
        self._submission_ls = []
        self._people = []
    
    def add_submission(self, submission):
        self._submission_ls.append(submission)
        
    

