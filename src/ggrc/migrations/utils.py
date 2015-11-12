# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com

from ggrc import db
from sqlalchemy import and_
from sqlalchemy.orm import aliased


def resolve_duplicates(model, attr):
  v0, v1 = aliased(model, name="v0"), aliased(model, name="v1")
  query = db.session.query(v0).join(v1, and_(
      getattr(v0, attr) == getattr(v1, attr),
      v0.id > v1.id
  ))
  for v in query:
    setattr(v, attr, getattr(v, attr, model.type) + u"-" + unicode(v.id))
    db.session.add(v)
  db.session.commit()
