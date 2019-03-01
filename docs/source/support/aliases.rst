=======
Aliases
=======

You can create your own aliases by adding them into bash config files.

Containers aliases
------------------

Run this **outside** of docker containers:

**In commands below you need to change path to the project to the real one on your machine!**

In case you use Debian or Ubuntu:

..  code-block:: bash

    echo 'alias bcr="~/path/to/ggrc-core/bin/containers run"' >> ~/.bashrc
    echo 'alias bcc="~/path/to/ggrc-core/bin/containers connect"' >> ~/.bashrc

In case you use Mac OS:

..  code-block:: bash

    echo 'alias bcr="~/path/to/ggrc-core/bin/containers run"' >> ~/.bash_profile
    echo 'alias bcc="~/path/to/ggrc-core/bin/containers connect"' >> ~/.bash_profile

Commands above will setup two aliases: ``bcr`` and ``bcc``.

Commands differ because by default Mac OS Terminal app launches login shell.
And login shell doesn't launch ``.bashrc`` file, but instead launches ``.bash_profile``.
It's default login shell behavior in Mac OS.
That's why we write commands into ``.bash_profile`` instead of ``.bashrc``.

Now in **new** terminal window or tab you can use:

- ``bcr`` instead of ``cd ~/path/to/ggrc-core/ && bin/containers run``
- ``bcc`` instead of ``cd ~/path/to/ggrc-core/ && bin/containers connect``
