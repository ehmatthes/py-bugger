import libcst as cst
import os
import random
from pathlib import Path

from py_bugger.utils import file_utils
from py_bugger.utils import buggers


# class ImportCollector(cst.CSTVisitor):
#     """Visit all import nodes, without modifying."""

#     def __init__(self):
#         self.import_nodes = []

#     def visit_Import(self, node):
#         """Collect all import nodes."""
#         self.import_nodes.append(node)


# class ImportModifier(cst.CSTTransformer):
#     """Modify imports in the user's project."""

#     def __init__(self, nodes_to_break, bugs_introduced):
#         self.nodes_to_break = nodes_to_break
#         self.bugs_introduced = bugs_introduced

#     def leave_Import(self, original_node, updated_node):
#         """Modify a direct `import <package>` statement."""
#         names = updated_node.names

#         if original_node in self.nodes_to_break:
#             original_name = names[0].name.value

#             # Remove one letter from the package name.
#             chars = list(original_name)
#             char_remove = random.choice(chars)
#             chars.remove(char_remove)
#             new_name = "".join(chars)

#             # Modify the node name.
#             new_names = [cst.ImportAlias(name=cst.Name(new_name))]

#             # Update number of bugs.
#             self.bugs_introduced.append("ModuleNotFoundError")

#             return updated_node.with_changes(names=new_names)

#         return updated_node


def main(exception_type, target_dir, num_bugs):

    # Set a random seed when testing.
    if seed := os.environ.get("PY_BUGGER_RANDOM_SEED"):
        random.seed(int(seed))

    # Get a list of .py files we can consider modifying.
    py_files = file_utils.get_py_files(target_dir)

    # Track bugs that are introduced. For now, just a list of exceptions
    # that are induced. May expand to a sequence of dataclass objects with
    # more info about each bug?
    bugs_introduced = []

    # Currently, just one exception type. When multiple are supported, implement
    # more complex logic for choosing which ones to introduce, and tracking bugs.
    if exception_type == "ModuleNotFoundError":
        bug_made = buggers.module_not_found_bugger(py_files[:], num_bugs)

        # DEV: Logic here about success or failure.

        # # Keep trying .py files until we make a bug.
        # bug_made = False
        # py_files_copy = py_files[:]
        # random.shuffle(py_files_copy)

        # while py_files and (not bug_made):
        #     # Parse .py file.
        #     path = py_files_copy.pop()
        #     source = path.read_text()
        #     tree = cst.parse_module(source)

        #     # Collect all import nodes.
        #     import_collector = ImportCollector()
        #     tree.visit(import_collector)

        #     if not import_collector.import_nodes:
        #         continue

        #     nodes_to_break = random.choices(import_collector.import_nodes, k=num_bugs)

        #     # Modify user's code.
        #     bugs_before = len(bugs_introduced)
        #     modified_tree = tree.visit(ImportModifier(nodes_to_break, bugs_introduced))
        #     if len(bugs_introduced) > bugs_before:
        #         bug_made = True

        #     # Rewrite user's code.
        #     path.write_text(modified_tree.code)

        #     print(f"  Modified file: {path.as_posix()}")
