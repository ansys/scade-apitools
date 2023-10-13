"""
Wrapper of create_top_level.py for debugging.

Project: ./Template/Project.etp
"""

from pathlib import Path
from shutil import copytree, rmtree

from ansys.scade.apitools import declare_project

# isort: split

from create_top_level import main

# duplicate the model to a new directory
dir = Path(__file__).parent
source_dir = dir / 'Template'
target_dir = dir / 'Result'
if target_dir.exists():
    rmtree(target_dir)
copytree(source_dir, target_dir)

# declare the duplicated model
declare_project(str(target_dir / 'Project.etp'))

# regular script
main()
