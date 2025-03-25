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
    """Modify imports in the user's project."""

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


### --- *_bugger functions ---

def module_not_found_bugger(py_files, num_bugs):
    """Induce a ModuleNotFoundError.

    Returns:
        Int: Number of bugs made.
    """
    # Find all relevant nodes.
    paths_nodes = []
    for path in py_files:
        source = path.read_text()
        tree = cst.parse_module(source)

        # Collect all import nodes.
        import_collector = ImportCollector()
        tree.visit(import_collector)

        for node in import_collector.import_nodes:
            paths_nodes.append( (path, node) )

    # Select the set of nodes to modify. If num_bugs is greater than the number
    # of nodes, just change each node.
    num_changes = min(len(paths_nodes), num_bugs)
    paths_nodes = random.choices(paths_nodes, k=num_changes)

    # Modify each relevant path.
    for path, node in paths_nodes:
        # breakpoint()
        source = path.read_text()
        tree = cst.parse_module(source)

        # Modify user's code.
        modified_tree = tree.visit(ImportModifier(node))
        path.write_text(modified_tree.code)
        print(f"Added bug to: {path.as_posix()}")

    return num_changes
