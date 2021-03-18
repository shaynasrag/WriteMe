from datetime import datetime
from Entry import Entry

class Submission():
    def __init__(self):
        self._date = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
        self._entry_list = []
        self._person_list = []

    def add_entry(self, entry, person):
        self._entry_list.append(entry)
        self._person_list.append(person)        

        
        
        
        
