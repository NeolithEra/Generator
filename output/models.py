from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON, Text, DateTime 
from sqlalchemy.orm import relationship 
 
import uuid 
import datetime 
 
from ehelply_bootstrapper.utils.state import State
        

class MyModal(State.mysql.Base):
    """
    Represents a MyModal
    """
    __tablename__ = "my_modals"
    uuid = Column(String(64),primary_key=True,index=True,unique=False,nullable=False,default="None",)
    name = Column(String(32),unique=False,nullable=False,default="default name",)
    description = Column(Text,unique=False,nullable=False,default="what is this",)


class User(State.mysql.Base):
    """
    Represents a User
    """
    __tablename__ = "users"
    uuid = Column(String(64),primary_key=True,index=True,unique=False,nullable=False,default="None",)
    description = Column(Text,unique=False,nullable=False,default="what is this",)
    name = Column(String(50),unique=False,nullable=False,default="what is this",)

# END OF GENERATED CODE
