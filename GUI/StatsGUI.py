from sqlalchemy.sql.expression import column
from Static.static import get_text
from Objects.Statistics import Statistics
from Static.strings import category_ls
from tkinter import *
from PIL import ImageTk, Image

class StatsGUI:
    def __init__(self, journal, session, myJournal, show_main_menu):
        self.journal = journal
        self.session = session
        self._myJournal = myJournal
        self.show_main_menu = show_main_menu

        self.stats_object = Statistics(self.session, self.journal)
        self.query_num = 0
        self.query_string = ""
        self.query_type = None
        self.query_doc_name = None
        self.query = None

        self.personVar = StringVar()
        self.start_dateVar = StringVar()
        self.end_dateVar = StringVar()
        self.categoryVar = StringVar()

        self.stats_start_frame = Frame(self._myJournal)
        self.show_results_frame = Frame(self._myJournal)
        self.filters_frame = Frame(self._myJournal)
        self.graph_frame = Frame(self._myJournal)
        self.another_stats_frame = Frame(self._myJournal)
        self.show_graph_frame = Frame(self._myJournal)

    def run(self):
        self.filters_frame.destroy()
        self.graph_frame.destroy()
        self.another_stats_frame.destroy()
        self.stats_start_frame = Frame(self._myJournal)
        Label(self.stats_start_frame, text = get_text("welcome to stats")).grid(row=0, column=0)
        Button(self.stats_start_frame, text = "Next", command=self.set_filters).grid(row=1, column=0)
        Button(self.stats_start_frame, text = "Back to Main Menu", command= self.exit).grid(row=2, column=0)
        self.stats_start_frame.grid(row=0, column=0)

    def set_filters(self):
        self.stats_start_frame.destroy()
        self.show_results_frame.destroy()
        self.filters_frame = Frame(self._myJournal)
        people = self.journal.get_people()
        dates = self.stats_object.get_date_range()
        self.personVar.set("Everyone")
        self.categoryVar.set(category_ls[0])
        self.start_dateVar.set("All Dates")
        self.end_dateVar.set("All Dates")

        Label(self.filters_frame, text="Please choose any filters you'd like on the stats you'd like to view.").grid(row=0,column=0)
        Label(self.filters_frame, text="Person:").grid(row=1,sticky=W)
        OptionMenu(self.filters_frame, self.personVar, *people).grid(row=1, column=0)
        Label(self.filters_frame, text="Category:").grid(row=2,sticky=W)
        OptionMenu(self.filters_frame, self.categoryVar, *category_ls).grid(row=2,column=0)
        Label(self.filters_frame, text="Start Date:").grid(row=3,sticky=W)
        OptionMenu(self.filters_frame, self.start_dateVar, *dates).grid(row=3, column=0)
        Label(self.filters_frame, text="End Date:").grid(row=4,sticky=W)
        OptionMenu(self.filters_frame, self.end_dateVar, *dates).grid(row=4,column=0)
        Button(self.filters_frame, text = "Next", command=self.add_filters_to_obj).grid(row=5, column=0)
        Button(self.filters_frame, text = "Back", command=self.run).grid(row=6, column=0)
        self.filters_frame.grid(row=0,column=0)

    def add_filters_to_obj(self):
        self.filters_frame.destroy()
        self.stats_object.add_person_filter(self.personVar.get())
        self.query_type = self.stats_object.add_category_filter(self.categoryVar.get())
        if self.stats_object.add_start_date_filter(self.start_dateVar.get()):
            self.stats_object.add_end_date_filter(self.end_dateVar.get())
        self.query = self.stats_object.query_session()
        self.query_num += 1
        self.show_results()

    def show_results(self):
        self.show_results_frame = Frame(self._myJournal)
        Label(self.show_results_frame, text="Query Number: " + str(self.query_num) + ", Category: " + self.stats_object.category_filter + '\n').grid(row=0, column=0)
        row = 1
        for entry in self.query:
            attribute = entry.get_attribute(self.stats_object.category_filter)
            entry_string = "Date: " + entry._entry_date + ", Person: " + entry._person + ", " + self.stats_object.category_filter.capitalize() + ": " + str(attribute)
            Label(self.show_results_frame, text=entry_string).grid(row=row, column=0)
            self.query_string += (entry_string + '\n')
            row += 1
        Button(self.show_results_frame, text="Write Query to File", command=self.record_results).grid(row=row, column=0)
        if self.query_type == int:
            Button(self.show_results_frame, text="Skip to Graph", command=self.offer_and_save_graph).grid(row= row + 1, column=0)
        else:
            Button(self.show_results_frame, text="Back", command=self.set_filters).grid(row= row + 1, column=0)      
        self.show_results_frame.grid(row=0, column=0)

    def record_results(self):
        self.show_results_frame.destroy()
        self.record_results_frame = Frame(self._myJournal)
        if self.query_doc_name:
            Label(self.record_results_frame, text=get_text("new query doc", "'" + self.query_doc_name + "'")).grid(row=0,column=0)
            Button(self.record_results_frame, text="Write to New File", command=self.new_filename).grid(row=1, column=0)
            Button(self.record_results_frame, text="Write to Current Doc", command=self.write_query).grid(row=2,column=0)
            self.record_results_frame.grid(row=0,column=0)
        else:
            self.new_filename()
        
    def new_filename(self):
        self.record_results_frame.destroy()
        self.new_file_frame = Frame(self._myJournal)
        Label(self.new_file_frame, text=get_text("name query file")).grid(row=0,column=0)
        self.filename = Entry(self.new_file_frame)
        self.filename.grid(row=1,column=0)
        Button(self.new_file_frame, text="Next", command=self.set_filename).grid(row=2,column=0)
        self.new_file_frame.grid(row=0,column=0)
        
    def set_filename(self):
        self.query_doc_name = self.filename.get() + '.txt'
        self.record_results_frame.destroy()
        self.new_file_frame.destroy()
        self.write_query()

    def write_query(self):
        self.show_results_frame.destroy()
        self.record_results_frame.destroy()
        self.stats_object.write_query_to_file(self.query_doc_name, self.query_string)
        if self.query_type == int:
            self.offer_and_save_graph()
        else:
            self.another_stats()
    
    def offer_and_save_graph(self):
        self.show_results_frame.destroy()
        self.graph_frame = Frame(self._myJournal)
        Label(self.graph_frame, text=get_text("make graph")).grid(row=0,column=0)
        Button(self.graph_frame, text="Yes", command=self.show_graph).grid(row=1,column=0)
        Button(self.graph_frame, text ="Back to Stats", command=self.run).grid(row=2,column=0)
        self.graph_frame.grid(row=0,column=0)
    
    def show_graph(self):
        self.graph_frame.destroy()
        self.show_graph_frame = Frame(self._myJournal)
        graph_image = self.stats_object.make_and_save_graph(CLI=False)
        Label(self.show_graph_frame, text="Your graph has been saved under the name '{0}'".format(graph_image)).grid(row=0,column=0)
        self.graph_canvas = Canvas(self.show_graph_frame,width=700,height=500)
        self.graph_canvas.grid(row=1,column=0)
        self.image = ImageTk.PhotoImage(Image.open(graph_image))
        self.graph_canvas.create_image(30, 30, anchor=NW, image=self.image)
        Button(self.show_graph_frame, text="Next", command=self.another_stats).grid(row=2,column=0)
        self.show_graph_frame.grid(row=0,column=0)

    def another_stats(self):
        self.show_graph_frame.destroy()
        self.another_stats_frame = Frame(self._myJournal)
        Label(self.another_stats_frame, text=get_text("another stats")).grid(row=0,column=0)
        Button(self.another_stats_frame, text="Yes", command=self.run).grid(row=1,column=0)
        Button(self.another_stats_frame, text="Back to Main Menu", command=self.exit).grid(row=2,column=0)
        self.another_stats_frame.grid(row=0,column=0)

    def exit(self):
        self.stats_start_frame.destroy()
        self.another_stats_frame.destroy()
        self.show_main_menu()