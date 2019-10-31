from sqlalchemy.orm import Session 
 
from . import models, schemas 
 
from ehelply_bootstrapper.utils.state import State

from typing import List, Union
        
                
def get_my_modal(db: Session, my_modal_uuid: str) -> models.MyModal:
    """
    Used to get MyModal
    """
    
    return db.query(models.MyModal).filter(models.MyModal.uuid == my_modal_uuid).first()

                
def search_my_modal(db: Session) -> List[models.MyModal]:
    """
    Used to search MyModal
    """
    
    return db.query(models.MyModal).all()

                
def create_my_modal(db: Session, my_modal: schemas.MyModalDb) -> models.MyModal:
    """
    Used to create MyModal
    """
    
    db_entry = models.MyModal(**my_modal.dict())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

                
def update_my_modal(db: Session, my_modal_uuid: str, my_modal: schemas.MyModalUpdate) -> Union[models.MyModal, None]:
    """
    Used to update MyModal
    """
    
    if db.query(models.MyModal).filter(models.MyModal.uuid == my_modal_uuid).scalar() is not None:
        db_entry: models.MyModal = db.query(models.MyModal).filter(models.MyModal.uuid == my_modal_uuid).first()

        if my_modal.name is not None:
            db_entry.name = my_modal.name
 
        db.commit()
        return db_entry
    else:
        return None

                
def delete_my_modal(db: Session, my_modal_uuid: str):
    """
    Used to delete MyModal
    """
    
    db.query(models.MyModal).filter(models.MyModal.uuid == my_modal_uuid).delete()
    db.commit()

                
def get_user(db: Session, user_uuid: str) -> models.User:
    """
    Used to get User
    """
    
    return db.query(models.User).filter(models.User.uuid == user_uuid).first()

                
def search_user(db: Session) -> List[models.User]:
    """
    Used to search User
    """
    
    return db.query(models.User).all()

                
def create_user(db: Session, user: schemas.UserDb) -> models.User:
    """
    Used to create User
    """
    
    db_entry = models.User(**user.dict())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

                
def update_user(db: Session, user_uuid: str, user: schemas.UserUpdate) -> Union[models.User, None]:
    """
    Used to update User
    """
    
    if db.query(models.User).filter(models.User.uuid == user_uuid).scalar() is not None:
        db_entry: models.User = db.query(models.User).filter(models.User.uuid == user_uuid).first()

        if user.name is not None:
            db_entry.name = user.name
 
        db.commit()
        return db_entry
    else:
        return None

                
def delete_user(db: Session, user_uuid: str):
    """
    Used to delete User
    """
    
    db.query(models.User).filter(models.User.uuid == user_uuid).delete()
    db.commit()
