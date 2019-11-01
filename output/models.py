from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON, Text, DateTime 
from sqlalchemy.orm import relationship 
 
import uuid 
import datetime 
 
from ehelply_bootstrapper.utils.state import State
        

class Blog(State.mysql.Base):
    """
    Represents a Blog
    """
    __tablename__ = "blogs"

    uuid = Column(String(64), primary_key=True, index=True, unique=True, nullable=False)
    meta_id = Column(String(64), unique=False, nullable=True)

    blog_categories = relationship("BlogCategory", back_populates="blog", passive_deletes=True)

    blog_posts = relationship("BlogPost", back_populates="blog", passive_deletes=True)


class BlogCategory(State.mysql.Base):
    """
    Represents a BlogCategory
    """
    __tablename__ = "blog_categories"

    uuid = Column(String(64), primary_key=True, index=True, unique=True, nullable=False)
    blog_uuid = Column(String(64), ForeignKey('blogs.uuid', ondelete='CASCADE'), unique=False, nullable=False)
    meta_id = Column(String(64), unique=False, nullable=True)

    blog = relationship("Blog", back_populates="blog_categories", passive_deletes=False)

    blog_posts = relationship("BlogPost", back_populates="blog_category", passive_deletes=True)


class BlogPost(State.mysql.Base):
    """
    Represents a BlogPost
    """
    __tablename__ = "blog_posts"

    uuid = Column(String(64), primary_key=True, index=True, unique=True, nullable=False)
    blog_uuid = Column(String(64), ForeignKey('blogs.uuid', ondelete='CASCADE'), unique=False, nullable=False)
    meta_uuid = Column(String(64), unique=False, nullable=True)
    content_uuid = Column(String(64), unique=False, nullable=True)
    category_uuid = Column(String(64), ForeignKey('blog_categories.uuid', ondelete='CASCADE'), unique=False, nullable=False)
    locked = Column(Boolean, unique=False, nullable=False, default=False)
    frozen = Column(Boolean, unique=False, nullable=False, default=False)
    publish_at = Column(DateTime, unique=False, nullable=True)
    deleted_at = Column(DateTime, unique=False, nullable=True)

    blog = relationship("Blog", back_populates="blog_posts", passive_deletes=False)

    blog_category = relationship("BlogCategory", back_populates="blog_posts", passive_deletes=False)

# END OF GENERATED CODE
