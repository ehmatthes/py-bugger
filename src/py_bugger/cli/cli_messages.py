"""Messages for use in CLI output."""

# --- Static messages ---

msg_exception_type_required = (
    "You must be explicit about what kinds of errors you want to induce in the project."
)

msg_target_file_dir = (
    "Target file overrides target dir. Please only pass one of these args."
)


# --- Dynamic messages ---


def success_msg(num_added, num_requested):
    """Generate a success message at end of run."""

    # Show a final success/fail message.
    if num_added == num_requested:
        return "All requested bugs inserted."
    elif num_added == 0:
        return "Unable to introduce any of the requested bugs."
    else:
        msg = f"Inserted {num_added} bugs."
        msg += "\nUnable to introduce additional bugs of the requested type."
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