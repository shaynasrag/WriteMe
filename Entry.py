from Exceptions import IncorrectResponse

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Table, MetaData, Float, Boolean
from MyTime import MyTime

Base = declarative_base()

class Entry(Base):
    __tablename__ = "entry"
    _submission_id = Column(Integer, ForeignKey('submission._submission_number'))
    _entry_id = Column(Integer, primary_key= True)
    _person = Column(String)
    _gratitude = Column(String)
    _conflict = Column(String)
    _steps_to_secure = Column(String)
    _how_addressed = Column(String)
    _appreciate_other = Column(String)
    _appreciate_self = Column(String)
    _support_from_others = Column(String)
    _consent = Column(Integer)
    _self_soothe1 = Column(Integer)
    _other_soothe1 = Column(Integer)
    _self_soothe2 = Column(Integer)
    _other_soothe2 = Column(Integer)
    _communication_score = Column(Integer)
    _communal_strength = Column(Integer)
    _anxiety = Column(Integer)

    def __init__(self):
        self._person = None
        self._gratitude = None
        self._conflict = None
        self._steps_to_secure = None
        self._how_addressed = None
        self._appreciate_other = None
        self._appreciate_self = None
        self._support_from_others = None
        self._consent = None
        self._self_soothe1 = None
        self._other_soothe1 = None
        self._self_soothe2 = None
        self._other_soothe2 = None
        self._communication_score = 0
        self._communal_strength = None
        self._anxiety = None
    
    def add_person(self, person):
        self._person = person
    
    def add_gratitude(self, gratitude):
        self._gratitude = gratitude
    
    def add_conflict(self, conflict):
        self._conflict = conflict
    
    def add_steps_to_secure(self, steps):
        self._steps_to_secure = steps
    
    def add_addressed(self, addressed):
        self._how_addressed = addressed

    def add_appreciate_other(self, appreciate_other):
        self._appreciate_other = appreciate_other

    def add_appreciate_self(self, appreciate_self):
        self._appreciate_self = appreciate_self
    
    def add_support_from_others(self, support):
        self._support_from_others = support 
    
    def add_consent(self, consent):
        if consent.lower() == "yes":
            self._consent = 1
            self._communication_score += 1
        elif consent.lower() == "no":
            self._consent = 0
        else:
            raise IncorrectResponse(["Yes", "No"])
        
    def add_self_soothe1(self, self_soothe1):
        if self_soothe1 == "yes":
            self._self_soothe1 = 1
            self._communication_score += 1
        elif self_soothe1 == "no":
            self._self_soothe1 = 0
        else:
            raise IncorrectResponse(["Yes", "No"])
    
    def add_other_soothe1(self, other_soothe1):
        if other_soothe1 == "yes":
            self._other_soothe1 = 1
            self._communication_score += 1
        elif other_soothe1 == "no":
            self._other_soothe1 = 0
        else:
            raise IncorrectResponse(["Yes", "No"])
    
    def add_self_soothe2(self, self_soothe2):
        if self_soothe2 == "yes":
            self._self_soothe2 = 1
            self._communication_score += 1
        elif self_soothe2 == "no":
            self._self_soothe2 = 0
        else:
            raise IncorrectResponse(["Yes", "No"])

    def add_other_soothe2(self, other_soothe2):
        if other_soothe2 == "yes":
            self._other_soothe2 = 1
            self._communication_score += 1
        elif other_soothe2 == "no":
            self._other_soothe2 = 0
        else:
            raise IncorrectResponse(["Yes", "No"])

    def add_communal_strength(self, communal_strength):
        if communal_strength == "Close":
            self._communal_strength = 3
        elif communal_strength == "Not So Close":
            self._communal_strength = 2
        elif communal_strength == "Distanced":
            self._communal_strength = 1
        else:
            raise IncorrectResponse(["Close", "Not So Close", "Distanced"])
    
    def add_anxiety(self, anxiety):
        if anxiety == "High Anxiety":
            self._anxiety = 3
        elif anxiety == "Mid Anxiety":
            self._anxiety = 2
        elif anxiety == "Low Anxiety":
            self._anxiety = 1
        elif anxiety == "No Anxiety":
            self._anxiety = 0
        else:
            raise IncorrectResponse(["High Anxiety", "Mid Anxiety", "Low Anxiety", "No Anxiety"])

    def _talk_about_conflict(self, answer):
        if answer.lower() == "yes" or answer.lower() == "y":
            return True
        elif answer.lower() == "no" or answer.lower() == "n":
            return False
        else:
            raise IncorrectResponse(["Yes", "No"])

    def _addressed_conflict(self, answer):
        if answer.lower() == "yes" or answer.lower() == "y":
            return True
        elif answer.lower() == "no" or answer.lower() == "n":
            return False
        else:
            raise IncorrectResponse(["Yes", "No"])

