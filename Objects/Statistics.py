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
    
    def stats_to_graph(self, CLI):
        return Graph(CLI, self)
    
    def make_and_save_graph(self):
        pass

class Graph(Statistics):
    def __init__(self, CLI, stats):
        self.CLI = CLI
        self.journal = stats.journal
        self.session = stats.session
        self.category_filter = stats.category_filter
        self.person_filter = stats.person_filter
        self.start_date_filter = stats.start_date_filter
        self.end_date_filter = stats.end_date_filter
        self.query = stats.query
        self.today = stats.today
        self.bar_space = 0.0
        self.colors = {}
        self.bars, self.color_ls, self.xticks = [], [], []

    def make_and_save_graph(self):
        self.make_graph()
        return self.save_and_show_graph()

    def make_graph(self):
        self.set_labels_and_limits()
        self.make_axes_dicts()
        self.create_subplot()

    def set_labels_and_limits(self):
        plt.xlabel('Date of Entry')
        plt.ylabel(self.category_filter.capitalize())
        plt.title('Graph of ' + self.category_filter.capitalize() + ' for ' + self.person_filter.capitalize())
        plt.ylim([0, 3.5])
        rcParams['figure.figsize'] = 40,12

    def create_subplot(self):
        subplot = plt.subplot(111)
        self.add_bars(subplot)
        plt.xticks(ticks=self.xticks)
        subplot.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        subplot.xaxis_date()
        plt.legend()

    def add_bars(self, subplot):
        self.reset_bar_attributes()
        for person in self.people_ls:
            x_ls, y_ls = self.x_dict[person], self.y_dict[person]
            c = self.make_color(person)
            for i in range(len(x_ls)):
                self.create_bar(i, x_ls, y_ls, person, subplot, c)
                self.bar_space += .10
    
    def reset_bar_attributes(self):
        self.bar_space = 0.0
        self.colors = {}
        self.bars, self.color_ls, self.xticks = [], [], []

    def create_bar(self, i, x_ls, y_ls, person, subplot, c):
        x = date2num(x_ls[i])
        x_attr, l = self.set_bar_attributes(x, person, i)
        self.bars.append(subplot.bar(x_attr, y_ls[i], label = l, color=c, width=0.1))
        if x_ls[i] not in self.xticks:
            self.xticks.append(x_ls[i])

    def set_bar_attributes(self, x, person, i):
        x_attr = x - self.bar_space if i % 2 == 1 else x + self.bar_space
        label = person if i == 0 else ""
        return x_attr, label

    def make_color(self, person):
        if person not in self.colors:
            c = self.set_color()
            self.color_ls.append(c)
        else:
            c = self.colors[person]
        return c
    
    def set_color(self):
        c = (random(), random(), random())
        while c in self.color_ls:
            c = (random(), random(), random())
        return c

    def make_axes_dicts(self):
        self.x_dict, self.y_dict = {}, {}
        self.people_ls = []
        for entry in self.query:
            attribute = entry.get_attribute(self.category_filter)
            if entry._person not in self.y_dict:
                self.people_ls.append(entry._person)
                self.y_dict[entry._person] = [attribute]
                self.x_dict[entry._person] = [datetime(entry._entry_year, entry._entry_month, entry._entry_day)]
            else:
                self.y_dict[entry._person].append(attribute)
                self.x_dict[entry._person].append(datetime(entry._entry_year, entry._entry_month, entry._entry_day))
    
    def save_and_show_graph(self):
        pic_name = self.category_filter + ' for ' + self.person_filter + get_today() + '.png'
        plt.savefig(pic_name)
        if self.CLI:
            plt.show()
            plt.clf()
        else:
            plt.clf()
            return pic_name