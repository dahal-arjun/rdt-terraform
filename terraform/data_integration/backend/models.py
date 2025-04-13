from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
try:
    from database import Base
except:
    from data_integration.backend.database import Base


class Session(Base):
    __tablename__ = "session"

    id = Column(String, primary_key=True, index=True)
    application_id = Column(String)
    driver_id = Column(String)
    
class Cryptography(Base):
    __tablename__ = "cryptography"

    id = Column(Integer, primary_key=True, index=True)
    iv = Column(String)
    salt = Column(String)
    iteration = Column(Integer)
    length = Column(Integer)
    password = Column(String)
    
    
    

    
    

    
    