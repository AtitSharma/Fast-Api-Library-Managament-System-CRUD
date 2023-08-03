from app.database import Base
from sqlalchemy import Integer, Column, String, Boolean, ForeignKey,UniqueConstraint
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

class Library(Base):
    __tablename__ = "library"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    library_id=Column(Integer,ForeignKey("library.id"),nullable=True)
    author = relationship("User")
    library=relationship("Library")
    
    

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)




class Role(Base):
    __tablename__ ="roles"
    id=Column(Integer,primary_key=True,nullable=False)
    name=Column(String,nullable=False,unique=True,default="Borrower")
    
    

class User_Role(Base):
    __tablename__="user_role"
    id=Column(Integer,primary_key=True,nullable=False)
    user_id =Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    role_id=Column(Integer,ForeignKey("roles.id"),nullable=False)
    __table_args__ = (UniqueConstraint('user_id', 'role_id', name='_user_role_uc'),)
    
    
