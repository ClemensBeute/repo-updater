# updates all hg repositorys in a given directory
import os, sys, subprocess
from pathlib import Path
import importlib
# install python-git if missing
try:
    from pygit2 import Repository
except ImportError:
    print("Trying to Install required module: git (pip install python-git)")
    os.system(f'{sys.executable} -m pip install pygit2')
from pygit2 import Repository
# install click
try:
    import click
except ImportError:
    print("Trying to Install required module: click (pip install click)")
    os.system(f'{sys.executable} -m pip install click')
import click

conf = str(sys.argv[1])
upload = int(sys.argv[2])
config = importlib.import_module(conf)

for repo in config.repositories_directories:
    if not repo.exists():
        print("Hello")
        continue
    # only check directories
    print("Check all repositories in ", repo, "\n")
    for r in repo.rglob('**/'):
        # HG
        if r.name == ".hg":
            repository = r.parent
            print()
            print("HG: ", repository.parent.name)
            os.chdir(repository)
            if upload == 1:
                pipe = subprocess.Popen(['hg', 'st'], stdout=subprocess.PIPE)
                output = pipe.stdout.read()
                output = str(output)[2:-3].split("\\n")
                for x in output:
                    print(x)
                for x in output:
                    if any(x.startswith(y) for y in ["!", "?", "M", "A", "R"]):
                        prompt = click.prompt(
                            'c = commit and push? (addremoves automaticly) | r = revert changes and purge  | n = do nothing',
                            type=str
                        )
                        if prompt == "c":
                            os.system("hg addremove")
                            message = click.prompt('commit message', type=str)
                            os.system(f'hg ci -m "{message}"')
                            os.system("hg push")
                        elif prompt == "r":
                            if click.confirm(f'Do you really want to revert?', default=False):
                                os.system("hg revert --all")
                                os.system("hg purge --all")
                        else:
                            pass
                        break

            else:
                os.system("hg pull")
                os.system("hg up")
        # GIT
        elif r.name == ".git":
            repository = r.parent
            print()
            print("GIT: ", repository.name)
            os.chdir(repository)
            if upload == 1:
                repo = Repository(str(repository))
                status = repo.status()
                status_values = list(status.values())
                if not(all(x == 16384 for x in status_values) or status == {}):
                    os.system("git status")
                    prompt = click.prompt(
                        'c = commit and push? (addremoves automaticly) | r = restore and clean  | n = do nothing',
                        type=str
                    )
                    if prompt == "c":
                        os.system("git add .")
                        message = click.prompt('commit message', type=str)
                        os.system(f'git commit -m "{message}"')
                        os.system("git push")
                    elif prompt == "r":
                        if click.confirm(f'Do you really want to revert?', default=False):
                            os.system("git restore .")
                            os.system("git clean -d -f")
                    else:
                        pass
            else:
                os.system("git pull")
