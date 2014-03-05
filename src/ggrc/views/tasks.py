import json

from flask import flash, render_template

from ggrc.app import app
from ggrc.converters.common import ImportException
from ggrc.converters.import_helper import handle_csv_import, handle_converter_csv_export
from ggrc.models.task import queued_task, make_task_response


# Needs to be secured as we are removing @login_required
@app.route("/tasks/reindex", methods=["POST"])
@queued_task
def reindex(task):
  """
  Web hook to update the full text search index
  """

  from ggrc.fulltext import get_indexer
  from ggrc.fulltext.recordbuilder import fts_record_for, model_is_indexed

  indexer = get_indexer()
  indexer.delete_all_records(False)

  from ggrc.models import all_models
  from ggrc.app import db

  # Find all models then remove base classes
  #   (If we don't remove base classes, we get duplicates in the index.)
  inheritance_base_models = [
      all_models.Directive, all_models.SystemOrProcess, all_models.Response
      ]
  models = set(all_models.all_models) - set(inheritance_base_models)
  models = [model for model in models if model_is_indexed(model)]

  for model in models:
    mapper_class = model._sa_class_manager.mapper.base_mapper.class_
    query = model.query.options(
        db.undefer_group(mapper_class.__name__ + '_complete'),
        )
    for query_chunk in generate_query_chunks(query):
      for instance in query_chunk:
        indexer.create_record(fts_record_for(instance), False)
      db.session.commit()

  return app.make_response((
    'success', 200, [('Content-Type', 'text/html')]))

def import_redirect(location):
  # The textarea here is a custom response for 'remoteipart' to
  # proxy a JSON response through an iframe.
  return app.make_response((
    '<textarea data-type="application/json" response-code="200">{0}</textarea>'.format(
      json.dumps({ 'location': location })), 200, [('Content-Type', 'text/html')]))

@app.route("/tasks/import_people", methods=['POST'])
@queued_task
def import_people_task(task):
  from ggrc.converters.people import PeopleConverter
  from ggrc.models import Person

  csv_file = task.parameters.get("csv_file")
  dry_run = task.parameters.get("dry_run")
  try:
    options = {}
    options['dry_run'] = dry_run
    converter = handle_csv_import(PeopleConverter, csv_file.splitlines(True), **options)
    if dry_run:
      options['converter'] = converter
      options['results'] = converter.objects
      options['heading_map'] = converter.object_map
      return render_template("people/import_result.haml", **options)
    else:
      count = len(converter.objects)
      return import_redirect("/admin/people_redirect/{}".format(count))

  except ImportException as e:
    if e.show_preview:
      converter = e.converter
      return render_template("people/import_result.haml", exception_message=e,
          converter=converter, results=converter.objects, heading_map=converter.object_map)
    return render_template("directives/import_errors.haml",
          directive_id="People", exception_message=str(e))
    
@app.route("/tasks/import_help", methods=['POST'])
@queued_task
def import_help_task(task):
  from ggrc.converters.help import HelpConverter
  from ggrc.models import Help

  csv_file = task.parameters.get("csv_file")
  dry_run = task.parameters.get("dry_run")
  try:
    options = {}
    options['dry_run'] = dry_run
    converter = handle_csv_import(HelpConverter, csv_file.splitlines(True), **options)
    if dry_run:
      options['converter'] = converter
      options['results'] = converter.objects
      options['heading_map'] = converter.object_map
      return render_template("help/import_result.haml", **options)
    else:
      count = len(converter.objects)
      return import_redirect("/admin/help_redirect/{}".format(count))

  except ImportException as e:
    if e.show_preview:
      converter = e.converter
      return render_template("help/import_result.haml", exception_message=e,
          converter=converter, results=converter.objects, heading_map=converter.object_map)
    return render_template("directives/import_errors.haml",
          directive_id="Help", exception_message=str(e))

@app.route("/task/import_objective_directive", methods=['POST'])
@queued_task
def import_objective_directive_task(task):
  from ggrc.converters.objectives import ObjectivesConverter
  from ggrc.models import Directive
  from ggrc.utils import view_url_for

  csv_file = task.parameters.get("csv_file")
  dry_run = task.parameters.get("dry_run")
  directive_id = task.parameters.get("parent_id")
  directive = Directive.query.get(directive_id)
  directive_url = view_url_for(directive)
  return_to = task.parameters.get("return_to") or directive_url
  
  try:
    converter = handle_csv_import(ObjectivesConverter, csv_file.splitlines(True), **task.parameters)
    if dry_run:
      options = {
          'converter': converter,
          'results': converter.objects,
          'heading_map': converter.object_map,
      }
      return render_template("directives/import_objectives_result.haml", **options)
    else:
      count = len(converter.objects)
      flash(u'Successfully imported {} objective{}'.format(count, 's' if count > 1 else ''), 'notice')
      return import_redirect(return_to)
  except ImportException as e:
    if e.show_preview:
      converter = e.converter
      return render_template("directives/import_objectives_result.haml",
          exception_message=e, converter=converter, results=converter.objects,
          directive_id=directive_id, heading_map=converter.object_map)
    return render_template("directives/import_errors.haml",
        directive_id=directive_id, exception_message=str(e))

  return render_template("directives/import.haml", directive_id=directive_id, import_kind='Objectives', return_to=return_to, parent_type=(directive.kind or directive.meta_kind))

@app.route('/task/import_control_directive', methods=['POST'])
@queued_task
def import_control_directive_task(task):
  from ggrc.converters.controls import ControlsConverter
  from ggrc.models import Directive
  from ggrc.utils import view_url_for

  csv_file = task.parameters.get("csv_file")
  dry_run = task.parameters.get("dry_run")
  directive_id = task.parameters.get("parent_id")
  directive = Directive.query.get(directive_id)
  directive_url = view_url_for(directive)
  return_to = task.parameters.get("return_to") or directive_url
  try:
    converter = handle_csv_import(ControlsConverter, csv_file.splitlines(True), **task.parameters)
    if dry_run:
      options = {
          'converter': converter,
          'results': converter.objects,
          'heading_map': converter.object_map,
      }
      return render_template("directives/import_controls_result.haml", **options)
    else:
      count = len(converter.objects)
      flash(u'Successfully imported {} control{}'.format(count, 's' if count > 1 else ''), 'notice')
      return import_redirect(return_to)
  except ImportException as e:
    if e.show_preview:
      converter = e.converter
      return render_template("directives/import_controls_result.haml",
          exception_message=e, converter=converter, results=converter.objects,
          directive_id=directive_id, heading_map=converter.object_map)
    return render_template("directives/import_errors.haml",
       directive_id=directive_id, exception_message=str(e))

@app.route("/task/import_control_program", methods=['POST'])
@queued_task
def import_control_program_task(task):
  from ggrc.converters.controls import ControlsConverter
  from ggrc.models import Program
  from ggrc.utils import view_url_for

  csv_file = task.parameters.get("csv_file")
  dry_run = task.parameters.get("dry_run")
  program_id = task.parameters.get("parent_id")
  program = Program.query.get(program_id)
  program_url = view_url_for(program)
  return_to = task.parameters.get("return_to") or program_url

  try:
    converter = handle_csv_import(ControlsConverter, csv_file.splitlines(True), **task.parameters)
    if dry_run:
      options = {
          'converter': converter,
          'results': converter.objects,
          'heading_map': converter.object_map,
      }
      return render_template("programs/import_controls_result.haml", **options)
    else:
      count = len(converter.objects)
      flash(u'Successfully imported {} control{}'.format(count, 's' if count > 1 else ''), 'notice')
      return import_redirect(return_to)

  except ImportException as e:
    if e.show_preview:
      converter = e.converter
      return render_template("programs/import_controls_result.haml",
          exception_message=e, converter=converter, results=converter.objects,
          program_id=program.id, heading_map=converter.object_map)
    return render_template("programs/import_errors.haml",
        program_id=program.id, exception_message=str(e))

@app.route("/task/import_system", methods=["POST"])
@app.route("/task/import_process", methods=["POST"])
@queued_task
def import_system_task(task):
  from ggrc.converters.systems import SystemsConverter

  kind_lookup = {"systems": "System(s)", "processes": "Process(es)"}
  csv_file = task.parameters.get("csv_file")
  object_kind = task.parameters.get("object_kind")
  dry_run = task.parameters.get("dry_run")
  options = {"dry_run": dry_run}
  if object_kind == "processes":
    options["is_biz_process"] = '1'
  try:
    converter = handle_csv_import(SystemsConverter, csv_file.splitlines(True), **options)
    if dry_run:
      return render_template("systems/import_result.haml", converter=converter, results=converter.objects, heading_map=converter.object_map)
    else:
      count = len(converter.objects)
      flash(u'Successfully imported {} {}'.format(count, kind_lookup[object_kind]), 'notice')
      return import_redirect("/admin")

  except ImportException as e:
    if e.show_preview:
      converter = e.converter
      return render_template("systems/import_result.haml", exception_message=e, converter=converter, results=converter.objects, heading_map=converter.object_map)
    return render_template("directives/import_errors.haml", exception_message=e)

@app.route("/tasks/export_people", methods=['POST'])
@queued_task
def export_people_task(task):
  from ggrc.converters.people import PeopleConverter
  from ggrc.models.all_models import Person
  options = {}
  options['export'] = True
  people = Person.query.all()
  filename = "PEOPLE.csv"
  return handle_converter_csv_export(filename, people, PeopleConverter, **options)

@app.route("/tasks/export_help", methods=['POST'])
@queued_task
def export_help_task(task):
  from ggrc.converters.help import HelpConverter
  from ggrc.models.all_models import Help
  options = {}
  options['export'] = True
  people = Help.query.all()
  filename = "HELP.csv"
  return handle_converter_csv_export(filename, people, HelpConverter, **options)

@app.route("/tasks/export_process", methods=['POST'])
@queued_task
def export_process_task(task):
  from ggrc.converters.systems import SystemsConverter
  from ggrc.converters.import_helper import handle_converter_csv_export
  from ggrc.models.all_models import Process

  options = {}
  options['export'] = True
  options['is_biz_process'] = '1'
  procs = Process.query.all()
  filename = "PROCESSES.csv"
  return handle_converter_csv_export(filename, procs, SystemsConverter, **options)

@app.route("/tasks/export_system", methods=['POST'])
@queued_task
def export_system_task(task):
  from ggrc.converters.systems import SystemsConverter
  from ggrc.converters.import_helper import handle_converter_csv_export
  from ggrc.models.all_models import System

  options = {}
  options['export'] = True
  systems = System.query.filter_by(is_biz_process=False).all()
  filename = "SYSTEMS.csv"
  return handle_converter_csv_export(filename, systems, SystemsConverter, **options)

