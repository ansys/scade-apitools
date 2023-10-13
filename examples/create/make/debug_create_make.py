"""
Wrapper of create_make.py for debugging.

Project: ./Template/Empty.etp
"""

from pathlib import Path
from shutil import copytree, rmtree

from ansys.scade.apitools import declare_project

# isort: split

from create_make import main

# duplicate the model to a new directory
dir = Path(__file__).parent
source_dir = dir / 'Template'
target_dir = dir / 'Result'
if target_dir.exists():
    rmtree(target_dir)
copytree(source_dir, target_dir)

# declare the duplicated model
declare_project(str(target_dir / 'Empty.etp'))

# regular script
main()