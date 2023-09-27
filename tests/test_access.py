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
Test suite for access.py.

Test strategy:

* Define a test model with all possible expressions and check all the roles.
"""

import pytest
import scade.model.suite as suite

# shall modify sys.path to access SCACE APIs
import ansys.scade.apitools.expr as expr
from conftest import load_session
from test_utils import get_resources_dir


@pytest.fixture(scope='session')
def model():
    """Unique instance of the test model ExprAccess."""
    pathname = get_resources_dir() / 'resources' / 'ExprAccess' / 'ExprAccess.etp'
    return load_session(pathname).model


def test_last(model):
    equation = model.get_object_from_path('Access::ExprId/last_=')
    assert isinstance(equation, suite.Equation)
    expression = expr.accessor(equation.right)
    assert expression.expression == equation.right
    assert isinstance(expression, expr.Last)
    assert expression.variable.name == 'variable'


def test_present(model):
    equation = model.get_object_from_path('Access::ExprId/present=')
    assert isinstance(equation, suite.Equation)
    expression = expr.accessor(equation.right)
    assert expression.expression == equation.right
    assert isinstance(expression, expr.Present)
    assert expression.signal.name == 'signal'


def test_id_expression_nominal(model):
    equation = model.get_object_from_path('Access::ExprId/idExpression=')
    assert isinstance(equation, suite.Equation)
    expression = expr.accessor(equation.right)
    assert expression.expression == equation.right
    assert isinstance(expression, expr.IdExpression)
    assert expression.path.name == 'path'


def test_const_value(model):
    equation = model.get_object_from_path('Access::ConstValue/constValue=')
    assert isinstance(equation, suite.Equation)
    expression = expr.accessor(equation.right)
    assert expression.expression == equation.right
    assert isinstance(expression, expr.ConstValue)
    assert expression.value == 'false'


def test_text_expression(model):
    equation = model.get_object_from_path('Access::TextExpression/textExpression=')
    assert isinstance(equation, suite.Equation)
    expression = expr.accessor(equation.right)
    assert expression.expression == equation.right
    assert isinstance(expression, expr.TextExpression)
    assert expression.text == 'syntax error'


def test_data_struct_op(model):
    equation = model.get_object_from_path('Access::StructureArray/dataStructOp=')
    assert isinstance(equation, suite.Equation)
    expression = expr.accessor(equation.right)
    assert expression.expression == equation.right
    assert isinstance(expression, expr.DataStructOp)
    data = [(_.label, _.flow.path.name) for _ in expression.data]
    assert data == [('label%d' % _, 'field%d' % _) for _ in range(1, 4)]


def test_data_array_op(model):
    equation = model.get_object_from_path('Access::StructureArray/dataArrayOp=')
    assert isinstance(equation, suite.Equation)
    expression = expr.accessor(equation.right)
    assert expression.expression == equation.right
    assert isinstance(expression, expr.DataArrayOp)
    data = [_.path.name for _ in expression.data]
    assert data == ['v%d' % _ for _ in range(3)]


def test_transpose_op(model):
    equation = model.get_object_from_path('Access::StructureArray/transposeOp=')
    assert isinstance(equation, suite.Equation)
    expression = expr.accessor(equation.right)
    assert expression.expression == equation.right
    assert isinstance(expression, expr.TransposeOp)
    assert expression.array.path.name == 'arrayTranspose'
    dimensions = [_.value for _ in expression.dimensions]
    assert dimensions == ['%d' % _ for _ in range(1, 3)]


def test_slice_op(model):
    equation = model.get_object_from_path('Access::StructureArray/sliceOp=')
    assert isinstance(equation, suite.Equation)
    expression = expr.accessor(equation.right)
    assert expression.expression == equation.right
    assert isinstance(expression, expr.SliceOp)
    assert expression.array.path.name == 'arraySlice'
    assert expression.from_index.value == '1'
    assert expression.to_index.value == '3'


def test_prj_dyn_op(model):
    equation = model.get_object_from_path('Access::StructureArray/prjDynOp=')
    assert isinstance(equation, suite.Equation)
    expression = expr.accessor(equation.right)
    assert expression.expression == equation.right
    assert isinstance(expression, expr.PrjDynOp)
    assert expression.array.path.name == 'arrayPrjDyn'
    indexes = expression.indexes
    assert indexes[0].value == '1'
    assert indexes[1].name == 'label'
    assert expression.default.value == '42'


def test_scalar_to_op(model):
    equation = model.get_object_from_path('Access::StructureArray/scalarToVectorOp=')
    assert isinstance(equation, suite.Equation)
    expression = expr.accessor(equation.right)
    assert expression.expression == equation.right
    assert isinstance(expression, expr.ScalarToVectorOp)
    names = [_.path.name for _ in expression.flows]
    assert names == ['flowScalarToVector']
    assert expression.size.value == '42'


def test_prj_op(model):
    equation = model.get_object_from_path('Access::StructureArray/prjOp=')
    assert isinstance(equation, suite.Equation)
    expression = expr.accessor(equation.right)
    assert expression.expression == equation.right
    assert isinstance(expression, expr.PrjOp)
    assert expression.flow.path.name == 'flowPrj'
    with_ = expression.with_
    assert with_[0].name == 'label'
    assert with_[1].value == '2'


def test_chg_ith_op(model):
    equation = model.get_object_from_path('Access::StructureArray/chgIthOp=')
    assert isinstance(equation, suite.Equation)
    expression = expr.accessor(equation.right)
    assert expression.expression == equation.right
    assert isinstance(expression, expr.ChgIthOp)
    assert expression.flow.path.name == 'flowChgIth'
    assert expression.value.path.name == 'valueChgIth'
    with_ = expression.with_
    assert with_[0].value == '31'
    assert with_[1].name == 'label'
    assert with_[2].value == '9'


def test_make_op(model):
    equation = model.get_object_from_path('Access::StructureArray/makeOp=')
    assert isinstance(equation, suite.Equation)
    expression = expr.accessor(equation.right)
    assert expression.expression == equation.right
    assert isinstance(expression, expr.MakeOp)
    names = [_.path.name for _ in expression.flows]
    assert names == ['flowMake%d' % _ for _ in range(1, 3)]
    assert expression.type_.name == 'Structure'


def test_flatten_op(model):
    equation = model.get_object_from_path('Access::StructureArray/flattenOp=')
    assert isinstance(equation, suite.Equation)
    expression = expr.accessor(equation.right)
    assert expression.expression == equation.right
    assert isinstance(expression, expr.FlattenOp)
    assert expression.flow.path.name == 'flowFlatten'
    assert expression.type_.name == 'Structure'


def test_if_then_else_op(model):
    equation = model.get_object_from_path('Access::Choice/ifThenElseOp=')
    assert isinstance(equation, suite.Equation)
    expression = expr.accessor(equation.right)
    assert expression.expression == equation.right
    assert isinstance(expression, expr.IfThenElseOp)
    assert expression.if_.path.name == 'flowIf'
    names = [_.path.name for _ in expression.then]
    assert names == ['flowThen']
    names = [_.path.name for _ in expression.else_]
    assert names == ['flowElse']


def test_case_op(model):
    equation = model.get_object_from_path('Access::Choice/caseOp=')
    assert isinstance(equation, suite.Equation)
    expression = expr.accessor(equation.right)
    assert expression.expression == equation.right
    assert isinstance(expression, expr.CaseOp)
    assert expression.switch.path.name == 'flowSwitch'
    cases = [(pattern, flow.path.name) for pattern, flow in expression.cases]
    assert cases == [('1', 'flowCase1'), ('2', 'flowCase2')]
    assert expression.default.path.name == 'flowDefault'


def test_init_op(model):
    equation = model.get_object_from_path('Access::Time/initOp=')
    assert isinstance(equation, suite.Equation)
    expression = expr.accessor(equation.right)
    assert expression.expression == equation.right
    assert isinstance(expression, expr.InitOp)
    assert [_.path.name for _ in expression.flows] == ['flowInit']
    assert [_.value for _ in expression.inits] == ['42']


def test_pre_op(model):
    equation = model.get_object_from_path('Access::Time/preOp=')
    assert isinstance(equation, suite.Equation)
    expression = expr.accessor(equation.right)
    assert expression.expression == equation.right
    assert isinstance(expression, expr.PreOp)
    assert [_.path.name for _ in expression.flows] == ['flowPre']


def test_fby_op(model):
    equation = model.get_object_from_path('Access::Time/fbyOp=')
    assert isinstance(equation, suite.Equation)
    expression = expr.accessor(equation.right)
    assert expression.expression == equation.right
    assert isinstance(expression, expr.FbyOp)
    assert [_.path.name for _ in expression.flows] == ['flowFby']
    assert expression.delay.value == '1'
    assert [_.value for _ in expression.inits] == ['42']


unary_data = [
    ('Access::StructureArray/_reverse_=', 'REVERSE', 'operandReverse'),
    ('Access::Mathematical/_unary_plus_=', 'POS', 'operand'),
    ('Access::Mathematical/_unary_minus_=', 'NEG', 'operand'),
    ('Access::Logical/_not_=', 'NOT', 'operand'),
    ('Access::Bitwise/_lnot_=', 'LNOT', 'operand'),
]


@pytest.mark.parametrize(
    'path, code, expected',
    unary_data,
    ids=[_[0].split(':')[-1].strip('/') for _ in unary_data],
)
def test_unary_op(model, path, code, expected):
    equation = model.get_object_from_path(path)
    assert isinstance(equation, suite.Equation)
    expression = expr.accessor(equation.right)
    assert expression.expression == equation.right
    assert isinstance(expression, expr.UnaryOp)
    assert expression.code.name == code
    assert expression.operand.path.name == expected


nary_data = [
    ('Access::StructureArray/_concatenation_=', 'CONCAT', 'operandConcatenation'),
    ('Access::Mathematical/_plus_=', 'PLUS', 'operand'),
    ('Access::Mathematical/_multiplication_=', 'MUL', 'operand'),
    ('Access::Logical/_and_=', 'AND', 'operand'),
    ('Access::Logical/_or_=', 'OR', 'operand'),
    ('Access::Logical/_exclusive_or_=', 'XOR', 'operand'),
    ('Access::Bitwise/_land_=', 'LAND', 'operand'),
    ('Access::Bitwise/_lor_=', 'LOR', 'operand'),
]


@pytest.mark.parametrize(
    'path, code, expected',
    nary_data,
    ids=[_[0].split(':')[-1].strip('/') for _ in nary_data],
)
def test_nary_op(model, path, code, expected):
    equation = model.get_object_from_path(path)
    assert isinstance(equation, suite.Equation)
    expression = expr.accessor(equation.right)
    assert expression.expression == equation.right
    assert isinstance(expression, expr.NAryOp)
    assert expression.code.name == code
    names = [_.path.name for _ in expression.operands]
    assert names == ['%s%d' % (expected, _) for _ in range(1, len(equation.right.parameters) + 1)]


binary_data = [
    ('Access::Mathematical/_minus_=', 'SUB', 'operand'),
    ('Access::Mathematical/_polymorphic_division_=', 'SLASH', 'operand'),
    ('Access::Mathematical/_modulo_=', 'MOD', 'operand'),
    ('Access::Comparison/_strictly_less_than_=', 'LESS', 'operand'),
    ('Access::Comparison/_less_than_equal_=', 'LEQUAL', 'operand'),
    ('Access::Comparison/_strictly_greater_than_=', 'GREAT', 'operand'),
    ('Access::Comparison/_greater_than_equal_=', 'GEQUAL', 'operand'),
    ('Access::Comparison/_different_=', 'NEQUAL', 'operand'),
    ('Access::Comparison/_equal_=', 'EQUAL', 'operand'),
    ('Access::Bitwise/_lxor_=', 'LXOR', 'operand'),
    ('Access::Bitwise/_lsl_=', 'LSL', 'operand'),
    ('Access::Bitwise/_lsr_=', 'LSR', 'operand'),
    ('Access::Time/_times_=', 'TIMES', 'operand'),
]


@pytest.mark.parametrize(
    'path, code, expected',
    binary_data,
    ids=[_[0].split(':')[-1].strip('/') for _ in binary_data],
)
def test_binary_op(model, path, code, expected):
    equation = model.get_object_from_path(path)
    assert isinstance(equation, suite.Equation)
    expression = expr.accessor(equation.right)
    assert expression.expression == equation.right
    assert isinstance(expression, expr.BinaryOp)
    assert expression.code.name == code
    names = [_.path.name for _ in expression.operands]
    assert names == ['%s%d' % (expected, _) for _ in range(1, len(equation.right.parameters) + 1)]


def test_numeric_cast_op(model):
    equation = model.get_object_from_path('Access::Mathematical/numericCastOp=')
    assert isinstance(equation, suite.Equation)
    expression = expr.accessor(equation.right)
    assert expression.expression == equation.right
    assert isinstance(expression, expr.NumericCastOp)
    assert expression.flow.path.name == 'operand'
    assert expression.type_.name == 'int32'


def test_sharp_op(model):
    equation = model.get_object_from_path('Access::Logical/sharpOp=')
    assert isinstance(equation, suite.Equation)
    expression = expr.accessor(equation.right)
    assert expression.expression == equation.right
    assert isinstance(expression, expr.SharpOp)
    names = [_.path.name for _ in expression.flows]
    assert names == ['operand%d' % _ for _ in range(1, len(equation.right.parameters) + 1)]


def test_op_call(model):
    equation = model.get_object_from_path('Access::Call/opCall=')
    assert isinstance(equation, suite.Equation)
    expression = expr.accessor(equation.right)
    assert expression.expression == equation.right
    assert isinstance(expression, expr.OpCall)
    assert expression.operator.name == 'Operator'
    assert expression.name == 'Toulouse'
    names = [_.path.name for _ in expression.call_parameters]
    assert names == ['callParameter%d' % _ for _ in range(1, len(equation.right.parameters) + 1)]
    assert len(expression.instance_parameters) == 1
    assert expression.instance_parameters[0].value == '42'


def test_restart_op(model):
    equation = model.get_object_from_path('Access::HigherOrder/restartOp=')
    assert isinstance(equation, suite.Equation)
    expression = expr.accessor(equation.right)
    assert isinstance(expression, expr.RestartOp)
    # called operator
    call = expression.operator
    assert call.expression == equation.right
    assert call.operator.name == 'Operator'
    assert call.name == '1'
    names = [_.path.name for _ in call.call_parameters]
    count = len(equation.right.parameters)
    assert names == ['callParameterRestart%d' % _ for _ in range(1, count + 1)]
    assert len(call.instance_parameters) == 1
    assert call.instance_parameters[0].value == '42'
    # higher order
    assert expression.expression == equation.right.modifier
    assert expression.every.path.name == 'everyRestart'


def test_activate_op(model):
    equation = model.get_object_from_path('Access::HigherOrder/activateOp=')
    assert isinstance(equation, suite.Equation)
    expression = expr.accessor(equation.right)
    assert isinstance(expression, expr.ActivateOp)
    # called operator
    call = expression.operator
    assert call.expression == equation.right
    assert call.operator.name == 'Operator'
    assert call.name == '2'
    names = [_.path.name for _ in call.call_parameters]
    count = len(equation.right.parameters)
    assert names == ['callParameterActivate%d' % _ for _ in range(1, count + 1)]
    assert len(call.instance_parameters) == 1
    assert call.instance_parameters[0].value == '31'
    # higher order
    assert expression.expression == equation.right.modifier
    assert expression.every.path.name == 'everyActivate'
    assert [_.value for _ in expression.defaults] == ['9', 'false', "'j'"]


def test_activate_no_init_op(model):
    equation = model.get_object_from_path('Access::HigherOrder/activateNoInitOp=')
    assert isinstance(equation, suite.Equation)
    expression = expr.accessor(equation.right)
    assert isinstance(expression, expr.ActivateNoInitOp)
    # called operator
    call = expression.operator
    assert call.expression == equation.right
    assert call.operator.name == 'Operator'
    assert call.name == '3'
    names = [_.path.name for _ in call.call_parameters]
    count = len(equation.right.parameters)
    assert names == ['callParameterActivateNoInit%d' % _ for _ in range(1, count + 1)]
    assert len(call.instance_parameters) == 1
    assert call.instance_parameters[0].value == '9'
    # higher order
    assert expression.expression == equation.right.modifier
    assert expression.every.path.name == 'everyActivateNoInit'
    assert [_.value for _ in expression.defaults] == ['true', '31', "'h'"]


iterator_data = [
    ('Access::HigherOrder/mapIteratorOp=', 'Map', 'N', '31', None),
    ('Access::HigherOrder/mapiIteratorOp=', 'Mapi', 'N', '32', None),
    ('Access::HigherOrder/foldIteratorOp=', 'Fold', 'N', '31', None),
    ('Access::HigherOrder/foldiIteratorOp=', 'Foldi', 'N', '32', None),
    ('Access::HigherOrder/mapfoldIteratorOp=', 'Mapfold', 'N', '31', '1'),
    ('Access::HigherOrder/mapfoldiIteratorOp=', 'Mapfoldi', 'N', '32', '1'),
]


@pytest.mark.parametrize(
    'path, param, inst_param, size, nacc',
    iterator_data,
    ids=[_[0].split(':')[-1].strip('/') for _ in iterator_data],
)
def test_iterator_op(model, path, param, inst_param, size, nacc):
    equation = model.get_object_from_path(path)
    assert isinstance(equation, suite.Equation)
    expression = expr.accessor(equation.right)
    assert isinstance(expression, expr.IteratorOp)
    # called operator
    call = expression.operator
    assert call.expression == equation.right
    assert call.operator.name == 'Operator'
    assert call.call_parameters[0].path.name == 'callParameter%s' % param
    assert len(call.instance_parameters) == 1
    assert call.instance_parameters[0].path.name == inst_param
    # higher order
    assert expression.expression == equation.right.modifier
    assert expression.size.value == size
    if nacc is None:
        assert expression.accumulator_count is None
    else:
        assert expression.accumulator_count.value == nacc


partial_iterator_data = [
    ('Access::HigherOrder/mapwIteratorOp=', 'Mapw', '81', 'N', ['46', 'false'], None),
    ('Access::HigherOrder/mapwiIteratorOp=', 'Mapwi', '82', 'N', ['65', 'true'], None),
    ('Access::HigherOrder/foldwIteratorOp=', 'Foldw', '81', 'N', None, None),
    ('Access::HigherOrder/foldwiIteratorOp=', 'Foldwi', '82', 'N', None, None),
    ('Access::HigherOrder/mapfoldwIteratorOp=', 'Mapfoldw', '81', 'N', ['46'], '1'),
    ('Access::HigherOrder/mapfoldwiIteratorOp=', 'Mapfoldwi', '82', 'N', [], '2'),
]


@pytest.mark.parametrize(
    'path, param, inst_param, size, defaults, nacc',
    partial_iterator_data,
    ids=[_[0].split(':')[-1].strip('/') for _ in partial_iterator_data],
)
def test_partial_iterator_op(model, path, param, inst_param, size, defaults, nacc):
    equation = model.get_object_from_path(path)
    assert isinstance(equation, suite.Equation)
    expression = expr.accessor(equation.right)
    assert isinstance(expression, expr.PartialIteratorOp)
    # called operator
    call = expression.operator
    assert call.expression == equation.right
    assert call.operator.name == 'Operator'
    assert call.call_parameters[0].path.name == 'callParameter%s' % param
    assert len(call.instance_parameters) == 1
    assert call.instance_parameters[0].value == inst_param
    # higher order
    assert expression.expression == equation.right.modifier
    assert expression.size.path.name == size
    assert expression.if_.path.name == 'if%s' % param
    if defaults is None:
        assert expression.defaults is None
    else:
        assert [_.value for _ in expression.defaults] == defaults
    if nacc is None:
        assert expression.accumulator_count is None
    else:
        assert expression.accumulator_count.value == nacc


# robustness test, list expressions are always sub-expressions
# thus not expected to be accessed directly
def test_list_expression(model):
    equation = model.get_object_from_path('Access::Choice/ifThenElseOp=')
    assert isinstance(equation, suite.Equation)
    # the second parameter of if-then-else is a sequence
    expression = expr.accessor(equation.right.parameters[1])
    assert isinstance(expression, expr.ListExpression)
    names = [_.path.name for _ in expression.items]
    assert names == ['flowThen']


# robustness test, type expressions are always sub-expressions
# and are not supported for a direct access
def test_type_expression_robustness(model):
    equation = model.get_object_from_path('Access::StructureArray/flattenOp=')
    assert isinstance(equation, suite.Equation)
    with pytest.raises(ValueError):
        # the second parameter of flatten is a reference to a type
        expression = expr.accessor(equation.right.parameters[1])


# robustness test, clock activate is not supported
def test_clock_activate_robustness(model):
    equation = model.get_object_from_path('Access::HigherOrder/_not_supported_op_=')
    assert isinstance(equation, suite.Equation)
    with pytest.raises(ValueError):
        # the higher order operator is not supported
        expression = expr.accessor(equation.right)


# robustness test, clock expressions are not supported
def test_clock_expressions_robustness(model):
    equation = model.get_object_from_path('Access::Time/_merge_not_supported_=')
    assert isinstance(equation, suite.Equation)
    with pytest.raises(ValueError):
        # the higher order operator is not supported
        expression = expr.accessor(equation.right)
