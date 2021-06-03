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
    _entry_type = Column(String(50))
    __mapper_args__ = {
        'polymorphic_identity': 'entry',
        'polymorphic_on': _entry_type
    }

    def __init__(self, person):
        self._person = person
    
    def add_gratitude(self, gratitude):
        pass
    
    def add_conflict(self, conflict):
        pass
    
    def add_steps_to_secure(self, steps):
        pass
    
    def add_addressed(self, addressed):
        pass

    def add_appreciate_other(self, appreciate_other):
        pass

    def add_appreciate_self(self, appreciate_self):
        pass
    
    def add_support_from_others(self, support):
        pass
    
    def add_consent(self, consent):
        pass
        
    def add_self_soothe1(self, self_soothe1):
        pass
    
    def add_other_soothe1(self, other_soothe1):
        pass
    
    def add_self_soothe2(self, self_soothe2):
        pass

    def add_other_soothe2(self, other_soothe2):
        pass

    def add_communal_strength(self, communal_strength):
        pass
    
    def add_anxiety(self, anxiety):
        pass

    def add_how_to_approach(self, how_to_approach):
        pass

    def add_their_side(self, their_side):
        pass

    def add_how_to_frame(self, how_to_frame):
        pass

    def add_intended(self, intended):
        pass

    def yes_or_no(self, answer):
        if answer.lower() == "yes" or answer.lower() == "y":
            return True
        elif answer.lower() == "no" or answer.lower() == "n":
            return False
        else:
            raise IncorrectResponse(["Yes", "No"])

class InterpersonalConflict(Entry):
    __tablename__ = "interpersonalconflict"
    _entry_id = Column(Integer, ForeignKey('entry._entry_id'), primary_key = True)
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
    _communication_score = Column(Integer)
    _communal_strength = Column(Integer)
    _anxiety = Column(Integer)
    _how_to_approach = Column(String)
    _their_side = Column(String)
    _how_to_frame = Column(String)
    _intended = Column(String)
    __mapper_args__ = {
        'polymorphic_identity': 'interpersonalconflict'
    }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
        self._communication_score = 0
        self._communal_strength = None
        self._anxiety = None
        self._how_to_approach = None
        self._their_side = None
        self._how_to_frame = None
        self._intended = None
    
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
    
    def add_how_to_approach(self, how_to_approach):
        self._how_to_approach = how_to_approach

    def add_their_side(self, their_side):
        self._their_side = their_side

    def add_how_to_frame(self, how_to_frame):
        self._how_to_frame = how_to_frame

    def add_intended(self, intended):
        self._intended = intended

    def add_consent(self, consent):

        if consent.lower() == "yes":
            self._consent = 1
            self._communication_score += 1
        elif consent.lower() == "no":
            self._consent = 0
        else:
            raise IncorrectResponse(["Yes", "No"])
        
    def add_self_soothe1(self, self_soothe1):
        if self_soothe1.lower() == "yes":
            self._self_soothe1 = 1
            self._communication_score += 1
        elif self_soothe1.lower() == "no":
            self._self_soothe1 = 0
        else:
            raise IncorrectResponse(["Yes", "No"])
    
    def add_other_soothe1(self, other_soothe1):
        if other_soothe1.lower() == "yes":
            self._other_soothe1 = 1
            self._communication_score += 1
        elif other_soothe1.lower() == "no":
            self._other_soothe1 = 0
        else:
            raise IncorrectResponse(["Yes", "No"])
    
    def add_self_soothe2(self, self_soothe2):
        if self_soothe2.lower() == "yes":
            self._self_soothe2 = 1
            self._communication_score += 1
        elif self_soothe2.lower() == "no":
            self._self_soothe2 = 0
        else:
            raise IncorrectResponse(["Yes", "No"])

    def add_other_soothe2(self, other_soothe2):
        if other_soothe2.lower() == "yes":
            self._other_soothe2 = 1
            self._communication_score += 1
        elif other_soothe2.lower() == "no":
            self._other_soothe2 = 0
        else:
            raise IncorrectResponse(["Yes", "No"])

    def add_communal_strength(self, communal_strength):
        if communal_strength.lower() == "close":
            self._communal_strength = 3
            return True
        elif communal_strength.lower() == "not so close":
            self._communal_strength = 2
            return False
        elif communal_strength.lower() == "distanced":
            self._communal_strength = 1
            return False
        else:
            raise IncorrectResponse(["Close", "Not So Close", "Distanced"])
    
    def add_anxiety(self, anxiety):
        if anxiety.lower() == "high anxiety":
            self._anxiety = 3
        elif anxiety.lower() == "mid anxiety":
            self._anxiety = 2
        elif anxiety.lower() == "low anxiety":
            self._anxiety = 1
        elif anxiety.lower() == "no anxiety":
            self._anxiety = 0
        else:
            raise IncorrectResponse(["High Anxiety", "Mid Anxiety", "Low Anxiety", "No Anxiety"])

    def get_stats(self, obj, filter, session, names=None):
        if names is not None:
            results = session.query(obj).all()
            anxiety_results = [r._anxiety for r in results]
            return anxiety_results
        else:
            results_ls = []
            for name in names:
                results_ls.append(session.query(obj).filter(obj._person == name))
            anxiety_results = []
            for results in results_ls:
                for r in results:
                    anxiety_results.append(r._anxiety)