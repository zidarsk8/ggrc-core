# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""The module provides service creating and manipulating GGRC's business
objects via Web UI."""

from lib.constants import element
from lib.entities.entities_factory import (
    AsmtTmplFactory, AsmtFactory, EntitiesFactory, ControlFactory)
from lib.page.widget.generic_widget import AsmtTmpls, Asmts, Controls
from lib.utils import selenium_utils


class BaseWebUiService(object):
  """Base class for business layer's services objects."""
  def __init__(self, driver):
    self.driver = driver

  @staticmethod
  def ui_elements_to_obj_attrs():
    """Get transformation dictionary {OLD KEY: NEW KEY}, where
    'OLD KEY' - UI elements correspond to the 'NEW KEY' - objects attributes.
    """
    fields = element.TransformationSetVisibleFields
    return {
        fields.TITLE.upper(): "title", fields.OWNER.upper(): "owner",
        fields.CODE.upper(): "code", fields.STATE.upper(): "state",
        fields.VERIFIED.upper(): "is_verified",
        fields.LAST_UPDATED.upper(): "last_update"
    }

  @staticmethod
  def remap_keys_for_list_dicts(transform_dict, list_old_dicts):
    """Remap keys names for old list of dictionaries according the
    transformation dictionary {OLD KEY: NEW KEY} and return the new updated
    list of dictionaries.
    """
    return [{transform_dict[key]: value for key, value in dic.iteritems()} for
            dic in list_old_dicts]

  def create_objs(self, factory, list_of_scopes):
    """Create business objects used entities factories and Web UI
    (list of text scopes (list of dicts) got from Web UI).
    Return list of objects.
    """
    objs = [factory.create() for _ in xrange(len(list_of_scopes))]
    list_of_scopes_remaped = self.remap_keys_for_list_dicts(
        transform_dict=self.ui_elements_to_obj_attrs(),
        list_old_dicts=list_of_scopes)
    return [
        EntitiesFactory.update_obj_attrs_values(obj=obj, **scope_remaped) for
        scope_remaped, obj in zip(list_of_scopes_remaped, objs)]


class AuditService(BaseWebUiService):
  """Service for working with business entity Audit."""
  def __init__(self, driver):
    super(AuditService, self).__init__(driver)

  def create_obj_via_modal(self, audit, obj, gen_widget):
    """Navigate to objects widget, open modal, fill data and create new object.
    """
    widget_url = gen_widget.URL.format(audit.id)
    selenium_utils.get_url_if_not_opened(self.driver, widget_url)
    objs_widget = gen_widget(self.driver).create()
    objs_widget.fill_minimal_data(obj.title, obj.code)
    objs_widget.save_and_close()

  def generate_objs_via_modal(self, audit, obj, objs_under, gen_widget):
    """Navigate to objects widget, open modal, fill data and generate new
    object(s).
    """
    objs_under_titles = [obj_under.title for obj_under in objs_under]
    widget_url = gen_widget.URL.format(audit.id)
    selenium_utils.get_url_if_not_opened(self.driver, widget_url)
    objs_widget = gen_widget(self.driver).generate()
    objs_widget.fill_minimal_data(obj.title, objs_under_titles)
    objs_widget.generate_and_close()

  def update_obj_via_info_panel(self, audit, gen_widget, old_obj):
    """Navigate to objects widget, select old (snapshotable) object in tree view
    and update it to the latest version via info panel."""
    widget_url = gen_widget.URL.format(audit.id)
    selenium_utils.get_url_if_not_opened(self.driver, widget_url)
    objs_widget = gen_widget(self.driver)
    objs_widget.update(old_obj.title)

  def get_count_of_objs_from_tab(self, audit, gen_widget):
    """Navigate to objects widget and get count of objects from tab
    navigation bar.
    """
    widget_url = gen_widget.URL.format(audit.id)
    selenium_utils.get_url_if_not_opened(self.driver, widget_url)
    return gen_widget(self.driver).member_count

  def get_list_of_scopes_from_tree_view(self, audit, gen_widget):
    """Navigate to objects widget, set visible fields and get list of objects
    scopes as dicts from header (keys) and items (values) that displayed
    in tree view.
    """
    widget_url = gen_widget.URL.format(audit.id)
    selenium_utils.get_url_if_not_opened(self.driver, widget_url)
    return gen_widget(self.driver).get_list_of_objs_scopes()


class AsmtTmplService(AuditService):
  """Service for working with business entity Assessment Template."""
  def __init__(self, driver):
    super(AsmtTmplService, self).__init__(driver)

  def create(self, audit, asmt_tmpl):
    """Create new Assessment Template via modal."""
    self.create_obj_via_modal(audit=audit, obj=asmt_tmpl, gen_widget=AsmtTmpls)

  def get_count(self, audit):
    """Return count of Assessment Templates from tab navigation bar."""
    return self.get_count_of_objs_from_tab(audit=audit, gen_widget=AsmtTmpls)

  def get_list_of_objs(self, audit):
    """Get list of Assessment Templates objects from list of scopes
    (list of dicts) which was got from tree view."""
    list_of_scopes = self.get_list_of_scopes_from_tree_view(
        audit=audit, gen_widget=AsmtTmpls)
    return self.create_objs(factory=AsmtTmplFactory(),
                            list_of_scopes=list_of_scopes)


class AsmtService(AuditService):
  """Service for working with business entity Assessment."""
  def __init__(self, driver):
    super(AsmtService, self).__init__(driver)

  def create(self, audit, asmt):
    """Create new Assessment via modal."""
    self.create_obj_via_modal(audit=audit, obj=asmt, gen_widget=Asmts)

  def generate(self, audit, asmt_tmpl, objs_under):
    """Generate new Assessment(s) via modal."""
    self.generate_objs_via_modal(audit=audit, obj=asmt_tmpl,
                                 objs_under=objs_under, gen_widget=Asmts)

  def get_count(self, audit):
    """Return count of Assessments from tab navigation bar."""
    return self.get_count_of_objs_from_tab(audit=audit, gen_widget=Asmts)

  def get_list_of_objs(self, audit):
    """Get list of Assessments objects from list of scopes (list of dicts)
    which was got from tree view."""
    list_of_scopes = self.get_list_of_scopes_from_tree_view(audit=audit,
                                                            gen_widget=Asmts)
    return self.create_objs(factory=AsmtFactory(),
                            list_of_scopes=list_of_scopes)


class ControlService(AuditService):
  """Service for working with business entity Control."""
  def __init__(self, driver):
    super(ControlService, self).__init__(driver)

  def update(self, audit, old_control):
    """Update old Control via tree view and info panel."""
    return self.update_obj_via_info_panel(audit=audit, gen_widget=Controls,
                                          old_obj=old_control)

  def get_count(self, audit):
    """Return count of Controls from tab navigation bar."""
    return self.get_count_of_objs_from_tab(audit=audit, gen_widget=Controls)

  def get_list_of_objs(self, audit):
    """Get list of Controls from list of scopes (list of dicts)
    which was got from tree view."""
    list_of_scopes = self.get_list_of_scopes_from_tree_view(
        audit=audit, gen_widget=Controls)
    return self.create_objs(factory=ControlFactory(),
                            list_of_scopes=list_of_scopes)
