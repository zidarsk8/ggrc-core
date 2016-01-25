<a name="top"></a>
# A simple helper/guide for reviewing pull requests

This guide consists of two parts:
* **Part 1:** Instructions on how to properly set up (and tear down) the local
    environment for testing the pull request -
    [link to Part 1](#setting-up-and-tearing-down-the-environment-for-pr-testing).
* **Part 2**: Instructions on how to actually review a pull request -
    [link to Part 2](#how-to-properly-review-a-pull-request).


## Setting up (and tearing down) the environment for PR testing

_NOTE: Before doing anything else, if you are reviewing a bugfix pull request,
you must first reproduce the issue on the main development branch as described
in [Part 2](#reviewing-a-bugfix-pr)._

_NOTE: Depending on your setup, some of the following steps may be omitted. If
you are not sure, just run them all._

1. Make sure your local files are up to date:

    ```console
    cd to/your/ggrc/clone
    git stash
    git checkout develop
    git fetch <remote_main>
    git rebase <remote_main>/develop
    ```

    Here `<remote_main>` stands for the name of the _remote_ representing the
    main development repository, i.e. the one the pull requests are sent to.
    Such a remote is commonly named `upstream`.

1. Test should be done on the merged branch:

    _NOTE: The merge must be a fast-forward, since all pull requests are merged
    with the `--no-ff` flag._

    ```console
    git checkout -b temp_branch
    git fetch <pr_origin>
    git merge --no-ff <pr_origin>/<feature_branch_name>
    ```

    Here `<pr_origin>` stands for the name of the _remote_ the pull request
    is originating from. This is most often a fork of the `<remote_main>` by
    one of the fellow developers on the project.

    `<feature_branch_name>` must of course be replaced with the actual name of
    the remote branch containing the changes, e.g. `feature/CORE-1234`.

    If you don't yet have the `<pr_origin>` defined, you need to add it
    ([instructions](https://git-scm.com/book/en/v2/Git-Basics-Working-with-Remotes#Adding-Remote-Repositories)).

1. Start your local development environment (Vagrant or Docker). No need if you
already have it running.

    ##### If using Vagrant

    ```console
    vagrant up

    # run the following if there were any changes in the provisioning files,
    # requirements, dev-requirements, or npm requirements...
    vagrant provision

    vagrant ssh
    ```

    ##### If using Docker

    ```console
    # TODO: write Docker commands
    ```

1. (optional) Run the database migration

    If the pull request is marked with the `migration` label, it modifies the
    database schema, and you thus need to update the schema locally as well.

    First, backup the current development database by running the following in
    the development container's console (you will be prompted for the database
    root password):

    ```console
    mysqldump ggrcdev -u root -p > db_backup.sql
    ```

    With the backup successfully created, run the actual database migration:

    ```console
    db_migrate
    ```

    _NOTE: Database migration must be run from the latest database state on
    the main `develop` branch. If your topic branch introduced any DB changes,
    they must first be reverted before running the migration._

1. Rebuild all asset files and launch the application:

    ```console
    deploy_appengine extras/deploy_settings_local.sh
    launch_ggrc
    ```

1. Test the application in incognito mode.

    _HINT: For incognito mode in Chrome press
    <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>n</kbd>
    (or <kbd>⌘Cmd</kbd>+<kbd>Shift</kbd>+<kbd>n</kbd> on Mac)_

    _NOTE: You have to close all current incognito browsers to get a clean
    session._

    Test the pull request as decribed in
    [Part 2](#how-to-properly-review-a-pull-request) of this guide.

1. Go back to your branch and continue with your work:

    After you have finished verifying the pull request, you can remove the
    temporary branch that was used for testing it:

    ```console
    git checkout develop
    git branch -D temp_branch
    ```

    ```console
    git checkout my/previous-branch
    git stash pop  # only needed if you had any changes stashed in Step 1
    ```

    If you tested a `migration` pull request, you should also revert the
    database to its previous state by running the following from the
    development container's console:
    ```console
    mysql -u root -p ggrcdev < db_backup.sql
    ```

#### Tip: Automatically checking out a pull request by its ID

If you feel that manually fetching and merging a pull request branch is too
tedious, you can add the following convenient git alias to your `.gitconfig`
file (e.g. the one located in your home directory):

```ini
[alias]
  pr = "!f() { \
    git checkout develop; \
    git branch -D pr-$1; \
    git fetch upstream develop:pr-$1; \
    git checkout pr-$1; \
    git fetch upstream pull/$1/head; \
    git merge --no-ff FETCH_HEAD -m \"Automatic merge\"; \
  }; f"
```

_NOTE: The alias assumes that the _remote_ representing the main development
repository is referred to as `upstream`. This is a common convention, but if
your local configuration uses a different name, you must replace the two
appearances of the word `upstream` in the alias with that name._

With this alias defined, you can now simply type the following:

```
git pr 5678
```

This command will automatically fetch and checkout the branch containing the
changes in the pull request 5678.

\[[Back to top](#top)\]


## How to properly review a pull request

First of all, make sure that you have properly set up the local environment as
described in
[Part 1](#setting-up-and-tearing-down-the-environment-for-pr-testing). Then
follow the guidelines described in the following sections.

#### Reviewing a new feature PR

The philosophy is simple - verify that the PR implements everything that is
required by the corresponding project task / specification. While reviewing, it
is highly recommended that you also test a few other application features
that might have been affected by the submitted code changes.

#### Reviewing a bugfix PR

If reviewing a pull request that contains a bug fix, you **must** first
reproduce the bug on the vanilla `develop` branch, i.e. the one without the PR
branch merged. Only after the bug has been reproduced, you can actually verify
that the PR indeed fixes something.

Again, try to also check that the bugfix has not accidentally introduced any
other issues.

#### Reviewing a PR containing database migration scripts

Pull requests that modify the database (marked with the `migration` label)
require additional checks to be performed on top of all the others regular
checks, namely the following:

* The migration works from a clean database,
* Downgrading and upgrading work on a clean database,
* Migrations work from the current database state on the main `develop` branch,
* Migrations work on a populated database (using the data from the `grc-dev`
  instance).


#### Acceptance criteria

A pull request **must be rejected** if **any** of the following is true:

* It does not do/fix what it claims to and/or it does that only partially,
* The review reveals that the PR has introduced new issues,
* At least one of the automatic checks on the continuous integration server
  fails, i.e. the build is broken,
* The new code contains severe readability, logical and/or architectural
  issues,
* The new code is not sufficiently covered with automated tests (subject to
  exceptions, e.g. when a test would be disproportionally difficult and
  time-consuiming to write, or for little UI changes like changing an icon or a
  font color).

The reviewer must mark the pull request with the `needs work` label, signalling
to the author that the PR cannot yet been merged as-is, and additional changes
are required. Along with the tagging, the reviewer should clearly explain why
the PR has temporarily been rejected, and what needs to be done before it can
be merged.

On the other hand, if the PR looks good to merge, the reviewer expresses this
by giving a thumb-up icon in a comment (:+1:). For this reason, the thumb-up
icon _should not_ be used in other comments, as it might give a false
impression that the pull request has been verified and confirmed.

#### Using GitHub labels

There are several labels defined on the GitHub project repository page that can
(and should!) be used for tagging pull requests. Labeling enables easier PR
categorization and searching, thus make sure to use them.

The meaning of the lables and their intended usage is as follows (sorted
alphabetically):

* `documentation` - a PR contains the updates of project documentation,
* `migration` - a PR contains a migration script that changes the database
  schema. Such pull requests require additional setup and verification steps,
* `needs work` - a reviewer has concluded that the PR requires additional work
  before it can be accepted and merged,
* `next release` - the PR will be merged after the next release and should not
  be merged in the current release cycle,
* `please review` - the author asked that the PR should be reviewed with a
  higher pripority. This label is usually used when the PR has not received
  enough attention for a considerable time period, or because it is important
  and attempts to resolve an important/blocking issue,
* `question` - a reviewer requires additional explanation from the PR author
  before a decision can be made on whether the PR meets all the requirements.
  Occasionally, this label is also used when a reviewer makes a non-essential
  suggestion for a PR change, but that change is not required to deem the PR
  ready to merge,
* `wrong branch` - the author sent the PR to the wrong branch. The author
  should re-issue the same PR against the correct branch.


\[[Back to top](#top)\]
