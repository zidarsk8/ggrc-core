## Simple helper/guide for reviewing pull requests

_Note: some steps may be ommited depending on your setup, if you're not sure, just run it all._

1. make sure you're up to date

```
cd to/your/ggrc/clone 
git stash
git checkout develop 
git fetch origin 
git rebase origin/develop 
```

2.  test should be done on the merged branch.
_Note: if the merge is not a fast-forward, it could break a few things._

```
git checkout -b temp_branch 
git merge origin/feature/CORE-1195 
```

3. Start your dev env. No need if you already have it running
```
vagrant up

# run this if there were any changes in the provision/ foder
vagrant provision 

vagrant ssh
```

4. Lauch the app
```
git checkout developy_appengine extras/deploy_settings_local.sh
launch_ggrc
```

5. test in the incognito mode. Chrome: ctrl+shift+n
_Note: that you have to close all current incognito browsers to get a clean sesion._
```
git checkout develop 
git branch -D temp_branch
```

6. Go back to your branch and contiue with your work
```
git checkout my/previous-branch
git stash pop
```

