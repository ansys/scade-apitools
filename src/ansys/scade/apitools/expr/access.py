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
Provides accessors for expressions.

This module wraps the expressions derived from ``suite.Expression`` using the classes
corresponding to the XSCADE serialization, as exposed in the SCADE documentation:
``SCADE Suite Metamodels for Java API > 12. Scade Language Metamodels > Expressions``.
These classes allow accessing precisely each member of an expression.

Use the :py:func:`~ansys.scade.apitools.expr.access.accessor` function to create
an accessor from any SCADE Suite expression.
"""

from __future__ import annotations

from collections import namedtuple
from typing import Optional

import scade.model.suite as suite

from .predef import Eck


class Expression:
    """
    Provides the top-level abstract class for the expression accessors.

    Parameters
    ----------
    expression : suite.Expression
        Expression to wrap.
    """

    def __init__(self, expression: suite.Expression):
        """Store the wrapped expression."""
        self.expression = expression


class Present(Expression):
    """
    Provides the presence of a signal.

    The format is ``'<signal>``.

    See the :ref:`present <ex__present>` example.

    Parameters
    ----------
    expression :
        Signal expression to wrap.
    """

    def __init__(self, expression: suite.ExprId):
        """Initialize the instance from the Scade expression."""
        # assert expression.reference and expression.reference.is_signal()
        super().__init__(expression)

    @property
    def signal(self) -> suite.LocalVariable:
        """Signal of the expression."""
        return self.expression.reference


class Last(Expression):
    """
    Provides the last of a local variable.

    The format is ``last '<variable>``.

    See the :ref:`last <ex__last>` example.

    Parameters
    ----------
    expression :
        Last variable expression to wrap.
    """

    def __init__(self, expression: suite.ExprId):
        """Initialize the instance from the Scade expression."""
        # assert expression.last
        super().__init__(expression)

    @property
    def variable(self) -> suite.LocalVariable:
        """Local variable of the expression."""
        return self.expression.reference


class IdExpression(Expression):
    """
    Provides the constant, sensor, or local variable.

    The format is ``<path>``.

    See the :ref:`id_expression <ex__id_expression>` example.

    Parameters
    ----------
    expression :
        Reference expression to wrap.
    """

    def __init__(self, expression: suite.ExprId):
        """Initialize the instance from the Scade expression."""
        super().__init__(expression)

    @property
    def path(self) -> suite.ConstVar:
        """Local variable, sensor, or constant of the expression."""
        return self.expression.reference


class ConstValue(Expression):
    """
    Provides the literal value.

    The format is ``<value>``.

    See the :ref:`const_value <ex__const_value>` example.

    Parameters
    ----------
    expression :
        Literal to wrap.
    """

    def __init__(self, expression: suite.ConstValue):
        """Initialize the instance from the Scade expression."""
        super().__init__(expression)

    @property
    def value(self) -> str:
        """Literal value."""
        return self.expression.value


class TextExpression(Expression):
    """
    Provides an expression with a syntax error.

    The format is ``any text which can't compile``.

    Parameters
    ----------
    expression :
        Erroneous expression to wrap.
    """

    def __init__(self, expression: suite.ExprText):
        """Initialize the instance from the Scade expression."""
        super().__init__(expression)
        self._text = expression.text

    @property
    def text(self) -> str:
        """Erroneous text."""
        return self._text


class CallExpression(Expression):
    """
    Provides the abstract class for expression calls.

    There are three kinds of operator calls:

    * Predefined operators
    * User operators
    * Higher-order operators

    Parameters
    ----------
    expression :
        Call expression to wrap.
    """

    def __init__(self, expression: suite.ExprCall):
        """Initialize the instance from the Scade expression."""
        super().__init__(expression)
        self._code = Eck(expression.predef_opr)
        self._name = expression.inst_name

    @property
    def name(self) -> str:
        """Instance name of the expression."""
        return self._name

    @property
    def code(self) -> Eck:
        """Code of the predefined operator call."""
        return self._code


# Data operators
LabelledExpression = namedtuple('LabelledExpression', ['label', 'flow'])
"""
Element of a structure.

The format is ``<label>: <flow>``.
"""


class DataStructOp(CallExpression):
    """
    Provides for construction of a structure.

    The format is ``{ <label>: <expression>, ..., <label> : <expression> }``.

    See the :ref:`data_struct_op <ex__data_struct_op>` example.

    Parameters
    ----------
    expression :
        Call expression to wrap.
    """

    def __init__(self, expression: suite.ExprCall):
        """Initialize the instance from the Scade expression."""
        # assert Eck(expression.predef_opr) == Eck.BLD_STRUCT
        super().__init__(expression)
        self._data = [LabelledExpression(_.label.name, accessor(_)) for _ in expression.parameters]

    @property
    def data(self) -> list[LabelledExpression]:
        """Pairs (str, Expression) to build the structure."""
        return self._data


class DataArrayOp(CallExpression):
    """
    Provides for construction of an array.

    The format is ``[ <expression>, ..., <expression> ]``.

    See the :ref:`data_array_op <ex__data_array_op>` example.

    Parameters
    ----------
    expression :
        Call expression to wrap.
    """

    def __init__(self, expression: suite.ExprCall):
        """Initialize the instance from the Scade expression."""
        # assert Eck(expression.predef_opr) == Eck.BLD_VECTOR
        super().__init__(expression)
        self._data = [accessor(_) for _ in expression.parameters]

    @property
    def data(self) -> list[Expression]:
        """Values to build the array."""
        return self._data


class ArrayOp(CallExpression):
    """
    Provides the abstract class for array expressions.

    Parameters
    ----------
    expression :
        Call expression to wrap.
    """

    def __init__(self, expression: suite.ExprCall):
        """Initialize the instance from the Scade expression."""
        # assert Eck(expression.predef_opr) in {Eck.TRANSPOSE, Eck.SLICE, Eck.PRJ_DYN}
        super().__init__(expression)
        self._array = accessor(expression.parameters[0])

    @property
    def array(self) -> Expression:
        """Array operand of the expression."""
        return self._array


class TransposeOp(ArrayOp):
    """
    Provides for the transposition of an array.

    See the :ref:`transpose_op <ex__transpose_op>` example.

    Parameters
    ----------
    expression :
        Call expression to wrap.
    """

    def __init__(self, expression: suite.ExprCall):
        """Initialize the instance from the Scade expression."""
        # assert Eck(expression.predef_opr) == Eck.TRANSPOSE
        super().__init__(expression)
        self._dimensions = (accessor(expression.parameters[1]), accessor(expression.parameters[2]))

    @property
    def dimensions(self) -> tuple[Expression, Expression]:
        """Dimensions to transpose."""
        return self._dimensions


class SliceOp(ArrayOp):
    """
    Provides the slice of an array.

    See the :ref:`slice_op <ex__slice_op>` example.

    Parameters
    ----------
    expression :
        Call expression to wrap.
    """

    def __init__(self, expression: suite.ExprCall):
        """Initialize the instance from the Scade expression."""
        # assert Eck(expression.predef_opr) == Eck.SLICE
        super().__init__(expression)
        self._from_index = accessor(expression.parameters[1])
        self._to_index = accessor(expression.parameters[2])

    @property
    def from_index(self) -> Expression:
        """Start index of the slice."""
        return self._from_index

    @property
    def to_index(self) -> Expression:
        """End index of the slice."""
        return self._to_index


class Label(Expression):
    """
    Provides the label of a projection.

    Parameters
    ----------
    expression :
        Call expression to wrap.
    """

    def __init__(self, expression: suite.ConstValue):
        """Initialize the instance from the Scade expression."""
        super().__init__(expression)
        self._name = expression.value

    @property
    def name(self) -> str:
        """Name of the label."""
        return self._name


class PrjDynOp(ArrayOp):
    """
    Provides the dynamic projection of an array.

    See the :ref:`prj_dyn_op <ex__prj_dyn_op>` example.

    Parameters
    ----------
    expression :
        Call expression to wrap.
    """

    def __init__(self, expression: suite.ExprCall):
        """Initialize the instance from the Scade expression."""
        # assert Eck(expression.predef_opr) == Eck.PRJ_DYN
        super().__init__(expression)
        # the indexes are either a label identifying a structure's
        # field or an index expression
        self._indexes = [
            Label(_)
            if isinstance(_, suite.ConstValue) and not _.value.isnumeric()
            else accessor(_)
            for _ in expression.parameters[1:-1]
        ]
        self._default = accessor(expression.parameters[-1])

    @property
    def indexes(self) -> list[Expression]:
        """Path of the projection."""
        return self._indexes

    @property
    def default(self) -> Expression:
        """Default value of the projection."""
        return self._default


class ListExpression(Expression):
    """
    Provides a group of expressions.

    Parameters
    ----------
    expression :
        Call expression to wrap.
    """

    def __init__(self, expression: suite.Expression):
        """Initialize the instance from the Scade expression."""
        super().__init__(expression)
        self._items = [accessor(_) for _ in expression.parameters]

    @property
    def items(self) -> list[Expression]:
        """Expressions of the group."""
        return self._items


class FlowOp(CallExpression):
    """
    Provides an abstract class for flow expressions.

    Parameters
    ----------
    expression :
        Call expression to wrap.
    flow :
        Expression operand.
    """

    def __init__(self, expression: suite.ExprCall, flow: suite.Expression):
        """Initialize the instance from the Scade expression."""
        super().__init__(expression)
        self._flow = accessor(flow)

    @property
    def flow(self) -> Expression:
        """Flow operand of the expression."""
        return self._flow


class ScalarToVectorOp(CallExpression):
    """
    Provides the vector from a flow and a size.

    The format is ``<flow> ^ <size>``.

    See the :ref:`scalar_to_vector_op <ex__scalar_to_vector_op>` example.

    Notes
    -----
    The design differs slightly from the meta-model. Because the input
    must be a group of flows, the :class:`~ScalarToVectorOp` class does not inherit
    from the :class:`~FlowOp` class. It exposes directly the list of input flows instead of
    having a flow that is a :class:`~ListExpression` class.

    Parameters
    ----------
    expression :
        Call expression to wrap.
    """

    def __init__(self, expression: suite.ExprCall):
        """Initialize the instance from the Scade expression."""
        # assert Eck(expression.predef_opr) == Eck.SCALAR_TO_VECTOR
        super().__init__(expression)
        # the last parameter is the size
        self._flows = [accessor(_) for _ in expression.parameters[:-1]]
        self._size = accessor(expression.parameters[-1])

    @property
    def flows(self) -> list[Expression]:
        """Input flows."""
        return self._flows

    @property
    def size(self) -> Expression:
        """Size of the vector."""
        return self._size


class ProjectionOp(FlowOp):
    """
    Provides the abstract class for static projection/assignment of a flow.

    Parameters
    ----------
    expression :
        Call expression to wrap.
    flow :
        Expression operand.
    with_expressions :
        Path of the expression.
    """

    def __init__(
        self,
        expression: suite.ExprCall,
        flow: suite.Expression,
        with_expressions: list[suite.Expression],
    ):
        """Initialize the instance from the Scade expression."""
        # assert Eck(expression.predef_opr) in {Eck.PRJ, Eck.CHANGE_ITH}
        super().__init__(expression, flow)
        # the indexes are either a label identifying a structure's
        # field or an index expression
        self._with = [
            Label(_)
            if isinstance(_, suite.ConstValue) and not _.value.isnumeric()
            else accessor(_)
            for _ in with_expressions
        ]

    @property
    def with_(self) -> list[Expression]:
        """
        Path of the expression.

        The elements are either labels or indexes.
        """
        return self._with


class PrjOp(ProjectionOp):
    """
    Provides the static projection of a flow.

    See the example :ref:`prj_op <ex__prj_op>`.

    Parameters
    ----------
    expression :
        Call expression to wrap.
    """

    def __init__(self, expression: suite.ExprCall):
        """Initialize the instance from the Scade expression."""
        # assert Eck(expression.predef_opr) == Eck.PRJ
        super().__init__(expression, expression.parameters[0], expression.parameters[1:])


class ChgIthOp(ProjectionOp):
    """
    Provides the static assignment of a flow.

    See the :ref:`chg_ith_op <ex__chg_ith_op>` example.

    Parameters
    ----------
    expression :
        Call expression to wrap.
    """

    def __init__(self, expression: suite.ExprCall):
        """Initialize the instance from the Scade expression."""
        # assert Eck(expression.predef_opr) == Eck.CHANGE_ITH
        super().__init__(expression, expression.parameters[0], expression.parameters[2:])
        self._value = accessor(expression.parameters[1])

    @property
    def value(self) -> Expression:
        """Value assigned."""
        return self._value


class MakeOp(CallExpression):
    """
    Provides the make of a structure.

    The format is ``(make <type>)(<flow>, ..., <flow>)``.

    See the :ref:`make_op <ex__make_op>` example.

    Notes
    -----
    The design differs slightly from the meta-model. This class derives from
    the :class:`~CallExpression` class.

    Parameters
    ----------
    expression :
        Call expression to wrap.
    """

    def __init__(self, expression: suite.ExprCall):
        """Initialize the instance from the Scade expression."""
        # assert Eck(expression.predef_opr) == Eck.MAKE
        super().__init__(expression)
        self._flows = [accessor(_) for _ in expression.parameters[0].parameters]
        self._type = expression.parameters[1].reference

    @property
    def flows(self) -> list[Expression]:
        """Components of the structure."""
        return self._flows

    @property
    def type_(self) -> suite.NamedType:
        """Type to build."""
        return self._type


class FlattenOp(CallExpression):
    """
    Provides flattening of a structure.

    The format is ``(flatten <type>)(<flow>)``.

    See the :ref:`flatten_op <ex__flatten_op>` example.

    Notes
    -----
    The design differs slightly from the meta-model. This class derives from
    the :class:`~CallExpression` class.

    Parameters
    ----------
    expression :
        Call expression to wrap.
    """

    def __init__(self, expression: suite.ExprCall):
        """Initialize the instance from the Scade expression."""
        # assert Eck(expression.predef_opr) == Eck.FLATTEN
        super().__init__(expression)
        self._flow = accessor(expression.parameters[0])
        self._type = expression.parameters[1].reference

    @property
    def flow(self) -> Expression:
        """Input flow."""
        return self._flow

    @property
    def type_(self) -> suite.NamedType:
        """Type to build."""
        return self._type


class AryOp(CallExpression):
    """
    Provides the abstract class for unary, binary, and nary operators.

    Parameters
    ----------
    expression :
        Call expression to wrap.
    """

    def __init__(self, expression: suite.ExprCall):
        """Initialize the instance from the Scade expression."""
        super().__init__(expression)


class UnaryOp(AryOp):
    """
    Provides an expression with one operand.

    The format is ``<operator> <operand>``, where ``<operator>`` is one of
    these:

    * ``reverse``
    * ``-``, ``+``
    * ``not``
    * ``lnot``

    See the :ref:`unary_op <ex__unary_op>` example.

    Parameters
    ----------
    expression :
        Call expression to wrap.
    """

    def __init__(self, expression: suite.ExprCall):
        """Initialize the instance from the Scade expression."""
        # assert len(expression.parameters) == 1
        super().__init__(expression)
        self._operand = accessor(expression.parameters[0])

    @property
    def operand(self) -> Expression:
        """Operand of the operator."""
        return self._operand


class NAryOp(AryOp):
    """
    Provides an expression with two or more operands.

    The format is ``<operand> <operator> <operand> <operator> ... <operator> <operand>``,
    where ``<operator>`` is one of these:

    * ``@``
    * ``and``, ``or``, ``xor``
    * ``+``, ``*``
    * ``land``, ``lor``

    See the :ref:`n_ary_op <ex__n_ary_op>` example.

    Notes
    -----
    The ``xor`` operator is binary, but it is stored as a nary operator in the XSCADE files.

    Parameters
    ----------
    expression :
        Call expression to wrap.
    """

    def __init__(self, expression: suite.ExprCall):
        """Initialize the instance from the Scade expression."""
        # assert len(expression.parameters) >= 2
        super().__init__(expression)
        self._operands = [accessor(_) for _ in expression.parameters]

    @property
    def operands(self) -> list[Expression]:
        """Operand of the operator."""
        return self._operands


class BinaryOp(NAryOp):
    """
    Provides an expression with two operands.

    The format is ``<operand> <operator> <operand>``, where ``<operator>`` is one of these:

    * ``-``, ``/``, ``mod``
    * ``<``, ``<=``, ``>``, ``>=``, ``=``, ``<>``
    * ``lxor``, ``lsl``, ``lsr``
    * ``times``

    See the :ref:`binary_op <ex__binary_op>` example.

    Parameters
    ----------
    expression :
        Call expression to wrap.
    """

    def __init__(self, expression: suite.ExprCall):
        """Initialize the instance from the Scade expression."""
        # assert len(expression.parameters) == 2
        super().__init__(expression)


class NumericCastOp(FlowOp):
    """
    Provides the numeric cast of a flow.

    See the :ref:`numeric_cast_op <ex__numeric_cast_op>` example.

    Parameters
    ----------
    expression :
        Call expression to wrap.
    """

    def __init__(self, expression: suite.ExprCall):
        """Initialize the instance from the Scade expression."""
        # assert len(expression.parameters) == 2
        assert isinstance(expression.parameters[1], suite.ExprType)  # nosec B101  # addresses linter
        super().__init__(expression, expression.parameters[0])
        self._type = expression.parameters[1].type

    @property
    def type_(self) -> suite.Type:
        """Conversion type."""
        return self._type


class SharpOp(CallExpression):
    """
    Provides a sharp expression with two or more flows.

    The format is ``#(<flow>, ..., <flow>)``.

    See the :ref:`sharp_op <ex__sharp_op>` example.

    Parameters
    ----------
    expression :
        Call expression to wrap.
    """

    def __init__(self, expression: suite.ExprCall):
        """Initialize the instance from the Scade expression."""
        # assert len(expression.parameters) >= 2
        super().__init__(expression)
        self._flows = [accessor(_) for _ in expression.parameters]

    @property
    def flows(self) -> list[Expression]:
        """Operands of the operator."""
        return self._flows


class IfThenElseOp(CallExpression):
    """
    Provides a vector from a flow and a size.

    The format is ``if <if> then <then>, ..., <then> else <else>, ..., <else>``.

    See the :ref:`if_then_else_op <ex__if_then_else_op>` example.

    Notes
    -----
    The design differs slightly from the meta-model. Because the then/else
    parts must be groups of flows, the :class:`~IfThenElseOp` class exposes directly
    the list of then/else flows instead of a flow that is an instance of the
    :class:`~ListExpression` class.

    Parameters
    ----------
    expression :
        Call expression to wrap.
    """

    def __init__(self, expression: suite.ExprCall):
        """Initialize the instance from the Scade expression."""
        # assert Eck(expression.predef_opr) == Eck.IF
        super().__init__(expression)
        self._if = accessor(expression.parameters[0])
        self._then = [accessor(_) for _ in expression.parameters[1].parameters]
        self._else = [accessor(_) for _ in expression.parameters[2].parameters]

    @property
    def if_(self) -> Expression:
        """Condition of the expression."""
        return self._if

    @property
    def then(self) -> list[Expression]:
        """Flows when the condition is true."""
        return self._then

    @property
    def else_(self) -> list[Expression]:
        """Flows when the condition is false."""
        return self._else


class CaseOp(CallExpression):
    """
    Provides the case expression.

    Here is the format:

    .. code::

       ( case <switch> of ``
         | <pattern> :   <flow>
         | ...
         | <pattern> :   <flow>
         | _ :   <default>)

    See the :ref:`case_op <ex__case_op>` example.

    Notes
    -----
    The design differs slightly from the meta-model. The ``Case`` case used to
    implement the ``case`` collection is replaced by a tuple (``pattern``, ``flow``).

    A new property, ``default``, provides the optional default value.

    Parameters
    ----------
    expression :
        Call expression to wrap.
    """

    def __init__(self, expression: suite.ExprCall):
        """Initialize the instance from the Scade expression."""
        # assert Eck(expression.predef_opr) == Eck.CASE
        super().__init__(expression)
        self._switch = accessor(expression.parameters[0])
        flows = [accessor(_) for _ in expression.parameters[1].parameters]
        patterns = [accessor(_) for _ in expression.parameters[2].parameters]
        self._default = flows.pop() if len(flows) > len(patterns) else None
        self._cases: list = [(pattern, flow) for pattern, flow in zip(patterns, flows)]

    @property
    def switch(self) -> Expression:
        """Selector of the case expression."""
        return self._switch

    @property
    def cases(self) -> list[tuple[Expression, Expression]]:
        """Pairs (:class:`~Expression`, :class:`~Expression`) to build the case."""
        return self._cases

    @property
    def default(self) -> Optional[Expression]:
        """Value to use as default when not ``None``."""
        return self._default


class InitOp(CallExpression):
    """
    Provides for the initialization of flows.

    The format is ``<init>, ..., <init> -> <flow>, ..., <flow>``.

    See the :ref:`init_op <ex__init_op>` example.

    Notes
    -----
    The design differs slightly from the meta-model. Because the inputs
    must be groups of flows, the :class:`~InitOp` class does not inherit
    from the :class:`~FlowOp` class. It exposes directly the lists of flows and initial
    values instead of having flows that are instances of the :class:`~ListExpression`
    class.

    Parameters
    ----------
    expression :
        Call expression to wrap.
    """

    def __init__(self, expression: suite.ExprCall):
        """Initialize the instance from the Scade expression."""
        # assert len(expression.parameters) == 2 and Eck(expression.predef_opr) == Eck.FOLLOW
        super().__init__(expression)
        self._flows = [accessor(_) for _ in expression.parameters[0].parameters]
        self._inits = [accessor(_) for _ in expression.parameters[1].parameters]

    @property
    def flows(self) -> list[Expression]:
        """Flows after the first cycle."""
        return self._flows

    @property
    def inits(self) -> list[Expression]:
        """Initial values of the flows."""
        return self._inits


class PreOp(CallExpression):
    """
    Provides the previous value of flows.

    The format is ``pre <flow>, ..., <flow>``.

    See the :ref:`pre_op <ex__pre_op>` example.

    Notes
    -----
    The design differs slightly from the meta-model. Because the input
    must be a group of flows, the :class:`~PreOp` class does not inherit
    from the :class:`~FlowOp` class. It exposes directly the lists of flows instead of
    having a flow that is an instance of a :class:`~ListExpression` class.

    Parameters
    ----------
    expression :
        Call expression to wrap.
    """

    def __init__(self, expression: suite.ExprCall):
        """Initialize the instance from the Scade expression."""
        # assert Eck(expression.predef_opr) == Eck.PRE
        super().__init__(expression)
        self._flows = [accessor(_) for _ in expression.parameters]

    @property
    def flows(self) -> list[Expression]:
        """Flows after the first cycle."""
        return self._flows


class FbyOp(CallExpression):
    """
    Provides the delay of flows.

    The format is ``fby(<flow>, ..., <flow>; <delay>; <init>, ..., <init>)``.

    See the :ref:`fby_op <ex__fby_op>` example.

    Parameters
    ----------
    expression :
        Call expression to wrap.
    """

    def __init__(self, expression: suite.ExprCall):
        """Initialize the instance from the Scade expression."""
        # assert len(expression.parameters) >= 3 and Eck(expression.predef_opr) == Eck.FBY
        super().__init__(expression)
        n = int((len(expression.parameters) - 1) / 2)
        self._flows = [accessor(_) for _ in expression.parameters[:n]]
        self._delay = accessor(expression.parameters[n])
        self._inits = [accessor(_) for _ in expression.parameters[n + 1 :]]

    @property
    def flows(self) -> list[Expression]:
        """Flows after the first cycle."""
        return self._flows

    @property
    def delay(self) -> Expression:
        """Delay of the expression."""
        return self._delay

    @property
    def inits(self) -> list[Expression]:
        """Initialization values of the flows."""
        return self._inits


class OpCall(CallExpression):
    """
    Calls a user-defined operator.

    The format is ``<operator><< <instance parameter>, ...>>(<call parameter>, ...)``.

    Notes
    -----
    The design differs slightly from the meta-model. The :class:`~OpCall` class
    is no longer aggregated by the :class:`~CallExpression` class but derives from it.
    This leads to a simpler design.

    Parameters
    ----------
    expression :
        Expression to wrap.
    """

    def __init__(self, expression: suite.ExprCall):
        """Initialize the instance from the Scade expression."""
        # assert expression.operator
        super().__init__(expression)
        self._call_parameters = [accessor(_) for _ in expression.parameters]
        self._instance_parameters = [accessor(_) for _ in expression.inst_parameters]
        self._operator = expression.operator

    @property
    def operator(self) -> suite.Operator:
        """User operator."""
        return self._operator

    @property
    def call_parameters(self) -> list[Expression]:
        """Call parameters."""
        return self._call_parameters

    @property
    def instance_parameters(self) -> list[Expression]:
        """Instance call parameters."""
        return self._instance_parameters


class OpOp(CallExpression):
    """
    Provides the abstract class for higher-order operators.

    Notes
    -----
    The design differs slightly from the meta-model. The :class:`~OpOp` class is
    no longer aggregated by the :class:`~CallExpression` class but derives from it.
    This leads to a simpler design.

    Parameters
    ----------
    expression :
        Higher-order expression to wrap.
    operator :
        Operator call expression.
    """

    def __init__(self, expression: suite.ExprCall, operator: CallExpression):
        """Initialize the instance from the Scade expression."""
        super().__init__(expression)
        self._operator = operator

    @property
    def operator(self) -> CallExpression:
        """Underlying expression."""
        return self._operator


class ConditionalOp(OpOp):
    """
    Provides the abstract class for restart and activate operators.

    Parameters
    ----------
    expression :
        Higher-order expression to wrap.
    operator :
        Operator call expression.
    """

    def __init__(self, expression: suite.ExprCall, operator: CallExpression):
        """Initialize the instance from the Scade expression."""
        super().__init__(expression, operator)
        self._every = accessor(expression.parameters[0])

    @property
    def every(self) -> Expression:
        """Condition expression."""
        return self._every


class RestartOp(ConditionalOp):
    """
    Provides for restart of an operator.

    See the :ref:`restart_op <ex__restart_op>` example.

    Parameters
    ----------
    expression :
        Higher-order expression to wrap.
    operator :
        Operator call expression.
    """

    pass


class CondactOp(ConditionalOp):
    """
    Provides the abstract class for activate operators.

    Notes
    -----
    The design differs slightly from the meta-model. Because the flow
    ``default`` must be a group of flows, the :class:`~CondactOp` class exposes directly
    the list of default values instead of an instance of the :class:`~ListExpression` class.

    Parameters
    ----------
    expression :
        Higher-order expression to wrap.
    operator :
        Operator call expression.
    """

    def __init__(self, expression: suite.ExprCall, operator: CallExpression):
        """Initialize the instance from the Scade expression."""
        super().__init__(expression, operator)
        self._defaults = [accessor(_) for _ in expression.parameters[1].parameters]

    @property
    def defaults(self) -> list[Expression]:
        """Initialization or default values."""
        return self._defaults


class ActivateOp(CondactOp):
    """
    Activation of an operator with initial values.

    See the :ref:`activate_op <ex__activate_op>` example.

    Parameters
    ----------
    expression :
        Higher-order expression to wrap.
    operator :
        Operator call expression.
    """

    pass


class ActivateNoInitOp(CondactOp):
    """
    Provides activation of an operator with default values.

    See the :ref:`activate_no_init_op <ex__activate_no_init_op>` example.

    Parameters
    ----------
    expression :
        Higher-order expression to wrap.
    operator :
        Operator call expression.
    """

    pass


class IteratorOp(OpOp):
    """
    Provides the base class for iteration operators.

    See the :ref:`iterator_op <ex__iterator_op>` example.

    Parameters
    ----------
    expression :
        Higher-order expression to wrap.
    operator :
        Operator call expression.
    """

    def __init__(self, expression: suite.ExprCall, operator: CallExpression):
        """Initialize the instance from the Scade expression."""
        super().__init__(expression, operator)
        self._size = accessor(expression.parameters[0])
        if self.code in {Eck.MAPFOLD, Eck.MAPFOLDI, Eck.MAPFOLDW, Eck.MAPFOLDWI}:
            self._accumulator_count = accessor(expression.parameters[1])
        else:
            # n/a
            self._accumulator_count = None

    @property
    def size(self) -> Expression:
        """Size of the iterator."""
        return self._size

    # TODO CREATE: mapfold with N accumulators...
    @property
    def accumulator_count(self) -> Optional[Expression]:
        """Number of accumulators when suitable, otherwise ``None``."""
        return self._accumulator_count


class PartialIteratorOp(IteratorOp):
    """
    Provides partial iteration of an operator.

    See the :ref:`partial_iterator_op <ex__partial_iterator_op>` example.

    Parameters
    ----------
    expression :
        Higher-order expression to wrap.
    operator :
        Operator call expression.
    """

    def __init__(self, expression: suite.ExprCall, operator: CallExpression):
        """Initialize the instance from the Scade expression."""
        super().__init__(expression, operator)
        # mapfold iterators have a extra parameter, second position which
        # defines the number of accumulators
        offset = 1 if self.code in {Eck.MAPFOLDW, Eck.MAPFOLDWI} else 0
        self._if = accessor(expression.parameters[1 + offset])
        # following might be empty when not MAP*W*
        if len(expression.parameters) == 3 + offset:
            # assert self.code in {Eck.MAPW, Eck.MAPWI, Eck.MAPFOLDW, Eck.MAPFOLDWI}
            self._defaults = [accessor(_) for _ in expression.parameters[2 + offset].parameters]
        else:
            # assert self.code in {Eck.FOLDW, Eck.FOLDWI}
            self._defaults = None

    @property
    def if_(self) -> Expression:
        """Condition of the iterator."""
        return self._if

    @property
    def defaults(self) -> Optional[list[Expression]]:
        """Default values when suitable, otherwise ``None``."""
        return self._defaults


UNARY_OPS = {
    Eck.REVERSE: 'reverse',
    Eck.NEG: '-',
    Eck.POS: '+',
    Eck.NOT: 'not',
    Eck.LNOT: 'lnot',
}
BINARY_OPS = {
    Eck.SUB: '-',
    Eck.SLASH: '/',
    Eck.MOD: 'mod',
    Eck.LESS: '<',
    Eck.LEQUAL: '<=',
    Eck.GREAT: '>',
    Eck.GEQUAL: '>=',
    Eck.EQUAL: '=',
    Eck.NEQUAL: '<>',
    Eck.LXOR: 'lxor',
    Eck.LSL: 'lsl',
    Eck.LSR: 'lsr',
    Eck.TIMES: 'times',
    # TODO CREATE: bitwise...
}
NARY_OPS = {
    Eck.CONCAT: '@',
    Eck.AND: 'and',
    Eck.OR: 'or',
    # xor shall be binary but stored as nary in the xscade files
    Eck.XOR: 'xor',
    Eck.PLUS: '+',
    Eck.MUL: '*',
    Eck.LAND: 'land',
    Eck.LOR: 'lor',
}
MAP_OPERATORS = {
    Eck.BLD_STRUCT: DataStructOp,
    Eck.BLD_VECTOR: DataArrayOp,
    Eck.TRANSPOSE: TransposeOp,
    Eck.SLICE: SliceOp,
    Eck.PRJ_DYN: PrjDynOp,
    Eck.SEQ_EXPR: ListExpression,
    Eck.SCALAR_TO_VECTOR: ScalarToVectorOp,
    Eck.PRJ: PrjOp,
    Eck.CHANGE_ITH: ChgIthOp,
    Eck.MAKE: MakeOp,
    Eck.FLATTEN: FlattenOp,
    Eck.NUMERIC_CAST: NumericCastOp,
    Eck.SHARP: SharpOp,
    Eck.IF: IfThenElseOp,
    Eck.CASE: CaseOp,
    Eck.FOLLOW: InitOp,
    Eck.PRE: PreOp,
    Eck.FBY: FbyOp,
}
MAP_HIGHER_ORDER = {
    Eck.RESTART: RestartOp,
    Eck.ACTIVATE: ActivateOp,
    Eck.ACTIVATE_NOINIT: ActivateNoInitOp,
    Eck.MAP: IteratorOp,
    Eck.MAPI: IteratorOp,
    Eck.MAPW: PartialIteratorOp,
    Eck.MAPWI: PartialIteratorOp,
    Eck.FOLD: IteratorOp,
    Eck.FOLDI: IteratorOp,
    Eck.FOLDW: PartialIteratorOp,
    Eck.FOLDWI: PartialIteratorOp,
    Eck.MAPFOLD: IteratorOp,
    Eck.MAPFOLDI: IteratorOp,
    Eck.MAPFOLDW: PartialIteratorOp,
    Eck.MAPFOLDWI: PartialIteratorOp,
}

# overall map of operators
map_operators = {}
map_operators.update(MAP_OPERATORS)
map_operators.update({_: UnaryOp for _ in UNARY_OPS})
map_operators.update({_: BinaryOp for _ in BINARY_OPS})
map_operators.update({_: NAryOp for _ in NARY_OPS})


def _modifier_accessor(modifier: suite.Expression, call: CallExpression) -> CallExpression:
    if modifier:
        call = _modifier_accessor(modifier.modifier, call)
        class_ = MAP_HIGHER_ORDER.get(Eck(modifier.predef_opr))
        if not class_:
            raise ValueError('Higher order operator %d not supported' % modifier.predef_opr)
        else:
            call = class_(modifier, call)

    return call


def accessor(expression: suite.Expression) -> Expression:
    """
    Build the accessor for a SCADE Suite expression.

    Parameters
    ----------
    expression : suite.Expression
        Expression to wrap.

    Returns
    -------
    Expression
        Expression accessor.
    """
    # ExprId
    if isinstance(expression, suite.ExprId):
        if expression.reference and expression.reference.is_signal():
            return Present(expression)
        elif expression.last:
            return Last(expression)
        else:
            return IdExpression(expression)

    # ConstValue
    if isinstance(expression, suite.ConstValue):
        return ConstValue(expression)

    # TextExpression
    if isinstance(expression, suite.ExprText):
        return TextExpression(expression)

    # ...
    if isinstance(expression, suite.ExprType):
        raise ValueError('Type sub-expressions not supported')

    assert isinstance(expression, suite.ExprCall)  # nosec B101  # addresses linter
    if expression.operator:
        call = OpCall(expression)
    else:
        class_ = map_operators.get(Eck(expression.predef_opr))
        if class_:
            call = class_(expression)
        else:
            raise ValueError('Predefined operator %d not supported' % expression.predef_opr)

    return _modifier_accessor(expression.modifier, call)
