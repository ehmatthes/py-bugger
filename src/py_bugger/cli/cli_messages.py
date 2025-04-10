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
