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

"""Helpers to describe expression trees."""

from typing import List, Union

import scade.model.suite as suite

from ..expr import Eck
from .project import _check_object
from .scade import _add_pending_link

# association tables
_unary_ops = {
    '-': 'NEG',
    '+': 'POS',
    '!': 'NOT',
    'int': 'REAL2INT',
    'real': 'INT2REAL',
    'lnot': 'LNOT',
}
_binary_ops = {
    '&': 'AND',
    '|': 'OR',
    '^': 'XOR',
    '#': 'SHARP',
    '+': 'PLUS',
    '-': 'SUB',
    '*': 'MUL',
    '/': 'SLASH',
    ':': 'DIV',
    '%': 'MOD',
    '<': 'LESS',
    '<=': 'LEQUAL',
    '>': 'GREAT',
    '>=': 'GEQUAL',
    '=': 'EQUAL',
    '<>': 'NEQUAL',
    'land': 'LAND',
    'lor': 'LOR',
    'lxor': 'LXOR',
    '<<': 'LSL',
    '>>': 'LSR',
}
_nary_ops = {'&': 'AND', '|': 'OR', '^': 'XOR', '#': 'SHARP', '+': 'PLUS', '*': 'MUL'}

# aliases to enhance readability
ET = list
"""Expression Tree: list of tokens."""


def create_call(operator: suite.Operator, args: List[ET], inst_args: List[ET] = None) -> ET:
    """
    Return the expression tree for a call to an operator.

    Parameters
    ----------
        op : suite.Operator
            Called operator

        args : List[ET]
            Parameters: expression trees.

        inst_args : List[ET]
            Instance parameters: expression trees.

    Returns
    -------
        ET
    """
    if inst_args is None:
        inst_args = []
    _check_object(operator, 'create_call', 'operator', suite.Operator)
    return [operator, args, inst_args, []]


def create_higher_order_call(
    operator: suite.Operator, args: List[ET], modifiers: List[ET], inst_args: List[ET] = None
) -> ET:
    """
    Return the expression tree for a call to an operator.

    Parameters
    ----------
        op : suite.Operator
            Called operator

        args : List[ET]
            Parameters: expression trees.

        modifiers : List[ET]
            Higher order constructs: expression trees.

        inst_args : List[ET]
            Instance parameters: expression trees.

    Returns
    -------
        ET
    """
    if inst_args is None:
        inst_args = []
    _check_object(operator, 'create_higher_order_call', 'operator', suite.Operator)
    return [operator, args, inst_args, modifiers]


# arithmetic and logic


def create_unary(op: str, tree: ET) -> ET:
    """
    Return the expression tree for an unary operator.

    Parameters
    ----------
        op : str
            Operator: - | + | !

        tree : ET
            Operand: expression tree.

    Returns
    -------
        ET
    """
    id = _unary_ops.get(op)
    if id is None:
        raise ExprSyntaxError('create_unary', op)
    return ['_', id, [tree], [], []]


def create_binary(op: str, tree1: ET, tree2: ET) -> ET:
    """
    Return the expression tree for a binary operator.

    Parameters
    ----------
        op : str
            Operator: & | | | ^ | # | + | - | * | / | : | % | < | <= | > | >= | = | <>

        tree1 : ET
            First operand: expression tree.

        tree2 : ET
            Second operand: expression tree.

    Returns
    -------
        ET
    """
    id = _binary_ops.get(op)
    if id is None:
        raise ExprSyntaxError('create_binary', op)
    return ['_', id, [tree1, tree2], [], []]


def create_nary(op: ET, *args: List[ET]) -> ET:
    """
    Return the expression tree for a nary operator.

    Parameters
    ----------
        op : str
            Operator: & | | | ^ | # | + | *

        *args : List[ET]
            Operands: expression trees.

    Returns
    -------
        ET
    """
    id = _nary_ops.get(op)
    if id is None:
        raise ExprSyntaxError('CreateNAry', op)
    if len(args) < 2:
        raise ExprSyntaxError('CreateNAry', args)
    return ['_', id, args, [], []]


# selectors


def create_if(condition: ET, *args: List[ET]) -> ET:
    """
    Return the expression tree for the operator if-then-else.

    Parameters
    ----------
        condition : ET
            Expression tree corresponding to the condition of the selector.

        *args : List[ET]
            Then/else expression trees, expressed as [ <then>, <else>, ]+

    Returns
    -------
        ET
    """
    length = len(args)
    if length == 0 or length % 2 != 0:
        raise ExprSyntaxError('create_if', args)

    thens = []
    elses = []
    for i in range(length // 2):
        thens.append(args[2 * i])
        elses.append(args[2 * i + 1])
    then_tree = _create_sequence(thens)
    else_tree = _create_sequence(elses)

    return ['_', 'IF', [condition, then_tree, else_tree], [], []]


def create_case(selector: ET, *args: List[ET]) -> ET:
    """
    Return the expression tree for the operator case.

    Parameters
    ----------
        selector : ET
            Expression tree corresponding to the selector.

        *args : List[ET]
            Pattern/values expression trees, expressed as [ <pattern>, <value>, ]+

            The pattern '_', corresponding to the optional default, must be the last one.

    Returns
    -------
        ET
    """
    length = len(args)
    if length == 0 or length % 2 != 0:
        raise ExprSyntaxError('create_case', args)
    if '_' in args and args.index('_') != length - 2:
        raise ExprSyntaxError('create_case', args)

    patterns = []
    inputs = []
    for i in range(length // 2):
        pattern = args[2 * i]
        if pattern != '_':
            patterns.append(pattern)
        inputs.append(args[2 * i + 1])
    pattern_tree = _create_sequence(patterns)
    input_tree = _create_sequence(inputs)

    return ['_', 'CASE', [selector, input_tree, pattern_tree], [], []]


# types


def create_make(type_: suite.NamedType, *args: List[ET]) -> ET:
    """
    Return the expression tree for making a structured value.

    Parameters
    ----------
        type : suite.NamedType
            Type to be instantiated.

        *args : List[ET]
            Values of the type instance.

    Returns
    -------
        ET
    """
    _check_object(type_, 'create_make', 'type', suite.NamedType)
    if len(args) < 1:
        raise ExprSyntaxError('create_make', args)

    return ['_', 'MAKE', [_create_sequence(args), type_], [], []]


def create_flatten(type_: suite.NamedType, arg: ET) -> ET:
    """
    Return the expression tree for flattening a structured value.

    Parameters
    ----------
        type : suite.NamedType
            Type to be instantiated.

        arg : ET
            Value to flatten.

    Returns
    -------
        ET
    """
    _check_object(type_, 'create_flatten', 'type', suite.NamedType)
    return ['_', 'FLATTEN', [arg, type_], [], []]


# structures


def create_scalar_to_vector(size: ET, *args: List[ET]) -> ET:
    """
    Return the expression tree for the operator scalar_to_vector.

    Note: interface change with respet to the SCADE Creation Library, the parameter size
    has moved from the last position to the first one.

    Parameters
    ----------
        size: ET
            Size of the vector.

        args : List[ET]
            Input values.

    Returns
    -------
        ET
    """
    if len(args) == 0:
        raise ExprSyntaxError('create_scalar_to_vector', args)
    # the size must be the last parameter
    return ['_', 'SCALAR_TO_VECTOR', list(args) + [size], [], []]


def create_data_array(*args: List[ET]) -> ET:
    """
    Return the expression tree for the operator data_array.

    Parameters
    ----------
        args : List[ET]
            Values of the array.

    Returns
    -------
        ET
    """
    if len(args) == 0:
        raise ExprSyntaxError('create_data_array', args)
    return ['_', 'BLD_VECTOR', args, [], []]


def create_data_struct(*args: List[ET]):
    """
    Return the expression tree for the operator data_struct.

    Parameters
    ----------
        args : List[ET]
            Label/values expression trees, expressed as [ <label>, <value>, ]+

            Where <label> is an identifier and <value> is an expression tree.

    Returns
    -------
        ET
    """
    length = len(args)
    if length == 0 or length % 2 != 0:
        raise ExprSyntaxError('create_data_struct', args)

    parameters = []
    for i in range(length // 2):
        label = args[2 * i]
        if not isinstance(label, str) or not label.isidentifier():
            raise TypeIdentifierError('create_data_struct', args)
        parameters.append([label, args[2 * i + 1]])
    return ['_', 'BLD_STRUCT', parameters, [], []]


def create_prj(flow: ET, path: List[ET]) -> ET:
    """
    Return the expression tree for the operator projection.

    Parameters
    ----------
        flow : ET
            Input flow of the projection.

        path : List[ET]
            Elements of the path, either label or index.

    Returns
    -------
        ET
    """
    if len(path) == 0:
        raise ExprSyntaxError('create_prj', path)
    parameters = [flow] + path
    return ['_', 'PRJ', parameters, [], []]


def create_prj_dyn(flow: ET, path: List[ET], default: ET) -> ET:
    """
    Return the expression tree for the operator dynamic projection.

    Parameters
    ----------
        flow : ET
            Input flow of the projection.

        path : List[ET]
            Elements of the path, either label, index or variable.

        default : ET
            Default value for the projection when the path is incorrect.

    Returns
    -------
        ET
    """
    if len(path) == 0:
        raise ExprSyntaxError('create_prj_dyn', path)
    parameters = [flow] + path + [default]
    return ['_', 'PRJ_DYN', parameters, [], []]


def create_change_ith(flow: ET, path: List[ET], value: ET) -> ET:
    """
    Return the expression tree for the operator with.

    Parameters
    ----------
        flow : ET
            Input flow of the projection.

        path : List[ET]
            Elements of the path, either label, index or variable.

        value : ET
            Value to assign.

    Returns
    -------
        ET
    """
    if len(path) == 0:
        raise ExprSyntaxError('create_change_ith', path)
    parameters = [flow, value] + path
    return ['_', 'CHANGE_ITH', parameters, [], []]


# time


def create_pre(*args: List[ET]) -> ET:
    """
    Return the expression tree for the operator pre.

    Parameters
    ----------
        args : List[ET]
            Input flows.

    Returns
    -------
        ET
    """
    if len(args) == 0:
        raise ExprSyntaxError('create_pre', '')
    return ['_', 'PRE', args, [], []]


def create_init(flows: Union[ET, List[ET]], inits: Union[ET, List[ET]]) -> ET:
    """
    Return the expression tree for the operator init.

    Note: interface change with respet to the SCADE Creation Library, the flows
    and their initial values are now specified in two separate lists.

    Parameters
    ----------
        flows : Union[ET, List[ET]]
            Input flows.

        inits : Union[ET, List[ET]]
            Initial values.

    Returns
    -------
        ET
    """
    if isinstance(flows, list):
        length = len(flows)
        if not isinstance(inits, list) or length == 0 or length != len(inits):
            raise ExprSyntaxError('create_init', flows)
    else:
        if isinstance(inits, list):
            raise ExprSyntaxError('create_init', inits)
        flows = [flows]
        inits = [inits]

    flows_tree = _create_sequence(flows)
    inits_tree = _create_sequence(inits)

    return ['_', 'FOLLOW', [flows_tree, inits_tree], [], []]


def create_fby(flows: Union[ET, List[ET]], delay: ET, inits: Union[ET, List[ET]]) -> ET:
    """
    Return the expression tree for the operator init.

    Note: interface change with respet to the SCADE Creation Library, the flows
    and their initial values are now specified in two separate lists.

    Parameters
    ----------
        flows : Union[ET, List[ET]]
            Input flows.

        delay : ET
            Delay of the operator.

        inits : Union[ET, List[ET]]
            Initial values.

    Returns
    -------
        ET
    """
    if isinstance(flows, list):
        length = len(flows)
        if not isinstance(inits, list) or length == 0 or length != len(inits):
            raise ExprSyntaxError('create_fby', flows)
    else:
        if isinstance(inits, list):
            raise ExprSyntaxError('create_fby', inits)
        flows = [flows]
        inits = [inits]

    parameters = flows + [delay] + inits
    return ['_', 'FBY', parameters, [], []]


def create_times(number: ET, flow: ET) -> ET:
    """
    Return the expression tree for the operator times.

    Parameters
    ----------
        number : ET
            Number of cycles.

        flow : ET
            Input flows.

    Returns
    -------
        ET
    """
    return ['_', 'TIMES', [number, flow], [], []]


# array


def create_slice(array: ET, start: ET, end: ET) -> ET:
    """
    Return the expression tree for the operator slice.

    Parameters
    ----------
        array : ET
            Input array.

        start : ET
            Start index of the slice.

        end : ET
            End index of the slice.

    Returns
    -------
        ET
    """
    return ['_', 'SLICE', [array, start, end], [], []]


def create_concat(*args: List[ET]) -> ET:
    """
    Return the expression tree for the operator concat.

    Parameters
    ----------
        args : List[ET]
            Input arrays to concatenate.

    Returns
    -------
        ET
    """
    if len(args) < 2:
        raise ExprSyntaxError('create_concat', args)
    return ['_', 'CONCAT', args, [], []]


def create_reverse(flow: ET) -> ET:
    """
    Return the expression tree for the operator reverse.

    Parameters
    ----------
        flow : ET
            Input flow.

    Returns
    -------
        ET
    """
    return ['_', 'REVERSE', [flow], [], []]


def create_transpose(array: ET, dim1: ET, dim2: ET) -> ET:
    """
    Return the expression tree for the operator transpose.

    Parameters
    ----------
        array : ET
            Input array.

        dim1 : ET
            First dimension.

        dim2 : ET
            Second dimension.

    Returns
    -------
        ET
    """
    return ['_', 'TRANSPOSE', [array, dim1, dim2], [], []]


# activation


def create_restart(every: ET) -> ET:
    """
    Return the expression tree for the higher order construct restart.

    Parameters
    ----------
        every : ET
            Input condition.

    Returns
    -------
        ET
    """
    return ['_', 'RESTART', [every], [], []]


def create_activate(every: ET, *args: List[ET]) -> ET:
    """
    Return the expression tree for the higher order construct activate with initial values.

    Parameters
    ----------
        every : ET
            Input condition.

        args: List[ET]
            Initial values.

    Returns
    -------
        ET
    """
    # args may be empty
    return ['_', 'ACTIVATE', [every, _create_sequence(args)], [], []]


def create_activate_no_init(every: ET, *args: List[ET]) -> ET:
    """
    Return the expression tree for the higher order construct activate with default values.

    Parameters
    ----------
        every : ET
            Input condition.

        args: List[ET]
            Default values.

    Returns
    -------
        ET
    """
    # args may be empty
    return ['_', 'ACTIVATE_NOINIT', [every, _create_sequence(args)], [], []]


# iterators


def create_map(size: ET) -> ET:
    """
    Return the expression tree for the higher order construct map.

    Parameters
    ----------
        size : ET
            Number of iterations.

    Returns
    -------
        ET
    """
    return ['_', 'MAP', [size], [], []]


def create_mapi(size: ET) -> ET:
    """
    Return the expression tree for the higher order construct mapi.

    Parameters
    ----------
        size : ET
            Number of iterations.

    Returns
    -------
        ET
    """
    return ['_', 'MAPI', [size], [], []]


def create_fold(size: ET) -> ET:
    """
    Return the expression tree for the higher order construct fold.

    Parameters
    ----------
        size : ET
            Number of iterations.

    Returns
    -------
        ET
    """
    return ['_', 'FOLD', [size], [], []]


def create_foldi(size: ET) -> ET:
    """
    Return the expression tree for the higher order construct foldi.

    Parameters
    ----------
        size : ET
            Number of iterations.

    Returns
    -------
        ET
    """
    return ['_', 'FOLDI', [size], [], []]


def create_mapfold(size: ET, acc: ET) -> ET:
    """
    Return the expression tree for the higher order construct mapfold.

    Parameters
    ----------
        size : ET
            Number of iterations.

        acc : ET
            Number of accumulators.

    Returns
    -------
        ET
    """
    return ['_', 'MAPFOLD', [size, acc], [], []]


def create_mapfoldi(size: ET, acc: ET) -> ET:
    """
    Return the expression tree for the higher order construct mapfoldi.

    Parameters
    ----------
        size : ET
            Number of iterations.

        acc : ET
            Number of accumulators.

    Returns
    -------
        ET
    """
    return ['_', 'MAPFOLDI', [size, acc], [], []]


def create_foldw(size: ET, condition: ET) -> ET:
    """
    Return the expression tree for the higher order construct foldw.

    Parameters
    ----------
        size : ET
            Number of iterations.

        condition : ET
            Initial value of the iteration condition.

    Returns
    -------
        ET
    """
    return ['_', 'FOLDW', [size, condition], [], []]


def create_foldwi(size: ET, condition: ET) -> ET:
    """
    Return the expression tree for the higher order construct foldwi.

    Parameters
    ----------
        size : ET
            Number of iterations.

        condition : ET
            Initial value of the iteration condition.

    Returns
    -------
        ET
    """
    return ['_', 'FOLDWI', [size, condition], [], []]


def create_mapw(size: ET, condition: ET, default: ET) -> ET:
    """
    Return the expression tree for the higher order construct mapw.

    Parameters
    ----------
        size : ET
            Number of iterations.

        condition : ET
            Initial value of the iteration condition.

        default : ET
            Default value of the iteration.

    Returns
    -------
        ET
    """
    return ['_', 'MAPW', [size, condition, default], [], []]


def create_mapwi(size: ET, condition: ET, default: ET) -> ET:
    """
    Return the expression tree for the higher order construct mapdwi.

    Parameters
    ----------
        size : ET
            Number of iterations.

        condition : ET
            Initial value of the iteration condition.

        default : ET
            Default value of the iteration.

    Returns
    -------
        ET
    """
    return ['_', 'MAPWI', [size, condition, default], [], []]


def create_mapfoldw(size: ET, acc: ET, condition: ET, default: ET) -> ET:
    """
    Return the expression tree for the higher order construct mapfoldw.

    Parameters
    ----------
        size : ET
            Number of iterations.

        acc : ET
            Number of accumulators.

        condition : ET
            Initial value of the iteration condition.

        default : ET
            Default value of the iteration.

    Returns
    -------
        ET
    """
    return ['_', 'MAPFOLDW', [size, acc, condition, default], [], []]


def create_mapfoldwi(size: ET, acc: ET, condition: ET, default: ET) -> ET:
    """
    Return the expression tree for the higher order construct mapfoldwi.

    Parameters
    ----------
        size : ET
            Number of iterations.

        acc : ET
            Number of accumulators.

        condition : ET
            Initial value of the iteration condition.

        default : ET
            Default value of the iteration.

    Returns
    -------
        ET
    """
    return ['_', 'MAPFOLDWI', [size, acc, condition, default], [], []]


# ----------------------------------------------------------------------------
# Helpers (private)


def _create_sequence(flows: List[ET]) -> ET:
    """Create an expression tree for a group of flows."""
    return ['_', 'SEQ_EXPR', flows, [], []]


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
        super().__init__('_build_expression_tree: Illegal empty tree')


def _is_int(number: str) -> bool:
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
    tokens = number.split('_', 1)
    if len(tokens) == 2 and tokens[1] in ('f32', 'f64'):
        try:
            r = float(tokens[0])
            return True
        except:
            pass
    return False


# TODO: instance name
def _build_expression_tree(context: suite.Object, tree: ET) -> suite.Expression:
    """
    Return an expression resulting from tree.

    Parameters
    ----------
        context : suite.Object
            Scade model or element from which some
            declarations might be resolved, such as polymporphic types.

            In most of the cases, this parameter may be None.

        tree : ET
            Expression tree to build the expression from.

    Returns
    -------
        suite.ExprId
    """
    if isinstance(tree, list):
        length = len(tree)
        if length == 0:
            raise EmptyTreeError()
        item = tree[0]
    else:
        length = 1
        item = tree

    # check the presence of a label
    if length == 2 and isinstance(item, str) and item != '_':
        label = item
        if not label.isidentifier():
            raise TypeIdentifierError('_build_expression_tree', tree)

        tree = tree[1]
        if isinstance(tree, list):
            # TODO: recursion required, else how to deal with embedded structure literals?
            length = len(tree)
            if length == 0:
                raise EmptyTreeError()
            item = tree[0]
        else:
            length = 1
            item = tree
    else:
        label = None

    if length == 1:
        if not isinstance(item, suite.Object):
            # true | false | <integer> | <real> | ' <char> ' | " <ident> "
            if isinstance(item, bool):
                value = str(item).lower()
                kind = 'Bool'
            elif isinstance(item, int):
                value = str(item)
                kind = 'Int'
            elif isinstance(item, float):
                value = str(item)
                kind = 'Real'
            elif isinstance(item, str):
                if _is_int(item):
                    # number with one of the suffixes _i8, ui32, etc.
                    value = item
                    kind = 'Int'
                elif _is_real(item):
                    # number suffixed by _f32 or _f64
                    value = item
                    kind = 'Real'
                elif len(item) > 1 and item[0] == "'":
                    # no additional verification on the syntax
                    value = item
                    kind = 'Char'
                elif item.isidentifier():
                    # used in projections only
                    kind = 'String'
                    value = item
                else:
                    value = None
            else:
                value = None

            if not value:
                raise ExprSyntaxError('_build_expression_tree', tree)

            expr = suite.ConstValue(context)
            expr.value = value
            expr.kind = kind
            # {{ no comment...
            if kind == 'String':
                expr.role_kind = 'For Structure'
            # }}
        else:
            # <const_var> | <named_type>
            if isinstance(item, suite.ConstVar):
                expr = suite.ExprId(context)
                role = 'reference'
            elif isinstance(item, suite.NamedType):
                expr = suite.ExprType(context)
                role = 'type'
            else:
                raise ExprSyntaxError('_build_expression_tree', tree)

            _add_pending_link(expr, role, item)
    else:
        expr = suite.ExprCall(context)
        if item == '_':
            # Call to a predefined operator
            ident = tree[1]
            try:
                code = Eck[ident].value
            except KeyError:
                raise ExprSyntaxError('_build_expression_tree', tree)
            expr.predef_opr = code
            treecdr = tree[2:]
        else:
            # Call to an operator
            _check_object(item, '_build_expression_tree', tree, suite.Operator)
            _add_pending_link(expr, 'operator', item)
            treecdr = tree[1:]

        if len(treecdr) != 3:
            raise ExprSyntaxError('_build_expression_tree', tree)
        args, inst_args, modifiers = treecdr
        expr.parameters = [_build_expression_tree(context, _) for _ in args]
        expr.inst_parameters = [_build_expression_tree(context, _) for _ in inst_args]
        owner = expr
        for modifier in modifiers:
            subexpr = _build_expression_tree(context, modifier)
            owner.modifier = subexpr
            owner = subexpr

    if label is not None:
        lab = suite.Label(context)
        expr.label = lab
        lab.name = label
    return expr


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
