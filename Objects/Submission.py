from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Table, MetaData, create_engine
from sqlalchemy.orm import relationship
from Objects.Entry import Base

class Submission(Base):
    __tablename__ = "submission"
    _entries = relationship("InterpersonalConflict")
    _date = Column(String(length = 20))
    _journal_id = Column(Integer, ForeignKey("journal._id"))
    _submission_number = Column(Integer, primary_key = True)

    def __init__(self):
        self._date = str(datetime.now().strftime("%m-%d-%Y %H:%M:%S"))

    def add_entry(self, entry):
        self._entries.append(entry)
    
    def get_entries(self):
        return self._entries
    
    def write_submission_to_file(self, sub_num):
        filename = "Submission-" + sub_num
        entries = self._entries
        with open(filename, "w") as f:
            f.write("Submission #" + sub_num + ": " + str(self._date) + "\n")
            count = 1
            for entry in entries:
                f.write("Entry: " + str(count) + "\n")
                f.write("Person: " + entry._person + "\n")
                f.write("Anxiety Level: " + str(entry._anxiety) + "/3" + "\n")
                f.write("Closeness: " + str(entry._communal_strength) + "/3" + "\n")
                if entry._conflict is not None:
                    f.write("Description of Conflict: " + entry._conflict + "\n")
                if entry._how_addressed is not None:
                    f.write("How conflict was addressed: " + entry._how_addressed + "\n")
                    f.write("Consent score: " + str(entry._consent) + "/1" + "\n")
                    f.write("Self soothe score: " + str(entry._self_soothe1) + "/1" + "\n")
                    f.write("Other soothe score: " + str(entry._other_soothe1) + "/1" + "\n")
                    f.write("Total communication score: " + str(entry._communication_score) + "/3" + "\n")
                if entry._how_to_approach is not None:
                    f.write("How to approach: " + entry._how_to_approach + "\n")
                    f.write("Their side: " + entry._their_side + "\n")
                    f.write("Another way to make the conversation feel safe: " + entry._how_to_approach + "\n")
                    f.write("What to say: " + entry._how_to_approach + "\n")
                    
                if entry._steps_to_secure is not None:
                    f.write("Steps to security: " + entry._steps_to_secure + "\n")
                if entry._appreciate_other is not None:
                    f.write("Appreciation of " + entry._person + ":" + entry._appreciate_other + "\n")
                if entry._appreciate_self is not None:
                    f.write("Appreciation of self: " + entry._appreciate_self + "\n")
                if entry._gratitude is not None:
                    f.write("Gratitude: " + entry._gratitude + "\n")
                if entry._support_from_others is not None:
                    f.write("Support from others: " + entry._support_from_others + "\n")    
                f.write("______________________________\n")
                count += 1
                

        
        
        
        
