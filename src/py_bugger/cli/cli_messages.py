"""Messages for use in CLI output."""

# --- Static messages ---

msg_target_file_dir = (
    "Target file overrides target dir. Please only pass one of these args."
)

msg_git_not_available = "Git does not seem to be available. It's highly recommended that you run py-bugger against a file or project with a clean Git status. You can ignore this check with the --ignore-git-status argument."

msg_unclean_git_status = "You have uncommitted changes in your project. It's highly recommended that you run py-bugger against a file or project with a clean Git status. You can ignore this check with the --ignore-git-status argument."


# def success_msg(num_added, num_requested):
def success_msg():
    """Generate a success message at end of run."""
    # Importing these here makes for a faster test suite.
    from py_bugger.cli.config import pb_config
    from py_bugger.utils.modification import modifications

    # Show a final success/fail message.
    num_added = len(modifications)
    if num_added == pb_config.num_bugs:
        return "All requested bugs inserted."
    elif num_added == 0:
        return "Unable to introduce any of the requested bugs."
    else:
        msg = f"Inserted {num_added} bugs."
        msg += "\nUnable to introduce additional bugs of the requested type."
        return msg


# Validation for exception type.
def msg_apparent_typo(actual, expected):
    """Suggest a typo fix for an exception type."""
    msg = f"You specified {actual} for --exception-type. Did you mean {expected}?"
    return msg


def msg_unsupported_exception_type(exception_type):
    """Specified an unsupported exception type."""
    msg = f"The exception type {exception_type} is not currently supported."
    return msg


# Messagess for invalid --target-dir calls.


def msg_file_not_dir(target_file):
    """Specified --target-dir, but passed a file."""
    msg = f"You specified --target-dir, but {target_file.name} is a file. Did you mean to use --target-file?"
    return msg


def msg_nonexistent_dir(target_dir):
    """Passed a nonexistent dir to --target-dir."""
    msg = f"The directory {target_dir.name} does not exist. Did you make a typo?"
    return msg


def msg_not_dir(target_dir):
    """Passed something that exists to --target-dir, but it's not a dir."""
    msg = f"{target_dir.name} does not seem to be a directory."
    return msg


# Messages for invalid --target-file calls.


def msg_dir_not_file(target_dir):
    """Specified --target-file, but passed a dir."""
    msg = f"You specified --target-file, but {target_dir.name} is a directory. Did you mean to use --target-dir, or did you intend to pass a specific file from that directory?"
    return msg


def msg_nonexistent_file(target_file):
    """Passed a nonexistent file to --target-file."""
    msg = f"The file {target_file.name} does not exist. Did you make a typo?"
    return msg


def msg_not_file(target_file):
    """Passed something that exists to --target-file, but it's not a file."""
    msg = f"{target_file.name} does not seem to be a file."
    return msg


def msg_file_not_py(target_file):
    """Passed a non-.py file to --target-file."""
    msg = f"{target_file.name} does not appear to be a Python file."
    return msg


# Messages for --target-lines.
msg_target_lines_no_target_file = "You specified --target-lines, without a --target-file. If you want to use --target-lines, please also specify a target file."

def msg_invalid_target_line(target_line, target_file, file_length):
    """Passed a target line that's not in the target file."""
    msg = f"You asked to target line {target_line}, but {target_file.as_posix()} only has {file_length} lines."
    return msg

def msg_invalid_target_lines(end_line, target_file, file_length):
    """Passed a block that's not in the target file."""
    msg = f"You asked to target a block ending at line {end_line}, but {target_file.as_posix()} only has {file_length} lines."
    return msg

# Messages for Git status-related issues.
def msg_git_not_used(pb_config):
    """Git is not being used to manage target file or directory."""
    if pb_config.target_file:
        target = "file"
    else:
        target = "directory"

    msg = f"The {target} you're running py-bugger against does not seem to be under version control. It's highly recommended that you run py-bugger against a file or project with a clean Git status. You can ignore this check with the --ignore-git-status argument."
    return msg
