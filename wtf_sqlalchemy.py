#!/usr/bin/env python
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine('sqlite:///app.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    children = relationship("Child")

class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    parent_id = Column(Integer, ForeignKey('parent.id'))
    friends = relationship("Friend")


class Friend(Base):
    __tablename__ = 'friend'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    child_id = Column(Integer, ForeignKey('child.id'))

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

jeff = Friend(name="jeff")
craig = Friend(name="craig")
sally = Friend(name="sally")

my_son = Child(name="my son", friends=[jeff, craig])
my_daughter = Child(name="my daughter", friends=[sally])

me = Parent(
    name="me",
    children=[my_son, my_daughter]
)

session.add(me)
session.commit()

# Get all friends of my children. Expecting 3.
friends = session.query(Parent).join(Child).join(Friend).all()
# Friends is only one row! It's a parent object.

# However, this returns 3.
print(session.query(Parent).join(Child).join(Friend).count())
