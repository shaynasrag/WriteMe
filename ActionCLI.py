from static import print_text, add_and_commit, validate, yes_or_no, get_input
from EntryCLI import EntryCLI
from Submission import Submission
from Statistics import Statistics
from strings import category_ls

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
            print_text("not valid")

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
        self.stats_object = Statistics(self.session, self.journal)
        self.query_num = 0
        self.query_string = ""
        self.query_type = None
        self.query_doc_name = None
        self.query = None
    
    def run(self):
        print_text("welcome to stats")
        get_stats = True
        while get_stats:
            self.set_filters()
            self.show_and_record_results()
            self.offer_and_save_graph()
            if not validate(yes_or_no, "another stats"):
                return

    def set_filters(self):
        validate(self.stats_object.add_person_filter, "people stats", '\n'.join(self.journal.get_people()) + ' ')
        self.query_type = validate(self.stats_object.add_category_filter, "category stats", '\n'.join(category_ls))
        if validate(self.stats_object.add_start_date_filter, "start date stats"):
            validate(self.stats_object.add_end_date_filter, "end date stats")
    
    def show_and_record_results(self):
        self.query = self.stats_object.query_session()
        self.query_num += 1
        self.show_results()
        self.record_results()

    def show_results(self):
        self.query_string = "Query Number: " + str(self.query_num) + ", Category: " + self.stats_object.category_filter + '\n'
        print(self.query_string) 
        for entry in self.query:
            attribute = entry.get_attribute(self.stats_object.category_filter)
            entry_string = "Date: " + entry._entry_date + ", Person: " + entry._person + ", " + self.stats_object.category_filter.capitalize() + ": " + str(attribute)
            print(entry_string)
            self.query_string += (entry_string + '\n')

    def record_results(self):
        if validate(yes_or_no, "write query to file"):
            self.verify_filename()
            self.stats_object.write_query_to_file(self.query_doc_name, self.query_string)

    def verify_filename(self):
        if not self.query_doc_name:
            self.query_doc_name = get_input("name query file") 
        else:
            if validate(yes_or_no, "new query doc", self.query_doc_name):
                self.query_doc_name = get_input("name query file") 
    
    def offer_and_save_graph(self):
        if self.query_type == int and validate(yes_or_no, "make graph"):
            self.stats_object.make_and_save_graph()
        

    
