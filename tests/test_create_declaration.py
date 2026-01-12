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
from typing import Optional

import pytest

import ansys.scade.apitools.create as create

# import suite from declaration to ensure import order: models after apitools
# import scade.model.suite as suite
from ansys.scade.apitools.create.declaration import suite

# import std from prj to ensure import order: models after apitools
# import scade.model.project.stdproject as std
from ansys.scade.apitools.create.project import std
from test_utils import get_resources_dir


def _get_path(project: std.Project, rel_path: str) -> Optional[Path]:
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
        ('PackageImportedType', 'Package:', 'ExternalTypes.h', None),
        ('RootImportedType', '', 'ExternalTypes.h', None),
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

    nominal_graphical_operator_data = [
        # nominal uses cases
        ('PackageOperator', 'Package:', create.VK.PUBLIC),
        ('RootOperator', '', create.VK.PRIVATE),
    ]

    @pytest.mark.parametrize(
        'name, owner, visibility',
        nominal_graphical_operator_data,
        ids=[_[0] for _ in nominal_graphical_operator_data],
    )
    def test_create_graphical_operator(self, tmp_project_session, name, owner, visibility):
        # project/session must have been duplicated to a temporary directory
        project, session = tmp_project_session
        owner = session.model.get_object_from_path(owner)
        operator = create.create_graphical_operator(owner, name, None, visibility=visibility)
        # add the unit to the project
        create.add_element_to_project(project, operator, folder=None, default=True)
        # the created operator must be accessible
        operator_path = '%s%s/' % (owner.get_full_path(), name)
        assert session.model.get_object_from_path(operator_path) == operator
        assert isinstance(operator.diagrams[0], suite.NetDiagram)
        assert operator.visibility == visibility.value
        create.save_all()

    nominal_textual_operator_data = [
        # nominal uses cases
        ('PackageNode', 'Package:', True),
        ('RootFuntion', '', False),
    ]

    @pytest.mark.parametrize(
        'name, owner, state',
        nominal_textual_operator_data,
        ids=[_[0] for _ in nominal_textual_operator_data],
    )
    def test_create_textual_operator(self, tmp_project_session, name, owner, state):
        # project/session must have been duplicated to a temporary directory
        project, session = tmp_project_session
        owner = session.model.get_object_from_path(owner)
        operator = create.create_textual_operator(owner, name, None, state=state)
        # add the unit to the project
        create.add_element_to_project(project, operator, folder=None, default=True)
        # the created operator must be accessible
        operator_path = '%s%s/' % (owner.get_full_path(), name)
        assert session.model.get_object_from_path(operator_path) == operator
        assert isinstance(operator.diagrams[0], suite.TextDiagram)
        assert operator.state == state
        create.save_all()

    nominal_imported_operator_data = [
        # nominal uses cases
        ('PackageImportedOp', 'Package:', None),
        ('RootImportedOp', '', 'Operator.c'),
    ]

    @pytest.mark.parametrize(
        'name, owner, file',
        nominal_imported_operator_data,
        ids=[_[0] for _ in nominal_imported_operator_data],
    )
    def test_create_imported_operator(self, tmp_project_session, name, owner, file):
        # project/session must have been duplicated to a temporary directory
        project, session = tmp_project_session
        owner = session.model.get_object_from_path(owner)
        operator = create.create_imported_operator(owner, name, None)
        # add the unit to the project
        create.add_element_to_project(project, operator, folder=None, default=True)
        if file:
            create.add_imported_to_project(project, operator, file)
        # the created operator must be accessible
        operator_path = '%s%s/' % (owner.get_full_path(), name)
        assert session.model.get_object_from_path(operator_path) == operator
        assert len(operator.diagrams) == 0
        create.save_all()

    set_specialized_operator_data = [
        # nominal uses cases
        ('Operator', create.ParamImportedError),
        ('Imported', None),
    ]

    @pytest.mark.parametrize(
        'specialized, exception',
        set_specialized_operator_data,
        ids=[_[0] for _ in set_specialized_operator_data],
    )
    def test_specialized_operator(self, tmp_project_session, specialized, exception):
        # project/session must have been duplicated to a temporary directory
        project, session = tmp_project_session
        specialized = session.model.get_object_from_path(specialized)
        name = 'Specializing%s' % specialized.name
        operator = create.create_graphical_operator(session.model, name, None)
        create.add_element_to_project(project, operator, folder=None, default=True)
        if exception:
            with pytest.raises(exception):
                create.set_specialized_operator(operator, specialized)
        else:
            create.set_specialized_operator(operator, specialized)
            create.save_all()

    nominal_operator_io_vars_data = [
        ([('zero', 'bool')], 'one'),
        ([('two', 'char')], 'three'),
        ([('four', 'int32'), ('five', 'float64')], None),
        ([('six', "'T")], 'unknown'),
    ]
    nominal_io_operator_kind_data = [
        ('inputs'),
        ('hiddens'),
        ('outputs'),
    ]

    @pytest.mark.parametrize(
        'vars, before',
        nominal_operator_io_vars_data,
        ids=[_[0][0][0] for _ in nominal_operator_io_vars_data],
    )
    @pytest.mark.parametrize(
        'kind',
        nominal_io_operator_kind_data,
        ids=[_[0] for _ in nominal_io_operator_kind_data],
    )
    def test_add_operator_io_nominal(self, tmp_project_session, kind, vars, before):
        # project/session must have been duplicated to a temporary directory
        project, session = tmp_project_session
        # hardcoded for operator IO
        operator = session.model.get_object_from_path('IO')
        fct = {
            'inputs': create.add_operator_inputs,
            'hiddens': create.add_operator_hidden,
            'outputs': create.add_operator_outputs,
        }[kind]
        # add the prefix to vars and before
        prefix = kind[0]
        before = None if not before else kind[0] + before.capitalize()
        vars = [(prefix + _[0].capitalize(), _[1]) for _ in vars]
        # store the names for some minimal verifications
        names = {_.name for _ in getattr(operator, kind)}
        names |= {_[0] for _ in vars}
        # add the ios
        before = next((_ for _ in getattr(operator, kind) if _.name == before), None)
        result = fct(operator, vars, before)
        # some verifications...
        assert [_.name for _ in result] == [_[0] for _ in vars]
        assert names == {_.name for _ in getattr(operator, kind)}
        # finally, make sure the created elements can be accessed
        for io in result:
            io_path = '%s%s/' % (operator.get_full_path(), io.name)
            assert session.model.get_object_from_path(io_path) == io
        create.save_all()

    robstness_operator_io_data = [
        ([('zero', 'bool')], 'IOOther/other'),
    ]

    @pytest.mark.parametrize(
        'vars, before',
        robstness_operator_io_data,
        ids=[_[0][0][0] for _ in robstness_operator_io_data],
    )
    def test_add_operator_io_robustness(self, tmp_project_session, vars, before):
        # project/session must have been duplicated to a temporary directory
        project, session = tmp_project_session
        # hardcoded for operator IO
        operator = session.model.get_object_from_path('IO')
        before = session.model.get_object_from_path(before)
        with pytest.raises(create.IllegalIOError):
            create.add_operator_inputs(operator, vars, before)

    nominal_operator_parameters_data = [
        (['A'], 'IO/B'),
        (['B'], 'IO/A'),
        (['C', 'D'], None),
    ]

    @pytest.mark.parametrize(
        'parameters, before',
        nominal_operator_parameters_data,
        ids=[_[0][0] for _ in nominal_operator_parameters_data],
    )
    def test_add_operator_parameters_nominal(self, tmp_project_session, parameters, before):
        # project/session must have been duplicated to a temporary directory
        project, session = tmp_project_session
        # hardcoded for operator IO
        operator = session.model.get_object_from_path('IO')
        # add the prefix to vars and before
        before = session.model.get_object_from_path(before) if before else None
        # store the names for some minimal verifications
        names = {_.name for _ in operator.parameters}
        names |= set(parameters)
        # add the parameters
        result = create.add_operator_parameters(operator, parameters, before)
        # some verifications...
        assert [_.name for _ in result] == parameters
        assert names == {_.name for _ in operator.parameters}
        # finally, make sure the created elements can be accessed
        for parameter in result:
            parameter_path = '%s%s/' % (operator.get_full_path(), parameter.name)
            assert session.model.get_object_from_path(parameter_path) == parameter
        create.save_all()

    robstness_operator_parameters_data = [
        (['N'], 'IOOther/OTHER'),
    ]

    @pytest.mark.parametrize(
        'parameters, before',
        robstness_operator_parameters_data,
        ids=[_[0][0] for _ in robstness_operator_parameters_data],
    )
    def test_add_operator_parameters_robustness(self, tmp_project_session, parameters, before):
        # project/session must have been duplicated to a temporary directory
        project, session = tmp_project_session
        # hardcoded for operator IO
        operator = session.model.get_object_from_path('IO')
        before = session.model.get_object_from_path(before)
        with pytest.raises(create.IllegalIOError):
            create.add_operator_parameters(operator, parameters, before)

    type_constraint_data = [
        ('t1', 'numeric', None),
        ('t2', 'integer', None),
        ('t3', 'signed', None),
        ('t4', 'unsigned', None),
        ('t5', 'float', None),
        ('tu', 'unknown', Exception),
    ]

    @pytest.mark.parametrize(
        'name, constraint, exception',
        type_constraint_data,
        ids=[_[0] for _ in type_constraint_data],
    )
    def test_type_constraint(self, tmp_project_session, name, constraint, exception):
        # project/session must have been duplicated to a temporary directory
        project, session = tmp_project_session
        # hardcoded for operator IO
        operator = session.model.get_object_from_path('IO')
        io = create.add_operator_inputs(operator, [(name, ("'%s" % name).capitalize())], None)[0]
        if exception:
            with pytest.raises(exception):
                create.set_type_constraint(io.type, constraint)
        else:
            create.set_type_constraint(io.type, constraint)
            create.save_all()
