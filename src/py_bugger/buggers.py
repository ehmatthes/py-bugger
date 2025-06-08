"""Utilities for introducing specific kinds of bugs."""

import libcst as cst
import random

from py_bugger.utils import cst_utils
from py_bugger.utils import file_utils
from py_bugger.utils import bug_utils

from py_bugger.cli.config import pb_config


### --- *_bugger functions ---


def module_not_found_bugger(py_files):
    """Induce a ModuleNotFoundError.

    Returns:
        Int: Number of bugs made.
    """
    # Find all relevant nodes.
    paths_nodes = cst_utils.get_paths_nodes(py_files, node_type=cst.Import)

    # Select the set of nodes to modify. If num_bugs is greater than the number
    # of nodes, just change each node.
    num_changes = min(len(paths_nodes), pb_config.num_bugs)
    paths_nodes_modify = random.sample(paths_nodes, k=num_changes)

    # Modify each relevant path.
    bugs_added = 0
    for path, node in paths_nodes_modify:
        source = path.read_text()
        tree = cst.parse_module(source)

        # Modify user's code.
        try:
            modified_tree = tree.visit(cst_utils.ImportModifier(node))
        except TypeError:
            # DEV: Figure out which nodes are ending up here, and update
            # modifier code to handle these nodes.
            # For diagnostics, can run against Pillow with -n set to a
            # really high number.
            ...
        else:
            path.write_text(modified_tree.code)
            _report_bug_added(path)
            bugs_added += 1

    return bugs_added


def attribute_error_bugger(py_files):
    """Induce an AttributeError.

    Returns:
        Int: Number of bugs made.
    """
    # Find all relevant nodes.
    paths_nodes = cst_utils.get_paths_nodes(py_files, node_type=cst.Attribute)

    # Select the set of nodes to modify. If num_bugs is greater than the number
    # of nodes, just change each node.
    num_changes = min(len(paths_nodes), pb_config.num_bugs)
    paths_nodes_modify = random.sample(paths_nodes, k=num_changes)

    # Modify each relevant path.
    bugs_added = 0
    for path, node in paths_nodes_modify:
        source = path.read_text()
        tree = cst.parse_module(source)

        # Pick node to modify if more than one match in the file.
        node_count = cst_utils.count_nodes(tree, node)
        if node_count > 1:
            node_index = random.randrange(0, node_count - 1)
        else:
            node_index = 0

        # Modify user's code.
        try:
            modified_tree = tree.visit(cst_utils.AttributeModifier(node, node_index))
        except TypeError:
            # DEV: Figure out which nodes are ending up here, and update
            # modifier code to handle these nodes.
            # For diagnostics, can run against Pillow with -n set to a
            # really high number.
            ...
        else:
            path.write_text(modified_tree.code)
            _report_bug_added(path)
            bugs_added += 1

    return bugs_added


def indentation_error_bugger(py_files):
    """Induce an IndentationError.

    This simply parses raw source files. Conditions are pretty concrete, and LibCST
    doesn't make it easy to create invalid syntax.

    Returns:
        Int: Number of bugs made.
    """
    # Find relevant files and lines.
    targets = [
        "for",
        "while",
        "def",
        "class",
        "if",
        "with",
        "match",
        "try",
    ]
    paths_lines = file_utils.get_paths_lines(py_files, targets=targets)

    # Select the set of lines to modify. If num_bugs is greater than the number
    # of lines, just change each line.
    num_changes = min(len(paths_lines), pb_config.num_bugs)
    paths_lines_modify = random.sample(paths_lines, k=num_changes)

    # Modify each relevant path.
    bugs_added = 0
    for path, target_line in paths_lines_modify:
        if bug_utils.add_indentation(path, target_line):
            _report_bug_added(path)
            bugs_added += 1

    return bugs_added


# --- Helper functions ---
# DEV: This is a good place for helper functions, before they are refined enough
# to move to utils/.


def _report_bug_added(path_modified):
    """Report that a bug was added."""
    if pb_config.verbose:
        print(f"Added bug to: {path_modified.as_posix()}")
    else:
        print(f"Added bug.")
