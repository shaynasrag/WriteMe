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
 
    # def __init__(self):
    #     self._people = []
    
    def add_submission(self, submission):
        self._submissions.append(submission)
    
    def get_people(self):
        return self._people
    
    def add_person(self, person):
        self._people.append(person)    
    
class People(Base):
    __tablename__ = "people"
    _journal_id = Column(Integer, ForeignKey("journal._id"))
    _people_id = Column(Integer, primary_key = True)
    _person = Column(String)

    def __init__(self, person):
        self._person = person

    # def add_person(self, person, session):
    #     if person not in session.query(self).all():
    #         self._person = person