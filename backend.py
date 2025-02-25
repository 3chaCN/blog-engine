import json
import sqlalchemy
from sqlalchemy import MetaData
from sqlalchemy import literal_column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy import select, insert
from sqlalchemy.orm import Session
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship

# Create a connection to the database
engine = create_engine('postgresql://zyx:Postgres123@localhost:5432/testdb');
connection = engine.connect()
session = Session(engine)

class Base(DeclarativeBase):
    # default schema
    metadata = MetaData(schema="blog")

# version table
class TableVersion(Base):
    __tablename__ = 'version'
    version: Mapped[str] = mapped_column(String(10), primary_key=True)

    def __repr__(self) -> str:
        pass
        #return "{" + "\"version\":" + f"\"{self.version}\"" + "}" 
        #return json.loads(str("{" + f"\"version\":\"{self.version}\"" + "}"))
        return json.dumps({"version": self.version})

class TableUsers(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(20))
    password: Mapped[str] = mapped_column(String(255))
    
    posts: Mapped[list["TablePosts"]] = relationship("TablePosts", back_populates="author")

    def __repr__(self) -> str:
        #return  "{" + f"\"id\":\"{self.id}\"," + f"\"username\":\"{self.username}\"," + f"\"password\":\"{self.password}\"" + "}"
        return json.dumps({"id": self.id, "username": self.username, "password": self.password})

class TableCategories(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(primary_key=True)
    caption: Mapped[str] = mapped_column(Text)

    posts: Mapped[list["TablePosts"]] = relationship("TablePosts", back_populates="category")

    def __repr__(self) -> str:
        return json.dumps({"id": self.id, "caption":self.caption})

class TablePosts(Base):
    __tablename__ = 'posts'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(Text)
    content: Mapped[str] = mapped_column(Text)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date: Mapped[str] = mapped_column(String(15))
    
    category: Mapped["TableCategories"] = relationship("TableCategories", back_populates="posts")  
    author: Mapped["TableUsers"] = relationship("TableUsers", back_populates="posts")

    def __repr__(self) -> str:
        return f"id={self.id}, title={self.title}, content={self.content}, author={self.author}"
        #return "{" + f"\"id\":\"{self.id}\", \"title\":\"{self.title}\", \"content\":\"{self.content}\"" + "}" 
    # \"author\":\"{self.author}\"" + "}"
        #return json.dumps({"id": self.id, "title": self.title, "content": self.content, "author": self.author})

def get_posts(count=None) -> list:
    if count is not None:
        stmt = select(TablePosts.id, TablePosts.title, TablePosts.content, TableUsers.username, TablePosts.date, TableCategories.caption).join(TableUsers, TablePosts.author_id == TableUsers.id).join(TableCategories, TablePosts.category_id == TableCategories.id).order_by(TablePosts.date.desc()).limit(count)
    else:
        stmt = select(TablePosts.id, TablePosts.title, TablePosts.content, TableUsers.username, TablePosts.date, TableCategories.caption).join(TableUsers, TablePosts.author_id == TableUsers.id).join(TableCategories, TablePosts.category_id == TableCategories.id).order_by(TablePosts.date.desc())
 
    query = session.execute(stmt).all()
    return query

def get_post_num(num):
    stmt = select(TablePosts.id, TablePosts.title, TablePosts.content, TableUsers.username, TablePosts.date, TableCategories.caption).join(TableUsers, TablePosts.author_id == TableUsers.id).join(TableCategories, TablePosts.category_id == TableCategories.id).where(TablePosts.id == num)

    query = session.execute(stmt).one()

    return query

def get_post_by_cat(category):
    stmt = select(TablePosts.id, TablePosts.title, TablePosts.content, TableUsers.username, TablePosts.date, TableCategories.caption).join(TableUsers, TablePosts.author_id == TableUsers.id).join(TableCategories, TablePosts.category_id == TableCategories.id).where(TableCategories.caption == category)

    query = session.execute(stmt).all()

    return query

def get_author(username) -> list:
    stmt = select(TableUsers.id, TableUsers.username).where(TableUsers.username == username)
    query = session.execute(stmt)

    return query.one()

def get_categories() -> list:
    stmt = select(TableCategories.id, TableCategories.caption)
    query = session.execute(stmt).all()

    return query

def get_category(category) -> list:
    stmt = select(TableCategories.id, TableCategories.caption).where(TableCategories.caption == category)
    query = session.execute(stmt)

    return query.one()

def get_version() -> str:
    stmt = select(TableVersion)
    return json.loads(str(session.scalars(stmt).one()))

def insert_user(username, password):
    username = TableUsers(username=username, 
                          password=password)
    session.add(username)
    session.commit()

def insert_category(category):
    cat = TableCategories(caption=category)
    session.add(cat)
    session.commit()

def insert_post(title, data, author, category, date):
    post = TablePosts(title=title, 
                      content=data, 
                      author_id=get_author(author)[0],
                      category_id=get_category(category)[0],
                      date=date)
    print("Insert new post")                    
    session.add(post)
    session.commit()

def check_password(username, password):
    stmt = select(TableUsers.username, literal_column(f"blog.users.password = crypt('{password}', password)").label("p")).where(TableUsers.username == f"{username}")
    result = session.execute(stmt)
    return result.one()[1]

try:
    get_version() 
except:
    Base.metadata.create_all(engine)
    session.commit()
    version = TableVersion(version="1.0.0")
    session.add(version)
    try:
        session.commit()
        print("Commit successful")
    except Exception as e:
        session.rollback()
        print("Commit failed")

