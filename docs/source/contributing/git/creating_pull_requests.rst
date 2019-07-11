Creating a pull requests
========================

0. Create and push
===================

1. Firstly you should sign in your GitHub and go to the ggrc repo. Find the "Fork" button and click it. Go on
forked ggrc in your GitHub and clone it with

..  code-block:: bash

    git clone https://github.com/<your_nickname>/ggrc-core

Git automatically set origin and upstream remote repos on your forked ggrc repo and the google/ggrc one respectively.

More you can find on official `GitHub guide <https://help.github.com/en/articles/fork-a-repo>`_.

2. Before you start work on ticket (fix issue, implement feature) you must create a branch for your solution.
More you can find on `branching management <branch_management.rst>`_.

To keep your branch updated you have to fetch new commits from upstream. Use the following commands:

..  code-block:: bash

    git fetch upstream
    git rebase upstream/<branch_to_rebase_on>

.. note::
    If you have uncommitted changes, stash them (:code:`git stash`), execute a rebase command and then pop your
    changes from stash list (:code:`git stash pop`).

Usually the branch_to_rebase_on branch is dev branch.

3. Once the solution in your branch is ready you need to update your branch again and rebase to dev branch (see
commands above).
In the end you should push your code to your repo with :code:`git push`.

1. Create pull request
======================

1. After your code pushed to your repository, you should create a pull request to merge your solution to dev
branch. Click on "New pull request" button, then choose your branch as a head branch and merged on the dev branch as a base branch.

..  note::
    When some critical issues appear in release pull request should be created to the release branch.

    Once the pull request is merged BACKMERGE pull request should be created from release to dev branch.

2. For pull request titles we should use the same rules as for the subject
line of a commit, but we need to prefix the title with one of:

- GGRC-JIRA ISSUE ID when we have one or more issues (in latter case we separate our titles with `,` or `/`)
- QUICK-FIX when there is no jira ticket for the codechange
- DOCS when for PRs that update only documentation and there is no jira ticket
- BACKMERGE for merging release or master branches back into dev
- MERGE for dev branch to release and release to master

A pull request title must also reflect on what changes have been done.
If the pull request title states that it contains test modifications, it must not contain any code changes outside of tests.
If there are logic changes in the PR, the title must reflect those and the changes in the tests are implied with the code changes.

The description itself conform to pull request `template </PULL_REQUEST_TEMPLATE.md>`_.
You need only to fill the issue, solution descriptions and steps to reproduce from JIRA ticket.


Examples::

    GGRC-9999 Fix performance issues on bulk operations
    GGRC-1111/1112/9900 Fix rbac issues for creators
    GGRC-1111,GGRC-1112 Fix rbac issues for editors
    QUICK-FIX Break test cases into smaller parts
    DOCS Add section that explains client side mappings
    BACKMERGE master into Release/xyz
    BACKMERGE Release/xyz into dev
    MERGE dev into Release/xyz
    MERGE Release/xyz into master

Pull request adding step fully described in official `guide <https://help.github.com/en/articles/creating-a-pull-request>`_.

3. Set someone from your team as pull request assignee.
Leave a reviewer field empty.

4. Once review and kokoro tests passed pull request can be merged to the base branch.
More on how to review a pull request you can find `here <reviewing_pull_requests.rst>`_.