WARNING:
=======
If you have hooks configured on your local machine, please back them up.
These instructions will delete them by deleting the .git/hooks directory.

INSTRUCTIONS:
=======
Run this on your local machine to enable the hooks:

cd ggrc-core; rm -rf .git/hooks; ln -s ../git_hooks .git/hooks