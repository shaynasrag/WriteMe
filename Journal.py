from Exceptions import IncorrectResponse
from sqlalchemy import Column, Integer, String, ForeignKey, Table, MetaData, create_engine
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.session import sessionmaker

from sqlalchemy.types import TypeDecorator
from Submission import Submission, Base
from static import get_today

class Journal(Base):
    __tablename__ = "journal"
    _submissions = relationship("Submission")
    _id = Column(Integer, primary_key = True)
    _people = relationship("People")
    _name = Column(String)

    def __init__(self):
        self.start_date = get_today()
 
    def add_submission(self, submission):
        self._submissions.append(submission)
    
    def get_submissions(self):
        return self._submissions
    
    def get_submission(self, index):
        return self._submissions[index]
    
    def get_people(self):
        return [p._person for p in self._people]
    
    def add_person(self, name):
        if name not in self.get_people():
            person = People(name)
            self._people.append(person)
            return person
        return None

    def person_exists(self, person):
        if person in self.get_people():
            return person
        elif person.lower() == "new person":
            return False
        else:
            raise IncorrectResponse(self.get_people())    
    
class People(Base):
    __tablename__ = "people"
    _journal_id = Column(Integer, ForeignKey("journal._id"))
    _people_id = Column(Integer, primary_key = True)
    _person = Column(String)

    def __init__(self, person):
        self._person = person