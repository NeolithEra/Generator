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
    name: str


class MyModalDb(BaseModel):
    """
    Used for Db
    """
    uuid: str
    name: str


class UsersGet(BaseModel):
    """
    Used for Get
    """
    name: str


class UsersCreate(BaseModel):
    """
    Used for Create
    """
    name: str


class UsersUpdate(BaseModel):
    """
    Used for Update
    """
    name: str = None


class UsersDb(BaseModel):
    """
    Used for Db
    """
    uuid: str
    name: str

# END OF GENERATED CODE
