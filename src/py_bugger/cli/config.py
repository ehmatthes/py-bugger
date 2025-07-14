"""Config object to collect CLI options."""

from dataclasses import dataclass
from pathlib import Path


SUPPORTED_EXCEPTION_TYPES = [
    "ModuleNotFoundError",
    "AttributeError",
    "IndentationError",
]


@dataclass
class PBConfig:
    exception_type: str = ""
    target_dir: Path = ""
    target_file: Path = ""
    target_lines: str = ""
    num_bugs: int = 1
    ignore_git_status: bool = False
    verbose: bool = True


pb_config = PBConfig()
