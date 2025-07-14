"""Utilities for working with the CST."""

import libcst as cst
from libcst.metadata import MetadataWrapper, PositionProvider

from py_bugger.utils import bug_utils
from py_bugger.utils.modification import Modification, modifications

from py_bugger.cli.config import pb_config


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


class ImportModifier(cst.CSTTransformer):
    """Modify imports in the user's project.

    Note: Each import should be unique, so there shouldn't be any need to track
    whether a bug was introduced. node_to_break should only match one node in the
    tree.
    """

    def __init__(self, node_to_break, path, metadata):
        self.node_to_break = node_to_break

        # Need this to record the modification we're making.
        self.path = path
        self.metadata = metadata

    def leave_Import(self, original_node, updated_node):
        """Modify a direct `import <package>` statement."""
        names = updated_node.names

        if original_node.deep_equals(self.node_to_break):
            original_name = names[0].name.value

            # Add a typo to the name of the module being imported.
            new_name = bug_utils.make_typo(original_name)

            # Modify the node name.
            new_names = [cst.ImportAlias(name=cst.Name(new_name))]

            # Record this modification.
            modified_node = updated_node.with_changes(names=new_names)

            position = self.metadata[original_node]
            line_num = position.start.line

            modification = Modification(
                path=self.path,
                original_node=original_node,
                modified_node=modified_node,
                line_num=line_num,
                exception_induced=ModuleNotFoundError,
            )
            modifications.append(modification)

            return updated_node.with_changes(names=new_names)

        return updated_node


class AttributeModifier(cst.CSTTransformer):
    """Modify attributes in the user's project."""

    def __init__(self, node_to_break, node_index, path, metadata):
        self.node_to_break = node_to_break

        # There may be identical nodes in the tree. node_index determines which to modify.
        self.node_index = node_index
        self.identical_nodes_visited = 0

        # Each use of this class should only generate one bug. But multiple nodes
        # can match node_to_break, so make sure we only modify one node.
        self.bug_generated = False

        # Need this to record the modification we're making.
        self.path = path
        self.metadata = metadata

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

            # Record this modification.
            modified_node = updated_node.with_changes(attr=new_attr)

            position = self.metadata[original_node]
            line_num = position.start.line

            modification = Modification(
                path=self.path,
                original_node=original_node,
                modified_node=modified_node,
                line_num=line_num,
                exception_induced=AttributeError,
            )
            modifications.append(modification)

            self.bug_generated = True

            return updated_node.with_changes(attr=new_attr)

        return updated_node


def get_paths_nodes(py_files, node_type):
    """Get all nodes of given type."""
    paths_nodes = []
    for path in py_files:
        source = path.read_text()
        tree = cst.parse_module(source)

        wrapper = MetadataWrapper(tree)
        metadata = wrapper.resolve(PositionProvider)

        node_collector = NodeCollector(node_type=node_type)
        wrapper.module.visit(node_collector)

        for node in node_collector.collected_nodes:
            position = metadata.get(node)
            line_num = position.start.line

            if not pb_config.target_lines:
                paths_nodes.append((path, node))
            elif line_num in pb_config.target_lines:
                paths_nodes.append((path, node))

    return paths_nodes


def get_all_nodes(path):
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


def count_nodes(tree, node):
    """Count the number of nodes in path that match node.

    Useful when a file has multiple identical nodes, and we want to choose one.
    """
    # Count all relevant nodes.
    node_counter = NodeCounter(node)
    tree.visit(node_counter)

    return node_counter.node_count
