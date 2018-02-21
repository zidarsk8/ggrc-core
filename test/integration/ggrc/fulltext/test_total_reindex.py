# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Test for total reindex procedure"""

import ddt
from sqlalchemy import orm

from ggrc import db
from ggrc import fulltext
from ggrc.fulltext.mysql import MysqlRecordProperty
from ggrc.utils import QueryCounter
from ggrc.fulltext import mysql

from integration.ggrc import TestCase
from integration.ggrc.models import factories as ggrc_factories
from integration.ggrc_workflows.models import factories as wf_factories


@ddt.ddt
class TestTotalReindex(TestCase):
  """Tests for total reindex procedure."""

  # Each reindex require at least 3 queries:
  # 1 get values from db
  # 2 remove old records
  # 3 create new records
  INDEX_QUERY_LIMIT = {
      'Assessment': 10,
      'AssessmentTemplate': 6,
      'Audit': 7,
      'Comment': 4,
      'Contract': 9,
      'Control': 12,
      'Cycle': 5,
      'CycleTaskEntry': 3,
      'CycleTaskGroup': 5,
      'CycleTaskGroupObjectTask': 5,
      'Document': 4,
      'Issue': 8,
      'Market': 8,
      'Objective': 9,
      'OrgGroup': 8,
      'Person': 5,
      'Policy': 9,
      'Process': 8,
      'Program': 7,
      'Regulation': 9,
      'TaskGroup': 3,
      'TaskGroupObject': 5,
      'TaskGroupTask': 4,
      'Workflow': 6,
  }

  def setUp(self):
    super(TestTotalReindex, self).setUp()
    mysql.MysqlRecordProperty.query.delete()

  INDEXED_MODEL_FACTORIES = [
      ggrc_factories.AuditFactory,
      ggrc_factories.AssessmentFactory,
      ggrc_factories.AssessmentTemplateFactory,
      ggrc_factories.CommentFactory,
      ggrc_factories.ContractFactory,
      ggrc_factories.ControlFactory,
      ggrc_factories.IssueFactory,
      ggrc_factories.MarketFactory,
      ggrc_factories.ObjectiveFactory,
      ggrc_factories.OrgGroupFactory,
      ggrc_factories.PersonFactory,
      ggrc_factories.PolicyFactory,
      ggrc_factories.ProcessFactory,
      ggrc_factories.ProgramFactory,
      ggrc_factories.RegulationFactory,
      ggrc_factories.DocumentFactory,
      wf_factories.CycleFactory,
      wf_factories.CycleTaskGroupFactory,
      wf_factories.CycleTaskEntryFactory,
      wf_factories.CycleTaskFactory,
      wf_factories.TaskGroupFactory,
      wf_factories.TaskGroupTaskFactory,
      wf_factories.WorkflowFactory,
  ]

  OBJECT_TEST_COUNT = 10

  def test_simple_reindex(self):
    """Test for check simple reindex procedure."""
    with ggrc_factories.single_commit():
      for factory in self.INDEXED_MODEL_FACTORIES:
        for _ in range(5):
          factory()
    indexer = fulltext.get_indexer()
    count = indexer.record_type.query.count()
    count = indexer.record_type.query.delete()
    self.client.get("/login")
    self.client.post("/admin/reindex")

    # ACR roles are created in migration and aren't removed in setup
    # Index for them will be created only after reindexing
    reindexed_count = indexer.record_type.query.filter(
        MysqlRecordProperty.type != "AccessControlRole"
    ).count()
    self.assertEqual(count, reindexed_count)

  COMMIT_INDEX_TEST_CASES = [(f, OBJECT_TEST_COUNT)
                             for f in INDEXED_MODEL_FACTORIES]

  @ddt.data(*COMMIT_INDEX_TEST_CASES)
  @ddt.unpack
  def test_index_on_commit(self, factory, obj_count):
    """Test count number of queries on reindex procedure."""
    model = factory._meta.model  # pylint: disable=protected-access
    with ggrc_factories.single_commit():
      obj_to_index = {factory() for _ in range(obj_count)}
    db.session.expire_all()
    db.session.reindex_set = model.query.filter(
        model.id.in_([i.id for i in obj_to_index]),
    ).options(
        orm.Load(model).load_only("id")
    ).all()
    with QueryCounter() as counter:
      mysql.update_indexer(db.session)
      self.assertLessEqual(
          counter.get,
          self.INDEX_QUERY_LIMIT[model.__name__],
          "Index {model} has too much queries: "
          "{counted} greater than {expected} for generate "
          "{obj_count} instances".format(
              model=model,
              expected=self.INDEX_QUERY_LIMIT[model.__name__],
              counted=counter.get,
              obj_count=obj_count,
          )
      )
