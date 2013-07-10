import csv

def handle_csv_import(converter_class, filepath, **options):
  rows = []
  # TODO: Handle template stuff here
  with open(filepath,'rbU') as csvfile:
    csv_reader = unicode_csv_reader(csvfile)
    rows = [row for row in csv_reader]

  converter = converter_class.from_rows(rows, **options)
  # TODO: Add preview check here. Defaulting to preview for now.
  return converter.do_import()


# This will force utf-8 encoding in order to yield appropriate data
def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
  # csv.py doesn't do Unicode; encode temporarily as UTF-8:
  csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
  for row in csv_reader:
    # ensure rows are made up of unicode strings
    yield [unicode(cell, 'utf-8') for cell in row]

def utf_8_encoder(unicode_csv_data):
  for line in unicode_csv_data:
    yield line.encode('utf-8')
