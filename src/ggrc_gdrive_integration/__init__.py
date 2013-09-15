from flask import Blueprint
from ggrc import settings
from ggrc.app import app

blueprint = Blueprint(
  'gdrive',
  __name__,
  template_folder='templates',
  static_folder='static',
  static_url_path='/static/ggrc_gdrive_integration',
)

for key in settings.exports:
  app.config.public_config[key] = app.config[key]

# Initialize views
import ggrc_gdrive_integration.views
