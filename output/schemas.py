from typing import List, Dict, Tuple, Any 
 
from pydantic import BaseModel 
        

class BlogGet(BaseModel):
    """
    Used for Get
    """
    description_history: list = None
    summary_history: list = None
    name: str
    slug: str
    description: str
    summary: str
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
    uuid: str = None
    meta_id: str = None

    class Config:
        orm_mode = True


class BlogCategoryGet(BaseModel):
    """
    Used for Get
    """
    uuid: str
    name: str
    description: str


class BlogCategoryCreate(BaseModel):
    """
    Used for Create
    """
    name: str
    description: str


class BlogCategoryUpdate(BaseModel):
    """
    Used for Update
    """
    name: str = None
    description: str = None


class BlogCategoryDb(BaseModel):
    """
    Used for Db
    """
    uuid: str = None
    blog_uuid: str = None
    meta_id: str = None

    class Config:
        orm_mode = True


class BlogPostGet(BaseModel):
    """
    Used for Get
    """
    uuid: str
    content: str
    content_history: list = None
    summary_history: list = None
    category_uuid: str = None
    locked: bool = None
    frozen: bool = None
    publish_at: str = None
    name: str
    slug: str
    summary: str
    created_at: str


class BlogPostCreate(BaseModel):
    """
    Used for Create
    """
    content: str
    category_uuid: str = None
    locked: bool = None
    frozen: bool = None
    publish_at: str = None
    name: str
    summary: str


class BlogPostUpdate(BaseModel):
    """
    Used for Update
    """
    content: str = None
    category_uuid: str = None
    locked: bool = None
    frozen: bool = None
    publish_at: str = None
    name: str = None
    summary: str = None


class BlogPostDb(BaseModel):
    """
    Used for Db
    """
    uuid: str = None
    blog_uuid: str = None
    meta_uuid: str = None
    content_uuid: str = None
    category_uuid: str = None
    locked: bool = None
    frozen: bool = None
    publish_at: str = None
    deleted_at: str = None

    class Config:
        orm_mode = True

# END OF GENERATED CODE
