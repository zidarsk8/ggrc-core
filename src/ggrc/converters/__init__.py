from .sections import SectionsConverter

all_converters = [
    ('sections', SectionsConverter)
    ]

def get_converter(name):
  return all_converters(name)
