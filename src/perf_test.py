"""Performance tests."""

import time
import logging

from sqlalchemy import exc

from ggrc import db
from ggrc.models import all_models


logger = logging.getLogger(__name__)


class Benchmark(object):

  def __init__(self, res, message):
    self.message = message
    self.res = res
    self.start = 0

  def __enter__(self):
    self.start = time.time()

  def __exit__(self, exc_type, exc_value, exc_trace):
    end = time.time()
    self.res.append((self.message, end - self.start))


class Tests(object):
  titled_models = [
      all_models.Control,
      all_models.Process,
      all_models.Program,
      all_models.AccessGroup,
      all_models.Assessment,
  ]

  test_models = titled_models + [
      all_models.Person,
  ]

  @staticmethod
  def clear_data():
    """Remove data from ggrc tables.

    This is a helper function to remove any data that might have been generated
    during a test. The ignored tables are the ones that don't exist or have
    constant data in them, that was populated with migrations.

    This function is used to speed up resetting of the database for each test.
    the proper way would be to run all migrations on a fresh database, but that
    would take too much time. This function should act as if the database was
    just created, with the exception of autoincrement indexes.

    Note:
      The deletion is a hack because db.metadata.sorted_tables does not sort by
      dependencies. The events table is given before Person table and reversed
      order in then incorrect.
    """
    ignore_tables = (
        "categories",
        "notification_types",
        "object_types",
        "options",
        "relationship_test_mock_model",
        "roles",
        "test_model",
        "contexts",
    )
    tables = set(db.metadata.tables).difference(ignore_tables)
    for _ in range(len(tables)):
      if len(tables) == 0:
        break  # stop the loop once all tables have been deleted
      for table in reversed(db.metadata.sorted_tables):
        if table.name in tables:
          try:
            db.engine.execute(table.delete())
            tables.remove(table.name)
          except exc.IntegrityError:
            pass
    contexts = db.metadata.tables["contexts"]
    db.engine.execute(contexts.delete(contexts.c.id > 1))
    db.session.commit()

  def __init__(self, n=10):
    self.n = n
    self.results = []
    self.full_models = {}

  def _fill_model(self, model, i):
    obj = model()
    names = [
        "slug",
        "title",
        "company",
        "description",
        "notes",
    ]
    val = str(i)
    for name in names:
      if hasattr(obj, name):
        setattr(obj, name, val)
    if hasattr(obj, "email"):
      obj.email = "user{}@example.com".format(i)
    return obj

  def test_generate_empty(self):
    for model in self.test_models:
      with Benchmark(self.results,
                     "generate empty model: {}".format(model.__name__)):
        [model() for _ in xrange(self.n)]

  def test_model_title(self):
    for model in self.titled_models:
      with Benchmark(self.results,
                     "generate model with title: {}".format(model.__name__)):
        [model(title="a") for _ in xrange(self.n)]

  def test_model_full(self):
    for model in self.test_models:
      with Benchmark(self.results,
                     "generate full model: {}".format(model.__name__)):
        [self._fill_model(model, i) for i in xrange(self.n)]

  def _generate_test_models(self):
    return {
        model: [self._fill_model(model, i) for i in xrange(self.n)]
        for model in self.test_models
    }

  def test_orm_save_objects(self):
    test_models = self._generate_test_models()
    self.clear_data()
    for model, values in test_models.iteritems():
      with Benchmark(self.results,
                     "ORM save model: {}".format(model.__name__)):
        [db.session.add(value)for value in values]
        db.session.commit()

  def test_bulk_save_objects(self):
    test_models = self._generate_test_models()
    self.clear_data()
    for model, values in test_models.iteritems():
      with Benchmark(self.results,
                     "ORM bulk save objects: {}".format(model.__name__)):
        db.session.bulk_save_objects(values)
        db.session.commit()

  def test_bulk_save_return(self):
    test_models = self._generate_test_models()
    self.clear_data()
    for model, values in test_models.iteritems():
      with Benchmark(self.results,
                     "ORM bulk save objects return defaults: {}".format(
                         model.__name__)):
        db.session.bulk_save_objects(values, return_defaults=True)
        db.session.commit()

  def test_core_insert(self):
    test_models = self._generate_test_models()
    self.clear_data()
    for model, values in test_models.iteritems():
      with Benchmark(self.results,
                     "core insert object: {}".format(model.__name__)):
        db.engine.execute(
            model.__table__.insert(),
            [v.__dict__ for v in values]
        )
        db.session.commit()


  def _single_statement_insert(self, model, values):
    insert_str = str(model.__table__.insert())
    stm, params = insert_str.split("VALUES")
    keys = params.strip(" ():").split(", :")
    new_params = "({})".format(", ".join(["%s"] * len(keys)))

    single_insert = "{} VALUES {}".format(stm, ", ".join([new_params] * len(values)))
    db.engine.execute(
        single_insert,
        sum([[v.__dict__.get(key) for key in keys] for v in values], [])
    )

  def test_single_insert(self):
    test_models = self._generate_test_models()
    self.clear_data()
    for model, values in test_models.iteritems():
      with Benchmark(self.results,
                     "single insert object: {}".format(model.__name__)):
        self._single_statement_insert(model, values)
        db.session.commit()

  def __str__(self):
    max_len = max(len(r[0]) for r in self.results)
    template = "{{:<{}}} : {{:>.6f}}".format(max_len)
    return "\n".join(template.format(*r) for r in self.results)

  def run_all(self):
    with Benchmark(self.results, "All:"):
      self.test_generate_empty()
      self.test_model_title()
      self.test_model_full()
      # self.test_orm_save_objects()
      # self.test_bulk_save_return()
      self.test_bulk_save_objects()
      self.test_core_insert()
      # self.test_single_insert()


def run_all(n):
  tests = Tests(n)
  tests.run_all()
  return str(tests)
