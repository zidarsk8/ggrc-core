# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""The module provides services for creating and manipulating GGRC's objects
via UI."""

from lib.constants import element
from lib.entities.entities_factory import (
    AsmtTmplFactory, AsmtFactory, EntitiesFactory, ControlFactory)
from lib.page.widget.generic_widget import AsmtTmpls, Asmts, Controls
from lib.utils import selenium_utils, string_utils


class BaseWebUiService(object):
  """Base class for business layer's services objects."""
  def __init__(self, driver):
    self.driver = driver

  def create_list_objs(self, factory, list_scopes):
    """Create and return list of objects used entity factory and UI data
    (list of scopes UI text elements {"header": "item", ...} remapped to
    list of dicts {"attr": "value", ...}). Return list of created objects.
    """
    list_factory_objs = [factory.create() for _ in xrange(len(list_scopes))]
    list_scopes_remapped = string_utils.remap_keys_for_list_dicts(
        dict_transformation_keys=self.ui_elements_to_obj_attrs(),
        list_dicts=list_scopes)
    return [
        EntitiesFactory.update_obj_attrs_values(
            obj=factory_obj, **scope_remapped) for
        scope_remapped, factory_obj in zip(list_scopes_remapped,
                                           list_factory_objs)]

  @staticmethod
  def ui_elements_to_obj_attrs():
    """Get transformation dictionary {"OLD KEY": "NEW KEY"}, where
    "OLD KEY" - UI elements correspond to the "NEW KEY" - objects attributes.
    """
    fields = element.TransformationSetVisibleFields
    return {
        fields.TITLE.upper(): "title", fields.OWNER.upper(): "owner",
        fields.CODE.upper(): "code", fields.STATE.upper(): "state",
        fields.VERIFIED.upper(): "is_verified",
        fields.LAST_UPDATED.upper(): "last_update"
    }

  def create_obj_via_tree_view(self, widget_url, gen_widget, obj):
    """Navigate to widget URL, open creation modal from tree view,
    fill data according to object attributes and create new object.
    """
    selenium_utils.open_url(self.driver, widget_url)
    objs_widget = gen_widget(self.driver).create()
    objs_widget.fill_minimal_data(obj.title, obj.code)
    objs_widget.save_and_close()

  def get_count_objs_from_tab(self, widget_url, gen_widget):
    """Navigate to widget URL, get count of objects from tab navigation bar
    and return got count.
    """
    selenium_utils.open_url(self.driver, widget_url)
    return gen_widget(self.driver).member_count

  def get_list_scopes_from_tree_view(self, widget_url, gen_widget):
    """Navigate to widget URL, set visible fields and get list of objects
    scopes as dicts from header (keys) and items (values) that displayed
    in tree view.
    """
    selenium_utils.open_url(self.driver, widget_url)
    return gen_widget(self.driver).get_list_objs_scopes()


class AuditsService(BaseWebUiService):
  """Service for working with entity Audits entities."""

  def __init__(self, driver):
    super(AuditsService, self).__init__(driver)

  def generate_objs_via_tree_view(self, widget_url, gen_widget, obj,
                                  objs_under):
    """Navigate to widget URL, open generation modal from tree view,
    fill data according to object and objects under attributes,
    generate new object(s).
    """
    selenium_utils.open_url(self.driver, widget_url)
    objs_widget = gen_widget(self.driver).generate()
    objs_under_titles = [obj_under.title for obj_under in objs_under]
    objs_widget.fill_minimal_data(obj.title, objs_under_titles)
    objs_widget.generate_and_close()

  def update_obj_ver_via_info_panel(self, widget_url, gen_widget, obj):
    """Navigate to widget URL, select snapshotable object from tree view
    by title and update object to the latest version via info panel.
    """
    selenium_utils.open_url(self.driver, widget_url)
    objs_widget = gen_widget(self.driver)
    objs_widget.update_ver(obj.title)


class AsmtTmplsService(BaseWebUiService):
  """Service for working with Assessment Template entities."""
  def __init__(self, driver):
    super(AsmtTmplsService, self).__init__(driver)

  def create_via_tree_view(self, source_obj, asmt_tmpl_obj):
    """Create new Assessment Template object via tree view."""
    self.create_obj_via_tree_view(
        widget_url=AsmtTmpls.URL.format(source_obj_url=source_obj.url),
        gen_widget=AsmtTmpls, obj=asmt_tmpl_obj)

  def get_count_from_tab(self, source_obj):
    """Get and return count of Assessment Templates objects from tab
    navigation bar."""
    return self.get_count_objs_from_tab(
        widget_url=AsmtTmpls.URL.format(source_obj_url=source_obj.url),
        gen_widget=AsmtTmpls)

  def get_objs_from_tree_view(self, source_obj):
    """Get and return list of Assessment Templates objects from tree view."""
    list_scopes = self.get_list_scopes_from_tree_view(
        widget_url=AsmtTmpls.URL.format(source_obj_url=source_obj.url),
        gen_widget=AsmtTmpls)
    return self.create_list_objs(
        factory=AsmtTmplFactory(), list_scopes=list_scopes)


class AsmtsService(BaseWebUiService):
  """Service for working with entity Assessment entities."""
  def __init__(self, driver):
    super(AsmtsService, self).__init__(driver)

  def create_via_tree_view(self, source_obj, asmt_obj):
    """Create new Assessment object via tree view."""
    self.create_obj_via_tree_view(
        widget_url=Asmts.URL.format(source_obj_url=source_obj.url),
        gen_widget=Asmts, obj=asmt_obj)

  def generate_via_tree_view(self, source_obj, asmt_tmpl_obj, objs_under_asmt):
    """Generate new Assessment(s) object(s) via tree view."""
    AuditsService(self.driver).generate_objs_via_tree_view(
        widget_url=Asmts.URL.format(source_obj_url=source_obj.url),
        gen_widget=Asmts, obj=asmt_tmpl_obj, objs_under=objs_under_asmt)

  def get_count_from_tab(self, source_obj):
    """Get and return count of Assessments objects from tab navigation bar."""
    return self.get_count_objs_from_tab(
        widget_url=Asmts.URL.format(source_obj_url=source_obj.url),
        gen_widget=Asmts)

  def get_objs_from_tree_view(self, source_obj):
    """Get and return list of Assessments objects from tree view."""
    list_scopes = self.get_list_scopes_from_tree_view(
        widget_url=Asmts.URL.format(source_obj_url=source_obj.url),
        gen_widget=Asmts)
    return self.create_list_objs(
        factory=AsmtFactory(), list_scopes=list_scopes)


class ControlsService(AuditsService):
  """Service for working with Controls entities."""
  def __init__(self, driver):
    super(ControlsService, self).__init__(driver)

  def update_ver_via_info_panel(self, source_obj, control_obj):
    """Update version of Control object via info panel from tree view."""
    self.update_obj_ver_via_info_panel(
        widget_url=Controls.URL.format(source_obj_url=source_obj.url),
        gen_widget=Controls, obj=control_obj)

  def get_count_from_tab(self, source_obj):
    """Get and return count of Controls objects from tab navigation bar."""
    return self.get_count_objs_from_tab(
        widget_url=Controls.URL.format(source_obj_url=source_obj.url),
        gen_widget=Controls)

  def get_objs_from_tree_view(self, source_obj):
    """Get and return list of Controls objects from tree view."""
    list_scopes = self.get_list_scopes_from_tree_view(
        widget_url=Controls.URL.format(source_obj_url=source_obj.url),
        gen_widget=Controls)
    return self.create_list_objs(
        factory=ControlFactory(), list_scopes=list_scopes)
