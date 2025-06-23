"""Model for modifications made to files to introduce bugs.

This is used to track which modifications have been made, so we don't make multiple
modifications to the same node or line.
"""

from dataclasses import dataclass
from pathlib import Path

import libcst as cst


@dataclass
class Modification:
    path: Path = ""

    # Only data for a line or node will be set, not both.
    # DEV: For line, may want to store line number?
    original_node: cst.CSTNode = None
    modified_node: cst.CSTNode = None

    original_line: str = ""
    modified_line: str = ""

# Only make one instance of this list.
modifications = []


# def already_used(candidate_path, candidate_node=None, candidate_line=None):
#     """Check if a node or line has already been modifed."""
#     # If this path hasn't been modified at all, return False.
#     # if candidate_path not in [m.path for m in modifications]:
#     #     return False

#     # # This path has been modified. Check the nodes/ lines.
#     # modified_nodes = [m.node for m in modifications if ]


#     # for modification in modifications:
#     #     if candidate_path != modification.path:
#     #         return False



#     # Only look at modifications in the candidate path.
#     relevant_modifications = [m if m.path == candidate_path for m in modifications]

#     if not relevant_modifications:
#         return False

#     modified_nodes = [m.modified_node for m in relevant_modifications]
#     modified_lines = [m.modified_line for m in relevant_modifications]

#     if candidate_node in modified_nodes:
#         return True
#     if candidate_line in modified_lines:
#         return True

#     # The candidate node or line has not been modified during this run of py-bugger.
#     return False
