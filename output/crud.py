from sqlalchemy.orm import Session 
 
from . import models, schemas 
 
from ehelply_bootstrapper.utils.state import State

from typing import List, Union
        
                
def get_blog(db: Session, blog_uuid: str) -> models.Blog:
    """
    Used to get Blog
    """
    
    return db.query(models.Blog).filter(models.Blog.uuid == blog_uuid).first()

                
def search_blog(db: Session) -> List[models.Blog]:
    """
    Used to search Blog
    """
    
    return db.query(models.Blog).all()

                
def create_blog(db: Session, blog: schemas.BlogDb) -> models.Blog:
    """
    Used to create Blog
    """
    
    db_entry = models.Blog(**blog.dict())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

                
def update_blog(db: Session, blog_uuid: str, blog: schemas.BlogUpdate) -> Union[models.Blog, None]:
    """
    Used to update Blog
    """
    
    if db.query(models.Blog).filter(models.Blog.uuid == blog_uuid).scalar() is not None:
        db_entry: models.Blog = db.query(models.Blog).filter(models.Blog.uuid == blog_uuid).first()
 
        db.commit()
        return db_entry
    else:
        return None

                
def delete_blog(db: Session, blog_uuid: str):
    """
    Used to delete Blog
    """
    
    db.query(models.Blog).filter(models.Blog.uuid == blog_uuid).delete()
    db.commit()

                
def get_blog_category(db: Session, blog_category_uuid: str) -> models.BlogCategory:
    """
    Used to get BlogCategory
    """
    
    return db.query(models.BlogCategory).filter(models.BlogCategory.uuid == blog_category_uuid).first()

                
def search_blog_category(db: Session) -> List[models.BlogCategory]:
    """
    Used to search BlogCategory
    """
    
    return db.query(models.BlogCategory).all()

                
def create_blog_category(db: Session, blog_category: schemas.BlogCategoryDb) -> models.BlogCategory:
    """
    Used to create BlogCategory
    """
    
    db_entry = models.BlogCategory(**blog_category.dict())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

                
def update_blog_category(db: Session, blog_category_uuid: str, blog_category: schemas.BlogCategoryUpdate) -> Union[models.BlogCategory, None]:
    """
    Used to update BlogCategory
    """
    
    if db.query(models.BlogCategory).filter(models.BlogCategory.uuid == blog_category_uuid).scalar() is not None:
        db_entry: models.BlogCategory = db.query(models.BlogCategory).filter(models.BlogCategory.uuid == blog_category_uuid).first()
 
        db.commit()
        return db_entry
    else:
        return None

                
def delete_blog_category(db: Session, blog_category_uuid: str):
    """
    Used to delete BlogCategory
    """
    
    db.query(models.BlogCategory).filter(models.BlogCategory.uuid == blog_category_uuid).delete()
    db.commit()

                
def get_blog_post(db: Session, blog_post_uuid: str) -> models.BlogPost:
    """
    Used to get BlogPost
    """
    
    return db.query(models.BlogPost).filter(models.BlogPost.uuid == blog_post_uuid).first()

                
def search_blog_post(db: Session) -> List[models.BlogPost]:
    """
    Used to search BlogPost
    """
    
    return db.query(models.BlogPost).all()

                
def create_blog_post(db: Session, blog_post: schemas.BlogPostDb) -> models.BlogPost:
    """
    Used to create BlogPost
    """
    
    db_entry = models.BlogPost(**blog_post.dict())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

                
def update_blog_post(db: Session, blog_post_uuid: str, blog_post: schemas.BlogPostUpdate) -> Union[models.BlogPost, None]:
    """
    Used to update BlogPost
    """
    
    if db.query(models.BlogPost).filter(models.BlogPost.uuid == blog_post_uuid).scalar() is not None:
        db_entry: models.BlogPost = db.query(models.BlogPost).filter(models.BlogPost.uuid == blog_post_uuid).first()

        if blog_post.category_uuid is not None:
            db_entry.category_uuid = blog_post.category_uuid

        if blog_post.locked is not None:
            db_entry.locked = blog_post.locked

        if blog_post.frozen is not None:
            db_entry.frozen = blog_post.frozen

        if blog_post.publish_at is not None:
            db_entry.publish_at = blog_post.publish_at
 
        db.commit()
        return db_entry
    else:
        return None

                
def delete_blog_post(db: Session, blog_post_uuid: str):
    """
    Used to delete BlogPost
    """
    
    db.query(models.BlogPost).filter(models.BlogPost.uuid == blog_post_uuid).delete()
    db.commit()
