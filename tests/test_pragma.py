# Copyright (C) 2023 - 2025 ANSYS, Inc. and/or its affiliates.
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
Test suite for pragma.py.

Test strategy:

* Read existing pragmas and compare the values to the expected ones.
* Set a pragma and verify its value is set as expected.
"""

import pytest

# shall modify sys.path to access SCACE APIs
import ansys.scade.apitools.prop as prop
from test_utils import get_resources_dir

# some arbitrary data for testing the pragma values
json_data = {'bool': True, 'Number': 42, 'text': 'a\nb'}
text_data = 'Text pragma Ada'


@pytest.mark.project(get_resources_dir() / 'resources' / 'JsonPragma' / 'JsonPragma.etp')
class TestGetPragmaJson:
    nominal_data = [
        ('GetJson::noPragma/', 'at', {}),
        ('GetJson::pragmaDict/', 'at', json_data),
        ('GetJson::pragmaList/', 'at', [9, 11, 12, 31, 46, 81, 82]),
        ('GetJson::wrongPragma/', 'at', None),
    ]

    @pytest.mark.parametrize(
        'path, id, expected',
        nominal_data,
        ids=[_[0].split(':')[-1].strip('/') for _ in nominal_data],
    )
    def test_get_pragma_json_nominal(self, project_session, path, id, expected):
        _, session = project_session
        assert session
        assert session.model
        object_ = session.model.get_object_from_path(path)
        assert object_
        value = prop.get_pragma_json(object_, id)

        assert value == expected

    robustness_data = [
        ('GetJson::xmlPragma/', 'at'),
    ]

    @pytest.mark.parametrize(
        'path, id', robustness_data, ids=[_[0].split(':')[-1].strip('/') for _ in robustness_data]
    )
    def test_get_pragma_json_robustness(self, project_session, path, id):
        _, session = project_session
        assert session
        assert session.model
        object_ = session.model.get_object_from_path(path)
        assert object_
        with pytest.raises(TypeError):
            _ = prop.get_pragma_json(object_, id)


@pytest.mark.project(get_resources_dir() / 'resources' / 'JsonPragma' / 'JsonPragma.etp')
class TestSetPragmaJson:
    nominal_data = [
        ('SetJson::pragmaAlreadyEmpty/', 'at', {}, False),
        ('SetJson::pragmaChange/', 'at', json_data, True),
        ('SetJson::pragmaCreate/', 'at', json_data, True),
        ('SetJson::pragmaDelete/', 'at', {}, True),
        ('SetJson::pragmaUnchange/', 'at', json_data, False),
    ]

    @pytest.mark.parametrize(
        'path, id, value, expected',
        nominal_data,
        ids=[_[0].split(':')[-1].strip('/') for _ in nominal_data],
    )
    def test_set_pragma_json_nominal(self, tmp_project_session, path, id, value, expected):
        # project/session must have been duplicated to a temporary directory
        project, session = tmp_project_session
        # pathname = project.pathname
        object_ = session.model.get_object_from_path(path)
        assert object_
        status = prop.set_pragma_json(object_, id, value)
        assert status == expected
        object_.defined_in.sao_modified = True
        current = prop.get_pragma_json(object_, id)
        assert current == value

    robustness_data = [
        ('GetJson::xmlPragma/', 'at', json_data),
    ]

    @pytest.mark.parametrize(
        'path, id, value',
        robustness_data,
        ids=[_[0].split(':')[-1].strip('/') for _ in robustness_data],
    )
    def test_set_pragma_json_robustness(self, project_session, path, id, value):
        _, session = project_session
        assert session
        assert session.model
        object_ = session.model.get_object_from_path(path)
        assert object_
        with pytest.raises(TypeError):
            prop.set_pragma_json(object_, id, value)


@pytest.mark.project(get_resources_dir() / 'resources' / 'ToolPragma' / 'ToolPragma.etp')
class TestGetPragmaTool:
    nominal_data = [
        ('GetKcg::noPragma/', 'kcg', 'C:name', None),
        ('GetKcg::pragmaCName/', 'kcg', 'C:name', 'CName'),
        ('GetKcg::pragmaAdaName/', 'kcg', 'Ada:name', 'AdaName'),
        ('GetKcg::pragmaNames/', 'kcg', 'C:name', 'CName'),
        ('GetKcg::pragmaNames/', 'kcg', 'Ada:name', 'AdaName'),
        ('GetKcg::pragmaNames/', 'kcg', 'Ada:pragma', text_data),
        ('GetKcg::Scalar/', 'kcg', 'C:scalar', ''),
        ('GetKcg::Scalar/', 'kcg', 'C:initializer', '42'),
        ('GetKcg::CAll/', 'kcg', 'C:name', 'CName'),
        ('GetKcg::CAll/', 'kcg', 'C:scalar', ''),
        ('GetKcg::CAll/', 'kcg', 'manifest', ''),
    ]

    @pytest.mark.parametrize(
        'path, id, key, expected',
        nominal_data,
        ids=['%s-%s' % (_[0].split(':')[-1].strip('/'), _[2]) for _ in nominal_data],
    )
    def test_get_pragma_tool(self, project_session, path, id, key, expected):
        _, session = project_session
        assert session
        assert session.model
        object_ = session.model.get_object_from_path(path)
        assert object_
        value = prop.get_pragma_tool_text(object_, id, key)

        assert value == expected

    robustness_data = [
        ('GetTool::xmlPragma/', 'tool', 'key'),
    ]

    @pytest.mark.parametrize(
        'path, id, key',
        robustness_data,
        ids=[_[0].split(':')[-1].strip('/') for _ in robustness_data],
    )
    def test_get_pragma_tool_robustness(self, project_session, path, id, key):
        _, session = project_session
        assert session
        assert session.model
        object_ = session.model.get_object_from_path(path)
        assert object_
        with pytest.raises(TypeError):
            _ = prop.get_pragma_tool_text(object_, id, key)


@pytest.mark.project(get_resources_dir() / 'resources' / 'ToolPragma' / 'ToolPragma.etp')
class TestSetPragmaTool:
    nominal_data = [
        ('SetKcg::PragmaChange/', 'kcg', 'C:name', 'newCName', True),
        ('SetKcg::PragmaCreate/', 'kcg', 'C:name', 'CName', True),
        ('SetKcg::PragmaCreate/', 'kcg', 'manifest', '', True),
        ('SetKcg::PragmaDelete/', 'kcg', 'C:name', None, True),
        ('SetKcg::PragmaDelete/', 'kcg', 'manifest', None, True),
        ('SetKcg::PragmaEmpty/', 'kcg', 'C:name', None, False),
        ('SetKcg::PragmaEmpty/', 'kcg', 'manifest', None, False),
        ('SetKcg::PragmaUnchange/', 'kcg', 'C:name', 'CName', False),
        ('SetKcg::PragmaUnchange/', 'kcg', 'manifest', '', False),
    ]

    @pytest.mark.parametrize(
        'path, id, key, value, expected',
        nominal_data,
        ids=['%s-%s' % (_[0].split(':')[-1].strip('/'), _[2]) for _ in nominal_data],
    )
    def test_set_pragma_tool(self, tmp_project_session, path, id, key, value, expected):
        # project/session must have been duplicated to a temporary directory
        project, session = tmp_project_session
        object_ = session.model.get_object_from_path(path)
        assert object_
        if value is None:
            # suppress the pragma
            status = prop.remove_pragma_tool(object_, id, key)
        else:
            status = prop.set_pragma_tool_text(object_, id, key, value)
        assert status == expected
        object_.defined_in.sao_modified = True
        current = prop.get_pragma_tool_text(object_, id, key)
        assert current == value

    robustness_data = [
        ('SetTool::xmlPragma/', 'tool', 'key', 'any value'),
    ]

    @pytest.mark.parametrize(
        'path, id, key, value',
        robustness_data,
        ids=[_[0].split(':')[-1].strip('/') for _ in robustness_data],
    )
    def test_set_pragma_tool_robustness(self, project_session, path, id, key, value):
        _, session = project_session
        assert session
        assert session.model
        object_ = session.model.get_object_from_path(path)
        assert object_
        with pytest.raises(TypeError):
            prop.set_pragma_tool_text(object_, id, key, value)
