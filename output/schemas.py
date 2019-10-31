from typing import List, Dict, Tuple, Any 
 
from pydantic import BaseModel 
        

class MyModalGet(BaseModel):
    """
    Used for Get
    """
    name: str


class MyModalCreate(BaseModel):
    """
    Used for Create
    """
    name: str


class MyModalUpdate(BaseModel):
    """
    Used for Update
    """
    name: str = None


class MyModalDb(BaseModel):
    """
    Used for Db
    """
    uuid: str
    name: str


class UserGet(BaseModel):
    """
    Used for Get
    """
    name: str


class UserCreate(BaseModel):
    """
    Used for Create
    """
    name: str


class UserUpdate(BaseModel):
    """
    Used for Update
    """
    name: str = None


class UserDb(BaseModel):
    """
    Used for Db
    """
    uuid: str
    name: str

# END OF GENERATED CODE
