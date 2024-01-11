# Copyright (C) 2023 - 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-FileCopyrightText: 2023 ANSYS, Inc. All rights reserved.

"""
Test suite for create/expression.py.

The tests of this module operate on an empty model: these constructs must not
be used for real scripts.
"""

import pytest

import ansys.scade.apitools.create as create
from ansys.scade.apitools.create.expression import EX, _build_expression, _normalize_tree
from ansys.scade.apitools.create.scade import _link_pendings, suite


def _tree_to_string(tree: EX, context: suite.Object = None) -> str:
    """Build an expression from a tree and return textual representation."""
    expr = _build_expression(tree, context)
    # link pending references so that to_string gives the expected result
    _link_pendings()
    text = expr.to_string().strip()
    # to_string() is not deterministic for expressions: remove the indentation
    text = '\n'.join([_.strip() for _ in text.split('\n')])
    return text


create_call_data = [
    # nominal
    ('Empty', [], [], 'Empty()'),
    ('EmptySized', [], [42], '(EmptySized<<42>>)()'),
    ('Regular', [True, 1], [], 'Regular(true, 1)'),
    ('Sized', ["'O'"], [9, 31], "(Sized<<9, 31>>)('O')"),
    ('EmptySizedLx', [], 42, '(EmptySizedLx<<42>>)()'),
    ('RegularLx', [True, 1], None, 'RegularLx(true, 1)'),
    ('SizedLx', "'O'", [9, 31], "(SizedLx<<9, 31>>)('O')"),
]
ids = [_[0] for _ in create_call_data]


@pytest.mark.parametrize('name, args, inst_args, expected', create_call_data, ids=ids)
def test_create_call_nominal(name: str, args, inst_args, expected: str):
    operator = suite.Operator()
    operator.name = name
    # nominal
    if inst_args:
        tree = create.create_call(operator, args, inst_args)
    else:
        tree = create.create_call(operator, args)
    assert _tree_to_string(tree) == expected


def test_create_call_robustness():
    constant = suite.Constant()
    with pytest.raises(TypeError):
        _ = create.create_call(constant, [])


def test_create_higher_order_call_robustness():
    constant = suite.Constant()
    with pytest.raises(TypeError):
        _ = create.create_higher_order_call(constant, [], [])


create_unary_data = [
    # nominal
    # logical
    ('!', True, 'not true'),
    # arithmetic
    ('-', 9, '- 9'),
    ('+', 31, '+ 31'),
    # bitwise
    ('lnot', 12, 'lnot 12'),
    # casts for Scade < 6.5
    ('int', 65.0, ''),
    ('real', 81, ''),
    # robustness
    # unknown operator
    ('x', True, create.ExprSyntaxError),
]
ids = [_[0] for _ in create_unary_data]


@pytest.mark.parametrize('symbol, arg, expected', create_unary_data, ids=ids)
def test_create_unary(symbol, arg, expected):
    if isinstance(expected, str):
        # nominal
        tree = create.create_unary(symbol, arg)
        assert _tree_to_string(tree) == expected
    else:
        # robustness
        with pytest.raises(expected):
            _ = create.create_unary(symbol, arg)


create_binary_data = [
    # nominal
    # logical
    ('&', True, True, 'true and true'),
    ('|', True, False, 'true or false'),
    ('^', False, True, 'false xor true'),
    ('#', False, False, '# (false, false)'),
    # arithmetic
    ('-', 9, 12, '9 - 12'),
    ('+', 31, 32, '31 + 32'),
    ('*', 81, 82, '81 * 82'),
    ('/', 46, 65, '46 / 65'),
    ('%', 99, 11, '99 mod 11'),
    # comparison
    ('<', 9, 12, '9 < 12'),
    ('>', 31, 32, '31 > 32'),
    ('=', 81, 82, '81 = 82'),
    ('<>', 46, 65, '46 <> 65'),
    ('<=', 42, 69, '42 <= 69'),
    ('>=', 99, 11, '99 >= 11'),
    # bitwise
    ('land', 9, 12, '9 land 12'),
    ('lor', 31, 32, '31 lor 32'),
    ('lxor', 81, 82, '81 lxor 82'),
    ('<<', 42, 69, '42 lsl 69'),
    ('>>', 99, 11, '99 lsr 11'),
    # arithmetic for Scade < 6.5
    (':', 42, 69, ''),
    # robustness
    # unknown operator
    ('x', True, False, create.ExprSyntaxError),
]
ids = [_[0] for _ in create_binary_data]


@pytest.mark.parametrize('symbol, arg1, arg2, expected', create_binary_data, ids=ids)
def test_create_binary(symbol: str, arg1, arg2, expected):
    if isinstance(expected, str):
        # nominal
        tree = create.create_binary(symbol, arg1, arg2)
        assert _tree_to_string(tree) == expected
    else:
        # robustness
        with pytest.raises(expected):
            _ = create.create_binary(symbol, arg1, arg2)


create_nary_data = [
    # nominal
    # logical
    ('&', (True, True), 'true and true'),
    ('|', (True, False, True), 'true or false or true'),
    ('^', (False, True, False), 'false xor true xor false'),
    ('#', (False, False, False, True), '# (false, false, false, true)'),
    # arithmetic
    ('+', (9, 12, 31, 32), '9 + 12 + 31 + 32'),
    ('*', (46, 65, 81, 82), '46 * 65 * 81 * 82'),
    # robustness
    # unknown operator
    ('x', [0, 1, 2], create.ExprSyntaxError),
    # not enough operands
    ('+', [], create.ExprSyntaxError),
    ('*', [0], create.ExprSyntaxError),
]
ids = [_[0] for _ in create_nary_data]


@pytest.mark.parametrize('symbol, args, expected', create_nary_data, ids=ids)
def test_create_nary(symbol: str, args, expected):
    if isinstance(expected, str):
        # nominal
        tree = create.create_nary(symbol, *args)
        assert _tree_to_string(tree) == expected
    else:
        # robustness
        with pytest.raises(expected):
            _ = create.create_nary(symbol, *args)


create_if_data = [
    # nominal
    ('if-single', True, [0], [1], 'if true then (0) else (1)'),
    ('if-singlelx', True, 0, 1, 'if true then (0) else (1)'),
    ('if-double', False, [0, 1], [2, 3], 'if false then (0, 1) else (2, 3)'),
    # robustness
    ('empty', True, [], [False], create.EmptyTreeError),
    ('diff', False, [0], [1, 2], create.ExprSyntaxError),
]
ids = [_[0] for _ in create_if_data]


@pytest.mark.parametrize('id, condition, thens, elses, expected', create_if_data, ids=ids)
def test_create_if(id: str, condition, thens, elses, expected):
    if isinstance(expected, str):
        # nominal
        tree = create.create_if(condition, thens, elses)
        assert _tree_to_string(tree) == expected
    else:
        # robustness
        with pytest.raises(expected):
            _ = create.create_if(condition, thens, elses)


create_case_data = [
    # nominal
    ('single', True, [("'A'", 65)], None, "( case true of\n| 'A' :   65)"),
    (
        'double',
        1,
        [(0, 'false'), (1, 'true')],
        None,
        '( case 1 of\n| 0 :   false\n| 1 :   true)',
    ),
    ('default', 6, [(1, 2), (3, 4)], 5, '( case 6 of\n| 1 :   2\n| 3 :   4\n| _ :   5)'),
    # robustness
    ('empty', False, [], None, create.ExprSyntaxError),
]
ids = [_[0] for _ in create_case_data]


@pytest.mark.parametrize('id, selector, args, default, expected', create_case_data, ids=ids)
def test_create_case(id: str, selector, args, default, expected):
    if isinstance(expected, str):
        # nominal
        if default:
            tree = create.create_case(selector, args, default)
        else:
            tree = create.create_case(selector, args)
        assert _tree_to_string(tree) == expected
    else:
        # robustness
        with pytest.raises(expected):
            _ = create.create_case(selector, args, default)


create_make_data = [
    # nominal
    ('Single', [42], suite.NamedType, '(make Single)(42)'),
    ('Double', [False, 42], suite.NamedType, '(make Double)(false, 42)'),
    # robustness
    ('Empty', [], suite.NamedType, create.ExprSyntaxError),
    ('Constant', [0, 1, 2], suite.Constant, TypeError),
]
ids = [_[0] for _ in create_make_data]


@pytest.mark.parametrize('name, args, class_, expected', create_make_data, ids=ids)
def test_create_make(name: str, args, class_, expected):
    type_ = class_()
    type_.name = name
    if isinstance(expected, str):
        # nominal
        tree = create.create_make(type_, *args)
        assert _tree_to_string(tree) == expected
    else:
        # robustness
        with pytest.raises(expected):
            _ = create.create_make(type_, *args)


create_flatten_data = [
    # nominal
    ('Type', 42, suite.NamedType, '(flatten Type)(42)'),
    # robustness
    ('Constant', False, suite.Constant, TypeError),
]
ids = [_[0] for _ in create_flatten_data]


@pytest.mark.parametrize('name, arg, class_, expected', create_flatten_data, ids=ids)
def test_create_flatten(name: str, arg, class_, expected):
    type_ = class_()
    type_.name = name
    if isinstance(expected, str):
        # nominal
        tree = create.create_flatten(type_, arg)
        assert _tree_to_string(tree) == expected
    else:
        # robustness
        with pytest.raises(expected):
            _ = create.create_flatten(type_, arg)


create_scalar_to_vector_data = [
    # nominal
    (1, [42], '42 ^ 1'),
    (2, [9, 31], '(9, 31) ^ 2'),
    # robustness
    (0, [], create.ExprSyntaxError),
]
ids = [_[0] for _ in create_scalar_to_vector_data]


@pytest.mark.parametrize('size, args, expected', create_scalar_to_vector_data, ids=ids)
def test_create_scalar_to_vector(size, args, expected):
    if isinstance(expected, str):
        # nominal
        tree = create.create_scalar_to_vector(size, *args)
        assert _tree_to_string(tree) == expected
    else:
        # robustness
        with pytest.raises(expected):
            _ = create.create_scalar_to_vector(size, *args)


create_data_array_data = [
    # nominal
    ('single', [42], '[42]'),
    ('double', [False, True], '[false, true]'),
    # robustness
    ('empty', [], create.ExprSyntaxError),
]
ids = [_[0] for _ in create_data_array_data]


@pytest.mark.parametrize('id, args, expected', create_data_array_data, ids=ids)
def test_create_data_array(id: str, args, expected):
    if isinstance(expected, str):
        # nominal
        tree = create.create_data_array(*args)
        assert _tree_to_string(tree) == expected
    else:
        # robustness
        with pytest.raises(expected):
            _ = create.create_data_array(*args)


create_data_struct_data = [
    # nominal
    ('single', [('one', 1)], '{one : 1}'),
    ('double', [('one', 1), ('two', 2)], '{one : 1, two : 2}'),
    # robustness
    ('empty', [], create.ExprSyntaxError),
    ('empty embed', [('one', []), ('four', 4)], create.EmptyTreeError),
    ('not ident', [('not ident', 1)], create.TypeIdentifierError),
    ('number', [(0, 1)], create.TypeIdentifierError),
]
ids = [_[0] for _ in create_data_struct_data]


@pytest.mark.parametrize('id, args, expected', create_data_struct_data, ids=ids)
def test_create_data_struct(id: str, args, expected):
    if isinstance(expected, str):
        # nominal
        tree = create.create_data_struct(*args)
        assert _tree_to_string(tree) == expected
    else:
        # robustness
        with pytest.raises(expected):
            _ = create.create_data_struct(*args)


create_prj_data = [
    # nominal
    ('index', [42], 'index[42]'),
    ('field', ['a'], 'field.a'),
    ('mixed', [9, 'b', 31], 'mixed[9].b[31]'),
    ('indexlx', 42, 'indexlx[42]'),
    ('fieldlx', 'a', 'fieldlx.a'),
    # robustness
    ('empty', [], create.EmptyTreeError),
]
ids = [_[0] for _ in create_prj_data]


@pytest.mark.parametrize('name, path, expected', create_prj_data, ids=ids)
def test_create_prj(name: str, path, expected):
    c = suite.Constant()
    c.name = name
    if isinstance(expected, str):
        # nominal
        tree = create.create_prj(c, path)
        assert _tree_to_string(tree) == expected
    else:
        # robustness
        with pytest.raises(expected):
            _ = create.create_prj(c, path)


create_prj_dyn_data = [
    # nominal
    ('index', [42], False, '(index.[42] default false)'),
    ('field', ['a', -1], 0, '(field. .a[(-1)] default 0)'),
    ('mixed', [9, 'b', 31], "' '", "(mixed.[9].b[31] default ' ')"),
    ('indexlx', 42, False, '(indexlx.[42] default false)'),
    # robustness
    ('empty', [], 0, create.EmptyTreeError),
]
ids = [_[0] for _ in create_prj_dyn_data]


@pytest.mark.parametrize('name, path, default, expected', create_prj_dyn_data, ids=ids)
def test_create_prj_dyn(name: str, path, default, expected):
    c = suite.Constant()
    c.name = name
    if isinstance(expected, str):
        # nominal
        tree = create.create_prj_dyn(c, path, default)
        assert _tree_to_string(tree) == expected
    else:
        # robustness
        with pytest.raises(expected):
            _ = create.create_prj_dyn(c, path, default)


create_change_ith_data = [
    # nominal
    ('index', [42], False, '(index with [42] = false)'),
    ('field', ['a', -1], 0, '(field with .a[(-1)] = 0)'),
    ('mixed', [9, 'b', 31], "' '", "(mixed with [9].b[31] = ' ')"),
    ('indexlx', 42, False, '(indexlx with [42] = false)'),
    # robustness
    ('empty', [], 0, create.EmptyTreeError),
]
ids = [_[0] for _ in create_change_ith_data]


@pytest.mark.parametrize('name, path, value, expected', create_change_ith_data, ids=ids)
def test_create_change_ith(name: str, path, value, expected):
    c = suite.Constant()
    c.name = name
    if isinstance(expected, str):
        # nominal
        tree = create.create_change_ith(c, path, value)
        assert _tree_to_string(tree) == expected
    else:
        # robustness
        with pytest.raises(expected):
            _ = create.create_change_ith(c, path, value)


create_pre_data = [
    # nominal
    ([False], 'pre false'),
    ([9, 31], 'pre (9, 31)'),
    # robustness
    ([], create.ExprSyntaxError),
]
ids = [str(_[0]) for _ in create_pre_data]


@pytest.mark.parametrize('flows, expected', create_pre_data, ids=ids)
def test_create_pre(flows, expected):
    if isinstance(expected, str):
        # nominal
        tree = create.create_pre(*flows)
        assert _tree_to_string(tree) == expected
    else:
        # robustness
        with pytest.raises(expected):
            _ = create.create_pre(*flows)


create_init_data = [
    # nominal
    (True, False, '(false) -> (true)'),
    ([9, "'a'"], [31, "'g'"], "(31, 'g') -> (9, 'a')"),
    # robustness
    ([], [], create.EmptyTreeError),
    ([1, 2], [3, 4, 5], create.ExprSyntaxError),
    (1, [2, 3], create.ExprSyntaxError),
    ([1, 2], [3], create.ExprSyntaxError),
]
ids = ['%s - %s' % (_[0], _[1]) for _ in create_init_data]


@pytest.mark.parametrize('flows, inits, expected', create_init_data, ids=ids)
def test_create_init(flows, inits, expected):
    if isinstance(expected, str):
        # nominal
        tree = create.create_init(flows, inits)
        assert _tree_to_string(tree) == expected
    else:
        # robustness
        with pytest.raises(expected):
            _ = create.create_init(flows, inits)


create_fby_data = [
    # nominal
    (True, 1, False, 'fby(true; 1; false)'),
    ([9, "'a'"], 2, [31, "'g'"], "fby(9, 'a'; 2; 31, 'g')"),
    # robustness
    ([], 0, [], create.EmptyTreeError),
    ([1, 2], 1, [3, 4, 5], create.ExprSyntaxError),
    (1, 2, [2, 3], create.ExprSyntaxError),
    ([1, 2], 3, [3], create.ExprSyntaxError),
]
ids = ['%s - %s' % (_[0], _[1]) for _ in create_fby_data]


@pytest.mark.parametrize('flows, delay, inits, expected', create_fby_data, ids=ids)
def test_create_fby(flows, delay, inits, expected):
    if isinstance(expected, str):
        # nominal
        tree = create.create_fby(flows, delay, inits)
        assert _tree_to_string(tree) == expected
    else:
        # robustness
        with pytest.raises(expected):
            _ = create.create_fby(flows, delay, inits)


create_times_data = [
    # nominal
    (42, False, '42 times false'),
]
ids = ['%s - %s' % (_[0], _[1]) for _ in create_times_data]


@pytest.mark.parametrize('number, flow, expected', create_times_data, ids=ids)
def test_create_times(number, flow, expected: str):
    # nominal
    tree = create.create_times(number, flow)
    assert _tree_to_string(tree) == expected


create_slice_data = [
    # nominal
    ('constant', 0, 1, 'constant[0 .. 1]'),
]
ids = [_[0] for _ in create_slice_data]


@pytest.mark.parametrize('name, start, end, expected', create_slice_data, ids=ids)
def test_create_slice(name, start, end, expected: str):
    # nominal
    constant = suite.Constant()
    constant.name = name
    tree = create.create_slice(constant, start, end)
    assert _tree_to_string(tree) == expected


create_concat_data = [
    # nominal
    (['a', 'b', 'c'], 'a @ b @ c'),
    # robustness
    ([], create.ExprSyntaxError),
    (['a'], create.ExprSyntaxError),
]
ids = [str(_[0]) for _ in create_concat_data]


@pytest.mark.parametrize('names, expected', create_concat_data, ids=ids)
def test_create_concat(names, expected):
    arrays = []
    for name in names:
        c = suite.Constant()
        c.name = name
        arrays.append(c)
    if isinstance(expected, str):
        # nominal
        tree = create.create_concat(*arrays)
        assert _tree_to_string(tree) == expected
    else:
        # robustness
        with pytest.raises(expected):
            _ = create.create_concat(*arrays)


create_reverse_data = [
    # nominal
    ('c', 'reverse c'),
]
ids = [_[0] for _ in create_reverse_data]


@pytest.mark.parametrize('name, expected', create_reverse_data, ids=ids)
def test_create_reverse(name, expected: str):
    c = suite.Constant()
    c.name = name
    tree = create.create_reverse(c)
    assert _tree_to_string(tree) == expected


create_transpose_data = [
    # nominal
    ('c', 1, 2, 'transpose(c; 1; 2)'),
]
ids = [_[0] for _ in create_transpose_data]


@pytest.mark.parametrize('name, dim1, dim2, expected', create_transpose_data, ids=ids)
def test_create_transpose(name, dim1, dim2, expected: str):
    c = suite.Constant()
    c.name = name
    tree = create.create_transpose(c, dim1, dim2)
    assert _tree_to_string(tree) == expected


# data from create_call
create_restart_data = [
    # nominal
    ('Empty', [], [], True, '(restart Empty every true)()'),
    ('EmptySized', [], [42], False, '(restart (EmptySized<<42>>) every false)()'),
    ('Regular', [True, 1], [], True, '(restart Regular every true)(true, 1)'),
    ('Sized', ["'O'"], [9, 31], False, "(restart (Sized<<9, 31>>) every false)('O')"),
    ('EmptySizedLx', [], 42, False, '(restart (EmptySizedLx<<42>>) every false)()'),
    ('RegularLx', [True, 1], None, True, '(restart RegularLx every true)(true, 1)'),
    ('SizedLx', "'O'", [9, 31], False, "(restart (SizedLx<<9, 31>>) every false)('O')"),
]
ids = [_[0] for _ in create_restart_data]


@pytest.mark.parametrize('name, args, inst_args, every, expected', create_restart_data, ids=ids)
def test_create_restart(name: str, args, inst_args, every, expected: str):
    operator = suite.Operator()
    operator.name = name
    # nominal
    modifier = create.create_restart(every)
    if inst_args:
        # use extended mode for the single modifier
        tree = create.create_higher_order_call(operator, args, modifier, inst_args)
    else:
        tree = create.create_higher_order_call(operator, args, [modifier])
    assert _tree_to_string(tree) == expected


# op parameters and instance parameters with higher order
# are considered in test_create_restart
create_activate_data = [
    # nominal
    ('Empty', [], True, '(activate Empty every true initial default ())()'),
    ('Regular', [True, 1], True, '(activate Regular every true initial default (true, 1))()'),
]
ids = [_[0] for _ in create_activate_data]


@pytest.mark.parametrize('name, args, every, expected', create_activate_data, ids=ids)
def test_create_activate(name: str, args, every, expected: str):
    operator = suite.Operator()
    operator.name = name
    # nominal
    modifier = create.create_activate(every, *args)
    tree = create.create_higher_order_call(operator, [], [modifier])
    assert _tree_to_string(tree) == expected


# op parameters and instance parameters with higher order
# are considered in test_create_restart
create_activate_no_init_data = [
    # nominal
    ('Empty', [], True, '(activate Empty every true default ())()'),
    ('Regular', [True, 1], True, '(activate Regular every true default (true, 1))()'),
]
ids = [_[0] for _ in create_activate_no_init_data]


@pytest.mark.parametrize('name, args, every, expected', create_activate_no_init_data, ids=ids)
def test_create_activate_no_init(name: str, args, every, expected: str):
    operator = suite.Operator()
    operator.name = name
    # nominal
    modifier = create.create_activate_no_init(every, *args)
    tree = create.create_higher_order_call(operator, [], [modifier])
    assert _tree_to_string(tree) == expected


# design different from other expressions: a single function for all the iterators
create_iterator_data = [
    # nominal
    ('Map', [1], '(map Map <<1>>)()'),
    ('Mapi', [2], '(mapi Mapi <<2>>)()'),
    ('Fold', [3], '(fold Fold <<3>>)()'),
    ('Foldi', [4], '(foldi Foldi <<4>>)()'),
    ('MapFold', [5, 1], '(mapfold 1 MapFold <<5>>)()'),
    ('MapFoldi', [6, 2], '(mapfoldi 2 MapFoldi <<6>>)()'),
    ('Foldw', [7, False], '(foldw Foldw <<7>> if false)()'),
    ('Foldwi', [8, True], '(foldwi Foldwi <<8>> if true)()'),
    ('Mapw', [9, False, '0_f32'], '(mapw Mapw <<9>> if false default 0_f32)()'),
    ('Mapwi', [10, True, False], '(mapwi Mapwi <<10>> if true default false)()'),
    ('MapFoldw', [11, 3, False, 3.14], '(mapfoldw 3 MapFoldw <<11>> if false default 3.14)()'),
    ('MapFoldwi', [12, 4, True, '3_i8'], '(mapfoldwi 4 MapFoldwi <<12>> if true default 3_i8)()'),
]
ids = [_[0] for _ in create_iterator_data]


@pytest.mark.parametrize('name, args, expected', create_iterator_data, ids=ids)
def test_create_iterator(name: str, args, expected: str):
    operator = suite.Operator()
    operator.name = name
    # nominal
    modifier = eval('create.create_%s(*args)' % name.lower())
    tree = create.create_higher_order_call(operator, [], [modifier])
    assert _tree_to_string(tree) == expected


# _normalize_tree is checked through the unit tests for the individual wrappers
# the following test cases are intended for coverage of the nominal uses cases and robustness
normalize_tree_value_data = [
    # nominal
    # Python literals
    (False, 'false', 'Bool'),
    (True, 'true', 'Bool'),
    (1, '1', 'Int'),
    (-2, '-2', 'Int'),
    (3.14, '3.14', 'Real'),
    # Scade literals
    ('false', 'false', 'Bool'),
    ('true', 'true', 'Bool'),
    ('1', '1', 'Int'),
    ('-2', '-2', 'Int'),
    ('3.14e+0', '3.14e+0', 'Real'),
    ('1_i8', '1_i8', 'Int'),
    ('2_i16', '2_i16', 'Int'),
    ('3_i32', '3_i32', 'Int'),
    ('4_i64', '4_i64', 'Int'),
    ('5_ui8', '5_ui8', 'Int'),
    ('6_ui16', '6_ui16', 'Int'),
    ('7_ui32', '7_ui32', 'Int'),
    ('8_ui64', '8_ui64', 'Int'),
    ('1.2_f32', '1.2_f32', 'Real'),
    ('.3_f64', '.3_f64', 'Real'),
    ("'a'", "'a'", 'Char'),
    # projection path element
    ('a_i8', 'a_i8', 'String'),
    # robustness
    ('a b_i8', create.ExprSyntaxError, None),
    ('+_f32', create.ExprSyntaxError, None),
    (set(), create.ExprSyntaxError, None),
    # literals
    ('0_ui24', create.ExprSyntaxError, None),
    ([], create.EmptyTreeError, None),
]
ids = [str(_[0]) for _ in normalize_tree_value_data]


@pytest.mark.parametrize('tree, expected_value, expected_kind', normalize_tree_value_data, ids=ids)
def test_normalize_tree_value(tree, expected_value, expected_kind):
    if isinstance(expected_value, str):
        # nominal
        tree = _normalize_tree(tree)
        # tree must be an instance of _Value
        assert tree.value == expected_value
        assert tree.kind == expected_kind
    else:
        # robustness
        with pytest.raises(expected_value):
            _ = _normalize_tree(tree)


# additional tests with Scade model elements
normalize_tree_reference_data = [
    # nominal
    (suite.Constant, 'constant', 'constant'),
    (suite.Sensor, 'sensor', 'sensor'),
    (suite.LocalVariable, 'local', 'local'),
    # robustness
    (suite.Operator, 'operator', create.ExprSyntaxError),
]
ids = [str(_[1]) for _ in normalize_tree_reference_data]


@pytest.mark.parametrize('class_, name, expected', normalize_tree_reference_data, ids=ids)
def test_normalize_tree_reference(class_: str, name: str, expected):
    object_ = class_()
    object_.name = name
    tree = object_
    if isinstance(expected, str):
        # nominal
        tree = _normalize_tree(tree)
        assert tree.reference.name == expected
    else:
        # robustness
        with pytest.raises(expected):
            _ = _normalize_tree(tree)


# additional tests with Scade model elements
normalize_tree_type_data = [
    # nominal
    (suite.NamedType, 'type_', 'type_'),
]
ids = [str(_[1]) for _ in normalize_tree_type_data]


@pytest.mark.parametrize('class_, name, expected', normalize_tree_type_data, ids=ids)
def test_normalize_tree_type(class_: str, name: str, expected):
    object_ = class_()
    object_.name = name
    tree = object_
    # nominal
    tree = _normalize_tree(tree)
    assert tree.type.name == expected


# additional tests with a tree
def test_normalize_tree_tree():
    first = _normalize_tree(True)
    second = _normalize_tree(first)
    assert second == first
