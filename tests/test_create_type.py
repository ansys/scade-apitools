# Copyright (C) 2023 ANSYS, Inc. and/or its affiliates.
# SPDX-FileCopyrightText: 2023 ANSYS, Inc. All rights reserved.

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
from ansys.scade.apitools.create.scade import _link_pendings, suite
from ansys.scade.apitools.create.type import TX, _build_type, _normalize_tree
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


def _tree_to_string(tree: TX, context: suite.Object) -> str:
    """Create a type and return its textual representation."""
    type_ = _build_type(tree, context) if tree else None
    # link pending references so that to_string gives the expected result
    _link_pendings()
    return type_.to_string().strip() if type_ else ''


@pytest.mark.project(get_resources_dir() / 'resources' / 'CreateType' / 'CreateType.etp')
class TestCreateType:
    create_sized_data = [
        # nominal
        ([False, 8], 'unsigned<<8>>'),
        ([True, '16'], 'signed<<16>>'),
        ([False, 32], 'unsigned<<32>>'),
        ([True, '64'], 'signed<<64>>'),
        ([True, '@N/'], 'signed<<N>>'),
        # robustness
        ([False, 4], ValueError),
    ]

    @pytest.mark.parametrize(
        'args, expected',
        create_sized_data,
        ids=[str(_[0]) for _ in create_sized_data],
    )
    def test_create_sized(self, project_session, args, expected):
        _, session = project_session
        args = _pre_process_type_tree(session.model, args)
        if isinstance(expected, str):
            # nominal
            tree = create.create_sized(*args)
            assert _tree_to_string(tree, session.model) == expected
        else:
            # robustness
            with pytest.raises(expected):
                tree = create.create_sized(*args)

    create_table_data = [
        # nominal
        # arrays
        ([[3], 'int8'], 'int8 ^3'),
        ([9, 'float64'], 'float64 ^9'),
        (['@N/', 'char'], 'char ^N'),
        ([[3, 4], 'bool'], 'bool ^3 ^4'),
        # robustness
        ([[], 'int8'], ValueError),
    ]

    @pytest.mark.parametrize(
        'args, expected',
        create_table_data,
        ids=[str(_[0]) for _ in create_table_data],
    )
    def test_create_table(self, project_session, args, expected):
        _, session = project_session
        args = _pre_process_type_tree(session.model, args)
        if isinstance(expected, str):
            # nominal
            tree = create.create_table(*args)
            assert _tree_to_string(tree, session.model) == expected
        else:
            # robustness
            with pytest.raises(expected):
                tree = create.create_table(*args)

    create_structure_data = [
        # nominal
        # structure
        ([('r', 'float32'), ('i', 'float32')], '{r : float32, i : float32}'),
        ([('none', None)], '{none : _null}'),
        # robustness
        ([], ValueError),
    ]

    @pytest.mark.parametrize(
        'args, expected',
        create_structure_data,
        ids=[str(_[0]) for _ in create_structure_data],
    )
    def test_create_structure(self, project_session, args, expected):
        _, session = project_session
        args = _pre_process_type_tree(session.model, args)
        if isinstance(expected, str):
            # nominal
            tree = create.create_structure(*args)
            assert _tree_to_string(tree, session.model) == expected
        else:
            # robustness
            with pytest.raises(expected):
                tree = create.create_structure(*args)

    # _normalize_tree is checked through the unit tests for the individual wrappers
    # the following test cases are intended for coverage of the nominal uses cases and robustness
    build_type_data = [
        # nominal
        # predefined
        ('char', 'char'),
        ('bool', 'bool'),
        ('int8', 'int8'),
        ('int16', 'int16'),
        ('int32', 'int32'),
        ('int64', 'int64'),
        ('uint8', 'uint8'),
        ('uint16', 'uint16'),
        ('uint32', 'uint32'),
        ('uint64', 'uint64'),
        ('float32', 'float32'),
        ('float64', 'float64'),
        # old predefined
        ('int', ''),
        ('real', ''),
        # type
        ('@Int32/', 'Int32 = int32'),
        # robustness
        (None, ''),
        ('unknown', ValueError),
        ([], ValueError),
        ("'T", ValueError),
        ('@N/', ValueError),
    ]
    ids = [str(_[0]) for _ in build_type_data]

    @pytest.mark.parametrize('tree, expected', build_type_data, ids=ids)
    def test_build_type(self, project_session, tree, expected):
        _, session = project_session
        tree = _pre_process_type_tree(session.model, tree)
        if isinstance(expected, str):
            # nominal
            assert _tree_to_string(tree, session.model) == expected
        else:
            # robustness
            with pytest.raises(expected):
                tree = _normalize_tree(tree)
