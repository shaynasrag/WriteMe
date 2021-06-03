from sqlalchemy import Column, Integer, String, ForeignKey, Table, MetaData, create_engine
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.session import sessionmaker

from sqlalchemy.types import TypeDecorator
from Submission import Submission, Base

class Journal(Base):
    __tablename__ = "journal"
    _submissions = relationship("Submission")
    _id = Column(Integer, primary_key = True)
    _people = relationship("People")
    _name = Column(String)
 
    def add_submission(self, submission):
        self._submissions.append(submission)
    
    def get_submissions(self):
        return self._submissions
    
    def get_submission(self, index):
        return self._submissions[index]
    
    def get_people(self):
        return [p._person for p in self._people]
    
    def add_person(self, person):
        self._people.append(person)    
    
class People(Base):
    __tablename__ = "people"
    _journal_id = Column(Integer, ForeignKey("journal._id"))
    _people_id = Column(Integer, primary_key = True)
    _person = Column(String)

    def __init__(self, person):
        self._person = person