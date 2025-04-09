"""Config object to collect CLI options."""

from dataclasses import dataclass
from pathlib import Path

# from typing import Optional


@dataclass
class PBConfig:
    exception_type: str = ""
    target_dir: Path = ""
    target_file: Path = ""
    num_bugs: int = 1

pb_config = PBConfig()