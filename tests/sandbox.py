# Copyright (C) 2023 - 2024 ANSYS, Inc. and/or its affiliates.
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

# for debug purposes and quick tests
# (breakpoints can't be always hit with VS/pytest)

import ansys.scade.apitools.create as create
from tests.conftest import load_project, load_session
from tests.test_create_declaration import _get_path
from tests.test_utils import get_resources_dir

if __name__ == '__main__':
    project_path = get_resources_dir() / 'tmp' / 'TestCreateDeclaration' / 'CreateDeclaration.etp'
    project = load_project(project_path)
    session = load_session(project_path)
    try:
        owner = session.model.get_object_from_path('Package::ChildPackage::')
        name = 'ChildPackagePackageUpperFolder'
        path = _get_path(project, 'NewChildPackageUpperFolder.xscade')
        package = create.create_package(owner, name, path)
        create.add_unit_to_project(project, package.defined_in, folder=None, default=True)
        # the created package must be accessible
        package_path = '%s%s::' % (owner.get_full_path(), name)
        print('package_path', package_path)
        assert session.model.get_object_from_path(package_path) == package
        create.save_all()
        create.save_project(project)
    except BaseException as e:
        print(e)
