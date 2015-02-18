
# make sure you're up to date

cd to/your/clone
git stash
git checkout develop 
git fetch origin 
git rebase origin/develop 

# test should be done on the merged branch.
# if the merge is not a FF, it can break a few things

git checkout -b temp_branch 
git merge origin/feature/CORE-1195 

# no need if you already have it running
vagrant up

# run this if there were any changes in the provision/ foder
vagrant provision

vagrant ssh
#### inside the vagrant machine ####
git checkout developy_appengine extras/deploy_settings_local.sh
launch_ggrc

# test in the incognito mode. Chrome: ctrl+shift+n
# Note that you have to close all current incognito browsers to get a clean sesion.
####
git checkout develop 
git branch -D temp_branch

# go back to your branch and contiue with your work
git checkout my/previous-branch
git stash pop

