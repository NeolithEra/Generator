from typing import List, Dict, Tuple, Any 
 
from pydantic import BaseModel 
        

class BlogGet(BaseModel):
    """
    Used for Get
    """
    name: str
    slug: str
    description: str
    summary: str
    description_history: list = None
    summary_history: list = None
    created_at: str
    updated_at: str


class BlogCreate(BaseModel):
    """
    Used for Create
    """
    name: str
    description: str
    summary: str


class BlogUpdate(BaseModel):
    """
    Used for Update
    """
    name: str = None
    description: str = None
    summary: str = None


class BlogDb(BaseModel):
    """
    Used for Db
    """
    uuid: str
    meta_id: str

    class Config:
        orm_mode = True


class BlogPostGet(BaseModel):
    """
    Used for Get
    """
    uuid: str
    name: str
    slug: str
    summary: str
    content: str
    content_history: list = None
    summary_history: list = None
    category_uuid: str = None
    locked: bool = None
    frozen: bool = None
    publish_at: str = None


class BlogPostCreate(BaseModel):
    """
    Used for Create
    """
    name: str
    summary: str
    content: str
    category_uuid: str = None
    locked: bool = None
    frozen: bool = None
    publish_at: str = None


class BlogPostUpdate(BaseModel):
    """
    Used for Update
    """
    name: str = None
    summary: str = None
    content: str = None
    category_uuid: str = None
    locked: bool = None
    frozen: bool = None
    publish_at: str = None


class BlogPostDb(BaseModel):
    """
    Used for Db
    """
    uuid: str
    blog_uuid: str
    meta_uuid: str
    content_uuid: str
    category_uuid: str
    locked: bool
    frozen: bool
    publish_at: str
    deleted_at: str

    class Config:
        orm_mode = True

# END OF GENERATED CODE
