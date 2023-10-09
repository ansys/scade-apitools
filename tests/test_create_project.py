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
Test suite for create/project.py.

Test strategy:

The tests of this module operate make a copy of a reference project and add project
elements. The project is saved once all the tests of a class are executed.

The status of the tests cases is assessed by ensuring the functions execute properly and
by testing a few properties of the created data: This gives enough confidence for the
correctness of the execution. Indeed, it is not easy to compare the resulting project
to some expected result, nor easy to maintain.

Anyways, the result projects can be exmined after the execution of the tests, for a deep analysis.
"""

from typing import List, Union

import pytest

import ansys.scade.apitools.create as create

# import std from prj to ensure import order: models after apitools
# import scade.model.project.stdproject as std
from ansys.scade.apitools.create.project import std
from test_utils import get_resources_dir


# utilities (to be moved to query?)
def get_elements(parent: Union[std.Project, std.Folder]) -> List[std.Element]:
    return parent.roots if isinstance(parent, std.Project) else parent.elements


def find_element(project: std.Project, path: str) -> std.Annotable:
    parent = project
    if not path:
        # root
        return parent
    names = path.split('/')
    for name in names[:-2]:
        parent = next(
            _ for _ in get_elements(parent) if isinstance(_, std.Folder) and _.name == name
        )
    name = names[-1]
    return next(_ for _ in get_elements(parent) if _.name == name)


def find_configuration(project: std.Project, name: str) -> std.Configuration:
    return next((_ for _ in project.configurations if _.name == name), None)


@pytest.mark.project(get_resources_dir() / 'resources' / 'CreateProject' / 'CreateProject.etp')
class TestCreateProject:
    nominal_folder_data = [
        ('', 'Root Folder', None),
        ('Folder', 'Child', '.txt'),
    ]

    @pytest.mark.parametrize(
        'path, name, extensions',
        nominal_folder_data,
        ids=['%s-%s' % (_[0], _[1]) for _ in nominal_folder_data],
    )
    def test_create_folder(self, tmp_project_session, path, name, extensions):
        # project/session must have been duplicated to a temporary directory
        project, _ = tmp_project_session
        parent = find_element(project, path)
        assert parent
        if extensions:
            folder = create.create_folder(parent, name, extensions)
        else:
            folder = create.create_folder(parent, name)
        assert folder.name == name
        assert folder.project == project

    robustness_folder_data = [
        'Default',
        'Unknown',
    ]

    @pytest.mark.parametrize(
        'name',
        robustness_folder_data,
        ids=[_ for _ in robustness_folder_data],
    )
    def test_create_folder_robustness(self, project_session, name):
        project, _ = project_session
        conf = find_configuration(project, name)
        with pytest.raises(TypeError):
            folder = create.create_folder(conf, 'some name')

    nominal_file_ref_data = [
        ('', '$(VAR)\\Root File.txt'),
        ('Folder', '../Child.txt'),
    ]

    @pytest.mark.parametrize(
        'path, persist_as',
        nominal_file_ref_data,
        ids=['%s-%s' % (_[0], _[1]) for _ in nominal_file_ref_data],
    )
    def test_create_file_ref(self, tmp_project_session, path, persist_as):
        # project/session must have been duplicated to a temporary directory
        project, _ = tmp_project_session
        parent = find_element(project, path)
        assert parent
        file_ref = create.create_file_ref(parent, persist_as)
        assert file_ref.persist_as == persist_as
        assert file_ref.project == project

    robustness_file_ref_data = [
        'Default',
        'Unknown',
    ]

    @pytest.mark.parametrize(
        'name',
        robustness_file_ref_data,
        ids=[_ for _ in robustness_file_ref_data],
    )
    def test_create_file_ref_robustness(self, project_session, name):
        project, _ = project_session
        conf = find_configuration(project, name)
        with pytest.raises(TypeError):
            folder = create.create_file_ref(conf, 'some.name')

    nominal_prop_data = [
        ('', 'PROJECT_NO_CONF', ['1'], None),
        ('', 'PROJECT_DEFAULT', ['1'], 'Default'),
        ('Folder', 'FOLDER_NO_CONF', ['1', '2'], None),
        ('Folder', 'FOLDER_DEFAULT', [], 'Default'),
        ('FileRef.txt', 'FILE_REF_NO_CONF', ['true'], None),
        ('FileRef.txt', 'FILE_REF_DEFAULT', ['0', 'false', '<a\nb\nc>'], 'Default'),
    ]

    @pytest.mark.parametrize(
        'path, name, values, configuration',
        nominal_prop_data,
        ids=['%s-%s' % (_[0], _[1]) for _ in nominal_prop_data],
    )
    def test_create_prop(self, tmp_project_session, path, name, values, configuration):
        # project/session must have been duplicated to a temporary directory
        project, _ = tmp_project_session
        element = find_element(project, path)
        assert element
        conf = find_configuration(project, configuration)
        prop = create.create_prop(element, conf, name, values)
        assert prop.name == name
        assert prop.values == values
        assert prop.entity == element

    robustness_prop_data = [
        'Default',
        'Unknown',
    ]

    @pytest.mark.parametrize(
        'name',
        robustness_prop_data,
        ids=[_ for _ in robustness_prop_data],
    )
    def test_create_prop_robustness(self, project_session, name):
        project, _ = project_session
        conf = find_configuration(project, name)
        with pytest.raises(TypeError):
            folder = create.create_prop(conf, None, 'some.name', ['some value'])

    nominal_configuration_data = [
        'KCG',
    ]

    @pytest.mark.parametrize(
        'name',
        nominal_configuration_data,
        ids=[_ for _ in nominal_configuration_data],
    )
    def test_create_configuration(self, tmp_project_session, name):
        # project/session must have been duplicated to a temporary directory
        project, _ = tmp_project_session
        print('create conf with', name)
        configuration = create.create_configuration(project, name)
        print('result', configuration)
        assert configuration.name == name

    robustness_configuration_data = [
        'Default',
        'Unknown',
    ]

    @pytest.mark.parametrize(
        'name',
        robustness_configuration_data,
        ids=[_ for _ in robustness_configuration_data],
    )
    def test_create_configuration_robustness(self, project_session, name):
        project, _ = project_session
        conf = find_configuration(project, name)
        with pytest.raises(TypeError):
            configuration = create.create_configuration(conf, 'some name')

    robustness_project_data = [
        'Default',
        'Unknown',
    ]

    @pytest.mark.parametrize(
        'name',
        robustness_project_data,
        ids=[_ for _ in robustness_project_data],
    )
    def test_save_project_robustness(self, project_session, name):
        project, _ = project_session
        conf = find_configuration(project, name)
        with pytest.raises(TypeError):
            configuration = create.save_project(conf)
