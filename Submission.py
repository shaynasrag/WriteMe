from datetime import datetime
from Entry import Entry, Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table, MetaData, create_engine
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.session import sessionmaker
from MyTime import MyTime
from sqlalchemy.types import TypeDecorator

class Submission(Base):
    __tablename__ = "submission"
    _entries = relationship("Entry")
    _date = Column(MyTime(length = 20))
    _journal_id = Column(Integer, ForeignKey("journal._id"))
    _submission_number = Column(Integer, primary_key = True)

    def __init__(self):
        self._date = datetime.now().strftime("%m-%d-%Y %H:%M:%S")

    def add_entry(self, entry, person):
        self._entries.append(entry)
                

        
        
        
        
