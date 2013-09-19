
from ggrc.models.all_models import all_models,  __all__
from .object_folder import ObjectFolder
from .object_file import ObjectFile
import sys

all_models += [ObjectFolder, ObjectFile]

__all__ += [ObjectFolder.__name__, ObjectFile.__name__]
