from Exceptions import IncorrectResponse
from Entry import InterpersonalConflict as IC
from strings import category_ls, category_types
from static import get_today, get_input
import matplotlib.pyplot as plt
import matplotlib.dates as dates
from datetime import datetime


from Exceptions import IncorrectResponse
class Statistics():
    def __init__(self, session, journal):
        self.journal = journal
        self.session = session
        self.person_filter = None
        self.category_filter = None
        self.start_date_filter = None
        self.end_date_filter = None
        self.query = None
        self.today = get_today()
        

    def query_session(self):

        if self.person_filter and not self.start_date_filter:
            self.query = self.session.query(IC).filter(IC._person == self.person_filter)
        
        elif self.start_date_filter and not self.person_filter:
            self.query = self.session.query(IC).filter(IC._entry_day >= self.start_date_filter[0], IC._entry_day <= self.end_date_filter[0],
                                                    IC._entry_month >= self.start_date_filter[1], IC._entry_month <= self.end_date_filter[1],
                                                    IC._entry_year >= self.start_date_filter[2], IC._entry_year <= self.end_date_filter[2])

        elif self.person_filter and self.start_date_filter:
            self.query = self.session.query(IC).filter(IC._person == self.person_filter, 
                                                    IC._entry_day >= self.start_date_filter[0], IC._entry_day <= self.end_date_filter[0],
                                                    IC._entry_month >= self.start_date_filter[1], IC._entry_month <= self.end_date_filter[1],
                                                    IC._entry_year >= self.start_date_filter[2], IC._entry_year <= self.end_date_filter[2])
        else:
            self.query = self.session.query(IC).all()
        
        return self.query
    
    def add_person_filter(self, person):
        people_ls = self.journal.get_people()
        if person in people_ls:
            self.person_filter = person
            return True
        elif person.lower() == "everyone":
            return False
        else:
            raise IncorrectResponse('\n'.join(people_ls) + ' ')
    
    def add_category_filter(self, category):
        if category.lower() in category_ls:
            self.category_filter = category.lower()
            return category_types[self.category_filter]
        else:
            raise IncorrectResponse(category_ls)
    
    def add_start_date_filter(self, start_date):
        if start_date.lower() == "all dates":
            return False
        else:
            start_date_ls = [int(d) for d in start_date.split('-')]
            month, journal_start_month = int(start_date_ls[0]), self.journal.start_date[0]
            day, journal_start_day = int(start_date_ls[1]), self.journal.start_date[1]
            year, journal_start_year = int(start_date_ls[2]), self.journal.start_date[2]

            if year < journal_start_year or (year >= journal_start_year and month < journal_start_month) or (year >= journal_start_year and month >= journal_start_month and day < journal_start_day):
                raise IncorrectResponse(["date after" + '-'.join(self.journal.start_date)])
            else:
                self.start_date_filter = start_date_ls
                return True
    
    def add_end_date_filter(self, end_date):
        today_ls = get_today()
        end_date_ls = [int(d) for d in end_date.split('-')]
        month, journal_end_month = int(end_date_ls[0]), today_ls[0]
        day, journal_end_day = int(end_date_ls[1]), today_ls[1]
        year, journal_end_year = int(end_date_ls[2]), today_ls[2]

        if year > journal_end_year or (year <= journal_end_year and month > journal_end_month) or (year <= journal_end_year and month <= journal_end_month and day > journal_end_day):
            raise IncorrectResponse(["date before" + '-'.join(today_ls)])
        
        else:
            self.end_date_filter = end_date_ls

    def write_query_to_file(self, query_doc_name, query_string):        
        with open(query_doc_name, "a+") as f:
            f.write(query_string + "\n")
    
    def make_graph(self):
        people_dict_x = {}
        people_dict_y = {}
        people_ls = []
        plt.xlabel('Date of Entry')
        plt.ylabel(self.category_filter.capitalize())
        plt.xlim([self.journal.start_date])
        for entry in self.query:
            attribute = entry.get_attribute(self.category_filter)
            formatted_date = dates.datestr2num(datetime.strptime(entry._entry_date, '%m-%d-%Y').strftime('%m/%d/%Y'))
            if entry._person not in people_dict_y:
                people_ls.append(entry._person)
                people_dict_y[entry._person] = [attribute]
                people_dict_x[entry._person] = [formatted_date]
            else:
                people_dict_y[entry._person].append(attribute)
                people_dict_x[entry._person].append(formatted_date)
        
        for person in people_ls:
            plt.plot_date(people_dict_x[person], people_dict_y[person], label = person)
        # plt.plot_date()
        plt.show()
            





    

        
    