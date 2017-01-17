# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
Resolve duplicates.

This helper is used by the following migrations:

* ggrc.migrations.verisions.20160223152916_204540106539;
* ggrc_risk_assessments.migrations.verisions.20151112161029_62f26762d0a.

"""

from sqlalchemy import and_
from sqlalchemy.orm import aliased

from ggrc import db


def resolve_duplicates(model, attr, separator=u"-"):
  """Resolve duplicates on a model property

  Check and remove by renaming duplicate attribute for values.

  Args:
    model: model that will be checked
    attr: attribute that will be checked
    separator: (default -) Separator between old attr value and integer
  """
  # pylint: disable=invalid-name
  v0, v1 = aliased(model, name="v0"), aliased(model, name="v1")
  query = db.session.query(v0).join(v1, and_(
      getattr(v0, attr) == getattr(v1, attr),
      v0.id > v1.id
  ))
  for v in query:
    i = 1
    nattr = "{}{}{}".format(getattr(v, attr, model.type), separator, i)
    while db.session.query(model).\
            filter(getattr(model, attr) == nattr).count():
      i += 1
      nattr = "{}{}{}".format(getattr(v, attr, model.type), separator, i)
    setattr(v, attr, nattr)
    db.session.add(v)
    db.session.flush()
  db.session.commit()
