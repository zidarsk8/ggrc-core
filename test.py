#!/usr/bin/env python
from sqlalchemy import create_engine, or_
from sqlalchemy import Column, Integer, String, Text, Index
from sqlalchemy import event
from sqlalchemy.schema import DDL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.sql.expression import literal, union_all, union
import random
import string
import sys
import timeit

Base = declarative_base()
DATABASE_URI = "mysql+mysqldb://root:root@localhost/ggrcdev?charset=utf8"
model_count = 100
number_of_entries = 1000
notes_length = 50
description_length = 100


class FullText(Base):
  __tablename__ = "fulltext_index"
  id = Column(Integer, primary_key=True)
  object_id = Column(Integer)
  object_type = Column(String(64))
  name = Column(String(250))
  content = Column(Text)

  @declared_attr
  def __table_args__(cls):
    return (
        # Index('{}_text_idx'.format(cls.__tablename__), 'content'),
        Index('ix_{}_id'.format(cls.__tablename__), 'id'),
        Index('ix_{}_name'.format(cls.__tablename__), 'name'),
        {'mysql_engine': 'myisam'},
    )

# event.listen(
#     FullText.__table__,
#     'after_create',
#     DDL(
#         """ALTER TABLE {tablename}
#         ADD FULLTEXT INDEX {tablename}_text_idx
#         (content)""".format(tablename=FullText.__tablename__)
#     )
# )


def random_string(length=20, chars=None):
  if chars is None:
    chars = "{}{} ".format(string.ascii_uppercase, string.digits)
  return "".join(random.choice(chars) for _ in xrange(length))


def gen_model(name):
  return type(name, (Base,), {
      "__tablename__": name,
      "id": Column(Integer, primary_key=True),
      "slug": Column(String(250)),
      "title": Column(String(250)),
      "description": Column(Text),
      "notes": Column(Text),
      "__table_args__": (
      )
  })

MODELS = [gen_model("obj_{}".format(i)) for i in range(model_count)]


def generate_objects(session):
  def create_index_entries(obj):
    kw = {"object_type": obj.__class__.__name__, "object_id": obj.id}
    session.add(FullText(name="slug", content=obj.slug, **kw))
    session.add(FullText(name="title", content=obj.title, **kw))
    session.add(FullText(name="notes", content=obj.notes, **kw))
    session.add(FullText(name="description", content=obj.description, **kw))

  for i in xrange(number_of_entries):
    for model in MODELS:
      obj = model(
          slug="slug_{}".format(i),
          title=random_string(),
          notes=random_string(notes_length),
          description=random_string(description_length),
      )
      session.add(obj)
      session.flush()
      create_index_entries(obj)
    sys.stdout.write("setup: {:>5}/{:>5}\r".format(i + 1, number_of_entries))
    sys.stdout.flush()
  session.commit()
  print "setup: {e:>5}/{e:>5}  [done]".format(e=number_of_entries)


def index_query(pattern):
  return session.query(FullText.object_type, FullText.object_id)\
      .filter(FullText.content.like(pattern)).distinct()


def index_query_ft(pattern):
  return session.query(FullText.object_type, FullText.object_id)\
      .filter(FullText.content.match(pattern)).distinct()


def join_query(pattern):
  queries = [
      session.query(
          literal(model.__name__).label("object_type"),
          model.id.label("object_id")
      ).filter(
          or_(
              model.slug.like(pattern),
              model.title.like(pattern),
              model.notes.like(pattern),
              model.description.like(pattern),
          )
      )
      for model in MODELS
  ]
  neki = union_all(*queries)

  # union = queries.pop()
  return session.query(neki.alias("neki"))


def join_query_ft(pattern):
  queries = [
      session.query(
          literal(model.__name__).label("object_type"),
          model.id.label("object_id")
      ).filter(
          or_(
              model.slug.match(pattern),
              model.title.match(pattern),
              model.notes.match(pattern),
              model.description.match(pattern),
          )
      )
      for model in MODELS
  ]
  neki = union_all(*queries)

  # union = queries.pop()
  return session.query(neki.alias("neki"))


def index_count(pattern):
  return index_query(pattern).count()


def index_count_ft(pattern):
  return index_query_ft(pattern).count()


def join_count(pattern):
  return join_query(pattern).count()


def join_count_ft(pattern):
  return join_query_ft(pattern).count()

stuff = set()


def index_select(pattern):
  stuff.add(tuple(["select"] + sorted(index_query(pattern).all())[:5]))


def index_select_ft(pattern):
  stuff.add(tuple(["select"] + sorted(index_query_ft(pattern).all())[:5]))


def join_select_ft(pattern):
  stuff.add(tuple(["join  "] + sorted(join_query_ft(pattern).all())[:5]))


def join_select(pattern):
  stuff.add(tuple(["join  "] + sorted(join_query(pattern).all())[:5]))


def search(pattern, pattern_ft):
  print "\nSearching: '{}' ".format(pattern)

  def j():
    return join_select(pattern)
    # return join_count(pattern)

  def i():
    return index_select_ft(pattern_ft)
    # return index_count(pattern)


  def j_ft():
    return join_select(pattern)
    # return join_count(pattern)

  def i_ft():
    return index_select_ft(pattern_ft)
    # return index_count(pattern)

  repeat = 1

  # times_i = timeit.Timer(i).repeat(repeat, 1)
  # average_time_i = sum(times_i) / len(times_i)
  # print "i    : {:>9.4f}   - models: {}   - found: {}".format(
  #   average_time_i,
  #   model_count,
  #   index_count(pattern),
  # )
  # times_j = timeit.Timer(j).repeat(repeat, 1)
  # average_time_j = sum(times_j) / len(times_j)
  # print "j    : {:>9.4f}   - models: {}   - found: {}".format(
  #   average_time_j,
  #   model_count,
  #   join_count(pattern),
  # )
  times_i_ft = timeit.Timer(i_ft).repeat(repeat, 1)
  average_time_i_ft = sum(times_i_ft) / len(times_i_ft)
  print "i ft : {:>9.4f}   - models: {}   - found: {}".format(
    average_time_i_ft,
    model_count,
    index_count_ft(pattern_ft),
  )
  times_j_ft = timeit.Timer(j_ft).repeat(repeat, 1)
  average_time_j_ft = sum(times_j_ft) / len(times_j_ft)
  print "j ft : {:>9.4f}   - models: {}   - found: {}".format(
    average_time_j_ft,
    model_count,
    join_count_ft(pattern_ft),
  )


engine = create_engine(DATABASE_URI, echo=False)
Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()

# generate_objects(session)
# join_select("A%")

# join_count_ft("A*")

search("A%", "A*")
# search("%AE%", "AE*")
# search("%A2E%", "A2E*")
# search("%UAEG%", "UAEG*")
# search("slug_34", "slug_34")
# search("9F9MGUT0DJEQ9CLYBRUF", "9F9MGUT0DJEQ9CLYBRUF")

print "\n\n"
for s in sorted(stuff):
  print s

# print "ALTER TABLE {t} ADD FULLTEXT INDEX {t}_{c}_ind ({c});".format(
#     t=FullText.__name__,
#     c="content",
# )
# for model in MODELS:
#   for column in ("slug", "title", "description", "notes"):
#     print "ALTER TABLE {t} ADD FULLTEXT INDEX {t}_{c}_ind ({c});".format(
#         t=model.__name__,
#         c=column,
#     )
