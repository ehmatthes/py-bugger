"""Model for modifications made to files to introduce bugs.

This is used to track which modifications have been made, so we don't make multiple
modifications to the same node or line.

Not currently using original_node or original_line, but including these means
the list of modifications can be used to stage all changes, and write them all at
once if that becomes a better approach.
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
