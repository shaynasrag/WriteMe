from datetime import datetime
from Text import Text
from Numerical import Numerical

class Submission():
    def __init__(self):
        self._date = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
        self._person = None
        self._text_submissions = Text()
        self._numerical_submissions = Numerical()
        
        
        
        
