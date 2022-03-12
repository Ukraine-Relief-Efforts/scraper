# Contributing

## Setting up a Python virtual environment

We recommend you use virtual environments for Python development. You can learn more about virtual environments in
Python's official documentation: https://docs.python.org/3/library/venv.html

Now, you can install requirements

`pip install -r requirements.txt`

After this, kindly setup the pre-commit hooks. The pre-commit-hook library has been added to the requirements.txt, and
you should have access to the pre-commit cli

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
