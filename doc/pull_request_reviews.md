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

1. (optional) Run database migration

TODO: if PR is marked as "migration"

1. Rebuild all asset files and lauch the application:

    ```console
    deploy_appengine extras/deploy_settings_local.sh
    launch_ggrc
    ```

1. Test in the application in incognito mode.

    _HINT: For incognito mode in Chrome press
    <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>n</kbd>
    (or <kbd>⌘Cmd</kbd>+<kbd>Shift</kbd>+<kbd>n</kbd> on Mac)_

    _NOTE: You have to close all current incognito browsers to get a clean
    session._

    After you have verified that everything works correctly, you can remove
    the temporary branch used for the testing:

    ```console
    git checkout develop
    git branch -D temp_branch
    ```

1. Go back to your branch and continue with your work:

    ```console
    git checkout my/previous-branch
    git stash pop  # only needed if you had any changes stashed in Step 1
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
