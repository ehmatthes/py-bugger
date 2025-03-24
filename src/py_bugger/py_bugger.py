import libcst as cst
import os
import random
from pathlib import Path


class ImportCollector(cst.CSTVisitor):
    """Visit all import nodes, without modifying."""

    def __init__(self):
        self.import_nodes = []

    def visit_Import(self, node):
        """Collect all import nodes."""
        self.import_nodes.append(node)


class ImportModifier(cst.CSTTransformer):
    """Modify imports in the user's project."""

    def __init__(self, nodes_to_break):
        self.nodes_to_break = nodes_to_break

    def leave_Import(self, original_node, updated_node):
        """Modify a direct `import <package>` statement."""
        names = updated_node.names

        if original_node in self.nodes_to_break:
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


def main(exception_type, target_dir, num_bugs):

    # Set a random seed when testing.
    if seed := os.environ.get("PY_BUGGER_RANDOM_SEED"):
        random.seed(int(seed))

    if exception_type == "ModuleNotFoundError":
        print("Introducing a ModuleNotFoundError...")

        # Get the first .py file in the project's root dir.
        if target_dir:
            path_project = Path(target_dir)
            assert path_project.exists()
        else:
            path_project = Path(os.getcwd())

        py_files = path_project.glob("*.py")
        path = next(py_files)

        # Read user's code.
        source = path.read_text()
        tree = cst.parse_module(source)

        # Collect all import nodes.
        import_collector = ImportCollector()
        tree.visit(import_collector)
        # breakpoint()

        nodes_to_break = random.choices(import_collector.import_nodes, k=num_bugs)

        # Modify user's code.
        modified_tree = tree.visit(ImportModifier(nodes_to_break))

        # Rewrite user's code.
        path.write_text(modified_tree.code)

        print("  Modified file.")
