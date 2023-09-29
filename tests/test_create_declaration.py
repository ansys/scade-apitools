# MIT License
#
# Copyright (c) 2023 ANSYS, Inc. All rights reserved.
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
Test suite for create/declaration.py.

Test strategy:

The tests of this module operate make a copy of a reference project and add Scade
elements. The project is saved once all the tests of a class are executed.

The status of the tests cases is assessed by ensuring the functions execute properly and
by testing a few properties of the created data: This gives enough confidence for the
correctness of the execution. Indeed, it is not easy to compare the resulting model
to some expected result, nor easy to maintain.

Anyways, the result models can be exmined after the execution of the tests, for a deep analysis.
"""

from os.path import abspath
from pathlib import Path

import pytest

import ansys.scade.apitools.create as create

# import std from prj to ensure import order: models after apitools
# import scade.model.project.stdproject as std
from ansys.scade.apitools.create.project import std
from test_utils import get_resources_dir

# import suite from declaration to ensure import order: models after apitools
# import scade.model.suite as suite
# from ansys.scade.apitools.create.declaration import suite


def _get_path(project: std.Project, rel_path: str) -> Path:
    """Return the absolute path with respect to the project and make sure the directory exists."""
    if rel_path:
        path = Path(abspath(Path(project.pathname).parent / rel_path))
        path.parent.mkdir(exist_ok=True)
    else:
        path = None
    return path


# project considered for the tests
project_path = get_resources_dir() / 'resources' / 'CreateDeclaration' / 'CreateDeclaration.etp'


@pytest.mark.project(project_path)
class TestCreateDeclaration:
    nominal_package_data = [
        # nominal uses cases
        ('RootPackageDefault', '', None),
        ('RootPackageSeparate', '', 'RootPackageSeparate.xscade'),
        ('SubPackage', 'Package:', None),
        # advanced use cases to test the various possible references to a file
        ('ChildDefault', 'Package::ChildPackage::', None),
        ('ChildSameFolder', 'Package::ChildPackage::', 'Child/ChildSameFolder.xscade'),
        ('ChildSubFolder', 'Package::ChildPackage::', 'Child/SubFolder/ChildSubFolder.xscade'),
        ('ChildUpperFolder', 'Package::ChildPackage::', 'ChildUpperFolder.xscade'),
        ('ChildSiblingFolder', 'Package::ChildPackage::', 'Folder/ChildSiblingFolder.xscade'),
    ]

    @pytest.mark.parametrize(
        'name, owner, rel_path',
        nominal_package_data,
        ids=[_[0] for _ in nominal_package_data],
    )
    def test_create_package(self, tmp_project_session, name, owner, rel_path):
        # project/session must have been duplicated to a temporary directory
        project, session = tmp_project_session
        owner = session.model.get_object_from_path(owner)
        path = _get_path(project, rel_path)
        package = create.create_package(owner, name, path)
        # add the unit to the project
        create.add_element_to_project(project, package, folder=None, default=True)
        # the created package must be accessible
        package_path = '%s%s::' % (owner.get_full_path(), name)
        assert session.model.get_object_from_path(package_path) == package
        create.save_all()

    nominal_type_data = [
        ('PackageType', 'Package:', 'int32', None),
        ('RootTypeDefault', '', 'bool', None),
        ('RootTypeSeparate', '', 'bool', 'NewType.xscade'),
        ('RootTypeSubFolder', '', 'bool', 'Folder/NewTypeSubFolder.xscade'),
    ]

    @pytest.mark.parametrize(
        'name, owner, tree, rel_path',
        nominal_type_data,
        ids=[_[0] for _ in nominal_type_data],
    )
    def test_create_named_type(self, tmp_project_session, name, owner, tree, rel_path):
        # project/session must have been duplicated to a temporary directory
        project, session = tmp_project_session
        owner = session.model.get_object_from_path(owner)
        path = _get_path(project, rel_path)
        type_ = create.create_named_type(owner, name, tree, path)
        # add the unit to the project
        folder = create.create_folder(project, 'Type Files')
        create.add_element_to_project(project, type_, folder=folder)
        # the created type must be accessible
        type_path = '%s%s/' % (owner.get_full_path(), name)
        assert session.model.get_object_from_path(type_path) == type_
        assert type_.type.name == tree
        create.save_all()

    nominal_imported_type_data = [
        ('PackageImported', 'Package:', 'ExternalTypes.h', None),
        ('RootImported', '', 'ExternalTypes.h', None),
        ('RootUnknown', '', None, None),
    ]

    @pytest.mark.parametrize(
        'name, owner, file, rel_path',
        nominal_imported_type_data,
        ids=[_[0] for _ in nominal_imported_type_data],
    )
    def test_create_imported_type(self, tmp_project_session, name, owner, file, rel_path):
        # project/session must have been duplicated to a temporary directory
        project, session = tmp_project_session
        owner = session.model.get_object_from_path(owner)
        path = _get_path(project, rel_path)
        type_ = create.create_imported_type(owner, name, path)
        # add the unit to the project
        folder = create.create_folder(project, 'Type Files')
        create.add_element_to_project(project, type_, folder=folder)
        if file:
            create.add_imported_to_project(project, type_, file)
        # the created type must be accessible
        type_path = '%s%s/' % (owner.get_full_path(), name)
        assert session.model.get_object_from_path(type_path) == type_
        create.save_all()

    nominal_enumeration_data = [
        ('RootEnumeration', '', ['BLUE', 'WHILE', 'RED']),
        ('PackageEnumeration', 'Package:', ['GREEN']),
    ]

    @pytest.mark.parametrize(
        'name, owner, values',
        nominal_enumeration_data,
        ids=[_[0] for _ in nominal_enumeration_data],
    )
    def test_create_enumeration(self, tmp_project_session, name, owner, values):
        # project/session must have been duplicated to a temporary directory
        project, session = tmp_project_session
        # hard-coded values: no need to test several owners or files,
        # this is redundant with previous test cases
        owner = session.model.get_object_from_path(owner)
        type_ = create.create_enumeration(owner, name, values, None)
        create.add_element_to_project(project, type_, default=False)
        # the created type must be accessible
        type_path = '%s%s/' % (owner.get_full_path(), name)
        assert session.model.get_object_from_path(type_path) == type_
        assert [_.name for _ in type_.type.values] == values
        create.save_all()

    nominal_enumeration_data = [
        ('AddBefore', 1, ['ZERO'], 'ONE'),
        ('AddMiddle', 2, ['TWO'], 'THREE'),
        ('AddAfter', 3, ['FOUR', 'FIVE'], None),
        ('AddUnknown', 4, ['SIX'], 'UNKNOWN'),
    ]

    @pytest.mark.parametrize(
        'name, suffix, values, before',
        nominal_enumeration_data,
        ids=[_[0] for _ in nominal_enumeration_data],
    )
    def test_add_enumeration_values(self, tmp_project_session, name, suffix, values, before):
        # project/session must have been duplicated to a temporary directory
        project, session = tmp_project_session
        # create an enumeration with two hard-coded values
        owner = session.model
        inits = ['%s_%d' % (_, suffix) for _ in ['ONE', 'THREE']]
        type_ = create.create_enumeration(owner, name, inits, None)
        create.add_element_to_project(project, type_, default=False)
        # insert values
        values = ['%s_%d' % (_, suffix) for _ in values]
        before = '%s_%d' % (before, suffix) if before else None
        create.add_enumeration_values(type_, values, before)
        # the created type must be accessible
        type_path = '%s%s/' % (owner.get_full_path(), name)
        assert session.model.get_object_from_path(type_path) == type_
        assert len(type_.type.values) == 2 + len(values)
        create.save_all()

    nominal_constant_data = [
        ('PACKAGE_INT32', 'Package:', 'int32', 42, None),
        ('ROOT_DEFAULT', '', 'bool', False, None),
        ('ROOT_SEPARATE', '', 'bool', False, 'NewConstant.xscade'),
        ('ROOT_SUB_FOLDER', '', 'bool', False, 'Folder/NewConstantSubFolder.xscade'),
    ]

    @pytest.mark.parametrize(
        'name, owner, type_, value, rel_path',
        nominal_constant_data,
        ids=[_[0] for _ in nominal_constant_data],
    )
    def test_create_constant(self, tmp_project_session, name, owner, type_, value, rel_path):
        # project/session must have been duplicated to a temporary directory
        project, session = tmp_project_session
        owner = session.model.get_object_from_path(owner)
        path = _get_path(project, rel_path)
        constant = create.create_constant(owner, name, type_, value, path)
        create.add_element_to_project(project, constant, default=False)
        # the created constant must be accessible
        constant_path = '%s%s/' % (owner.get_full_path(), name)
        assert session.model.get_object_from_path(constant_path) == constant
        assert constant.type.name == type_
        create.save_all()

    nominal_imported_constant_data = [
        ('PACKAGE_IMPORTED', 'Package:', 'int32', create.VK.PUBLIC),
        ('ROOT_IMPORTED', '', 'bool', create.VK.PRIVATE),
    ]

    @pytest.mark.parametrize(
        'name, owner, type_, visibility',
        nominal_imported_constant_data,
        ids=[_[0] for _ in nominal_imported_constant_data],
    )
    def test_create_imported_constant(self, tmp_project_session, name, owner, type_, visibility):
        # project/session must have been duplicated to a temporary directory
        project, session = tmp_project_session
        # hard-coded values: no need to test several owners or files,
        # this is redundant with previous test cases
        owner = session.model.get_object_from_path(owner)
        constant = create.create_imported_constant(owner, name, type_, None, visibility=visibility)
        create.add_element_to_project(project, constant)
        # the created constant must be accessible
        constant_path = '%s%s/' % (owner.get_full_path(), name)
        assert session.model.get_object_from_path(constant_path) == constant
        assert constant.type.name == type_
        create.save_all()

    nominal_sensor_data = [
        ('packageImported', 'Package:', 'int32'),
        ('rootImported', '', 'bool'),
    ]

    @pytest.mark.parametrize(
        'name, owner, type_',
        nominal_sensor_data,
        ids=[_[0] for _ in nominal_sensor_data],
    )
    def test_create_sensor(self, tmp_project_session, name, owner, type_):
        # project/session must have been duplicated to a temporary directory
        project, session = tmp_project_session
        owner = session.model.get_object_from_path(owner)
        sensor = create.create_sensor(owner, name, type_, None)
        create.add_element_to_project(project, sensor)
        # the created constant must be accessible
        sensor_path = '%s%s/' % (owner.get_full_path(), name)
        assert session.model.get_object_from_path(sensor_path) == sensor
        assert sensor.type.name == type_
        create.save_all()
