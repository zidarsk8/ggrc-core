# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Create, description, representation and equal of entities."""
# pylint: disable=too-many-arguments
# pylint: disable=too-few-public-methods


class Entity(object):
  """Class that represent model for base entity."""
  # pylint: disable=invalid-name
  # pylint: disable=redefined-builtin

  def __init__(self, type=None, id=None, title=None, href=None, url=None):
    self.type = type
    self.id = id
    self.title = title
    self.href = href
    self.url = url

  @staticmethod
  def attrs_names_all_entities():
    """Get list of all possible unique entities attributes' names."""
    all_entities_cls = [
        PersonEntity, CustomAttributeEntity, ProgramEntity,
        ControlEntity, AuditEntity, AssessmentEntity,
        AssessmentTemplateEntity, IssueEntity]
    all_entities_attrs_names = [
        entity_class().__dict__.keys() for
        entity_class in all_entities_cls]
    unique_entities_attrs_names = {
        val for sublist in all_entities_attrs_names for val in sublist}
    return unique_entities_attrs_names


class PersonEntity(object):
  """Class that represent model for Person."""
  # pylint: disable=invalid-name
  # pylint: disable=redefined-builtin
  # pylint: disable=too-many-instance-attributes
  __hash__ = None

  def __init__(self, type=None, id=None, name=None, href=None, url=None,
               email=None, company=None, system_wide_role=None,
               updated_at=None, custom_attribute_definitions=None,
               custom_attribute_values=None):
    super(PersonEntity, self).__init__()
    self.name = name
    self.id = id
    self.href = href
    self.url = url
    self.type = type
    self.email = email
    self.company = company
    self.system_wide_role = system_wide_role  # authorizations
    self.updated_at = updated_at  # last updated
    self.custom_attribute_definitions = custom_attribute_definitions
    self.custom_attribute_values = custom_attribute_values

  def __repr__(self):
    return ("type: {type}, id: {id}, name: {name}, href: {href}, url: {url}, "
            "email: {email}, company: {company}, "
            "system_wide_role: {system_wide_role}, updated_at: {updated_at}, "
            "custom_attribute_definitions: {custom_attribute_definitions}, "
            "custom_attribute_values: {custom_attribute_values}").format(
        type=self.type, id=self.id, name=self.name, href=self.href,
        url=self.url, email=self.email, company=self.company,
        system_wide_role=self.system_wide_role, updated_at=self.updated_at,
        custom_attribute_definitions=self.custom_attribute_definitions,
        custom_attribute_values=self.custom_attribute_values)


class CustomAttributeEntity(object):
  """Class that represent model for Custom Attribute."""
  # pylint: disable=invalid-name
  # pylint: disable=redefined-builtin
  # pylint: disable=too-many-instance-attributes
  __hash__ = None

  def __init__(self, title=None, id=None, href=None, type=None,
               definition_type=None, attribute_type=None, helptext=None,
               placeholder=None, mandatory=None, multi_choice_options=None):
    super(CustomAttributeEntity, self).__init__()
    self.title = title
    self.id = id
    self.href = href
    self.type = type
    self.definition_type = definition_type
    self.attribute_type = attribute_type
    self.helptext = helptext
    self.placeholder = placeholder
    self.mandatory = mandatory
    self.multi_choice_options = multi_choice_options

  def __repr__(self):
    return ("type: {type}, title: {title}, id: {id}, href: {href}, "
            "definition_type: {definition_type}, "
            "attribute_type: {attribute_type}, helptext: {helptext}, "
            "placeholder: {placeholder}, mandatory: {mandatory}, "
            "multi_choice_options: {multi_choice_options}").format(
        type=self.type, title=self.title, id=self.id, href=self.href,
        definition_type=self.definition_type,
        attribute_type=self.attribute_type, helptext=self.helptext,
        placeholder=self.placeholder, mandatory=self.mandatory,
        multi_choice_options=self.multi_choice_options)

  def __eq__(self, other):
    return (isinstance(other, self.__class__) and self.type == other.type and
            self.title == other.title and
            self.definition_type == other.definition_type and
            self.attribute_type == other.attribute_type and
            self.mandatory == other.mandatory)


class ProgramEntity(Entity):
  """Class that represent model for Program."""
  # pylint: disable=too-many-instance-attributes
  __hash__ = None

  def __init__(self, slug=None, status=None, manager=None, contact=None,
               secondary_contact=None, updated_at=None,
               custom_attribute_definitions=None,
               custom_attribute_values=None):
    super(ProgramEntity, self).__init__()
    self.slug = slug  # code
    self.status = status  # state
    self.manager = manager  # predefined and same as primary contact
    self.contact = contact  # primary contact
    self.secondary_contact = secondary_contact
    self.updated_at = updated_at  # last updated
    self.custom_attribute_definitions = custom_attribute_definitions
    self.custom_attribute_values = custom_attribute_values

  def __repr__(self):
    return ("type: {type}, id: {id}, title: {title}, href: {href}, "
            "url: {url}, slug: {slug}, status: {status}, manager: {manager}, "
            "contact: {contact}, secondary_contact: {secondary_contact}, "
            "updated_at: {updated_at}, "
            "custom_attribute_definitions: {custom_attribute_definitions}, "
            "custom_attribute_values: {custom_attribute_values}").format(
        type=self.type, title=self.title, id=self.id, href=self.href,
        url=self.url, slug=self.slug, status=self.status, manager=self.manager,
        contact=self.contact, secondary_contact=self.secondary_contact,
        updated_at=self.updated_at,
        custom_attribute_definitions=self.custom_attribute_definitions,
        custom_attribute_values=self.custom_attribute_values)

  def __eq__(self, other):
    return (isinstance(other, self.__class__) and self.type == other.type and
            self.title == other.title and self.slug == other.slug and
            self.status == other.status and
            (self.manager == other.manager or
             other.manager in self.manager.values()) and
            (self.contact == other.contact or
             other.contact in self.contact.values()))


class ControlEntity(Entity):
  """Class that represent model for Control."""
  # pylint: disable=too-many-instance-attributes
  __hash__ = None

  def __init__(self, slug=None, status=None, owners=None, contact=None,
               secondary_contact=None, updated_at=None,
               custom_attribute_definitions=None,
               custom_attribute_values=None):
    super(ControlEntity, self).__init__()
    self.slug = slug  # code
    self.status = status  # state
    self.owners = owners
    self.contact = contact  # primary contact
    self.secondary_contact = secondary_contact
    self.updated_at = updated_at  # last updated
    self.custom_attribute_definitions = custom_attribute_definitions
    self.custom_attribute_values = custom_attribute_values

  def __repr__(self):
    return ("type: {type}, id: {id}, title: {title}, href: {href}, "
            "url: {url}, slug: {slug}, status: {status}, owners: {owners}, "
            "contact: {contact}, secondary_contact: {secondary_contact}, "
            "updated_at: {updated_at}, "
            "custom_attribute_definitions: {custom_attribute_definitions}, "
            "custom_attribute_values: {custom_attribute_values}").format(
        type=self.type, title=self.title, id=self.id, href=self.href,
        url=self.url, slug=self.slug, status=self.status, owners=self.owners,
        contact=self.contact, secondary_contact=self.secondary_contact,
        updated_at=self.updated_at,
        custom_attribute_definitions=self.custom_attribute_definitions,
        custom_attribute_values=self.custom_attribute_values)

  def __eq__(self, other):
    return (isinstance(other, self.__class__) and self.type == other.type and
            self.title == other.title and self.slug == other.slug and
            self.status == other.status and
            (self.owners == other.owners or
             other.owners in [owner.values() for owner in self.owners][0]) and
            (self.contact == other.contact or other.contact in
             self.contact.values()))

  def __lt__(self, other):
    return self.slug < other.slug


class AuditEntity(Entity):
  """Class that represent model for Audit."""
  __hash__ = None

  def __init__(self, slug=None, status=None, program=None, contact=None,
               updated_at=None, custom_attribute_definitions=None,
               custom_attribute_values=None):
    super(AuditEntity, self).__init__()
    self.slug = slug  # code
    self.status = status  # status
    self.program = program
    self.contact = contact  # internal audit lead
    self.updated_at = updated_at  # last updated
    self.custom_attribute_definitions = custom_attribute_definitions
    self.custom_attribute_values = custom_attribute_values

  def __repr__(self):
    return ("type: {type}, id: {id}, title: {title}, href: {href}, "
            "url: {url}, slug: {slug}, status: {status}, program: {program}, "
            "contact: {contact}, updated_at: {updated_at}, "
            "custom_attribute_definitions: {custom_attribute_definitions}, "
            "custom_attribute_values: {custom_attribute_values}").format(
        type=self.type, title=self.title, id=self.id, href=self.href,
        url=self.url, slug=self.slug, status=self.status, program=self.program,
        contact=self.contact, updated_at=self.updated_at,
        custom_attribute_definitions=self.custom_attribute_definitions,
        custom_attribute_values=self.custom_attribute_values)

  def __eq__(self, other):
    return (isinstance(other, self.__class__) and self.type == other.type and
            self.title == other.title and self.slug == other.slug and
            self.status == other.status and
            (self.contact == other.contact or
             other.contact in self.contact.values()))


class AssessmentTemplateEntity(Entity):
  """Class that represent model for Assessment Template."""
  # pylint: disable=superfluous-parens
  # pylint: disable=too-many-instance-attributes
  __hash__ = None

  def __init__(self, slug=None, audit=None, default_people=None,
               verifiers=None, assessors=None,
               template_object_type=None, updated_at=None,
               custom_attribute_definitions=None,
               custom_attribute_values=None):
    super(AssessmentTemplateEntity, self).__init__()
    self.slug = slug  # code
    self.audit = audit
    self.default_people = default_people  # {"verifiers": *, "assessors": *}
    self.verifiers = verifiers  # item of default_people
    self.assessors = assessors  # item of default_people
    self.template_object_type = template_object_type
    self.updated_at = updated_at  # last updated
    self.custom_attribute_definitions = custom_attribute_definitions
    self.custom_attribute_values = custom_attribute_values

  def __repr__(self):
    return ("type: {type}, id: {id}, title: {title}, href: {href}, "
            "url: {url}, slug: {slug}, audit: {audit}, "
            "verifiers: {verifiers}, assessors: {assessors}, "
            "template_object_type: {template_object_type}, "
            "updated_at: {updated_at}, "
            "custom_attribute_definitions: {custom_attribute_definitions}, "
            "custom_attribute_values: {custom_attribute_values}").format(
        type=self.type, title=self.title, id=self.id, href=self.href,
        url=self.url, slug=self.slug, audit=self.audit,
        verifiers=self.verifiers, assessors=self.assessors,
        template_object_type=self.template_object_type,
        updated_at=self.updated_at,
        custom_attribute_definitions=self.custom_attribute_definitions,
        custom_attribute_values=self.custom_attribute_values)

  def __eq__(self, other):
    return (isinstance(other, self.__class__) and self.type == other.type and
            self.title == other.title and self.slug == other.slug)


class AssessmentEntity(Entity):
  """Class that represent model for Assessment."""
  # pylint: disable=too-many-instance-attributes
  # pylint: disable=redefined-builtin
  __hash__ = None

  def __init__(self, slug=None, status=None, object=None, audit=None,
               recipients=None, verified=None, updated_at=None,
               custom_attribute_definitions=None,
               custom_attribute_values=None):
    super(AssessmentEntity, self).__init__()
    self.slug = slug  # code
    self.status = status  # state
    self.object = object
    self.audit = audit
    self.recipients = recipients  # "Assessor,Creator,Verifier"
    self.verified = verified
    self.updated_at = updated_at  # last updated
    self.custom_attribute_definitions = custom_attribute_definitions
    self.custom_attribute_values = custom_attribute_values

  def __repr__(self):
    return ("type: {type}, id: {id}, title: {title}, href: {href}, "
            "url: {url}, slug: {slug}, status: {status}, object: {object}, "
            "audit: {audit}, recipients: {recipients}, verified: {verified}, "
            "updated_at: {updated_at}, "
            "custom_attribute_definitions: {custom_attribute_definitions}, "
            "custom_attribute_values: {custom_attribute_values}").format(
        type=self.type, title=self.title, id=self.id, href=self.href,
        url=self.url, slug=self.slug, status=self.status, object=self.object,
        audit=self.audit, recipients=self.recipients, verified=self.verified,
        updated_at=self.updated_at,
        custom_attribute_definitions=self.custom_attribute_definitions,
        custom_attribute_values=self.custom_attribute_values)

  def __eq__(self, other):
    return (isinstance(other, self.__class__) and self.type == other.type and
            self.title == other.title and self.slug == other.slug and
            self.status == other.status and
            self.verified == other.verified)


class IssueEntity(Entity):
  """Class that represent model for Issue."""
  # pylint: disable=too-many-instance-attributes
  __hash__ = None

  def __init__(self, slug=None, status=None, audit=None, owners=None,
               contact=None, secondary_contact=None, updated_at=None,
               custom_attribute_definitions=None,
               custom_attribute_values=None):
    super(IssueEntity, self).__init__()
    self.slug = slug  # code
    self.status = status  # state
    self.audit = audit
    self.owners = owners
    self.contact = contact  # primary contact
    self.secondary_contact = secondary_contact
    self.updated_at = updated_at  # last updated
    self.custom_attribute_definitions = custom_attribute_definitions
    self.custom_attribute_values = custom_attribute_values

  def __repr__(self):
    return ("type: {type}, id: {id}, title: {title}, href: {href}, "
            "url: {url}, slug: {slug}, status: {status}, audit: {audit}, "
            "owners: {owners}, contact: {contact}, "
            "secondary_contact: {secondary_contact}, "
            "updated_at: {updated_at}, "
            "custom_attribute_definitions: {custom_attribute_definitions}, "
            "custom_attribute_values: {custom_attribute_values}").format(
        type=self.type, title=self.title, id=self.id, href=self.href,
        url=self.url, slug=self.slug, status=self.status, audit=self.audit,
        owners=self.owners, contact=self.contact,
        secondary_contact=self.secondary_contact, updated_at=self.updated_at,
        custom_attribute_definitions=self.custom_attribute_definitions,
        custom_attribute_values=self.custom_attribute_values)

  def __eq__(self, other):
    return (isinstance(other, self.__class__) and self.type == other.type and
            self.title == other.title and self.slug == other.slug and
            self.status == other.status and
            (self.owners == other.owners or
            other.owners in [owner.values() for owner in self.owners][0]))
