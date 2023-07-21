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
Test suite for prop.type.py.

Test strategy:

* Use the queries on a set of types and/or typed objects.
* Typed objects' types allows accessing anonymous or polymorphic types.
"""

import pytest
import scade.model.suite as suite

# shall modify sys.path to access SCACE APIs
import ansys.scade.apitools.query as query
from conftest import load_session
from test_utils import get_resources_dir

# some arbitrary data for testing the pragma values
json_data = {'bool': True, 'Number': 42, 'text': 'a\nb'}
text_data = 'Text pragma Ada'


@pytest.fixture(scope='session')
def model():
    """Unique instance of the test model QueryType."""
    pathname = get_resources_dir() / 'resources' / 'QueryType' / 'QueryType.etp'
    return load_session(pathname).model


def format_test_data(data: list) -> tuple:
    """Add an id to each data, assuming the first element is a Scade path."""
    return [pytest.param(*_, id=_[0].split(':')[-1].strip('/')) for _ in data]


@pytest.mark.parametrize(
    'path, expected',
    format_test_data(
        [
            # typed objects
            ("Typed::anonymousArray/", "int8 ^1"),
            ("Typed::anonymousStructure/", "{f1 : bool, f2 : int32}"),
            ("Typed::predefined/", "int8"),
            ("Typed::speed/", "Speed"),
            ("Typed::color/", "Color"),
            ("Typed::noType/", "<null>"),
            ("Typed::O/N/", "uint32"),
            ("Typed::O/sized/", "signed<<N>>"),
            ("Typed::O/generic/", "'T"),
            ("Typed::O/array/", "'T ^N"),
        ]
    ),
)
def test_get_type_name(model, path, expected):
    typed = model.get_object_from_path(path)
    assert typed
    name = query.get_type_name(typed.type)
    assert name == expected


@pytest.mark.parametrize(
    'path, expected',
    format_test_data(
        [
            # types
            ("Types::ImportedScalar/", "ImportedScalar"),
            ("Types::Imported/", "Imported"),
            ("Types::ArrayScalar/", "ArrayScalar"),
            ("Types::Structure/", "Structure"),
            ("Types::ArrayStruct/", "ArrayStruct"),
            ("Types::Matrix/", "Matrix"),
            ("Types::Vector/", "Vector"),
            ("Types::Real/", "float32"),
            ("Types::Speed/", "float32"),
            ("Types::Enumeration/", "Enumeration"),
            ("Types::Color/", "Enumeration"),
            ("Types::Sized/", "Sized"),
            ("Types::ArrayArray/", "ArrayArray"),
            # typed objects
            ("Typed::anonymousArray/", "int8 ^1"),
            ("Typed::anonymousStructure/", "{f1 : bool, f2 : int32}"),
            ("Typed::predefined/", "int8"),
            ("Typed::speed/", "float32"),
            ("Typed::color/", "Enumeration"),
            ("Typed::noType/", "<null>"),
            ("Typed::O/N/", "uint32"),
            ("Typed::O/sized/", "signed<<N>>"),
            ("Typed::O/generic/", "'T"),
            ("Typed::O/array/", "'T ^N"),
        ]
    ),
)
def test_get_leaf_alias(model, path, expected):
    typed = model.get_object_from_path(path)
    assert typed
    type_ = typed if isinstance(typed, suite.NamedType) else typed.type
    leaf_alias = query.get_leaf_alias(type_)
    assert query.get_type_name(leaf_alias) == expected


@pytest.mark.parametrize(
    'path, expected',
    format_test_data(
        [
            # types
            ("Types::ImportedScalar/", "ImportedScalar"),
            ("Types::Imported/", "Imported"),
            ("Types::ArrayScalar/", "bool ^2"),
            ("Types::Structure/", "{f1 : bool, f2 : int32}"),
            ("Types::ArrayStruct/", "Structure ^3"),
            ("Types::Matrix/", "Vector ^3"),
            ("Types::Vector/", "Real ^2"),
            ("Types::Real/", "float32"),
            ("Types::Speed/", "float32"),
            ("Types::Enumeration/", "enum {BLUE, WHITE, RED}"),
            ("Types::Color/", "enum {BLUE, WHITE, RED}"),
            ("Types::Sized/", "signed<<32>>"),
            ("Types::ArrayArray/", "char ^3 ^2"),
            # typed objects
            ("Typed::anonymousArray/", "int8 ^1"),
            ("Typed::anonymousStructure/", "{f1 : bool, f2 : int32}"),
            ("Typed::predefined/", "int8"),
            ("Typed::speed/", "float32"),
            ("Typed::color/", "enum {BLUE, WHITE, RED}"),
            ("Typed::noType/", "<null>"),
            ("Typed::O/N/", "uint32"),
            ("Typed::O/sized/", "signed<<N>>"),
            ("Typed::O/generic/", "'T"),
            ("Typed::O/array/", "'T ^N"),
        ]
    ),
)
def test_get_leaf_type(model, path, expected):
    typed = model.get_object_from_path(path)
    assert typed
    type_ = typed if isinstance(typed, suite.NamedType) else typed.type
    leaf_alias = query.get_leaf_type(type_)
    assert query.get_type_name(leaf_alias) == expected


@pytest.mark.parametrize(
    'path, expected',
    format_test_data(
        [
            # types
            ("Types::ArrayScalar/", "bool"),
            ("Types::ArrayStruct/", "Structure"),
            ("Types::Matrix/", "Vector"),
            ("Types::Vector/", "Real"),
            ("Types::ArrayArray/", "char"),
            # typed objects
            ("Typed::anonymousArray/", "int8"),
            ("Typed::O/array/", "'T"),
        ]
    ),
)
def test_get_cell_type_noskip(model, path, expected):
    typed = model.get_object_from_path(path)
    assert typed
    type_ = typed if isinstance(typed, suite.NamedType) else typed.type
    leaf_alias = query.get_cell_type(type_)
    assert query.get_type_name(leaf_alias) == expected


@pytest.mark.parametrize(
    'path, expected',
    format_test_data(
        [
            # types
            ("Types::ArrayScalar/", "bool"),
            ("Types::ArrayStruct/", "Structure"),
            ("Types::Matrix/", "Real"),
            ("Types::Vector/", "Real"),
            ("Types::ArrayArray/", "char"),
            # typed objects
            ("Typed::anonymousArray/", "int8"),
            ("Typed::O/array/", "'T"),
        ]
    ),
)
def test_get_cell_type_skip(model, path, expected):
    typed = model.get_object_from_path(path)
    assert typed
    type_ = typed if isinstance(typed, suite.NamedType) else typed.type
    leaf_alias = query.get_cell_type(type_, skip_alias=True)
    assert query.get_type_name(leaf_alias) == expected


@pytest.mark.parametrize(
    'path',
    format_test_data(
        [
            # types
            ("Types::Imported/",),
            ("Types::Structure/",),
            ("Types::Speed/",),
            ("Types::Color/",),
            ("Types::Sized/",),
            # typed objects
            ("Typed::anonymousStructure/",),
            ("Typed::noType/",),
            ("Typed::O/generic/",),
        ]
    ),
)
def test_get_cell_type_robustness(model, path):
    typed = model.get_object_from_path(path)
    assert typed
    type_ = typed if isinstance(typed, suite.NamedType) else typed.type
    with pytest.raises(TypeError):
        query.get_cell_type(type_)


@pytest.mark.parametrize(
    'path, expected',
    format_test_data(
        [
            # types
            ("Types::Imported/", False),
            ("Types::ArrayScalar/", True),
            ("Types::Structure/", False),
            ("Types::ArrayStruct/", True),
            ("Types::Matrix/", True),
            ("Types::Vector/", True),
            ("Types::Real/", False),
            ("Types::Enumeration/", False),
            ("Types::Sized/", False),
            ("Types::ArrayArray/", True),
            # typed objects
            ("Typed::anonymousArray/", True),
            ("Typed::anonymousStructure/", False),
            ("Typed::noType/", False),
            ("Typed::O/N/", False),
            ("Typed::O/sized/", False),
            ("Typed::O/generic/", False),
            ("Typed::O/array/", True),
        ]
    ),
)
def test_is_array(model, path, expected):
    typed = model.get_object_from_path(path)
    assert typed
    type_ = typed if isinstance(typed, suite.NamedType) else typed.type
    status = query.is_array(type_)
    assert status == expected


@pytest.mark.parametrize(
    'path, expected',
    format_test_data(
        [
            # types
            ("Types::Imported/", False),
            ("Types::ArrayScalar/", False),
            ("Types::Structure/", True),
            ("Types::ArrayStruct/", False),
            ("Types::Enumeration/", False),
            ("Types::Sized/", False),
            # typed objects
            ("Typed::anonymousArray/", False),
            ("Typed::anonymousStructure/", True),
            ("Typed::noType/", False),
            ("Typed::O/N/", False),
            ("Typed::O/generic/", False),
            ("Typed::O/array/", False),
        ]
    ),
)
def test_is_structure(model, path, expected):
    typed = model.get_object_from_path(path)
    assert typed
    type_ = typed if isinstance(typed, suite.NamedType) else typed.type
    status = query.is_structure(type_)
    assert status == expected


@pytest.mark.parametrize(
    'path, expected',
    format_test_data(
        [
            # types
            ("Types::Imported/", False),
            ("Types::ArrayScalar/", False),
            ("Types::Structure/", False),
            ("Types::Vector/", False),
            ("Types::Real/", True),
            ("Types::Enumeration/", False),
            ("Types::Sized/", False),
            # typed objects
            ("Typed::anonymousArray/", False),
            ("Typed::anonymousStructure/", False),
            ("Typed::noType/", False),
            ("Typed::O/N/", True),
            ("Typed::O/sized/", False),
            ("Typed::O/generic/", False),
            ("Typed::O/array/", False),
        ]
    ),
)
def test_is_predefined(model, path, expected):
    typed = model.get_object_from_path(path)
    assert typed
    type_ = typed if isinstance(typed, suite.NamedType) else typed.type
    status = query.is_predefined(type_)
    assert status == expected


@pytest.mark.parametrize(
    'path, expected',
    format_test_data(
        [
            # types
            ("Types::Imported/", False),
            ("Types::ArrayScalar/", False),
            ("Types::Structure/", False),
            ("Types::ArrayStruct/", False),
            ("Types::Matrix/", False),
            ("Types::Vector/", False),
            ("Types::Real/", False),
            ("Types::Enumeration/", True),
            ("Types::Sized/", False),
            ("Types::ArrayArray/", False),
            # typed objects
            ("Typed::anonymousArray/", False),
            ("Typed::anonymousStructure/", False),
            ("Typed::noType/", False),
            ("Typed::O/N/", False),
            ("Typed::O/sized/", False),
            ("Typed::O/generic/", False),
            ("Typed::O/array/", False),
        ]
    ),
)
def test_is_enum(model, path, expected):
    typed = model.get_object_from_path(path)
    assert typed
    type_ = typed if isinstance(typed, suite.NamedType) else typed.type
    status = query.is_enum(type_)
    assert status == expected


@pytest.mark.parametrize(
    'path, expected',
    format_test_data(
        [
            # types
            ("Types::Imported/", True),
            ("Types::ArrayScalar/", False),
            ("Types::Structure/", False),
            ("Types::Vector/", False),
            ("Types::Real/", False),
            ("Types::Enumeration/", False),
            ("Types::Sized/", False),
            # typed objects
            ("Typed::anonymousArray/", False),
            ("Typed::anonymousStructure/", False),
            ("Typed::noType/", False),
            ("Typed::O/N/", False),
            ("Typed::O/sized/", False),
            ("Typed::O/generic/", False),
            ("Typed::O/array/", False),
        ]
    ),
)
def test_is_imported(model, path, expected):
    typed = model.get_object_from_path(path)
    assert typed
    type_ = typed if isinstance(typed, suite.NamedType) else typed.type
    status = query.is_imported(type_)
    assert status == expected


@pytest.mark.parametrize(
    'path, expected',
    format_test_data(
        [
            # types
            ("Types::Imported/", False),
            ("Types::ImportedScalar/", True),
            ("Types::ArrayScalar/", False),
            ("Types::Structure/", False),
            ("Types::Vector/", False),
            ("Types::Real/", True),
            ("Types::Enumeration/", True),
            ("Types::Sized/", True),
            # typed objects
            ("Typed::anonymousArray/", False),
            ("Typed::anonymousStructure/", False),
            ("Typed::noType/", False),
            ("Typed::O/N/", True),
            ("Typed::O/sized/", True),
            ("Typed::O/generic/", False),
            ("Typed::O/array/", False),
        ]
    ),
)
def test_is_scalar(model, path, expected):
    typed = model.get_object_from_path(path)
    assert typed
    type_ = typed if isinstance(typed, suite.NamedType) else typed.type
    status = query.is_scalar(type_)
    assert status == expected


@pytest.mark.parametrize(
    'path',
    format_test_data(
        [
            # types
            ("Types::ImportedScalar/",),
        ]
    ),
)
def test_is_scalar_robustness(model, path):
    typed = model.get_object_from_path(path)
    assert typed
    type_ = typed if isinstance(typed, suite.NamedType) else typed.type
    with pytest.raises(ValueError):
        query.is_scalar(type_, target='Python')
