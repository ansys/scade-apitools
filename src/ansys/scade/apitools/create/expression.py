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
Helpers to create expression trees.

Expression trees are intermediate structures to declare any arbitrary complex
expressions, and then create the corresponding SCADE Suite expressions in the
context of a model element, for example the right part of an equation or the
default value of an output.

This module provides functions to create an expression tree for any expression
of the Scade language, including higher order constructs. Thus, the intermediate
structures or classes defining the expression trees can be opaque.

Notes: the typing is relaxed in this module to ease the constructs.

* ``ET`` is an alias for ``ExpressionTree`` to shorten the declarations.

* ``EX``, standing for extended expression tree, is defined as::

     Union[bool, int, float, str, suite.ConstVar, suite.NamedType, ET]

  This enhances the usability of these functions by accepting some values,
  such as Python literals, string values or SCADE Python objects, as valid
  expression trees.

* ``LX``, standing for extended lists of expression trees, is defined as::

     Union[EX, List[EX]]

  When the expressions accept an arbitrary number of input flows, for example
  if-then-else or fby, it is allowed to provide either one expression tree or a list
  of expression trees.

"""

from typing import List, Tuple, Union

import scade.model.suite as suite

from ..expr import Eck
from .project import _check_object
from .scade import _add_pending_link


# expression trees
class ExpressionTree:
    """Top-level abstract class for expression trees."""

    def __init__(self, label: str = ''):
        """Any expression can have a label."""
        self.label = label

    def _build_expression(self, context: suite.Object) -> suite.Expression:
        """Build a SCADE Suite expression from the expression tree."""
        # must be overridden
        assert False  # pragma no cover

    def _set_label(self, expr: suite.Expression, context: suite.Object):
        """Add the label to the expression, if any."""
        if self.label:
            label = suite.Label(context)
            label.name = self.label
            expr.label = label


ET = ExpressionTree
"""Short name for Expression Tree to simplify the declarations."""

EX = Union[bool, int, float, str, suite.ConstVar, suite.NamedType, ET]
"""Extended expression tree to simply the usage of the creation functions."""

LX = Union[EX, List[EX]]
"""Extended lists of expression trees to simply the usage of the creation functions."""


class _Value(ET):
    """Literal value."""

    def __init__(self, value: str, kind: str, **kwargs):
        """Literal value."""
        super().__init__(**kwargs)
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
    """Reference to a SCADE ConstVar."""

    def __init__(self, reference: suite.ConstVar, **kwargs):
        """Shall be a constant, sensor or local variable."""
        super().__init__(**kwargs)
        self.reference = reference

    def _build_expression(self, context: suite.Object) -> suite.Expression:
        """Build a SCADE Suite expression from the expression tree."""
        expr = suite.ExprId(context)
        self._set_label(expr, context)
        _add_pending_link(expr, 'reference', self.reference)
        return expr


class _Type(ET):
    """Reference to a type."""

    def __init__(self, type_: suite.NamedType, **kwargs):
        """Shall be a named type."""
        super().__init__(**kwargs)
        self.type = type_

    def _build_expression(self, context: suite.Object) -> suite.Expression:
        """Build a SCADE Suite expression from the expression tree."""
        expr = suite.ExprType(context)
        _add_pending_link(expr, 'type', self.type)
        return expr


class _Call(ET):
    """Base class for expression calls."""

    def __init__(
        self, args: List[ET], inst_args: List[ET], modifiers: List[ET], name: str = '', **kwargs
    ):
        super().__init__(**kwargs)
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
    """Call to a predefined operator."""

    def __init__(self, eck: Eck, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.eck = eck

    def _build_expression(self, context: suite.Object) -> suite.Expression:
        """Build a SCADE Suite expression from the expression tree."""
        expr = super()._build_expression(context)
        expr.predef_opr = self.eck.value
        return expr


class _Operator(_Call):
    """Call to a user operator."""

    def __init__(self, operator: suite.Operator, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
        if len(any) == 0:
            raise EmptyTreeError()
        return [_normalize_tree(_) for _ in any]
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


def _normalize_tree_ex(any: LX) -> List[ET]:
    """Normalize a collection of expression trees or a single one."""
    if isinstance(any, list):
        return _normalize_tree(any)
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
    if tree is None:
        return None
    tree = _normalize_tree(tree)
    return tree._build_expression(context)


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


def create_call(operator: suite.Operator, args: LX, inst_args: LX = None) -> ET:
    """
    Return the expression tree for a call to an operator.

    Parameters
    ----------
        op : suite.Operator
            Called operator

        args : Union[EX, List[EX]]
            Parameters: expression trees.

        inst_args : Union[EX, List[EX]]
            Instance parameters: expression trees.

    Returns
    -------
        ET
    """
    if inst_args is None:
        inst_args = []
    _check_object(operator, 'create_call', 'operator', suite.Operator)
    args = _normalize_tree_ex(args) if args else []
    inst_args = _normalize_tree_ex(inst_args) if inst_args else []
    return _Operator(operator, args, inst_args, [])


def create_higher_order_call(
    operator: suite.Operator, args: LX, modifiers: Union[ET, List[ET]], inst_args: LX = None
) -> ET:
    """
    Return the expression tree for a call to an operator.

    Parameters
    ----------
        op : suite.Operator
            Called operator

        args : Union[EX, List[EX]]
            Parameters: expression trees.

        modifiers : Union[ET, List[ET]]
            Higher order constructs: expression trees.

        inst_args : Union[EX, List[EX]]
            Instance parameters: expression trees.

    Returns
    -------
        ET
    """
    if inst_args is None:
        inst_args = []
    _check_object(operator, 'create_higher_order_call', 'operator', suite.Operator)
    args = _normalize_tree_ex(args) if args else []
    inst_args = _normalize_tree_ex(inst_args) if inst_args else []
    modifiers = modifiers if isinstance(modifiers, list) else [modifiers] if modifiers else []
    return _Operator(operator, args, inst_args, modifiers)


# arithmetic and logic


def create_unary(op: str, tree: EX, modifiers: Union[ET, List[ET]] = None) -> ET:
    """
    Return the expression tree for an unary operator.

    Parameters
    ----------
        op : str
            Operator: - | + | !

        tree : EX
            Operand: expression tree.

        modifiers : Union[ET, LIST[ET]]
            Optional list of higher order constructs.

    Returns
    -------
        ET
    """
    eck = _unary_ops.get(op)
    if eck is None:
        raise ExprSyntaxError('create_unary', op)
    tree = _normalize_tree(tree)
    modifiers = modifiers if isinstance(modifiers, list) else [modifiers] if modifiers else []
    return _Predefined(eck, [tree], [], modifiers)


def create_binary(op: str, tree1: EX, tree2: EX, modifiers: Union[ET, List[ET]] = None) -> ET:
    """
    Return the expression tree for a binary operator.

    Parameters
    ----------
        op : str
            Operator: & | | | ^ | # | + | - | * | / | : | % | < | <= | > | >= | = | <>

        tree1 : EX
            First operand: expression tree.

        tree2 : EX
            Second operand: expression tree.

        modifiers : Union[ET, List[ET]]
            Optional list of higher order constructs.

    Returns
    -------
        ET
    """
    eck = _binary_ops.get(op)
    if eck is None:
        raise ExprSyntaxError('create_binary', op)
    tree1, tree2 = _normalize_tree((tree1, tree2))
    modifiers = modifiers if isinstance(modifiers, list) else [modifiers] if modifiers else []
    return _Predefined(eck, [tree1, tree2], [], modifiers)


def create_nary(op: str, *args: List[EX], modifiers: Union[ET, List[ET]] = None) -> ET:
    """
    Return the expression tree for a nary operator.

    Parameters
    ----------
        op : str
            Operator: & | | | ^ | # | + | *

        *args : List[EX]
            Operands: expression trees.

        modifiers : Union[ET, List[ET]]
            Optional list of higher order constructs, to be provided as keyword parameter.

    Returns
    -------
        ET
    """
    eck = _nary_ops.get(op)
    if eck is None:
        raise ExprSyntaxError('create_nary', op)
    if len(args) < 2:
        raise ExprSyntaxError('create_nary', args)
    args = _normalize_tree(args)
    modifiers = modifiers if isinstance(modifiers, list) else [modifiers] if modifiers else []
    return _Predefined(eck, args, [], modifiers)


# selectors


def create_if(condition: EX, then: LX, else_: LX) -> ET:
    """
    Return the expression tree for the operator if-then-else.

    Note: interface change with respect to the SCADE Creation Library, the flows
    'then' and the flows 'else' are now specified in two separate lists.

    Parameters
    ----------
        condition : EX
            Expression tree corresponding to the condition of the selector.

        then : Union[EX, List[EX]]
            List of expressions trees when condition is true.

        else_ : Union[EX, List[EX]]
            List of expressions trees when condition is false.

    Returns
    -------
        ET
    """
    norm_then = _normalize_tree_ex(then)
    norm_else = _normalize_tree_ex(else_)
    length = len(norm_then)
    if length == 0 or length != len(norm_else):
        raise ExprSyntaxError('create_if', then)

    condition = _normalize_tree(condition)
    then_tree = _create_sequence(norm_then)
    else_tree = _create_sequence(norm_else)

    return _Predefined(Eck.IF, [condition, then_tree, else_tree], [], [])


def create_case(selector: EX, cases: List[Tuple[EX, EX]], default: EX = None) -> ET:
    """
    Return the expression tree for the operator case.

    Note: interface change with respect to the SCADE Creation Library, the pairs pattern/value
    are now embedded in a list of tuples, and the default value is optional.

    Parameters
    ----------
        selector : EX
            Expression tree corresponding to the selector.

        cases : List[Tuple[EX, EX]]
            Pattern/values expression trees.

        default: EX
            Optional default value.

    Returns
    -------
        ET
    """
    if len(cases) == 0:
        raise ExprSyntaxError('create_case', cases)

    selector = _normalize_tree(selector)
    patterns = []
    inputs = []
    for pattern, input in cases:
        patterns.append(_normalize_tree(pattern))
        inputs.append(_normalize_tree(input))
    if default:
        patterns.append(_normalize_tree('_'))
        inputs.append(_normalize_tree(default))
    pattern_tree = _create_sequence(patterns)
    input_tree = _create_sequence(inputs)

    return _Predefined(Eck.CASE, [selector, input_tree, pattern_tree], [], [])


# types


def create_make(
    type_: suite.NamedType, *args: List[EX], modifiers: Union[ET, List[ET]] = None
) -> ET:
    """
    Return the expression tree for making a structured value.

    Parameters
    ----------
        type : suite.NamedType
            Type to be instantiated.

        *args : List[EX]
            Values of the type instance.

        modifiers : Union[ET, List[ET]]
            Optional list of higher order constructs, to be provided as keyword parameter.

    Returns
    -------
        ET
    """
    if len(args) < 1:
        raise ExprSyntaxError('create_make', args)
    _check_object(type_, 'create_make', 'type', suite.NamedType)
    args, type_ = _normalize_tree((args, type_))
    modifiers = modifiers if isinstance(modifiers, list) else [modifiers] if modifiers else []
    return _Predefined(Eck.MAKE, [_create_sequence(args), type_], [], modifiers)


def create_flatten(type_: suite.NamedType, arg: EX, modifiers: Union[ET, List[ET]] = None) -> ET:
    """
    Return the expression tree for flattening a structured value.

    Parameters
    ----------
        type : suite.NamedType
            Type to be instantiated.

        arg : EX
            Value to flatten.

        modifiers : Union[ET, List[ET]]
            Optional list of higher order constructs.

    Returns
    -------
        ET
    """
    _check_object(type_, 'create_flatten', 'type', suite.NamedType)
    arg, type_ = _normalize_tree((arg, type_))
    modifiers = modifiers if isinstance(modifiers, list) else [modifiers] if modifiers else []
    return _Predefined(Eck.FLATTEN, [arg, type_], [], modifiers)


# structures


def create_scalar_to_vector(size: EX, *args: List[EX]) -> ET:
    """
    Return the expression tree for the operator scalar_to_vector.

    Note: interface change with respect to the SCADE Creation Library, the parameter size
    has moved from the last position to the first one.

    Parameters
    ----------
        size: EX
            Size of the vector.

        args : List[EX]
            Input values.

    Returns
    -------
        ET
    """
    if len(args) == 0:
        raise ExprSyntaxError('create_scalar_to_vector', args)
    size = _normalize_tree(size)
    args = _normalize_tree(args)
    # the size must be the last parameter
    return _Predefined(Eck.SCALAR_TO_VECTOR, list(args) + [size], [], [])


def create_data_array(*args: List[EX]) -> ET:
    """
    Return the expression tree for the operator data_array.

    Parameters
    ----------
        args : List[EX]
            Values of the array.

    Returns
    -------
        ET
    """
    if len(args) == 0:
        raise ExprSyntaxError('create_data_array', args)
    args = _normalize_tree(args)
    return _Predefined(Eck.BLD_VECTOR, args, [], [])


def create_data_struct(*args: List[Tuple[str, EX]]) -> ET:
    """
    Return the expression tree for the operator data_struct.

    Note: interface change with respect to the SCADE Creation Library, the pairs name/value
    are now embedded in a list of tuples.

    Parameters
    ----------
        cases : List[Tuple[str, EX]]
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
    Return the expression tree for the operator projection.

    Parameters
    ----------
        flow : EX
            Input flow of the projection.

        path : Union[EX, List[EX]]
            Elements of the path, either label or index.

    Returns
    -------
        ET
    """
    flow = _normalize_tree(flow)
    path = _normalize_tree_ex(path)
    parameters = [flow] + path
    return _Predefined(Eck.PRJ, parameters, [], [])


def create_prj_dyn(flow: EX, path: LX, default: EX) -> ET:
    """
    Return the expression tree for the operator dynamic projection.

    Parameters
    ----------
        flow : EX
            Input flow of the projection.

        path : Union[EX, List[EX]]
            Elements of the path, either label, index or variable.

        default : EX
            Default value for the projection when the path is incorrect.

    Returns
    -------
        ET
    """
    flow, default = _normalize_tree((flow, default))
    path = _normalize_tree_ex(path)
    parameters = [flow] + path + [default]
    return _Predefined(Eck.PRJ_DYN, parameters, [], [])


def create_change_ith(flow: EX, path: LX, value: EX) -> ET:
    """
    Return the expression tree for the operator with.

    Parameters
    ----------
        flow : EX
            Input flow of the projection.

        path : Union[EX, List[EX]]
            Elements of the path, either label, index or variable.

        value : EX
            Value to assign.

    Returns
    -------
        ET
    """
    flow, value = _normalize_tree((flow, value))
    path = _normalize_tree_ex(path)
    parameters = [flow, value] + path
    return _Predefined(Eck.CHANGE_ITH, parameters, [], [])


# time


def create_pre(*args: List[EX]) -> ET:
    """
    Return the expression tree for the operator pre.

    Parameters
    ----------
        args : List[EX]
            Input flows.

    Returns
    -------
        ET
    """
    if len(args) == 0:
        raise ExprSyntaxError('create_pre', '')
    args = _normalize_tree(args)
    return _Predefined(Eck.PRE, args, [], [])


def create_init(flows: LX, inits: LX) -> ET:
    """
    Return the expression tree for the operator init.

    Note: interface change with respect to the SCADE Creation Library, the flows
    and their initial values are now specified in two separate lists.

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
    Return the expression tree for the operator init.

    Note: interface change with respect to the SCADE Creation Library, the flows
    and their initial values are now specified in two separate lists.

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

    delay = _normalize_tree(delay)
    parameters = norm_flows + [delay] + norm_inits
    return _Predefined(Eck.FBY, parameters, [], [])


def create_times(number: EX, flow: EX) -> ET:
    """
    Return the expression tree for the operator times.

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
    number, flow = _normalize_tree((number, flow))
    return _Predefined(Eck.TIMES, [number, flow], [], [])


# array


def create_slice(array: EX, start: EX, end: EX) -> ET:
    """
    Return the expression tree for the operator slice.

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
    array, start, end = _normalize_tree((array, start, end))
    return _Predefined(Eck.SLICE, [array, start, end], [], [])


def create_concat(*args: List[EX]) -> ET:
    """
    Return the expression tree for the operator concat.

    Parameters
    ----------
        args : List[EX]
            Input arrays to concatenate.

    Returns
    -------
        ET
    """
    if len(args) < 2:
        raise ExprSyntaxError('create_concat', args)
    args = _normalize_tree(args)
    return _Predefined(Eck.CONCAT, args, [], [])


def create_reverse(flow: EX) -> ET:
    """
    Return the expression tree for the operator reverse.

    Parameters
    ----------
        flow : EX
            Input flow.

    Returns
    -------
        ET
    """
    flow = _normalize_tree(flow)
    return _Predefined(Eck.REVERSE, [flow], [], [])


def create_transpose(array: EX, dim1: EX, dim2: EX) -> ET:
    """
    Return the expression tree for the operator transpose.

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
    array, dim1, dim2 = _normalize_tree((array, dim1, dim2))
    return _Predefined(Eck.TRANSPOSE, [array, dim1, dim2], [], [])


# activation


def create_restart(every: EX) -> ET:
    """
    Return the expression tree for the higher order construct restart.

    Parameters
    ----------
        every : EX
            Input condition.

    Returns
    -------
        ET
    """
    every = _normalize_tree(every)
    return _Predefined(Eck.RESTART, [every], [], [])


def create_activate(every: EX, *args: List[EX]) -> ET:
    """
    Return the expression tree for the higher order construct activate with initial values.

    Parameters
    ----------
        every : EX
            Input condition.

        args: List[EX]
            Initial values.

    Returns
    -------
        ET
    """
    every = _normalize_tree(every)
    # args may be empty
    args = _normalize_tree(args) if args else args
    return _Predefined(Eck.ACTIVATE, [every, _create_sequence(args)], [], [])


def create_activate_no_init(every: EX, *args: List[EX]) -> ET:
    """
    Return the expression tree for the higher order construct activate with default values.

    Parameters
    ----------
        every : EX
            Input condition.

        args: List[EX]
            Default values.

    Returns
    -------
        ET
    """
    every = _normalize_tree(every)
    # args may be empty
    args = _normalize_tree(args) if args else args
    return _Predefined(Eck.ACTIVATE_NOINIT, [every, _create_sequence(args)], [], [])


# iterators


def create_map(size: EX) -> ET:
    """
    Return the expression tree for the higher order construct map.

    Parameters
    ----------
        size : EX
            Number of iterations.

    Returns
    -------
        ET
    """
    size = _normalize_tree(size)
    return _Predefined(Eck.MAP, [size], [], [])


def create_mapi(size: EX) -> ET:
    """
    Return the expression tree for the higher order construct mapi.

    Parameters
    ----------
        size : EX
            Number of iterations.

    Returns
    -------
        ET
    """
    size = _normalize_tree(size)
    return _Predefined(Eck.MAPI, [size], [], [])


def create_fold(size: EX) -> ET:
    """
    Return the expression tree for the higher order construct fold.

    Parameters
    ----------
        size : EX
            Number of iterations.

    Returns
    -------
        ET
    """
    size = _normalize_tree(size)
    return _Predefined(Eck.FOLD, [size], [], [])


def create_foldi(size: EX) -> ET:
    """
    Return the expression tree for the higher order construct foldi.

    Parameters
    ----------
        size : EX
            Number of iterations.

    Returns
    -------
        ET
    """
    size = _normalize_tree(size)
    return _Predefined(Eck.FOLDI, [size], [], [])


def create_mapfold(size: EX, acc: EX) -> ET:
    """
    Return the expression tree for the higher order construct mapfold.

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
    size, acc = _normalize_tree((size, acc))
    return _Predefined(Eck.MAPFOLD, [size, acc], [], [])


def create_mapfoldi(size: EX, acc: EX) -> ET:
    """
    Return the expression tree for the higher order construct mapfoldi.

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
    size, acc = _normalize_tree((size, acc))
    return _Predefined(Eck.MAPFOLDI, [size, acc], [], [])


def create_foldw(size: EX, condition: EX) -> ET:
    """
    Return the expression tree for the higher order construct foldw.

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
    size, condition = _normalize_tree((size, condition))
    return _Predefined(Eck.FOLDW, [size, condition], [], [])


def create_foldwi(size: EX, condition: EX) -> ET:
    """
    Return the expression tree for the higher order construct foldwi.

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
    size, condition = _normalize_tree((size, condition))
    return _Predefined(Eck.FOLDWI, [size, condition], [], [])


def create_mapw(size: EX, condition: EX, default: EX) -> ET:
    """
    Return the expression tree for the higher order construct mapw.

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
    size, condition, default = _normalize_tree((size, condition, default))
    return _Predefined(Eck.MAPW, [size, condition, default], [], [])


def create_mapwi(size: EX, condition: EX, default: EX) -> ET:
    """
    Return the expression tree for the higher order construct mapdwi.

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
    size, condition, default = _normalize_tree((size, condition, default))
    return _Predefined(Eck.MAPWI, [size, condition, default], [], [])


def create_mapfoldw(size: EX, acc: EX, condition: EX, default: EX) -> ET:
    """
    Return the expression tree for the higher order construct mapfoldw.

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
    size, acc, condition, default = _normalize_tree((size, acc, condition, default))
    return _Predefined(Eck.MAPFOLDW, [size, acc, condition, default], [], [])


def create_mapfoldwi(size: EX, acc: EX, condition: EX, default: EX) -> ET:
    """
    Return the expression tree for the higher order construct mapfoldwi.

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
    size, acc, condition, default = _normalize_tree((size, acc, condition, default))
    return _Predefined(Eck.MAPFOLDWI, [size, acc, condition, default], [], [])


# ----------------------------------------------------------------------------
# Helpers (private)


def _create_sequence(flows: List[EX]) -> ET:
    """Create an expression tree for a group of flows."""
    return _Predefined(Eck.SEQ_EXPR, flows, [], [])


class ExprSyntaxError(Exception):
    """Generic exception for syntax errors in expression trees."""

    def __init__(self, context, item):
        """Provide a customized message."""
        super().__init__('%s: %s: Syntax error' % (context, item))


class TypeIdentifierError(Exception):
    """Exception for incorrect identifiers."""

    def __init__(self, context, item):
        """Provide a customized message."""
        super().__init__('%s: %s: Not a valid identifier' % (context, item))


class EmptyTreeError(Exception):
    """Exception for empty expression trees."""

    def __init__(self):
        """Provide a customized message."""
        super().__init__('_normalize_tree: Illegal empty tree')


def _is_int(number: str) -> bool:
    # trivial test first
    try:
        i = int(number)
        return True
    except:
        pass
    tokens = number.split('_', 1)
    if len(tokens) != 2:
        return False
    if tokens[1] in {'i8', 'i16', 'i32', 'i64', 'ui8', 'ui16', 'ui32', 'ui64'}:
        try:
            r = int(tokens[0])
            return True
        except:
            pass
    return False


def _is_real(number: str) -> bool:
    # trivial test first
    try:
        r = float(number)
        return True
    except:
        pass
    tokens = number.split('_', 1)
    if len(tokens) == 2 and tokens[1] in ('f32', 'f64'):
        try:
            r = float(tokens[0])
            return True
        except:
            pass
    return False


def _is_bool(value: str) -> bool:
    # trivial test first
    return value == 'true' or value == 'false'


# TODO: modifiers
# TODO: move to query
def _find_expr_id(expr: suite.Expression, index: int) -> suite.ExprId:
    """
    Return the instance of ExprId corresponding to the pin index of an equation.

    Note: the function is not complete for now and requires to
    be specified more precisely.

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
