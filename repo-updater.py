# updates all hg repositorys in a given directory
import sys
import math

sys.dont_write_bytecode = True
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

root_update = 0
if len(sys.argv) > 3:
    root_update = int(sys.argv[3])
config = importlib.import_module(conf)


def _is_different(main_dir, check_dir):
    different = False
    main_dir_start = len(main_dir.parts)
    for entry in main_dir.glob('**/*'):
        if ".backup" in str(entry):
            continue
        p1 = check_dir.parts
        p2 = entry.parts[main_dir_start:]
        p = p1 + p2
        entry_check = Path(*p)
        # check if file exist, if not, dir is different
        if not entry_check.exists():
            print("new file*s")
            different = True
            break
        if entry.is_file() == False:
            continue
        # check if date and file size are same, otherwise dir is different
        t1 = os.stat(str(entry)).st_mtime
        t2 = os.stat(str(entry_check)).st_mtime
        time_diff = math.isclose(t1, t2, rel_tol=1)

        s1 = os.stat(str(entry)).st_size 
        s2 = os.stat(str(entry_check)).st_size
        size_diff = s1 == s2
        if time_diff and size_diff:
            continue
        else:
            print(f"TIME {t1} {t2} | SIZE {s1} {s2} | {entry}")
            different = True
            break
    return different


for repo in config.repositories_directories:
    if not repo.exists():
        print("Repo doesn't exist")
        continue
    # only check directories
    print("Check all repositories in ", repo, "\n")
    # for r in repo.rglob('**/'):
    for r in repo.rglob('**/*'):
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
                if not root_update:
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
                if not (all(x == 16384 for x in status_values) or status == {}):
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

        # .backup (simple custom backup "repo")
        elif r.name == ".backup" and not root_update:
            repository = r.parent
            print()
            print("BACKUP: ", repository.parent.name)
            # backup = importlib.import_module(str(r / ".backup"))
            backup = importlib.machinery.SourceFileLoader("backup", str(r)).load_module()

            root_path = Path(backup.root_path)
            if root_path.exists():
                if upload == 1:
                    print("")
                    if _is_different(repository, root_path) is True:
                        print("changes found!")
                        prompt = click.prompt(f'copy changes to {str(root_path)}? y/n', type=str)
                        if prompt == "y":
                            os.system(f'robocopy "{repository}" "{root_path}" /e /purge /timfix /dcopy:DAT /copy:DAT')
                else:
                    if _is_different(root_path, repository) is True:
                        print("changes found!")
                        prompt = click.prompt(f'copy changes from {root_path}? y/n', type=str)
                        if prompt == "y":
                            os.system(f'robocopy "{root_path}" "{repository}" /e /purge /timfix /dcopy:DAT /copy:DAT')
            else:
                print(f"{root_path} doesn't exist! Typo?")
