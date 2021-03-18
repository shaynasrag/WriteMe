from sqlalchemy.types import TypeDecorator
from sqlalchemy import Column, Integer, String, ForeignKey, Table, MetaData, Float, Boolean
from datetime import datetime

# written by Timothy Barron 2021
class MyTime(TypeDecorator):    
    impl = String    
    def __init__(self, length=None, format="%m-%d-%Y %H:%M:%S", **kwargs):        
        super().__init__(length, **kwargs)        
        self.format = format    
    def process_literal_param(self, value, dialect):        
        # allow passing string or time to column        
        if isinstance(value, str):            
            value = datetime.strptime(value, self.format).time()        
        # convert python time to sql string       
        return value.strftime(self.format) if value is not None else None    
    
    process_bind_param = process_literal_param    
    def process_result_value(self, value, dialect):        
        # convert sql string to python time       
        return datetime.strptime(value, self.format).date() if value is not None else None