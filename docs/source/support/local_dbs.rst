==========================
Local databases management
==========================

Create custom db
----------------

To create a custom database on local (e.g. ``ggrcdev_test``):

1) Switch to the needed git branch

2) **Inside** container, set environment variable ``GGRC_DATABASE_URI`` value:

..  code-block:: bash

    export GGRC_DATABASE_URI=mysql+mysqldb://root:root@db/ggrcdev_test?charset=utf8

3) Check that environment variable value was set:

..  code-block:: bash

    env

4) Create a new db from dump ``db_reset -d {db_name} {sql_dump_name}``

..  code-block:: bash

    db_reset -d ggrcdev_test sql_dump.sql

It will create new db "ggrcdev_test" and run migrations from current branch.

Switch between databases
------------------------

The active database is the one in ``GGRC_DATABASE_URI`` environment variable.

To switch to desired db, run following command before doing launch_ggrc:

..  code-block:: bash

    export GGRC_DATABASE_URI=mysql+mysqldb://root:root@db/ggrcdev_desired_db?charset=utf8

Alias for switching branches
----------------------------

To make an alias for ``ggrcdev_test`` database usage, run **inside** container:

..  code-block:: bash

    echo 'alias test="export GGRC_DATABASE_URI=mysql+mysqldb://root:root@db/ggrcdev_test?charset=utf8"' >> ~/.bashrc
    . ~/.bashrc

Add other aliases, e.g.:

..  code-block:: bash

    echo 'alias dev="export GGRC_DATABASE_URI=mysql+mysqldb://root:root@db/ggrcdev?charset=utf8"' >> ~/.bashrc
    . ~/.bashrc

Now you can switch between databases using commands ``test`` and ``dev`` **inside**
container.
After switching, ``launch_ggrc`` can be run.

Please note that ``launch_gae_ggrc`` is not supported for this flow.
