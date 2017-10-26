from ggrc import app, db, models
from ggrc.utils import object_cleaner
object_cleaner.clean_all_orphan_entries()
