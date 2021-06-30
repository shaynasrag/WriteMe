from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from Static.static import get_today
from Objects.Exceptions import IncorrectResponse
Base = declarative_base()

class InterpersonalConflict(Base):
    __tablename__ = "entry"
    _submission_id = Column(Integer, ForeignKey('submission._submission_number'))
    _entry_id = Column(Integer, primary_key= True)
    _person = Column(String)
    _entry_type = Column(String(50))
    _entry_day = Column(Integer)
    _entry_month = Column(Integer)
    _entry_year = Column(Integer)
    _entry_date = Column(String)
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

    def __init__(self, person):
        self._communication_score = 0
        self._person = person
        self.set_date()

    def set_date(self):
        self._entry_date = get_today()
        date = [int(d) for d in self._entry_date.split('-')]
        self._entry_month = date[0]
        self._entry_day = date[1]
        self._entry_year = date[2]

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

    def get_attribute(self, command):
        category_commands = {
            "closeness": self._communal_strength, "relationship anxiety": self._anxiety, "gratitude texts": self._gratitude,
            "conflict descriptions": self._conflict, "how conflict was addressed": self._how_addressed, "how to approach other": self._how_to_approach,
            "empathizing with other": self._their_side, "how to frame conflict": self._how_to_frame, "intended conflict resolution": self._intended,
            "appreciation of other": self._appreciate_other, "appreciation of self": self._appreciate_self, "support from others": self._support_from_others,
            "steps to security": self._steps_to_secure, "consent score": self._consent, "self soothe score": self._self_soothe1,
            "other soothe score": self._other_soothe1, "total communication score": self._communication_score,
            } 
        return category_commands[command]