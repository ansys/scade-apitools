# Copyright (C) 2023 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Generation of Python classes from ecore for SCADE Display.

Note: original ecore model and display.py not consistent (2026 R1)
-> ./tools/Models/sdy.ecore modified locally to comply with delivered files.
"""

from pathlib import Path

from sdytools import SdyModel
from svcaccessor import AccessDeclarationsService, AccessFunctionsService

# from svcclass import ClassService
# from svcenum import EnumService
from svcvisit import VisitorService

import ansys.eseg.lbsjv.ecore as ecore
from ansys.eseg.lbsjv.vgl import get_manager_instance
from ansys.eseg.lbsjv.vgl.defaults import FileType
from ansys.eseg.lbsjv.vgl.interfaces import IManager
from ansys.eseg.lbsjv.vgl.predef import PYTHON


def init_module(manager: IManager):
    """Declare the provided services."""
    # default Python file type
    template = Path(__file__).parent / 'display.tp'
    ftp = FileType(r'^.*\.py$', template, PYTHON)
    manager.add_file_types([ftp])
    # services
    services = [
        # EnumService(),  # no longer needed
        # ClassService(),  # no longer needed
        VisitorService(),
        AccessFunctionsService(),
        AccessDeclarationsService(),
    ]
    manager.add_services(services)
    manager.activate_services([_.NAME for _ in services])


print('generating classes for sdy.ecore...')

target_dir = Path(__file__).parent.parent.parent / 'src' / 'ansys' / 'scade' / 'apitools'
go = get_manager_instance(target_dir, 'display')
go.load_environment()
init_module(go)

model_dir = Path(__file__).parent.parent / 'Models'
ecore_dir = Path(ecore.__file__).parent / 'model'

# CAUTION: declare the libraries first to make sure binding is performed
#          before the models are preprocessed
emodel = SdyModel(False, '', ecore_dir / 'ecore.ecore', 'NA', library=True)
common = SdyModel(False, '', model_dir / 'common.ecore', 'NA', library=True)
model = SdyModel(False, '', model_dir / 'sdy.ecore', 'sdy', library=False)

go.add_models([emodel, common, model])
# visitor file is not the default
path_visitor = target_dir / 'visitor' / 'sdyvisitor.py'
go.add_user_files([path_visitor])

go.go()
print('...done')
