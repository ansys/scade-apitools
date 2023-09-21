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
Test suite for create/scade.py.

The tests of this module operate make a copy of a reference model and add model
elements. The project is saved once all the tests of a class are executed.

The status of the tests cases is assessed by ensuring the functions execute properly and
by testing a few properties of the created data: This gives enough confidence for the
correctness of the execution. Indeed, it is not easy to compare the resulting project
to some expected result, nor easy to maintain.

Anyways, the result models can be exmined after the execution of the tests, for a deep analysis.

Note: Most of the functions of the module are tested though calls to higher
level functions and thus, are not addressed here.
"""

import pytest

import ansys.scade.apitools.create as create
from test_utils import get_resources_dir


def _pre_process_type_tree(model, tree):
    """Replace all occurrences of '@path' by the corresponding model element."""
    if isinstance(tree, list):
        return [_pre_process_type_tree(model, _) for _ in tree]
    elif isinstance(tree, str):
        if tree and tree[0] == '@':
            return model.get_object_from_path(tree[1:])
    # default
    return tree


@pytest.mark.project(get_resources_dir() / 'resources' / 'CreateScade' / 'CreateScade.etp')
class TestCreateScade:
    build_type_tree_predefined_data = [
        # predefined types
        'char',
        'bool',
        # numeric types
        'int8',
        'int16',
        'int32',
        'int64',
        'uint8',
        'uint16',
        'uint32',
        'uint64',
        'float32',
        'float64',
    ]

    @pytest.mark.parametrize(
        'name',
        build_type_tree_predefined_data,
        ids=[_ for _ in build_type_tree_predefined_data],
    )
    def test_build_type_tree_predefined(self, project_session, name):
        _, session = project_session
        type_ = create._build_type_tree(session.model, name)
        assert type_.is_predefined() and type_.name == name

    build_type_tree_old_predefined_data = [
        # backward compatibility
        'int',
        'real',
    ]

    @pytest.mark.parametrize(
        'name',
        build_type_tree_old_predefined_data,
        ids=[_ for _ in build_type_tree_old_predefined_data],
    )
    def test_build_type_tree_old_predefined(self, project_session, name):
        _, session = project_session
        type_ = create._build_type_tree(session.model, name)
        # type_ is None but no exception raised
        assert not type_

    nominal_build_type_tree_data = [
        # arrays
        ('vector int8 3', ['table', [3], 'int8'], 'int8 ^3'),
        ('vector char N', ['table', ['@N/'], 'char'], 'char ^N'),
        ('matrix bool 3 4', ['table', [3, 4], 'bool'], 'bool ^3 ^4'),
        ('vector (vector bool 4) 3', ['table', [3], ['table', [4], 'bool']], 'bool ^4 ^3'),
        # structure
        ('complex', ['struct', ['r', 'float32', 'i', 'float32']], '{r : float32, i : float32}'),
        # sized types
        ('sized 8', ['unsigned', 8], 'unsigned<<8>>'),
        ('sized N', ['unsigned', '@N/'], 'unsigned<<N>>'),
        # type
        ('Int32', '@Int32/', 'Int32 = int32'),
        # None
        ('none', None, ''),
    ]

    @pytest.mark.parametrize(
        'id, tree, expected',
        nominal_build_type_tree_data,
        ids=[_[0] for _ in nominal_build_type_tree_data],
    )
    def test_build_type_tree(self, project_session, id, tree, expected):
        # id only used to identify the test cases, unused here
        _, session = project_session
        tree = _pre_process_type_tree(session.model, tree)
        type_ = create._build_type_tree(session.model, tree)
        # link pending references so that to_string gives the expected result
        create._link_pendings()
        representation = type_.to_string() if type_ else ''
        assert representation == expected

    robustness_folder_data = [
        ('unknown', 'unknown', create.TypeSyntaxError),
        ('empty', [], create.TypeSyntaxError),
        ('null struct', ['struct', []], create.TypeSyntaxError),
        ('odd struct', ['x'], create.TypeSyntaxError),
        ('syn struct more', ['struct', ['c', 'char'], 'extra'], create.TypeSyntaxError),
        ('syn struct less', ['struct'], create.TypeSyntaxError),
        ('null array', ['table', [], 'int8'], create.TypeSyntaxError),
        ('syn array more', ['table', [2], 'int8', 'extra'], create.TypeSyntaxError),
        ('syn array less', ['table', [2]], create.TypeSyntaxError),
        ('syn sized more', ['unsigned', 8, 16], create.TypeSyntaxError),
        ('syn sized less', ['unsigned'], create.TypeSyntaxError),
        ('bad type', '<model>', TypeError),
        ("'T", "'T", create.TypePolymorphicError),
    ]

    @pytest.mark.parametrize(
        'id, tree, exception',
        robustness_folder_data,
        ids=[_[0] for _ in robustness_folder_data],
    )
    def test_build_type_tree_robustness(self, project_session, id, tree, exception):
        _, session = project_session
        if tree == '<model>':
            tree = session.model
        with pytest.raises(exception):
            create._build_type_tree(session.model, tree)
