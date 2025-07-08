"""
Wrapper of create_type.py for debugging.

Project: ./Model/Model.etp
"""

from pathlib import Path
from shutil import copytree, rmtree

from ansys.scade.apitools import declare_project

# isort: split

from create_type import main

# duplicate the model to a new directory
dir = Path(__file__).parent
source_dir = dir / 'Model'
target_dir = dir / 'Result'
if target_dir.exists():
    rmtree(target_dir)
copytree(source_dir, target_dir)

# declare the duplicated model
assert declare_project  # nosec
declare_project(str(target_dir / 'Model.etp'))

# regular script
main()
