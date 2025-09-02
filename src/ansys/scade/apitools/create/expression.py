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
Provides helpers for creating expression trees.

Expression trees are intermediate structures to declare any arbitrary complex
expressions. They create the corresponding SCADE Suite expressions in the
context of a model element, such as the right part of an equation or the
default value of an output.

This module provides functions to create an expression tree for any expression
of the Scade language, including higher-order constructs. Thus, the intermediate
structures or classes defining the expression trees can be opaque.

Notes: The typing is relaxed in this module to ease the constructs.

* ``ET`` is an alias for ``ExpressionTree`` to shorten the declarations.

* ``EX``, which stands for extended expression tree, is defined as follows::

     Union[bool, int, float, str, suite.ConstVar, suite.NamedType, ET]

  This enhances the usability of these functions by accepting some values,
  such as Python literals, string values, or SCADE Python objects, as valid
  expression trees.

* ``LX``, which stands for extended lists of expression trees, is defined as follows::

     Union[EX, List[EX]]

  When the expressions accept an arbitrary number of input flows, such as
  if-then-else or fby, you can provide either one expression tree or a list
  of expression trees.

"""

from abc import ABC, abstractmethod
from typing import List, Optional, Sequence, Tuple, Union

import scade.model.suite as suite

from ..expr import Eck
from .project import _check_object
from .scade import _add_pending_link


# expression trees
class ExpressionTree(ABC):
    """Provides the top-level abstract class for expression trees."""

    def __init__(self, label: str = ''):
        """Any expression can have a label."""
        self.label = label

    @abstractmethod
    def _build_expression(self, context: suite.Object) -> suite.Expression:
        """Build a SCADE Suite expression from the expression tree."""
        raise NotImplementedError  # pragma no cover

    def _set_label(self, expr: suite.Expression, context: suite.Object):
        """Add the label to the expression, if any."""
        if self.label:
            label = suite.Label(context)
            label.name = self.label
            expr.label = label


ET = ExpressionTree
"""Short name for an ``ExpressionTree`` instance to simplify the declarations."""

EX = Union[bool, int, float, str, suite.ConstVar, suite.NamedType, ET]
"""Extended expression tree to simplify use of the create functions."""

LX = Union[EX, Sequence[EX]]
"""Extended sequence of expression trees to simplify the use of create functions."""


class _Value(ET):
    """Provides a literal value."""

    def __init__(self, value: str, kind: str, label: str = ''):
        """Literal value."""
        super().__init__(label)
        self.value = value
        self.kind = kind

    def _build_expression(self, context: suite.Object) -> suite.Expression:
        """Build a SCADE Suite expression from the expression tree."""
        value = suite.ConstValue(context)
        value.value = self.value
        value.kind = self.kind
        # no comment...
        if self.kind == 'String':
            value.role_kind = 'For Structure'
        self._set_label(value, context)
        return value


class _Reference(ET):
    """Provides a reference to a SCADE constant or variable."""

    def __init__(self, reference: suite.ConstVar, label: str = ''):
        """Initialize a constant, sensor, or local variable."""
        super().__init__(label)
        self.reference = reference

    def _build_expression(self, context: suite.Object) -> suite.Expression:
        """Build a SCADE Suite expression from the expression tree."""
        expr = suite.ExprId(context)
        self._set_label(expr, context)
        _add_pending_link(expr, 'reference', self.reference)
        return expr


class _Type(ET):
    """Creates a reference to a type."""

    def __init__(self, type_: suite.NamedType, label: str = ''):
        """Initialize a named type."""
        super().__init__(label)
        self.type = type_

    def _build_expression(self, context: suite.Object) -> suite.Expression:
        """Build a SCADE Suite expression from the expression tree."""
        expr = suite.ExprType(context)
        _add_pending_link(expr, 'type', self.type)
        return expr


class _Call(ET):
    """Provides the base class for expression calls."""

    def __init__(
        self,
        args: List[ET],
        inst_args: List[ET],
        modifiers: List[ET],
        name: str = '',
        label: str = '',
    ):
        super().__init__(label)
        self.args = args
        self.inst_args = inst_args
        self.modifiers = modifiers
        self.name = name

    def _build_expression(self, context: suite.Object) -> suite.Expression:
        """Build a SCADE Suite expression from the expression tree."""
        expr = suite.ExprCall()
        expr.inst_name = self.name
        expr.parameters = [_._build_expression(context) for _ in self.args]
        expr.inst_parameters = [_._build_expression(context) for _ in self.inst_args]
        owner = expr
        for modifier in self.modifiers:
            subexpr = modifier._build_expression(context)
            owner.modifier = subexpr
            owner = subexpr
        # label, even if very unlinkely
        self._set_label(expr, context)
        return expr


class _Predefined(_Call):
    """Provides a calls to a predefined operator."""

    def __init__(
        self,
        eck: Eck,
        args: List[ET],
        inst_args: List[ET],
        modifiers: List[ET],
        name: str = '',
        label: str = '',
    ):
        super().__init__(args, inst_args, modifiers, name, label)
        self.eck = eck

    def _build_expression(self, context: suite.Object) -> suite.Expression:
        """Build a SCADE Suite expression from the expression tree."""
        expr = super()._build_expression(context)
        expr.predef_opr = self.eck.value
        return expr


class _Operator(_Call):
    """Provides a call to a user operator."""

    def __init__(
        self,
        operator: suite.Operator,
        args: List[ET],
        inst_args: List[ET],
        modifiers: List[ET],
        name: str = '',
        label: str = '',
    ):
        super().__init__(args, inst_args, modifiers, name, label)
        self.operator = operator

    def _build_expression(self, context: suite.Object) -> suite.Expression:
        """Build a SCADE Suite expression from the expression tree."""
        expr = super()._build_expression(context)
        expr.operator = self.operator
        return expr


def _normalize_tree(any: EX) -> ET:
    """Create expression tree instances from literals or SCADE objects."""
    if isinstance(any, ET):
        return any
    # collections
    if isinstance(any, tuple) or isinstance(any, list):
        # backward compatibility: use _normalize_trees instead for proper typing
        if len(any) == 0:
            raise EmptyTreeError()
        return [_normalize_tree(_) for _ in any]  # type: ignore
    # SCADE objects
    if isinstance(any, suite.ConstVar):
        return _Reference(any)
    if isinstance(any, suite.NamedType):
        return _Type(any)
    # literals
    # true | false | <integer> | <real> | ' <char> ' | " <ident> "
    if isinstance(any, bool):
        return _Value(str(any).lower(), 'Bool')
    elif isinstance(any, int):
        return _Value(str(any), 'Int')
    elif isinstance(any, float):
        return _Value(str(any), 'Real')
    elif isinstance(any, str):
        if _is_bool(any):
            return _Value(str(any), 'Bool')
        elif _is_int(any):
            # number with an optional suffix _i8, ui32, etc.
            return _Value(any, 'Int')
        elif _is_real(any):
            # number with an optional suffix _f32 or _f64
            return _Value(any, 'Real')
        elif len(any) > 1 and any[0] == "'":
            # no additional verification on the syntax
            return _Value(any, 'Char')
        elif any.isidentifier():
            # used in projections only
            return _Value(any, 'String')

    # fall through
    raise ExprSyntaxError('_normalize_tree', any)


def _normalize_trees(any: Sequence[EX]) -> List[ET]:
    """Normalize a collection of expression trees."""
    if len(any) == 0:
        raise EmptyTreeError()
    return [_normalize_tree(_) for _ in any]


def _normalize_tree_ex(any: LX) -> List[ET]:
    """Normalize a collection of expression trees or a single one."""
    if isinstance(any, list):
        return _normalize_trees(any)
    else:
        return [_normalize_tree(any)]


def _build_expression(tree: EX, context: suite.Object) -> suite.Expression:
    """
    Build an expression from an extended expression tree.

    Parameters
    ----------
    tree : EX
        Operand: expression tree.
    context : suite.Object
        Context of the creation of the expression.

    Returns
    -------
    suite.Expression
    """
    # backward compatibility: allow None expressions
    if tree is None:
        return None
    norm_tree = _normalize_tree(tree)
    return norm_tree._build_expression(context)


# association tables
_unary_ops = {
    '-': Eck.NEG,
    '+': Eck.POS,
    '!': Eck.NOT,
    'int': Eck.REAL2INT,
    'real': Eck.INT2REAL,
    'lnot': Eck.LNOT,
}
_binary_ops = {
    '&': Eck.AND,
    '|': Eck.OR,
    '^': Eck.XOR,
    '#': Eck.SHARP,
    '+': Eck.PLUS,
    '-': Eck.SUB,
    '*': Eck.MUL,
    '/': Eck.SLASH,
    ':': Eck.DIV,
    '%': Eck.MOD,
    '<': Eck.LESS,
    '<=': Eck.LEQUAL,
    '>': Eck.GREAT,
    '>=': Eck.GEQUAL,
    '=': Eck.EQUAL,
    '<>': Eck.NEQUAL,
    'land': Eck.LAND,
    'lor': Eck.LOR,
    'lxor': Eck.LXOR,
    '<<': Eck.LSL,
    '>>': Eck.LSR,
}
_nary_ops = {'&': Eck.AND, '|': Eck.OR, '^': Eck.XOR, '#': Eck.SHARP, '+': Eck.PLUS, '*': Eck.MUL}


def create_call(operator: suite.Operator, args: LX, inst_args: Optional[LX] = None) -> ET:
    """
    Return the expression tree for a call to an operator.

    Parameters
    ----------
    op : suite.Operator
        Operator to call.
    args : Union[EX, List[EX]]
        Parameters: expression trees.
    inst_args : Union[EX, List[EX], None], default: None
        Instance parameters: expression trees.

    Returns
    -------
    ET
    """
    if inst_args is None:
        inst_args = []
    _check_object(operator, 'create_call', 'operator', suite.Operator)
    norm_args = _normalize_tree_ex(args) if args else []
    norm_inst_args = _normalize_tree_ex(inst_args) if inst_args else []
    return _Operator(operator, norm_args, norm_inst_args, [])


def create_higher_order_call(
    operator: suite.Operator,
    args: LX,
    modifiers: Union[ET, List[ET]],
    inst_args: Optional[LX] = None,
) -> ET:
    """
    Return the expression tree for a call to an operator.

    Parameters
    ----------
    op : suite.Operator
        Operator to call.
    args : Union[EX, List[EX]]
        Parameters: expression trees.
    modifiers : Union[ET, List[ET]]
        Higher-order constructs: expression trees.
    inst_args : Union[EX, List[EX], None], default: None
        Instance parameters: expression trees.

    Returns
    -------
    ET
    """
    if inst_args is None:
        inst_args = []
    _check_object(operator, 'create_higher_order_call', 'operator', suite.Operator)
    norm_args = _normalize_tree_ex(args) if args else []
    norm_inst_args = _normalize_tree_ex(inst_args) if inst_args else []
    modifiers = modifiers if isinstance(modifiers, list) else [modifiers] if modifiers else []
    return _Operator(operator, norm_args, norm_inst_args, modifiers)


# arithmetic and logic


def create_unary(op: str, tree: EX, modifiers: Union[ET, List[ET], None] = None) -> ET:
    """
    Return the expression tree for a unary operator.

    Parameters
    ----------
    op : str
        Unary operator to call: - | + | !
    tree : EX
        Operand: expression tree.
    modifiers : Union[ET, LIST[ET], None], default: None
        List of higher-order constructs.

    Returns
    -------
    ET
    """
    eck = _unary_ops.get(op)
    if eck is None:
        raise ExprSyntaxError('create_unary', op)
    norm_tree = _normalize_tree(tree)
    modifiers = modifiers if isinstance(modifiers, list) else [modifiers] if modifiers else []
    return _Predefined(eck, [norm_tree], [], modifiers)


def create_binary(
    op: str, tree1: EX, tree2: EX, modifiers: Union[ET, List[ET], None] = None
) -> ET:
    """
    Return the expression tree for a binary operator.

    Parameters
    ----------
    op : str
        Binary operator to call: & | | | ^ | # | + | - | * | / | : | % | < | <= | > | >= | = | <>
    tree1 : EX
        First operand: expression tree.
    tree2 : EX
        Second operand: expression tree.
    modifiers : Union[ET, List[ET], None], default: None
        List of higher-order constructs.

    Returns
    -------
    ET
    """
    eck = _binary_ops.get(op)
    if eck is None:
        raise ExprSyntaxError('create_binary', op)
    norm_tree1, norm_tree2 = _normalize_trees((tree1, tree2))
    modifiers = modifiers if isinstance(modifiers, list) else [modifiers] if modifiers else []
    return _Predefined(eck, [norm_tree1, norm_tree2], [], modifiers)


def create_nary(op: str, *args: EX, modifiers: Union[ET, List[ET], None] = None) -> ET:
    r"""
    Return the expression tree for a nary operator.

    Parameters
    ----------
    op : str
        Nary operator to call: & | | | ^ | # | + | *
    \*args : EX
        Operands: expression trees.
    modifiers : Union[ET, List[ET], None], default: None
        List of higher-order constructs, to be provided as keyword parameter.

    Returns
    -------
    ET
    """
    eck = _nary_ops.get(op)
    if eck is None:
        raise ExprSyntaxError('create_nary', op)
    if len(args) < 2:
        raise ExprSyntaxError('create_nary', args)
    norm_args = _normalize_trees(args)
    modifiers = modifiers if isinstance(modifiers, list) else [modifiers] if modifiers else []
    return _Predefined(eck, norm_args, [], modifiers)


# selectors


def create_if(condition: EX, then: LX, else_: LX) -> ET:
    r"""
    Return the expression tree for the if-then-else operator.

    Notes
    -----
    This is an interface change with respect to the *SCADE Creation Library*.
    The ``then`` flows and ``else`` flows are now specified in two separate lists.

    Parameters
    ----------
    condition : EX
        Expression tree corresponding to the condition of the selector.
    then : Union[EX, List[EX]]
        List of expressions trees when the condition is ``True``.
    else\_ : Union[EX, List[EX]]
        List of expressions trees when the condition is ``False``.

    Returns
    -------
    ET
    """
    norm_then = _normalize_tree_ex(then)
    norm_else = _normalize_tree_ex(else_)
    length = len(norm_then)
    if length == 0 or length != len(norm_else):
        raise ExprSyntaxError('create_if', then)

    norm_condition = _normalize_tree(condition)
    then_tree = _create_sequence(norm_then)
    else_tree = _create_sequence(norm_else)

    return _Predefined(Eck.IF, [norm_condition, then_tree, else_tree], [], [])


def create_case(selector: EX, cases: List[Tuple[EX, EX]], default: Optional[EX] = None) -> ET:
    """
    Return the expression tree for the case operator.

    Notes
    -----
    This is an interface change with respect to the *SCADE Creation Library*.
    The pairs "pattern"/"value" are now embedded in a list of tuples, and the
    default value is optional.

    Parameters
    ----------
    selector : EX
        Expression tree corresponding to the selector.
    cases : List[Tuple[EX, EX]]
        Pattern/values expression trees.
    default: EX | None, default:None
        Default value.

    Returns
    -------
    ET
    """
    if len(cases) == 0:
        raise ExprSyntaxError('create_case', cases)

    norm_selector = _normalize_tree(selector)
    patterns = []
    inputs = []
    for pattern, input in cases:
        patterns.append(_normalize_tree(pattern))
        inputs.append(_normalize_tree(input))
    if default:
        inputs.append(_normalize_tree(default))
    pattern_tree = _create_sequence(patterns)
    input_tree = _create_sequence(inputs)

    return _Predefined(Eck.CASE, [norm_selector, input_tree, pattern_tree], [], [])


# types


def create_make(
    type_: suite.NamedType, *args: EX, modifiers: Union[ET, List[ET], None] = None
) -> ET:
    r"""
    Return the expression tree for making a structured value.

    Parameters
    ----------
    type\_ : suite.NamedType
        Type to instantiate.
    \*args : EX
        Values of the type instance.
    modifiers : Union[ET, List[ET], None], default: None
        List of higher-order constructs, which is provided as a keyword parameter.

    Returns
    -------
    ET
    """
    if len(args) < 1:
        raise ExprSyntaxError('create_make', args)
    _check_object(type_, 'create_make', 'type', suite.NamedType)
    norm_type = _normalize_tree(type_)
    norm_args = _normalize_trees(args)
    modifiers = modifiers if isinstance(modifiers, list) else [modifiers] if modifiers else []
    return _Predefined(Eck.MAKE, [_create_sequence(norm_args), norm_type], [], modifiers)


def create_flatten(
    type_: suite.NamedType, arg: EX, modifiers: Union[ET, List[ET], None] = None
) -> ET:
    r"""
    Return the expression tree for flattening a structured value.

    Parameters
    ----------
    type\_ : suite.NamedType
        Type to instantiate.
    arg : EX
        Value to flatten.
    modifiers : Union[ET, List[ET], None], default: None
        List of higher-order constructs.

    Returns
    -------
    ET
    """
    _check_object(type_, 'create_flatten', 'type', suite.NamedType)
    norm_type = _normalize_tree(type_)
    norm_arg = _normalize_tree(arg)
    modifiers = modifiers if isinstance(modifiers, list) else [modifiers] if modifiers else []
    return _Predefined(Eck.FLATTEN, [norm_arg, norm_type], [], modifiers)


def create_numeric_cast(type_: suite.NamedType, arg: EX) -> ET:
    r"""
    Return the expression tree for casting a numerical value.

    Parameters
    ----------
    type\_ : suite.NamedType
        Type to cast to.
    arg : EX
        Value to cast.

    Returns
    -------
    ET
    """
    _check_object(type_, 'create_numeric_cast', 'type', suite.NamedType)
    norm_type = _normalize_tree(type_)
    norm_arg = _normalize_tree(arg)
    return _Predefined(Eck.NUMERIC_CAST, [norm_arg, norm_type], [], [])


# structures


def create_scalar_to_vector(size: EX, *args: EX) -> ET:
    r"""
    Return the expression tree for the scalar-to-vector operator.

    Notes
    -----
    This is an interface change with respect to the *SCADE Creation Library*.
    The parameter size has moved from the last position to the first one.

    Parameters
    ----------
    size: EX
        Size of the vector.
    \*args : EX
        Input values.

    Returns
    -------
    ET
    """
    if len(args) == 0:
        raise ExprSyntaxError('create_scalar_to_vector', args)
    norm_size = _normalize_tree(size)
    norm_args = _normalize_trees(args)
    # the size must be the last parameter
    return _Predefined(Eck.SCALAR_TO_VECTOR, norm_args + [norm_size], [], [])


def create_data_array(*args: EX) -> ET:
    r"""
    Return the expression tree for the data array operator.

    Parameters
    ----------
    \*args : EX
        Values of the array.

    Returns
    -------
    ET
    """
    if len(args) == 0:
        raise ExprSyntaxError('create_data_array', args)
    norm_args = _normalize_trees(args)
    return _Predefined(Eck.BLD_VECTOR, norm_args, [], [])


def create_data_struct(*args: Tuple[str, EX]) -> ET:
    r"""
    Return the expression tree for the data strictire operator.

    Notes
    -----
    This is an interface change with respect to the *SCADE Creation Library*.
    The pairs "name"/"value" are now embedded in a list of tuples.

    Parameters
    ----------
    \*args : Tuple[str, EX]
        Label/values expression trees.

    Returns
    -------
    ET
    """
    length = len(args)
    if length == 0:
        raise ExprSyntaxError('create_data_struct', args)

    parameters = []
    for label, value in args:
        if not isinstance(label, str) or not label.isidentifier():
            raise TypeIdentifierError('create_data_struct', args)
        parameter = _normalize_tree(value)
        parameter.label = label
        parameters.append(parameter)
    return _Predefined(Eck.BLD_STRUCT, parameters, [], [])


def create_prj(flow: EX, path: LX) -> ET:
    """
    Return the expression tree for the projection operator.

    Parameters
    ----------
    flow : EX
        Input flow of the projection.
    path : Union[EX, List[EX]]
        Elements of the path, which is either the label or index.

    Returns
    -------
    ET
    """
    norm_flow = _normalize_tree(flow)
    norm_path = _normalize_tree_ex(path)
    parameters = [norm_flow] + norm_path
    return _Predefined(Eck.PRJ, parameters, [], [])


def create_prj_dyn(flow: EX, path: LX, default: EX) -> ET:
    """
    Return the expression tree for the dynamic projection operator.

    Parameters
    ----------
    flow : EX
        Input flow of the projection.
    path : Union[EX, List[EX]]
        Elements of the path, which is a label, index, or variable.
    default : EX
        Default value for the projection when the path is incorrect.

    Returns
    -------
    ET
    """
    norm_flow, norm_default = _normalize_trees((flow, default))
    norm_path = _normalize_tree_ex(path)
    parameters = [norm_flow] + norm_path + [norm_default]
    return _Predefined(Eck.PRJ_DYN, parameters, [], [])


def create_change_ith(flow: EX, path: LX, value: EX) -> ET:
    """
    Return the expression tree for the with operator.

    Parameters
    ----------
    flow : EX
        Input flow of the projection.
    path : Union[EX, List[EX]]
        Elements of the path, which is a label, index, or variable.
    value : EX
        Value to assign.

    Returns
    -------
    ET
    """
    norm_flow, norm_value = _normalize_trees((flow, value))
    norm_path = _normalize_tree_ex(path)
    parameters = [norm_flow, norm_value] + norm_path
    return _Predefined(Eck.CHANGE_ITH, parameters, [], [])


# time


def create_pre(*args: EX) -> ET:
    r"""
    Return the expression tree for the pre operator.

    Parameters
    ----------
    \*args : EX
        Input flows.

    Returns
    -------
    ET
    """
    if len(args) == 0:
        raise ExprSyntaxError('create_pre', '')
    norm_args = _normalize_trees(args)
    return _Predefined(Eck.PRE, norm_args, [], [])


def create_init(flows: LX, inits: LX) -> ET:
    """
    Return the expression tree for the init operator.

    Notes
    -----
    This is an interface change with respect to the *SCADE Creation Library*.
    The flows and their initial values are now specified in two separate lists.

    Parameters
    ----------
    flows : Union[EX, List[EX]]
        Input flows.
    inits : Union[EX, List[EX]]
        Initial values.

    Returns
    -------
    ET
    """
    norm_flows = _normalize_tree_ex(flows)
    norm_inits = _normalize_tree_ex(inits)
    length = len(norm_flows)
    if length == 0 or length != len(norm_inits):
        raise ExprSyntaxError('create_init', flows)

    flows_tree = _create_sequence(norm_flows)
    inits_tree = _create_sequence(norm_inits)

    return _Predefined(Eck.FOLLOW, [flows_tree, inits_tree], [], [])


def create_fby(flows: LX, delay: EX, inits: LX) -> ET:
    """
    Return the expression tree for the init operator.

    Notes
    -----
    This is an interface change with respect to the *SCADE Creation Library*.
    The flows and their initial values are now specified in two separate lists.

    Parameters
    ----------
    flows : Union[EX, List[EX]]
        Input flows.
    delay : EX
        Delay of the operator.
    inits : Union[EX, List[EX]]
        Initial values.

    Returns
    -------
    ET
    """
    norm_flows = _normalize_tree_ex(flows)
    norm_inits = _normalize_tree_ex(inits)
    length = len(norm_flows)
    if length == 0 or length != len(norm_inits):
        raise ExprSyntaxError('create_fby', flows)

    norm_delay = _normalize_tree(delay)
    parameters = norm_flows + [norm_delay] + norm_inits
    return _Predefined(Eck.FBY, parameters, [], [])


def create_times(number: EX, flow: EX) -> ET:
    """
    Return the expression tree for the times operator.

    Parameters
    ----------
    number : EX
        Number of cycles.
    flow : EX
        Input flow.

    Returns
    -------
    ET
    """
    norm_number, norm_flow = _normalize_trees((number, flow))
    return _Predefined(Eck.TIMES, [norm_number, norm_flow], [], [])


# array


def create_slice(array: EX, start: EX, end: EX) -> ET:
    """
    Return the expression tree for the slice operator.

    Parameters
    ----------
    array : EX
        Input array.
    start : EX
        Start index of the slice.
    end : EX
        End index of the slice.

    Returns
    -------
    ET
    """
    norm_array, norm_start, norm_end = _normalize_trees((array, start, end))
    return _Predefined(Eck.SLICE, [norm_array, norm_start, norm_end], [], [])


def create_concat(*args: EX) -> ET:
    r"""
    Return the expression tree for the concat operator.

    Parameters
    ----------
    \*args : EX
        Input arrays to concatenate.

    Returns
    -------
    ET
    """
    if len(args) < 2:
        raise ExprSyntaxError('create_concat', args)
    norm_args = _normalize_trees(args)
    return _Predefined(Eck.CONCAT, norm_args, [], [])


def create_reverse(flow: EX) -> ET:
    """
    Return the expression tree for the reverse operator.

    Parameters
    ----------
    flow : EX
        Input flow.

    Returns
    -------
    ET
    """
    norm_flow = _normalize_tree(flow)
    return _Predefined(Eck.REVERSE, [norm_flow], [], [])


def create_transpose(array: EX, dim1: EX, dim2: EX) -> ET:
    """
    Return the expression tree for the transpose operator.

    Parameters
    ----------
    array : EX
        Input array.
    dim1 : EX
        First dimension.
    dim2 : EX
        Second dimension.

    Returns
    -------
    ET
    """
    norm_array, norm_dim1, norm_dim2 = _normalize_trees((array, dim1, dim2))
    return _Predefined(Eck.TRANSPOSE, [norm_array, norm_dim1, norm_dim2], [], [])


# activation


def create_restart(every: EX) -> ET:
    """
    Return the expression tree for the higher-order construct for restarting.

    Parameters
    ----------
    every : EX
        Input condition.

    Returns
    -------
    ET
    """
    norm_every = _normalize_tree(every)
    return _Predefined(Eck.RESTART, [norm_every], [], [])


def create_activate(every: EX, *args: EX) -> ET:
    r"""
    Return the expression tree for the higher-order construct for activating with initial values.

    Parameters
    ----------
    every : EX
        Input condition.
    \*args: EX
        Initial values.

    Returns
    -------
    ET
    """
    norm_every = _normalize_tree(every)
    # args may be empty
    norm_args = _normalize_trees(args) if args else []
    return _Predefined(Eck.ACTIVATE, [norm_every, _create_sequence(norm_args)], [], [])


def create_activate_no_init(every: EX, *args: EX) -> ET:
    r"""
    Return the expression tree for the higher-order construct for activating with default values.

    Parameters
    ----------
    every : EX
        Input condition.
    \*args: EX
        Default values.

    Returns
    -------
    ET
    """
    norm_every = _normalize_tree(every)
    # args may be empty
    norm_args = _normalize_trees(args) if args else []
    return _Predefined(Eck.ACTIVATE_NOINIT, [norm_every, _create_sequence(norm_args)], [], [])


# iterators


def create_map(size: EX) -> ET:
    """
    Return the expression tree for the higher-order construct for map creation.

    Parameters
    ----------
    size : EX
        Number of iterations.

    Returns
    -------
    ET
    """
    norm_size = _normalize_tree(size)
    return _Predefined(Eck.MAP, [norm_size], [], [])


def create_mapi(size: EX) -> ET:
    """
    Return the expression tree for the higher-order construct for mapi creation.

    Parameters
    ----------
    size : EX
        Number of iterations.

    Returns
    -------
    ET
    """
    norm_size = _normalize_tree(size)
    return _Predefined(Eck.MAPI, [norm_size], [], [])


def create_fold(size: EX) -> ET:
    """
    Return the expression tree for the higher-order construct for fold creation.

    Parameters
    ----------
    size : EX
        Number of iterations.

    Returns
    -------
    ET
    """
    norm_size = _normalize_tree(size)
    return _Predefined(Eck.FOLD, [norm_size], [], [])


def create_foldi(size: EX) -> ET:
    """
    Return the expression tree for the higher-order construct for foldi creation.

    Parameters
    ----------
    size : EX
        Number of iterations.

    Returns
    -------
    ET
    """
    norm_size = _normalize_tree(size)
    return _Predefined(Eck.FOLDI, [norm_size], [], [])


def create_mapfold(size: EX, acc: EX) -> ET:
    """
    Return the expression tree for the higher-order construct for mapfold creation.

    Parameters
    ----------
    size : EX
        Number of iterations.
    acc : EX
        Number of accumulators.

    Returns
    -------
    ET
    """
    norm_size, norm_acc = _normalize_trees((size, acc))
    return _Predefined(Eck.MAPFOLD, [norm_size, norm_acc], [], [])


def create_mapfoldi(size: EX, acc: EX) -> ET:
    """
    Return the expression tree for the higher-order construct for mapfoldi creation.

    Parameters
    ----------
    size : EX
        Number of iterations.

    acc : EX
        Number of accumulators.

    Returns
    -------
    ET
    """
    norm_size, norm_acc = _normalize_trees((size, acc))
    return _Predefined(Eck.MAPFOLDI, [norm_size, norm_acc], [], [])


def create_foldw(size: EX, condition: EX) -> ET:
    """
    Return the expression tree for the higher-order construct for foldw creation.

    Parameters
    ----------
    size : EX
        Number of iterations.
    condition : EX
        Initial value of the iteration condition.

    Returns
    -------
    ET
    """
    norm_size, norm_condition = _normalize_trees((size, condition))
    return _Predefined(Eck.FOLDW, [norm_size, norm_condition], [], [])


def create_foldwi(size: EX, condition: EX) -> ET:
    """
    Return the expression tree for the higher-order construct for foldwi creation.

    Parameters
    ----------
    size : EX
        Number of iterations.
    condition : EX
        Initial value of the iteration condition.

    Returns
    -------
    ET
    """
    norm_size, norm_condition = _normalize_trees((size, condition))
    return _Predefined(Eck.FOLDWI, [norm_size, norm_condition], [], [])


def create_mapw(size: EX, condition: EX, default: EX) -> ET:
    """
    Return the expression tree for the higher-order construct for mapw creation.

    Parameters
    ----------
    size : EX
        Number of iterations.
    condition : EX
        Initial value of the iteration condition.
    default : EX
        Default value of the iteration.

    Returns
    -------
    ET
    """
    norm_size, norm_condition, norm_default = _normalize_trees((size, condition, default))
    return _Predefined(Eck.MAPW, [norm_size, norm_condition, norm_default], [], [])


def create_mapwi(size: EX, condition: EX, default: EX) -> ET:
    """
    Return the expression tree for the higher-order construct for mapdwi creation.

    Parameters
    ----------
    size : EX
        Number of iterations.
    condition : EX
        Initial value of the iteration condition.
    default : EX
        Default value of the iteration.

    Returns
    -------
    ET
    """
    norm_size, norm_condition, norm_default = _normalize_trees((size, condition, default))
    return _Predefined(Eck.MAPWI, [norm_size, norm_condition, norm_default], [], [])


def create_mapfoldw(size: EX, acc: EX, condition: EX, default: EX) -> ET:
    """
    Return the expression tree for the higher-order construct for mapfoldw creation.

    Parameters
    ----------
    size : EX
        Number of iterations.
    acc : EX
        Number of accumulators.
    condition : EX
        Initial value of the iteration condition.
    default : EX
        Default value of the iteration.

    Returns
    -------
    ET
    """
    norm_size, norm_acc, norm_condition, norm_default = _normalize_trees(
        (size, acc, condition, default)
    )
    return _Predefined(Eck.MAPFOLDW, [norm_size, norm_acc, norm_condition, norm_default], [], [])


def create_mapfoldwi(size: EX, acc: EX, condition: EX, default: EX) -> ET:
    """
    Return the expression tree for the higher-order construct for mapfoldwi creation.

    Parameters
    ----------
    size : EX
        Number of iterations.
    acc : EX
        Number of accumulators.
    condition : EX
        Initial value of the iteration condition.
    default : EX
        Default value of the iteration.

    Returns
    -------
    ET
    """
    norm_size, norm_acc, norm_condition, norm_default = _normalize_trees(
        (size, acc, condition, default)
    )
    return _Predefined(Eck.MAPFOLDWI, [norm_size, norm_acc, norm_condition, norm_default], [], [])


# ----------------------------------------------------------------------------
# Helpers (private)


def _create_sequence(flows: List[ET]) -> ET:
    """Create an expression tree for a group of flows."""
    return _Predefined(Eck.SEQ_EXPR, flows, [], [])


class ExprSyntaxError(Exception):
    """Provides the generic exception for syntax errors in expression trees."""

    def __init__(self, context, item):
        """Provide a customized message."""
        super().__init__('%s: %s: Syntax error' % (context, item))


class TypeIdentifierError(Exception):
    """Provides the exception for incorrect identifiers."""

    def __init__(self, context, item):
        """Provide a customized message."""
        super().__init__('%s: %s: Not a valid identifier' % (context, item))


class EmptyTreeError(Exception):
    """Provides the exception for empty expression trees."""

    def __init__(self):
        """Provide a customized message."""
        super().__init__('_normalize_tree: Illegal empty tree')


def _is_int(number: str) -> bool:
    # trivial test first
    try:
        _ = int(number)
        return True
    except ValueError:
        pass
    tokens = number.split('_', 1)
    if len(tokens) != 2:
        return False
    if tokens[1] in {'i8', 'i16', 'i32', 'i64', 'ui8', 'ui16', 'ui32', 'ui64'}:
        try:
            _ = int(tokens[0])
            return True
        except ValueError:
            pass
    return False


def _is_real(number: str) -> bool:
    # trivial test first
    try:
        _ = float(number)
        return True
    except ValueError:
        pass
    tokens = number.split('_', 1)
    if len(tokens) == 2 and tokens[1] in ('f32', 'f64'):
        try:
            _ = float(tokens[0])
            return True
        except ValueError:
            pass
    return False


def _is_bool(value: str) -> bool:
    # trivial test first
    return value == 'true' or value == 'false'


# TODO: modifiers
# TODO: move to query
def _find_expr_id(expr: suite.Expression, index: int) -> Optional[suite.ExprId]:
    """
    Return the ``ExprId`` instance corresponding to the pin index of an equation.

    Notes
    -----
    This function is not currently complete and must be specified more precisely.

    Parameters
    ----------
    expr : suite.Expression
        Expression to consider, either an ExprId or ExprCall.
    index : int
        Pin number.

    Returns
    -------
    suite.ExprId
    """
    if isinstance(expr, suite.ExprId):
        # the expression itself!
        # index shall be 0
        return expr if index == 0 else None
    elif not isinstance(expr, suite.ExprCall):
        # shall not occur: return the expression
        # the caller is responsible for displaying the error
        return None

    # expr is an ExprCall
    params = expr.parameters
    code = Eck(expr.predef_opr)
    if code == Eck.IF:
        expr_cond, expr_then, expr_else = params
        # rebuild a new list of parameters
        params = [expr_cond]
        params.extend(expr_then.parameters)
        params.extend(expr_else.parameters)
    elif code == Eck.CASE:
        expr_selector, expr_inputs, _ = params
        # rebuild a new list of parameters
        params = [expr_selector]
        params.extend(expr_inputs.parameters)
    elif code == Eck.MAKE:
        expr_inputs, _ = params
        # rebuild a new list of parameters
        params = expr_inputs.parameters
    elif code == Eck.BLD_STRUCT:
        # rebuild a new list of parameters
        params = (value for name, value in params)
    elif code == Eck.FOLLOW:
        expr_flows, expr_inits = params
        # rebuild a new list of parameters
        params = expr_flows.parameters + expr_inits.parameters
    else:
        # operator call
        # unary, n-ary...
        # "FLATTEN" - "SCALAR_TO_VECTOR" - "BLD_VECTOR" - "PRJ" - "PRJ_DYN" - "CHANGE_ITH" -
        # "PRE" - "FBY" - "TIMES" - "SLICE" - "CONCAT" - "REVERSE" - "TRANSPOSE"
        # (includes operator call)
        # ith parameter (TODO: check index vs [llength $params])
        # list params left unchanged
        pass
    # TODO RESTART, ACTIVATE, ACTIVATE_NO_INIT, MAP/FOLD*
    return params[index]
