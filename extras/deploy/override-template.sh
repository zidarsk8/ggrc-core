#!/usr/bin/env bash

export GGRC_DATABASE_URI='mysql+mysqldb://db-user:password@127.0.0.1/db_name?charset=utf8'
export GGRC_SETTINGS_MODULE="app_engine ggrc_basic_permissions.settings.development ggrc_risks.settings.development ggrc_risk_assessments.settings.development ggrc_workflows.settings.development ggrc_gdrive_integration.settings.development"
