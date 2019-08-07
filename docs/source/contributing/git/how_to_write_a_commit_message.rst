How to Write a Commit Message
=============================

This is all shamelessly based on
`chris.beams.io <http://chris.beams.io/posts/git-commit/>`_.

1. Separate subject from body with a blank line
2. Limit the subject line to 50 characters
3. Capitalize the subject line
4. Do not end the subject line with a period
5. Use the imperative mood in the subject line (spoken or written as if
   giving a command or instruction)
6. Wrap the body at 72 characters
7. Use the body to explain what and why vs. how

A properly formed git commit subject line should always be able to
complete the following sentence:

**If applied, this commit will *your subject line here***

Good: If applied, this commit will **refactor subsystem X for
readability**

Bad: If applied, this commit will **fixes for broken stuff**

Commit message should be summary line and description of what you have
done in the imperative mode, that is as if you were commanding someone.
Write "fix", "add", "change" instead of "fixed", "added", "changed".

Examples
--------

Bad
~~~

1. Fixed bug with {something}.
2. changing behavior of {something}
3. more fixes for broken stuff
4. sweet new API methods
5. Removing stuff

Good
~~~~

1. Fix bug when {something_else} doesn't exist
2. Change behavior of {something} to do {behavior_x}
3. [don't do this, fix one specific thing in a commit]
4. Add {method_a}, {method_b} and {method_c} methods to API
5. Remove unused {method_a}, {method_b}...

Commit content
~~~~~~~~~~~~~~

The commit message must also reflect the commit content. If a commit has to 
describe too many things, then that commit should be split into smaller logical
parts.

A few cases when commits must be split in order to improve readability:

1. When moving code around, unless it is just a few lines of code there should
   always be split commits for moving the code, and changing the moved code to
   work from the new location.
2. When refactoring any code that is obsolete should be removed in a separate
   commit unless it is trivial to see that the code is not used anywhere else.
3. When adding new functionality that affects a broader codebase not just local
   functions, such code should be in its own commit with a clear description as
   per commit message guidelines.

Merge commits
~~~~~~~~~~~~~

1. Merge commits can retain the default title and content.

2. If there are conflicts in a merge commit, it is recommended that we list the
   conflicting files at the end of the merge commit message. Git generates the
   list by default, and we should just uncomment it. Example:


    Merge branch 'master' into 'dev'

    Conflicts:
            src/ggrc/settings/default.py




Before Issuing a New Pull Request
---------------------------------

While every pull request is automatically checked on a continuous
integration server, it is better to catch issues early, resulting in
less broken builds and reduced time before the PR is merged. You should
thus run a few tests locally before submitting the PR for a review.

It is OK to defer some of the checks if they take too much time to be
feasible to run them locally (as a rule of thumb: 10+ minutes). These
checks can be deferred until the CI server runs them.

You are still encouraged to run them yourself, though, if you can afford
the waiting, e.g. just before taking a longer break (lunch, meeting...).


Checking the front-end code
---------------------------

Code style checks
~~~~~~~~~~~~~~~~~

The `ESLint <http://eslint.org/>`_ tool is used for checking the
Javascript code quality. You must assure that your pull request does not
have ESLint issues found.

To check the code quality of a particular file, run the following in the
development container's console:

..  code-block:: bash

    eslint path/to/some/file.js

You will see a list of all issues found and the corresponding line
numbers. Sample output::

    ...
    105:23  error    Strings must use singlequote                         quotes
    112:7   warning  Identifier name 'fooBaa...ar' is too long. (> 25)    id-length
    112:48  error    Missing space before function parentheses            space-before-function-paren
    114:23  error    Strings must use singlequote                         quotes
    120:3   error    Split 'var' declarations into multiple statements    one-var
    ...

    ✖ 74 problems (73 errors, 1 warning)

You need to resolve all the issues in the line(s) you have
modified.

When you submit a new pull request, a script will check how many
Javascript code issues there are on the PR branch.

If there are any issue found, the check will fail, because
new code should not introduce Javascript issues. To avoid
that and preemptively perform the same check locally, do the following:

-   Make sure that you are currently on a branch containing the changes
    that will be submitted with the pull request (the PR branch), and
    that you have these changes committed,
-   Make sure that you don't have any pending local file modifications.
    Use ``git stash`` if necessary,
-   Run the following in the development container's console:

    ..  code-block:: bash

        check_eslint

Running the tests
~~~~~~~~~~~~~~~~~

Run the following in the development container's console:

..  code-block:: bash

    run_karma

When the Karma server (a Javascript test runner) starts, open
``http://localhost:9876/`` in a browser. The browser will connect to the
Karma server and run all Javascript unit tests. The outcome of the tests
will be printed to the console, make sure they all pass.

*NOTE: The officially supported browser by the application is Chrome. It
is thus strongly recommended that you, too, use Chrome for running the
tests locally.*


Checking the back-end code
--------------------------

Code style checks
~~~~~~~~~~~~~~~~~

At the moment, no automatic Python coding style checks are performed -
yet. You should nevertheless make your best effort to write `PEP8
compliant <https://www.python.org/dev/peps/pep-0008/>`_ code to make it
more future compatible for when such automatic checks are introduced and
enforced.

Running the tests
~~~~~~~~~~~~~~~~~

To run the Python unit and integration tests, run the following in the
development container's console:

..  code-block:: bash

    run_pytests

*NOTE: Python integration tests take a while to run, around 20 minutes
(give or take) on a decent laptop.*


End-to-end tests
----------------

To run the full-fledged end-to-end system tests, go to the project root
directory **on the host machine** and run the following from its
console:

..  code-block:: bash

    ./bin/jenkins/run_selenium

Please keep in mind that, for various technical reasons, Selenium tests
**should not** be run from inside a container!

*NOTE: These tests only work with Docker-based development environments,
since they require Docker prerequisites to be installed on the host
machine. Vagrant is not supported.*
