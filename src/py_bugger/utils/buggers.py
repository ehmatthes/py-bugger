"""Utilities for introducing specific kinds of bugs."""

import libcst as cst
import random


# --- CST classes ---


class ImportCollector(cst.CSTVisitor):
    """Visit all import nodes, without modifying."""

    def __init__(self):
        self.import_nodes = []

    def visit_Import(self, node):
        """Collect all import nodes."""
        self.import_nodes.append(node)


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

            # Remove one letter from the package name.
            chars = list(original_name)
            char_remove = random.choice(chars)
            chars.remove(char_remove)
            new_name = "".join(chars)

            # Modify the node name.
            new_names = [cst.ImportAlias(name=cst.Name(new_name))]

            return updated_node.with_changes(names=new_names)

        return updated_node


class AttributeCollector(cst.CSTVisitor):
    """Visit all attribute-releated nodes, without modifying."""

    def __init__(self):
        self.attribute_nodes = []

    def visit_Attribute(self, node):
        """Collect all import nodes."""
        self.attribute_nodes.append(node)


class AttributeModifier(cst.CSTTransformer):
    """Modify attributes in the user's project."""

    def __init__(self, node_to_break):
        self.node_to_break = node_to_break

        # Each use of this class should only generate one bug. But multiple nodes
        # can match node_to_break, so make sure we only modify one node.
        self.bug_generated = False

    def leave_Attribute(self, original_node, updated_node):
        """Modify an attribute name, to generate AttributeError."""
        attr = updated_node.attr


        if original_node.deep_equals(self.node_to_break) and not self.bug_generated:
            original_identifier = attr.value

            # Remove one letter from the attribute name.
            chars = list(original_identifier)
            char_remove = random.choice(chars)
            chars.remove(char_remove)
            new_identifier = "".join(chars)

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
    paths_nodes = _get_paths_nodes_import(py_files)

    # Select the set of nodes to modify. If num_bugs is greater than the number
    # of nodes, just change each node.
    num_changes = min(len(paths_nodes), num_bugs)
    paths_nodes_modify = random.choices(paths_nodes, k=num_changes)

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
    paths_nodes = _get_paths_nodes_attribute_error(py_files)

    # Select the set of nodes to modify. If num_bugs is greater than the number
    # of nodes, just change each node.
    num_changes = min(len(paths_nodes), num_bugs)
    paths_nodes_modify = random.choices(paths_nodes, k=num_changes)

    # Modify each relevant path.
    bugs_added = 0
    for path, node in paths_nodes_modify:
        source = path.read_text()
        tree = cst.parse_module(source)

        # Modify user's code.
        try:
            modified_tree = tree.visit(AttributeModifier(node))
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


# --- Helper functions ---

def _get_paths_nodes_import(py_files):
    """Get all import-related nodes."""
    paths_nodes = []
    for path in py_files:
        source = path.read_text()
        tree = cst.parse_module(source)

        # Collect all import nodes.
        import_collector = ImportCollector()
        tree.visit(import_collector)

        for node in import_collector.import_nodes:
            paths_nodes.append((path, node))

    return paths_nodes

def _get_paths_nodes_attribute_error(py_files):
    """Get all nodes representing attributes."""
    paths_nodes = []
    for path in py_files:
        source = path.read_text()
        tree = cst.parse_module(source)

        # Collect all import nodes.
        attribute_collector = AttributeCollector()
        tree.visit(attribute_collector)

        for node in attribute_collector.attribute_nodes:
            paths_nodes.append((path, node))

    return paths_nodes