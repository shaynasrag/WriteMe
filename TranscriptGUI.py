from tkinter import *

class TranscriptGUI():
    def __init__(self, journal, session, myJournal, show_main_menu):
        self.journal = journal
        self.session = session
        self._myJournal = myJournal
        self.show_main_menu = show_main_menu

        self.show_submissions_frame = Frame(self._myJournal)
        self.write_sub_frame = Frame(self._myJournal)
        self.show_sub_frame = Frame(self._myJournal)
    
    def run(self):
        self.write_sub_frame.destroy()
        self.show_sub_frame.destroy()
        self.show_submissions_frame = Frame(self._myJournal)
        submissions = self.journal.get_submissions()
        self.subVar = IntVar()
        Label(self.show_submissions_frame, text = "Please select which submission you would like to view.").grid(row=0, column=0)
        row = 1
        for s in submissions:
            Radiobutton(self.show_submissions_frame, text = s._date, variable = self.subVar, value=row - 1).grid(row=row, column=0)
        Button(self.show_submissions_frame, text = "Back", command = self.exit).grid(row = row + 1, column = 0)
        Button(self.show_submissions_frame, text = "Next", command = self.show_submission).grid(row = row + 2, column = 0)
        self.show_submissions_frame.grid(row=0,column=0)
    
    def show_submission(self):
        self.show_submissions_frame.destroy()
        self.show_sub_frame = Frame(self._myJournal)
        self.sub_num = self.subVar.get()
        self.curr_submission = self.journal.get_submission(self.sub_num)
        Label(self.show_sub_frame, text = "Submission-" + str(self.sub_num)).grid(row=0, column=0)
        entries = self.curr_submission._entries
        count = 1
        row = 1
        for entry in entries:
            Label(self.show_sub_frame, text = "Entry: " + str(count)).grid(row=row, column=0)
            Label(self.show_sub_frame, text = "Person: " + entry._person).grid(row=row + 1, column=0)
            Label(self.show_sub_frame, text = "Anxiety Level: " + str(entry._anxiety) + "/3").grid(row=row + 2, column=0)
            Label(self.show_sub_frame, text = "Closeness: " + str(entry._communal_strength) + "/3").grid(row=row + 3, column=0)
            row += 3
            if entry._conflict is not None:
                Label(self.show_sub_frame, text = "Description of Conflict: " + entry._conflict).grid(row=row + 1, column=0)
                row += 1
            if entry._how_addressed is not None:
                Label(self.show_sub_frame, text = "How conflict was addressed: " + entry._how_addressed).grid(row=row + 1, column=0)
                Label(self.show_sub_frame, text = "Consent score: " + str(entry._consent) + "/1").grid(row=row + 2, column=0)
                Label(self.show_sub_frame, text = "Self soothe score: " + str(entry._self_soothe1) + "/1").grid(row=row + 3, column=0)
                Label(self.show_sub_frame, text = "Other soothe score: " + str(entry._other_soothe1) + "/1").grid(row=row + 4, column=0)
                Label(self.show_sub_frame, text = "Total communication score: " + str(entry._communication_score) + "/3").grid(row=row + 5, column=0)
                row += 5
            if entry._how_to_approach is not None:
                Label(self.show_sub_frame, text = "How to approach: " + entry._how_to_approach).grid(row=row + 1, column=0)
                Label(self.show_sub_frame, text = "Their side: " + entry._their_side).grid(row=row + 2, column=0)
                Label(self.show_sub_frame, text = "Another way to make the conversation feel safe: " + entry._how_to_approach).grid(row=row + 3, column=0)
                Label(self.show_sub_frame, text = "What to say: " + entry._how_to_approach).grid(row=row + 4, column=0)
                row += 4
                
            if entry._steps_to_secure is not None:
                Label(self.show_sub_frame, text = "Steps to security: " + entry._steps_to_secure).grid(row=row + 1, column=0)
                row += 1
            if entry._appreciate_other is not None:
                Label(self.show_sub_frame, text = "Appreciation of " + entry._person + ":" + entry._appreciate_other).grid(row=row + 1, column=0)
                row += 1
            if entry._appreciate_self is not None:
                Label(self.show_sub_frame, text = "Appreciation of self: " + entry._appreciate_self).grid(row=row + 1, column=0)
                row += 1
            if entry._gratitude is not None:
                Label(self.show_sub_frame, text = "Gratitude: " + entry._gratitude).grid(row=row + 1, column=0)
                row += 1
            if entry._support_from_others is not None:
                Label(self.show_sub_frame, text = "Support from others: " + entry._support_from_others).grid(row=row + 1, column=0)
                row += 1
            Label(self.show_sub_frame, text = "__________________________").grid(row=row + 1, column=0)
            row += 1
            count += 1
        Button(self.show_sub_frame, text = "Write Submission to File", command= self.write_submission).grid(row=row + 1, column = 0)
        Button(self.show_sub_frame, text = "Back", command= self.run).grid(row=row + 2, column = 0)
        self.show_sub_frame.grid(row=0,column=0)
    
    def write_submission(self):
        self.show_sub_frame.destroy()
        self.curr_submission.write_submission_to_file(str(self.sub_num))
        self.write_sub_frame = Frame(self._myJournal)
        Label(self.write_sub_frame, text= "Submission has been written to file.").grid(row=0, column=0)
        Button(self.write_sub_frame, text = "Back to Submissions", command=self.run).grid(row=1, column=0)
        Button(self.write_sub_frame, text = "Return to Main Menu", command=self.exit).grid(row=2, column=0)
        self.write_sub_frame.grid(row=0,column=0)
    
    def exit(self):
        self.write_sub_frame.destroy()
        self.show_submissions_frame.destroy()
        self.show_main_menu()