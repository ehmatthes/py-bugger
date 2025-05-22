import subprocess
import tempfile
import shutil
import os
from pathlib import Path
import pytest

from py_bugger.utils.git_utils import clean_git_status


# Creates a temporary Git repo with one committed Python file.
# This is used to test Git-related behavior in isolation.
@pytest.fixture
def clean_git_repo():
    temp_dir = tempfile.mkdtemp()
    subprocess.run(["git", "init"], cwd=temp_dir, check=True)

    file_path = Path(temp_dir) / "sample.py"
    file_path.write_text("print('hello')\n")

    subprocess.run(["git", "add", "sample.py"], cwd=temp_dir, check=True)
    subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=temp_dir, check=True)

    yield Path(temp_dir)

    # Always clean up the temp directory afterward
    shutil.rmtree(temp_dir)


# Helper function to run clean_git_status from inside a target directory.
# I use this to simulate running the check in an actual project folder.
def clean_git_status_in_repo(repo_path, force=False):
    original_cwd = os.getcwd()
    os.chdir(repo_path)
    try:
        clean_git_status(force=force)
    finally:
        os.chdir(original_cwd)


# Should pass when the repo is clean and force is False.
# This is the "normal case" where everything is set up correctly.
def test_clean_repo_passes(clean_git_repo):
    clean_git_status_in_repo(clean_git_repo, force=False)


# Should raise an error when there are uncommitted changes.
# I make a small change to the file but don't commit it.
def test_dirty_repo_fails(clean_git_repo):
    dirty_file = clean_git_repo / "sample.py"
    dirty_file.write_text("print('modified')\n")

    with pytest.raises(RuntimeError, match="Uncommitted changes found"):
        clean_git_status_in_repo(clean_git_repo, force=False)


# Should skip the Git cleanliness check if force=True.
# This test simulates someone using the --force flag.
def test_force_skips_dirty_check(clean_git_repo):
    dirty_file = clean_git_repo / "sample.py"
    dirty_file.write_text("print('forced')\n")

    # Should not raise any errors even though the repo is dirty. User still gets warning though!
    clean_git_status_in_repo(clean_git_repo, force=True)