class TranscriptCLI():
    def __init__(self):
        pass
    
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
