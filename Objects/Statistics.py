from Objects.Exceptions import IncorrectResponse
from Objects.Entry import InterpersonalConflict as IC
from Static.strings import category_ls, category_types
from Static.static import get_today
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import rcParams
from matplotlib.dates import date2num
from datetime import datetime
from random import random

class Statistics:
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

        if self.person_filter != 'everyone' and not self.start_date_filter:
            self.query = self.session.query(IC).filter(IC._person == self.person_filter)
        
        elif self.start_date_filter and self.person_filter == 'everyone':
            self.query = self.session.query(IC).filter(IC._entry_day >= self.start_date_filter[0], IC._entry_day <= self.end_date_filter[0],
                                                    IC._entry_month >= self.start_date_filter[1], IC._entry_month <= self.end_date_filter[1],
                                                    IC._entry_year >= self.start_date_filter[2], IC._entry_year <= self.end_date_filter[2])

        elif self.person_filter != 'everyone' and self.start_date_filter:
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
            self.person_filter = "everyone"
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
            input_ls, start_datetime, journal_startDatetime = self.make_datetimes(start_date, self.journal._start_date) 
            if start_datetime < journal_startDatetime:
                raise IncorrectResponse(["date after" + self.journal._start_date])
            else:
                self.start_date_filter = input_ls
                return True
    
    def add_end_date_filter(self, end_date):
        dates = self.get_date_range()  
        input_ls, end_datetime, journal_endDatetime = self.make_datetimes(end_date, dates[-1])   
        if end_datetime > journal_endDatetime:
            raise IncorrectResponse(["date before" + '-'.join(self.today)])
        else:
            self.end_date_filter = input_ls
    
    def make_datetimes(self, input_date, journal_date):
        input_ls = [int(d) for d in input_date.split('-')]
        journal_ls = [int(d) for d in journal_date.split('-')]
        return input_ls, datetime(input_ls[2], input_ls[0], input_ls[1]), datetime(journal_ls[2], journal_ls[0], journal_ls[1])
    
    def get_date_range(self):
        dates = self.session.query(IC._entry_date).all()
        return [d[0] for d in dates]

    def write_query_to_file(self, query_doc_name, query_string):        
        with open(query_doc_name, "a+") as f:
            f.write(query_string + "\n")
    
    def make_and_save_graph(self, CLI=True):
        plt.xlabel('Date of Entry')
        plt.ylabel(self.category_filter.capitalize())
        plt.title('Graph of ' + self.category_filter.capitalize() + ' for ' + self.person_filter.capitalize())
        plt.ylim([0, 3.5])
        people_dict_x, people_dict_y, people_ls = self.make_axes_dicts()     
        ax = plt.subplot(111)
        xticks = []
        num = 0.0
        bars = []
        colors = {}
        color_ls = []
        for person in people_ls:
            x_ls = people_dict_x[person]
            y_ls = people_dict_y[person]
            if person not in colors:
                r, b, g = random(), random(), random()
                c = (r, g, b)
                while c in color_ls:
                    r, b, g = random(), random(), random()
                    c = (r, g, b)
            else:
                c = colors[person]
            for i in range(len(x_ls)):
                x = date2num(x_ls[i])
                if i % 2 == 1:
                    bars.append(ax.bar(x - num, y_ls[i], label = person if i == 0 else "", color=c, width=0.1))
                else:
                    bars.append(ax.bar(x + num, y_ls[i], label = person, color=c, width=0.1))

                num += 0.10
                if x_ls[i] not in xticks:
                    xticks.append(x_ls[i])
                plt.xticks(ticks=xticks)

        plt.xticks(ticks=xticks)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        ax.xaxis_date()
        plt.legend()
        rcParams['figure.figsize'] = 40,12
        plt.savefig(self.category_filter + ' for ' + self.person_filter + get_today() + '.png')
        if CLI:
            plt.show()
            plt.clf()
        else:
            plt.clf()
            return self.category_filter + ' for ' + self.person_filter + get_today() + '.png'
    def make_axes_dicts(self):
        people_dict_x, people_dict_y = {}, {}
        people_ls = []
        for entry in self.query:
            attribute = entry.get_attribute(self.category_filter)
            if entry._person not in people_dict_y:
                people_ls.append(entry._person)
                people_dict_y[entry._person] = [attribute]
                people_dict_x[entry._person] = [datetime(entry._entry_year, entry._entry_month, entry._entry_day)]
            else:
                people_dict_y[entry._person].append(attribute)
                people_dict_x[entry._person].append(datetime(entry._entry_year, entry._entry_month, entry._entry_day))
        return people_dict_x, people_dict_y, people_ls