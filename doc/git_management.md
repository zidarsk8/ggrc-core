All code on https://github.com/google/ggrc-core should go through a proper
pull request procedure. There should be no direct pushes to google ggrc-core
repo. Anyone with the privilege to push to the main repo must configure their
system to prevent that, in order to avoid any "ninja commits".


This document is not a tutorial on how to use git forks and how to work with
multiple git remotes. It is only meant to help setting up your repo to prevent
pushes to google/ggrc-core.



1. create a fork on github


2. set up your repo

    1. Starting from a fresh clone:

        clone your repo

            git clone git@github.com:<nick>/ggrc-core.git


    2. Adding a remote to an existing clone

        delete the current origin remote

            git remote remove origin

        add your fork as origin

            git remote add origin git@github.com:<nick>/ggrc-core.git


3. add the upstream repo for easy fetching 

        git remote add upstream git@github.com:google/ggrc-core.git

4. prevent pushing to upstream.

        git remote set-url --push upstream git@github.com:<nick>/ggrc-core.git

        git fetch upstream

5. now make sure your develop branch is tracking the correct repo

        git checkout develop

        git checkout -b develop upstream/develop

6. to list your branches and their tracking branch run

        git branch -vv 





Extra: 

get a pull request from google/ggrc-core without adding other remotes to your
repo:

make an alias (assuming upstream is pointing to google/ggrc-core.git)

    git config alias.pr '!f() { git checkout develop; git branch -D pr-$1; git fetch upstream develop:pr-$1; git checkout pr-$1; git fetch upstream pull/$1/head; git merge FETCH_HEAD -m \"Automatic merge\"; }; f'

fetch a given pull request

    git pr 1234  # where the 1234 is a pull request number


Note: this method will fail to pull changes form the updated pull request if
the user uses force push to change any of the commits. In that case you need
to delete your local pr-1234 branch and run the ```git pr 1234``` again.

