"""Utilities for introducing specific kinds of bugs.

DEV: Don't rush to refactor bugger functions. for example, it's not yet clear whether this should
be a class. Also, not sure we need separate bugger functions, or one bugger function with some
conditional logic. Implement support for another exception type, and logical errors, and see what
things are looking like.
"""
import random

import libcst as cst
from libcst.metadata import MetadataWrapper, PositionProvider

from py_bugger.utils import cst_utils
from py_bugger.utils import file_utils
from py_bugger.utils import bug_utils

from py_bugger.cli.config import pb_config


### --- *_bugger functions ---


def module_not_found_bugger(py_files):
    """Induce a ModuleNotFoundError.

    Returns:
        Bool: Whether a bug was introduced or not.
    """
    # Get a random node that hasn't already been modified.
    path, node = _get_random_node(py_files, node_type=cst.Import)
    if not path:
        return False

    # Parse user's code.
    source = path.read_text()
    tree = cst.parse_module(source)
    wrapper = MetadataWrapper(tree)
    metadata = wrapper.resolve(PositionProvider)

    # Modify user's code
    try:
        modified_tree = wrapper.module.visit(cst_utils.ImportModifier(node, path, metadata))
    except TypeError:
        # DEV: Figure out which nodes are ending up here, and update
        # modifier code to handle these nodes.
        # For diagnostics, can run against Pillow with -n set to a
        # really high number.
        raise
    else:
        path.write_text(modified_tree.code)
        _report_bug_added(path)
        return True


def attribute_error_bugger(py_files):
    """Induce an AttributeError.

    Returns:
        Bool: Whether a bug was introduced or not.
    """
    # Get a random node that hasn't already been modified.
    path, node = _get_random_node(py_files, node_type=cst.Attribute)
    if not path:
        return False

    # Parse user's code.
    source = path.read_text()
    tree = cst.parse_module(source)
    wrapper = MetadataWrapper(tree)
    metadata = wrapper.resolve(PositionProvider)

    # Pick node to modify if more than one match in the file.
    # Note that not all bugger functions need this step.
    node_count = cst_utils.count_nodes(tree, node)
    if node_count > 1:
        node_index = random.randrange(0, node_count - 1)
    else:
        node_index = 0

    # Modify user's code.
    try:
        modified_tree = wrapper.module.visit(cst_utils.AttributeModifier(node, node_index, path, metadata))
    except TypeError:
        # DEV: Figure out which nodes are ending up here, and update
        # modifier code to handle these nodes.
        # For diagnostics, can run against Pillow with -n set to a
        # really high number.
        raise
    else:
        path.write_text(modified_tree.code)
        _report_bug_added(path)
        return True


def indentation_error_bugger(py_files):
    """Induce an IndentationError.

    This simply parses raw source files. Conditions are pretty concrete, and LibCST
    doesn't make it easy to create invalid syntax.

    Returns:
        Bool: Whether a bug was introduced or not.
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

    # We only need line numbers, not actual lines.
    paths_linenums = file_utils.get_paths_linenums(py_files, targets=targets)

    # Bail if there are no relevant lines.
    if not paths_linenums:
        return False

    path, target_linenum = random.choice(paths_linenums)

    if bug_utils.add_indentation_linenum(path, target_linenum):
        _report_bug_added(path)
        return True


# --- Helper functions ---
# DEV: This is a good place for helper functions, before they are refined enough
# to move to utils/.


def _report_bug_added(path_modified):
    """Report that a bug was added."""
    if pb_config.verbose:
        print(f"Added bug to: {path_modified.as_posix()}")
    else:
        print(f"Added bug.")


def _get_random_node(py_files, node_type):
    """Randomly select a node to modify.

    Make sure it's a node that hasn't already been modified.

    Returns:
        Tuple: (path, node) or (False, False)
    """
    # Find all relevant nodes. Bail if there are no relevant nodes.
    if not (paths_nodes := cst_utils.get_paths_nodes(py_files, node_type)):
        return False, False

    random.shuffle(paths_nodes)
    for path, node in paths_nodes:
        if file_utils.check_unmodified(path, candidate_node=node):
            return path, node
    else:
        # All nodes have already been modified to introduce a previous bug.
        return False, False
