# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Contains ValidateOnComplete mixin.

This defines a procedure of an object's validation when its status moves from
one of NOT_DONE_STATES to DONE_STATES.
"""

from collections import namedtuple

from sqlalchemy.orm import validates

from ggrc.models.custom_attribute_definition import CustomAttributeDefinition
from ggrc.models.exceptions import ValidationError


class ValidateOnComplete(object):
  """Defines the validation routine before marking an object as complete.

  Requires Stateful and Statusable to be mixed in as well."""

  # pylint: disable=too-few-public-methods

  def _find_value_for_definition(self, cad):
    """Find CA value for CA definition in self.custom_attribute_values."""
    cav = [cav for cav in self.custom_attribute_values
           if int(cav.custom_attribute_id) == cad.id]
    assert len(cav) <= 1
    cav = cav[0] if cav else None
    return cav

  def _get_custom_attributes_comments(self):
    # pylint: disable=no-self-use
    return []  # not implemented yet

  def _get_relevant_evidences(self):
    # pylint: disable=no-self-use
    return []  # not implemented yet

  @staticmethod
  def _multi_choice_options_to_flags(cad):
    """Parse mandatory comment and evidence flags from dropdown CA definition.

    Args:
      cad - a CA definition object

    Returns:
      {option_value: Flags} - a dict from dropdown options values to Flags
                              objects where Flags.comment_required and
                              Flags.evidence_required correspond to the values
                              from multi_choice_mandatory bitmasks
    """
    flags = namedtuple('Flags', ['comment_required', 'evidence_required'])

    def make_flags(multi_choice_mandatory):
      flags_mask = int(multi_choice_mandatory)
      return flags(comment_required=flags_mask & (CustomAttributeDefinition
                                                  .MultiChoiceMandatoryFlags
                                                  .COMMENT_REQUIRED),
                   evidence_required=flags_mask & (CustomAttributeDefinition
                                                   .MultiChoiceMandatoryFlags
                                                   .EVIDENCE_REQUIRED))

    if not cad.multi_choice_options or not cad.multi_choice_mandatory:
      return {}
    else:
      return dict(zip(
          cad.multi_choice_options.split(','),
          (make_flags(mask)
           for mask in cad.multi_choice_mandatory.split(',')),
      ))

  @validates('status')
  def validate_status(self, key, value):
    """Check that mandatory fields and CAs are filled in.

    Also checks that comments and evidences required by dropdown CAs present.
    """
    # support for multiple validators for status
    if hasattr(super(ValidateOnComplete, self), "validate_status"):
      value = super(ValidateOnComplete, self).validate_status(key, value)

    # pylint: disable=attribute-defined-outside-init ; it's a mixin

    if self.status in self.NOT_DONE_STATES and value in self.DONE_STATES:
      # CA checks
      errors = []
      comments = self._get_custom_attributes_comments()
      evidences = self._get_relevant_evidences()
      for cad in self.custom_attribute_definitions:
        # find the value for this definition
        cav = self._find_value_for_definition(cad)

        # check mandatory values
        errors += self._check_mandatory_value(cad, cav)

        # check relevant comments and attachments
        if cad.attribute_type == CustomAttributeDefinition.ValidTypes.DROPDOWN:
          errors += self._check_dropdown_requirements(cad, cav, comments,
                                                      evidences)

      if errors:
        raise ValidationError('. '.join(errors))

    return value

  @staticmethod
  def _check_mandatory_value(cad, cav):
    if cad.mandatory and (not cav or not cav.attribute_value):
      return [
          'Value for definition #{cad.id} is missing or empty'
          .format(cad=cad),
      ]
    else:
      return []

  def _check_dropdown_requirements(self, cad, cav, comments, evidences):
    """Check mandatory comment and evidence for the CA value."""
    errors = []
    options_to_flags = self._multi_choice_options_to_flags(cad)
    if cav:
      flags = options_to_flags.get(cav.attribute_value)
      if flags:
        if flags.comment_required:
          # check the presence of a comment mapped to the CA
          errors += self._check_mandatory_comment(cad, cav, comments)
        if flags.evidence_required:
          # check the presence of an evidence
          errors += self._check_mandatory_evidence(cad, cav, evidences)
    return errors

  def _check_mandatory_comment(self, cad, cav, comments):
    """Check mandatory comment for the CA value."""
    # pylint: disable=no-self-use
    # pylint: disable=unused-argument
    for comment in comments:
      # check if the comment is relevant to the cad
      # not implemented yet
      pass
    return []

  def _check_mandatory_evidence(self, cad, cav, evidences):
    # pylint: disable=no-self-use
    # pylint: disable=unused-argument
    # not implemented yet
    return []
