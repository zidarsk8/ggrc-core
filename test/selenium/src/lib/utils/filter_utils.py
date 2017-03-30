# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Utils for filter operations."""


class FilterUtils(object):
  """Class for work with filter utils."""

  @classmethod
  def _get_filter_exp(cls, criteria, grouping_operator="OR"):
    """Get filter expression for single and multiple criteria used grouping
    operator. Grouping operator can be "OR" or "AND".
    """
    def get_exp(criterion):
      """Get one filter expression according to criterion.
      Example:
      criterion = ("field", "=", "value")
      :return '"field" = "value"'
      """
      field, operator, value = criterion
      return u'"{}" {} "{}"'.format(field, operator, value)
    return u" {} ".format(grouping_operator).join(
        get_exp(criterion) for criterion in criteria)

  @staticmethod
  def get_filter_exp(field, operator, list_values):
    """Get filter expression to search data by title according to field, operator
    and list of values.
    Example:
    field = "field"
    operator = "="
    list_values = ["value1", "value2"]
    :return '"field" = "value1" OR "field" = "value2"'
    """
    return FilterUtils._get_filter_exp(
        [(field, operator, value) for value in list_values])

  @staticmethod
  def get_filter_exp_by_title(list_titles):
    """Get filter expression to search data by title according to list of titles.
    Example:
    list_titles = ["title1", "title2"]
    :return '"title" = "title1" OR "title" = "title2"'
    """
    return FilterUtils.get_filter_exp(field="title", operator="=",
                                      list_values=list_titles)
