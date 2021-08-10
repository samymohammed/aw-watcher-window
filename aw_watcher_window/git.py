import os
import subprocess

def get_path_from_title(title):
    """Get path given title."""
    titleparts = title.replace("*", "").split(" - ")
    if not os.path.exists(titleparts[0]):
        return "unknown"
    elif os.path.isfile(titleparts[0]):
        return titleparts[0]
    elif len(titleparts) > 1 and os.path.isfile(os.path.join(titleparts[0], titleparts[1])):
        return os.path.join(titleparts[0], titleparts[1])
    elif os.path.isdir(titleparts[0]) and len(titleparts) > 1:
        with os.scandir(titleparts[0]) as it:
            for entry in it:
                if entry.is_dir() and os.path.isfile(os.path.join(entry.path, titleparts[1])):
                    return os.path.join(entry.path, titleparts[1])
        return titleparts[0]
    elif os.path.isdir(titleparts[0]):
        return titleparts[0]

    return "unknown"

def get_repo_from_path(path):
    """Get git repo from path."""
    if path == "unknown":
        return "unknown"
    repo = subprocess.run("git -C " + (os.path.dirname(path) if os.path.isfile(path) else path) + " remote get-url origin", capture_output=True).stdout
    return repo.decode("utf-8").replace("\\n", "")

def get_branch_from_path(path):
    """Get git branch from path."""
    if path == "unknown":
        return "unknown"
    branch = subprocess.run("git -C " + (os.path.dirname(path) if os.path.isfile(path) else path) + " branch --show-current", capture_output=True).stdout
    return branch.decode("utf-8").replace("\\n","")
