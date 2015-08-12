# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: urban@reciprocitylabs.com
# Maintained By: urban@reciprocitylabs.com

"""repurpose type/means and kind/nature option fields for controls

Revision ID: 3046ce611147
Revises: 49b2ecde7ad0
Create Date: 2015-08-12 13:23:53.357325

"""

# revision identifiers, used by Alembic.
revision = '3046ce611147'
down_revision = '49b2ecde7ad0'

from alembic import op
import sqlalchemy as sa

# Migration for Kind/Nature
# Reactive -> Empty
# Preventative -> Preventative
# Detective -> Detective
# Administrative -> Empty
#
# SHOULD BE:
# Preventative
# Detective
# Corrective

###############################################################################

# Migration for Types/ Means
# Manual - Segregation of duties -> Empty
# Manual -> Empty
# IT-IT-Supported ITGC -> Empty
# IT-Automated ITGC -> Empty
# FIN - Manual -> Empty
# FIN - IT-Supported Manual -> Empty
# FIN - Application -> Empty
# Automated -> Empty
#
# SHOULD BE:
# Technical
# Administrative
# Physical

def upgrade():
    # Remove from controls kind_ids and means_ids that will be deleted from options
    op.execute("UPDATE controls SET means_id = NULL WHERE means_id IS NOT NULL;")
    op.execute("UPDATE controls SET kind_id = NULL WHERE kind_id IN (SELECT id FROM options WHERE title in ('Administrative', 'Reactive'));")

    # Delete deprecated kinds and means
    op.execute("DELETE FROM options WHERE role = 'control_kind' AND title IN ('Administrative', 'Reactive');")
    op.execute("DELETE FROM options WHERE role = 'control_means' AND title IN ( 'Automated', 'Fin - Application', 'Fin - IT-Supported Manual', 'Fin - Manual', 'IT - Automated ITGC', 'IT - IT-Supported ITGC', 'Manual', 'Manual - Segregation of Duties');")

    # Insert
    op.execute("INSERT INTO options (role, title) VALUES('control_kind', 'Corrective');")
    op.execute("INSERT INTO options (role, title) VALUES('control_means', 'Technical');")
    op.execute("INSERT INTO options (role, title) VALUES('control_means', 'Administrative');")
    op.execute("INSERT INTO options (role, title) VALUES('control_means', 'Physical');")


def downgrade():
    # Remove from controls kind_ids and means_ids that will be deleted from options
    op.execute("UPDATE controls SET means_id = NULL WHERE means_id IS NOT NULL;")
    op.execute("UPDATE controls SET kind_id = NULL WHERE kind_id IN (SELECT id FROM options WHERE title in ('Corrective'));")

    # Delete deprecated kinds and means
    op.execute("DELETE FROM options WHERE role = 'control_kind' AND title IN ('Corrective');")
    op.execute("DELETE FROM options WHERE role = 'control_means' AND title IN ('Technical', 'Administrative', 'Physical');")

    # Insert
    op.execute("INSERT INTO options (role, title) VALUES('control_kind', 'Administrative');")
    op.execute("INSERT INTO options (role, title) VALUES('control_kind', 'Reactive');")

    op.execute("INSERT INTO options (role, title) VALUES('control_means', 'Automated');")
    op.execute("INSERT INTO options (role, title) VALUES('control_means', 'Fin - Application');")
    op.execute("INSERT INTO options (role, title) VALUES('control_means', 'Fin - IT-Supported Manual');")
    op.execute("INSERT INTO options (role, title) VALUES('control_means', 'Fin - Manual');")
    op.execute("INSERT INTO options (role, title) VALUES('control_means', 'IT - Automated ITGC');")
    op.execute("INSERT INTO options (role, title) VALUES('control_means', 'IT - IT-Supported ITGC');")
    op.execute("INSERT INTO options (role, title) VALUES('control_means', 'Manual');")
    op.execute("INSERT INTO options (role, title) VALUES('control_means', 'Manual - Segregation of Duties');")
