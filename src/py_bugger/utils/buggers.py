"""Utilities for introducing specific kinds of bugs."""

import libcst as cst
import random

from py_bugger.utils import bug_utils


# --- CST classes ---


class NodeCollector(cst.CSTVisitor):
    """Collect all nodes of a specific kind."""

    def __init__(self, node_type):
        self.node_type = node_type
        self.collected_nodes = []

    def on_visit(self, node):
        """Visit each node, collecting nodes that match the node type."""
        if isinstance(node, self.node_type):
            self.collected_nodes.append(node)
        return True


class ImportModifier(cst.CSTTransformer):
    """Modify imports in the user's project.

    Note: Each import should be unique, so there shouldn't be any need to track
    whether a bug was introduced. node_to_break should only match one node in the
    tree.
    """

    def __init__(self, node_to_break):
        self.node_to_break = node_to_break

    def leave_Import(self, original_node, updated_node):
        """Modify a direct `import <package>` statement."""
        names = updated_node.names

        if original_node.deep_equals(self.node_to_break):
            original_name = names[0].name.value

            # Add a typo to the name of the module being imported.
            new_name = bug_utils.make_typo(original_name)

            # Modify the node name.
            new_names = [cst.ImportAlias(name=cst.Name(new_name))]

            return updated_node.with_changes(names=new_names)

        return updated_node


class AttributeModifier(cst.CSTTransformer):
    """Modify attributes in the user's project."""

    def __init__(self, node_to_break, node_index):
        self.node_to_break = node_to_break

        # There may be identical nodes in the tree. node_index determines which to modify.
        self.node_index = node_index
        self.identical_nodes_visited = 0

        # Each use of this class should only generate one bug. But multiple nodes
        # can match node_to_break, so make sure we only modify one node.
        self.bug_generated = False

    def leave_Attribute(self, original_node, updated_node):
        """Modify an attribute name, to generate AttributeError."""
        attr = updated_node.attr

        if original_node.deep_equals(self.node_to_break) and not self.bug_generated:
            # If there are identical nodes and this isn't the right one, bump count
            # and return unmodified node.
            if self.identical_nodes_visited != self.node_index:
                self.identical_nodes_visited += 1
                return updated_node

            original_identifier = attr.value

            # Add a typo to the attribute name.
            new_identifier = bug_utils.make_typo(original_identifier)

            # Modify the node name.
            new_attr = cst.Name(new_identifier)

            self.bug_generated = True

            return updated_node.with_changes(attr=new_attr)

        return updated_node


### --- *_bugger functions ---


def module_not_found_bugger(py_files, num_bugs):
    """Induce a ModuleNotFoundError.

    Returns:
        Int: Number of bugs made.
    """
    # Find all relevant nodes.
    paths_nodes = _get_paths_nodes(py_files, node_type=cst.Import)

    # Select the set of nodes to modify. If num_bugs is greater than the number
    # of nodes, just change each node.
    num_changes = min(len(paths_nodes), num_bugs)
    paths_nodes_modify = random.sample(paths_nodes, k=num_changes)

    # Modify each relevant path.
    bugs_added = 0
    for path, node in paths_nodes_modify:
        source = path.read_text()
        tree = cst.parse_module(source)

        # Modify user's code.
        try:
            modified_tree = tree.visit(ImportModifier(node))
        except TypeError:
            # DEV: Figure out which nodes are ending up here, and update
            # modifier code to handle these nodes.
            # For diagnostics, can run against Pillow with -n set to a
            # really high number.
            ...
        else:
            path.write_text(modified_tree.code)
            print(f"Added bug to: {path.as_posix()}")
            bugs_added += 1

    return bugs_added


def attribute_error_bugger(py_files, num_bugs):
    """Induce an AttributeError.

    Returns:
        Int: Number of bugs made.
    """
    # Find all relevant nodes.
    paths_nodes = _get_paths_nodes(py_files, node_type=cst.Attribute)

    # Select the set of nodes to modify. If num_bugs is greater than the number
    # of nodes, just change each node.
    num_changes = min(len(paths_nodes), num_bugs)
    paths_nodes_modify = random.sample(paths_nodes, k=num_changes)

    # Modify each relevant path.
    bugs_added = 0
    for path, node in paths_nodes_modify:
        source = path.read_text()
        tree = cst.parse_module(source)

        # Pick node to modify if more than one match in the file.
        # node_count = _count_nodes(tree, cst.Attribute)
        node_count = _count_nodes(tree, node)
        if node_count > 1:
            node_index = random.randrange(0, node_count - 1)
        else:
            node_index = 0

        # Modify user's code.
        try:
            modified_tree = tree.visit(AttributeModifier(node, node_index))
        except TypeError:
            # DEV: Figure out which nodes are ending up here, and update
            # modifier code to handle these nodes.
            # For diagnostics, can run against Pillow with -n set to a
            # really high number.
            ...
        else:
            path.write_text(modified_tree.code)
            print(f"Added bug to: {path.as_posix()}")
            bugs_added += 1

    return bugs_added


def indentation_error_bugger(py_files, num_bugs):
    """Induce an IndentationError.

    This simply parses raw source files. Conditions are pretty concrete, and LibCST
    doesn't make it easy to create invalid syntax.

    Returns:
        Int: Number of bugs made.
    """
    # Find relevant files and lines.
    targets = ["for", "while", "def", "class", "if", "elif", "else", "with", "match", "case", "try", "except", "finally"]
    paths_lines = _get_paths_lines(py_files, targets=targets)

    # Select the set of lines to modify. If num_bugs is greater than the number
    # of lines, just change each line.
    num_changes = min(len(paths_lines), num_bugs)
    paths_lines_modify = random.sample(paths_lines, k=num_changes)

    # Modify each relevant path.
    bugs_added = 0
    for path, target_line in paths_lines_modify:
        if bug_utils.add_indentation(path, target_line):
            print(f"Added bug to: {path.as_posix()}")
            bugs_added += 1

    return bugs_added


# --- Helper functions ---


def _get_paths_lines(py_files, targets):
    """Get all lines from all files matching targets."""
    paths_lines = []
    for path in py_files:
        lines = path.read_text().splitlines()
        for line in lines:
            stripped_line = line.strip()
            if any([stripped_line.startswith(target) for target in targets]):
                paths_lines.append((path, line))

    return paths_lines


def _get_paths_nodes(py_files, node_type):
    """Get all nodes of given type."""
    paths_nodes = []
    for path in py_files:
        source = path.read_text()
        tree = cst.parse_module(source)

        node_collector = NodeCollector(node_type=node_type)
        tree.visit(node_collector)

        for node in node_collector.collected_nodes:
            paths_nodes.append((path, node))

    return paths_nodes


def _get_all_nodes(path):
    """Get all nodes in a file.

    This is primarily for development work, where we want to see all the nodes
    in a short representative file.

    Example usage, from a #_bugger() function:
        nodes = _get_all_nodes(py_files[0])
    """
    source = path.read_text()
    tree = cst.parse_module(source)

    node_collector = NodeCollector(node_type=cst.CSTNode)
    tree.visit(node_collector)

    return node_collector.collected_nodes


class NodeCounter(cst.CSTVisitor):
    """Count all nodes matching the target node."""

    def __init__(self, target_node):
        self.target_node = target_node
        self.node_count = 0

    def on_visit(self, node):
        """Increment node_count if node matches.."""
        if node.deep_equals(self.target_node):
            self.node_count += 1
        return True


def _count_nodes(tree, node):
    """Count the number of nodes in path that match node.

    Useful when a file has multiple identical nodes, and we want to choose one.
    """
    # Count all relevant nodes.
    node_counter = NodeCounter(node)
    tree.visit(node_counter)

    return node_counter.node_count
