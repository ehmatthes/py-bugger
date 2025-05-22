import subprocess
import warnings

def clean_git_status(force=False):
    """
    Checks whether the current working directory is a clean Git repository.

    This function verifies that the directory is under Git version control and
    that there are NO uncommitted changes (staged, unstaged, or untracked files).
    If the `force` parameter is set to True, the check is skipped and a warning
    is issued. Skipping this check is not recommended, as it may result in
    modifying files with uncommitted changes.

    Parameters:
        force (bool): If True, bypass the Git cleanliness check and issue a warning.

    Raises:
        RuntimeError: If Git is not installed or not found in PATH.
        RuntimeError: If the current directory is not a Git repository.
        RuntimeError: If uncommitted changes are detected and `force` is False.
    """
    if force:
        warnings.warn(
            "Skipping Git cleanliness check with --force. "
            "This is not recommended, as it may overwrite uncommitted changes."
        )
        return

    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            check=True
        )

    except FileNotFoundError:
        raise RuntimeError("Git is not installed or not found in PATH.")

    except subprocess.CalledProcessError:
        raise RuntimeError("Failed to run `git status`. Are you in a Git repository?")

    if result.stdout.strip():
        raise RuntimeError(
            "Uncommitted changes found. Please commit or stash them, "
            "or use --force to proceed (not recommended)."
        )