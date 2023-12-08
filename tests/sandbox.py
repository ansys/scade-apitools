# Copyright (C) 2023 ANSYS, Inc. and/or its affiliates.

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
