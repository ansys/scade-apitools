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
Test suite for create/expression.py.

The tests of this module operate on an empty model: these constructs must not
be used for real scripts.
"""

import pytest

import ansys.scade.apitools.create as create
from ansys.scade.apitools.create.scade import suite
from ansys.scade.apitools.expr import Eck


def _pre_process_expression_tree(model, tree):
    """Replace all occurrences of '@path' by the corresponding model element."""
    if isinstance(tree, list):
        return [_pre_process_expression_tree(model, _) for _ in tree]
    elif isinstance(tree, str):
        if tree and tree[0] == '@':
            return model.get_object_from_path(tree[1:])
    # default
    return tree


def _build_expr(tree, context: suite.Object = None) -> str:
    """Build an expression from a tree and return textual representation."""
    expr = create._build_expression_tree(context, tree)
    create._link_pendings()
    return expr.to_string().strip()


create_call_data = [
    # nominal
    ('Empty', [], [], 'Empty()'),
    ('EmptySized', [], [42], '(EmptySized<<42>>)()'),
    ('Regular', [True, 1], [], 'Regular(true, 1)'),
    ('Sized', ["'O'"], [9, 31], "(Sized<<9, 31>>)('O')"),
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
    assert _build_expr(tree) == expected


def test_create_call_robustness():
    constant = suite.Constant()
    with pytest.raises(TypeError):
        tree = create.create_call(constant, [])


def test_create_higher_order_call_robustness():
    constant = suite.Constant()
    with pytest.raises(TypeError):
        tree = create.create_higher_order_call(constant, [], [])


create_unary_data = [
    # nominal
    # logical
    ('!', True, 'not true'),
    # arithmetic
    ('-', 9, '- 9'),
    ('+', 31, '+ 31'),
    # bitwise
    ('lnot', 12, 'lnot 12'),
    # more complex operand
    ('-', ['_', Eck.POS, [32], [], []], '- ( + 32)'),
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
        assert _build_expr(tree) == expected
    else:
        # robustness
        with pytest.raises(expected):
            tree = create.create_unary(symbol, arg)


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
        assert _build_expr(tree) == expected
    else:
        # robustness
        with pytest.raises(expected):
            tree = create.create_binary(symbol, arg1, arg2)


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
        assert _build_expr(tree) == expected
    else:
        # robustness
        with pytest.raises(expected):
            tree = create.create_nary(symbol, *args)


create_if_data = [
    # nominal
    ('if-single', True, [0, 1], 'if true then (0) else (1)'),
    ('if-double', False, [0, 1, 2, 3], 'if false then (0, 2) else (1, 3)'),
    # robustness
    ('empty', True, [], create.ExprSyntaxError),
    ('odd', False, [0, 1, 2], create.ExprSyntaxError),
]
ids = [_[0] for _ in create_if_data]


@pytest.mark.parametrize('id, condition, args, expected', create_if_data, ids=ids)
def test_create_if(id: str, condition, args, expected):
    if isinstance(expected, str):
        # nominal
        tree = create.create_if(condition, *args)
        assert _build_expr(tree) == expected
    else:
        # robustness
        with pytest.raises(expected):
            tree = create.create_if(condition, *args)


create_case_data = [
    # nominal
    ('single', True, ["'A'", 65], "( case true of \n | 'A' :   65)"),
    ('double', 1, [0, 'false', 1, 'true'], '( case 1 of \n | 0 :   false\n | 1 :   true)'),
    ('default', 6, [1, 2, 3, 4, '_', 5], '( case 6 of \n | 1 :   2\n | 3 :   4\n | _ :   5)'),
    # robustness
    ('empty', False, [], create.ExprSyntaxError),
    ('odd', "'a'", [0, 1, 2], create.ExprSyntaxError),
    ('default', 42, ['_', 0, 1, 2], create.ExprSyntaxError),
]
ids = [_[0] for _ in create_case_data]


@pytest.mark.parametrize('id, selector, args, expected', create_case_data, ids=ids)
def test_create_case(id: str, selector, args, expected):
    if isinstance(expected, str):
        # nominal
        tree = create.create_case(selector, *args)
        assert _build_expr(tree) == expected
    else:
        # robustness
        with pytest.raises(expected):
            tree = create.create_case(selector, *args)


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
        assert _build_expr(tree) == expected
    else:
        # robustness
        with pytest.raises(expected):
            tree = create.create_make(type_, *args)


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
        assert _build_expr(tree) == expected
    else:
        # robustness
        with pytest.raises(expected):
            tree = create.create_flatten(type_, arg)


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
        assert _build_expr(tree) == expected
    else:
        # robustness
        with pytest.raises(expected):
            tree = create.create_scalar_to_vector(size, *args)


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
        assert _build_expr(tree) == expected
    else:
        # robustness
        with pytest.raises(expected):
            tree = create.create_data_array(*args)


create_data_struct_data = [
    # nominal
    ('single', ['one', 1], '{one : 1}'),
    ('double', ['one', 1, 'two', 2], '{one : 1, two : 2}'),
    ('embed', ['one', ['_', Eck.PLUS, [2, 2], [], []]], '{one : 2 + 2}'),
    # robustness
    ('empty', [], create.ExprSyntaxError),
    # TODO: the test below fails: expected exception not raised
    # and the one after, which is identical, raises the expected exception
    # how to proceed?
    # ('empty embed', ['one', [], 'four', 4], create.EmptyTreeError),
    # ('empty embed', ['one', [], 'four', 4], ''),
    ('odd', ['one', 1, 'two'], create.ExprSyntaxError),
    ('not ident', ['not ident', 1], create.TypeIdentifierError),
    ('number', [0, 1], create.TypeIdentifierError),
]
ids = [_[0] for _ in create_data_struct_data]


@pytest.mark.parametrize('id, args, expected', create_data_struct_data, ids=ids)
def test_create_data_struct(id: str, args, expected):
    if isinstance(expected, str):
        # nominal
        tree = create.create_data_struct(*args)
        assert _build_expr(tree) == expected
    else:
        # robustness
        with pytest.raises(expected):
            tree = create.create_data_struct(*args)


create_prj_data = [
    # nominal
    ('index', [42], 'index[42]'),
    ('field', ['a'], 'field.a'),
    ('mixed', [9, 'b', 31], 'mixed[9].b[31]'),
    # robustness
    ('empty', [], create.ExprSyntaxError),
]
ids = [_[0] for _ in create_prj_data]


@pytest.mark.parametrize('name, path, expected', create_prj_data, ids=ids)
def test_create_prj(name: str, path, expected):
    c = suite.Constant()
    c.name = name
    if isinstance(expected, str):
        # nominal
        tree = create.create_prj(c, path)
        assert _build_expr(tree) == expected
    else:
        # robustness
        with pytest.raises(expected):
            tree = create.create_prj(c, path)


create_prj_dyn_data = [
    # nominal
    ('index', [42], False, '(index.[42] default false)'),
    ('field', ['a', -1], 0, '(field. .a[(-1)] default 0)'),
    ('mixed', [9, 'b', 31], "' '", "(mixed.[9].b[31] default ' ')"),
    # robustness
    ('empty', [], 0, create.ExprSyntaxError),
]
ids = [_[0] for _ in create_prj_dyn_data]


@pytest.mark.parametrize('name, path, default, expected', create_prj_dyn_data, ids=ids)
def test_create_prj_dyn(name: str, path, default, expected):
    c = suite.Constant()
    c.name = name
    if isinstance(expected, str):
        # nominal
        tree = create.create_prj_dyn(c, path, default)
        assert _build_expr(tree) == expected
    else:
        # robustness
        with pytest.raises(expected):
            tree = create.create_prj_dyn(c, path, default)


create_change_ith_data = [
    # nominal
    ('index', [42], False, '(index with [42] = false)'),
    ('field', ['a', -1], 0, '(field with .a[(-1)] = 0)'),
    ('mixed', [9, 'b', 31], "' '", "(mixed with [9].b[31] = ' ')"),
    # robustness
    ('empty', [], 0, create.ExprSyntaxError),
]
ids = [_[0] for _ in create_change_ith_data]


@pytest.mark.parametrize('name, path, value, expected', create_change_ith_data, ids=ids)
def test_create_change_ith(name: str, path, value, expected):
    c = suite.Constant()
    c.name = name
    if isinstance(expected, str):
        # nominal
        tree = create.create_change_ith(c, path, value)
        assert _build_expr(tree) == expected
    else:
        # robustness
        with pytest.raises(expected):
            tree = create.create_change_ith(c, path, value)


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
        assert _build_expr(tree) == expected
    else:
        # robustness
        with pytest.raises(expected):
            tree = create.create_pre(*flows)


create_init_data = [
    # nominal
    (True, False, '(false) -> (true)'),
    ([9, "'a'"], [31, "'g'"], "(31, 'g') -> (9, 'a')"),
    # robustness
    ([], [], create.ExprSyntaxError),
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
        assert _build_expr(tree) == expected
    else:
        # robustness
        with pytest.raises(expected):
            tree = create.create_init(flows, inits)


create_fby_data = [
    # nominal
    (True, 1, False, 'fby(true; 1; false)'),
    ([9, "'a'"], 2, [31, "'g'"], "fby(9, 'a'; 2; 31, 'g')"),
    # robustness
    ([], 0, [], create.ExprSyntaxError),
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
        assert _build_expr(tree) == expected
    else:
        # robustness
        with pytest.raises(expected):
            tree = create.create_fby(flows, delay, inits)


create_times_data = [
    # nominal
    (42, False, '42 times false'),
]
ids = ['%s - %s' % (_[0], _[1]) for _ in create_times_data]


@pytest.mark.parametrize('number, flow, expected', create_times_data, ids=ids)
def test_create_times(number, flow, expected: str):
    # nominal
    tree = create.create_times(number, flow)
    assert _build_expr(tree) == expected


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
    assert _build_expr(tree) == expected


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
        assert _build_expr(tree) == expected
    else:
        # robustness
        with pytest.raises(expected):
            tree = create.create_concat(*arrays)


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
    assert _build_expr(tree) == expected


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
    assert _build_expr(tree) == expected


# data from create_call
create_restart_data = [
    # nominal
    ('Empty', [], [], True, '(restart Empty every true)()'),
    ('EmptySized', [], [42], False, '(restart (EmptySized<<42>>) every false)()'),
    ('Regular', [True, 1], [], True, '(restart Regular every true)(true, 1)'),
    ('Sized', ["'O'"], [9, 31], False, "(restart (Sized<<9, 31>>) every false)('O')"),
]
ids = [_[0] for _ in create_restart_data]


@pytest.mark.parametrize('name, args, inst_args, every, expected', create_restart_data, ids=ids)
def test_create_restart(name: str, args, inst_args, every, expected: str):
    operator = suite.Operator()
    operator.name = name
    # nominal
    modifier = create.create_restart(every)
    if inst_args:
        tree = create.create_higher_order_call(operator, args, [modifier], inst_args)
    else:
        tree = create.create_higher_order_call(operator, args, [modifier])
    assert _build_expr(tree) == expected


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
    assert _build_expr(tree) == expected


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
    assert _build_expr(tree) == expected


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
    assert _build_expr(tree) == expected


# _build_expression_tree is checked through the unit tests for the individual wrappers
# The following test cases are intended for coverage of the nominal uses cases and robustness
build_expression_tree_data = [
    # nominal
    # Python literals
    (False, 'false'),
    (True, 'true'),
    (1, '1'),
    (-2, '-2'),
    # Scade literals
    ('false', 'false'),
    ('true', 'true'),
    ('1', '1'),
    ('-2', '-2'),
    ('3.14e+0', '3.14e+0'),
    ('1_i8', '1_i8'),
    ('2_i16', '2_i16'),
    ('3_i32', '3_i32'),
    ('4_i64', '4_i64'),
    ('5_ui8', '5_ui8'),
    ('6_ui16', '6_ui16'),
    ('7_ui32', '7_ui32'),
    ('8_ui64', '8_ui64'),
    ('1.2_f32', '1.2_f32'),
    ('.3_f64', '.3_f64'),
    ("'a'", "'a'"),
    # projection path element
    ('a_i8', 'a_i8'),
    # robustness
    ('a b_i8', create.ExprSyntaxError),
    ('+_f32', create.ExprSyntaxError),
    (set(), create.ExprSyntaxError),
    # literals
    ('0_ui24', create.ExprSyntaxError),
    ('a_i8', 'a_i8'),
    ([], create.EmptyTreeError),
    # too many parameters
    (['_', Eck.PLUS, [], [], [], []], create.ExprSyntaxError),
    # not enough parameters
    (['_', Eck.PLUS, [], []], create.ExprSyntaxError),
    (['_', Eck.PLUS, []], create.ExprSyntaxError),
    (['_', Eck.PLUS], create.ExprSyntaxError),
    # wrong label
    (['a b c', 2], create.TypeIdentifierError),
]
ids = [str(_[0]) for _ in build_expression_tree_data]


@pytest.mark.parametrize('tree, expected', build_expression_tree_data, ids=ids)
def test_build_expression_tree(tree: list, expected):
    if isinstance(expected, str):
        # nominal
        assert _build_expr(tree) == expected
    else:
        # robustness
        with pytest.raises(expected):
            expr = create._build_expression_tree(None, tree)


# additinal tests with Scade model elements
build_expression_tree_ex_data = [
    # nominal
    (suite.Constant, 'constant', 'constant'),
    (suite.Sensor, 'sensor', 'sensor'),
    (suite.NamedType, 'type_', 'type_'),
    (suite.LocalVariable, 'local', 'local'),
    # robustness
    (suite.Operator, 'operator', create.ExprSyntaxError),
]
ids = [str(_[1]) for _ in build_expression_tree_ex_data]


@pytest.mark.parametrize('class_, name, expected', build_expression_tree_ex_data, ids=ids)
def test_build_expression_tree_ex(class_: str, name: str, expected):
    object_ = class_()
    object_.name = name
    tree = object_
    if isinstance(expected, str):
        # nominal
        assert _build_expr(tree) == expected
    else:
        # robustness
        with pytest.raises(expected):
            expr = create._build_expression_tree(None, tree)
