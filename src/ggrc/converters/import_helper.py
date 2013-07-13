import csv
import os
import tempfile
import io

def handle_csv_import(converter_class, filepath, **options):
  rows = []
  csv_file = filepath
  if isinstance(filepath, basestring):
    csv_file = open(filepath,'rbU')

  csv_reader = unicode_csv_reader(csv_file.read().splitlines(True))
  rows = [row for row in csv_reader]
  csv_file.close()
  converter = converter_class.from_rows(rows, **options)
  return converter.do_import(options.get('dry_run', True))

def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
  csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
  for row in csv_reader:
    yield [unicode(cell, 'utf-8') for cell in row]

def utf_8_encoder(unicode_csv_data):
  for line in unicode_csv_data:
    yield line.encode('utf-8')


