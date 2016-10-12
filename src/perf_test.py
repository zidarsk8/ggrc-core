"""Performance tests."""

import time
from datetime import date
from ggrc.models import all_models

import logging
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


  def __init__(self, n=10):
    self.n = n
    self.results = []

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
      obj.email="user{}@example.com".format(i)
    return obj

  def test_generate_empty(self):
    for model in self.test_models:
      with Benchmark(self.results,
                     "generate empty model: {}".format(model.__name__)):
        [model() for _ in xrange(self.n)]

  def test_empty_dict(self):
    for model in self.test_models:
      with Benchmark(self.results,
                     "generate empty model dict: {}".format(model.__name__)):
        [model().__dict__ for _ in xrange(self.n)]


  def test_model_title(self):
    for model in self.titled_models:
      with Benchmark(self.results,
                     "generate model with title: {}".format(model.__name__)):
        [model(title="a") for _ in xrange(self.n)]

  def test_model_title_dict(self):
    for model in self.titled_models:
      with Benchmark(self.results,
                     "generate model with title dict: {}".format(model.__name__)):
        [model(title="a").__dict__ for _ in xrange(self.n)]

  def test_model_full(self):
    for model in self.test_models:
      with Benchmark(self.results,
                     "generate full model: {}".format(model.__name__)):
        [self._fill_model(model, i) for i in xrange(self.n)]

  def __str__(self):
    max_len = max(len(r[0]) for r in self.results)
    template = "{{:<{}}} : {{:>.6f}}".format(max_len)
    return "\n".join(template.format(*r) for r in self.results)



def run_all(n):
  tests = Tests(n)
  tests.test_generate_empty()
  # tests.test_empty_dict()
  # tests.test_model_title()
  tests.test_model_title_dict()
  tests.test_model_full()

  return str(tests)
