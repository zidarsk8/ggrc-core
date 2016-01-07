#!/usr/bin/env python

import random
import string
import timeit

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import literal

Base = declarative_base()
DATABASE_URI = "mysql+mysqldb://root:root@localhost/ggrcdev?charset=utf8"
model_count = 50


def random_string(length=20, chars=None):
  if chars is None:
    chars = "{}{} ".format(string.ascii_uppercase, string.digits)
  return "".join(random.choice(chars) for _ in xrange(length))


def gen_model(name):
  return type(name, (Base,), {
      "__tablename__": name,
      "id": Column(Integer, primary_key=True),
      "title": Column(String(250)),
  })


MODELS = [gen_model("obj_{}".format(i)) for i in range(model_count)]


def join_query(pattern):
  queries = [
      session.query(
          literal(model.__name__).label("object_type"),
          model.id.label("object_id")
      ).filter(
          model.title.like(pattern),
      )
      for model in MODELS
  ]
  union = queries.pop()
  return union.union(*queries)


def join_count(pattern):
  return join_query(pattern).count()


def search(pattern):
  def j():
    return join_count(pattern)

  times_j = timeit.Timer(j).repeat(1, 1)
  average_time_j = sum(times_j) / len(times_j)
  print "time j: {:>7.4f}   - models: {}".format(average_time_j, model_count)


engine = create_engine(DATABASE_URI, echo=False)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

search("%A%")
