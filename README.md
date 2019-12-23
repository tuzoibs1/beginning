# beginning
Hi everyone!

I'm new to GitHub, I'm looking to learn as much as I can..


git -v

git init
git add
git commit -m ""
git push origin branchName
git checkout nwbranchName 

// if modified you need to save branch and commit before checking 
git reset HEAD --hard id //after push to reset code

git config credential.helper store
vi test.txt

//delete folders or files in github. In the command-line, navigate to your local repository.
//Ensure you are in the default branch:
    git checkout master
//The rm -r command will recursively remove your folder:
    git rm -r folder-name
//Commit the change:
    git commit -m "Remove duplicated directory"
//Push the change to your remote repository:
    git push origin master

// add new remote to git repo
git remote add origin url
git remote -v

//Change Branch 
git branch //figure out which branch your in.
git branch name-branch //if  you wanted to create a new branch
git checkout name-branch //to check in to new branch
git checkout master // change to master 
git merge branch-name //merge code to master

//fix for Git refusing to merge unrelated histories on rebase
git pull origin branchname --allow-unrelated-histories
git merge master


///delete git log history 
Checkout

    git checkout --orphan latest_branch

//Add all the files

    git add -A

//Commit the changes

    git commit -am "commit message"

//Delete the branch

    git branch -D master

//Rename the current branch to master

    git branch -m master

//Finally, force update your repository

    git push -f origin master

//force a push update, if reject a push
   git push -f origin master

