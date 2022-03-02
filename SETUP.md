etup a basic development environment

Some contributors are new to setting up an environment, so I figured it would be a good time to write this.

Firstly, use a [virtual environment](https://docs.python.org/3/tutorial/venv.html)

`python3 -m venv venv`

The respective venv files have been safely set to be ignored in `.gitignore` for this structure, so it's safe to just create the venv in this folder (or whichever folder you want to keep your virtual environments in)

Secondly, activate the environment

`source ./venv/bin/activate`

You should now be inside the virtual environment.

Now, you can install requirements

`pip install -r requirements.txt`

After this, kindly setup the pre-commit hooks. The pre-commit-hook library has been added to the requirements.txt, and you should have access to the pre-commit cli

```
scraper git:add-precommit
(venv) ❯ pre-commit install
pre-commit installed at .git/hooks/pre-commit
```

Now, when you commit a file, `black` will automatically run as part of the pre-commit hook.

```
scraper git:add-precommit*
(venv) ❯ git commit -S --signoff -m "chore: add pre-commit-config.ymal"
[WARNING] Unstaged files detected.
[INFO] Stashing unstaged files to /home/jingkai/.cache/pre-commit/patch1646064677-74625.
[INFO] Initializing environment for https://github.com/psf/black.
[INFO] Installing environment for https://github.com/psf/black.
[INFO] Once installed this environment will be reused.
[INFO] This may take a few minutes...
black................................................(no files to check)Skipped
[INFO] Restored changes from /home/jingkai/.cache/pre-commit/patch1646064677-74625.
On branch add-precommit
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   README.md

no changes added to commit (use "git add" and/or "git commit -a")
```

