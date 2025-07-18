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
Provides create functions for Scade operator definitions.

* Interface
* Behavior
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Optional, Sequence, Tuple, Union

import scade.model.suite as suite

from .expression import EX, _build_expression, _find_expr_id
from .project import _check_object

# from .expression import ET
from .scade import _link_pendings, _set_modified
from .type import TX, _build_type, _object_link_type

# ----------------------------------------------------------------------------
# interface


def add_data_def_signals(data_def: suite.DataDef, names: List[str]) -> List[suite.LocalVariable]:
    """
    Add signals to a scope.

    Parameters
    ----------
    data_def : suite.DataDef
        Input scope, which is an operator, state, or action.
    names : List[str]
        Names of the signals to add.

    Returns
    -------
    List[suite.LocalVariable]
        List of added signals.
    """
    _check_object(data_def, 'add_data_def_signals', 'data_def', suite.DataDef)

    signals = []
    for name in names:
        signal = suite.LocalVariable(data_def)
        signal.name = name
        data_def.signals.append(signal)
        signals.append(signal)

    _set_modified(data_def)
    return signals


# private common procedure for operator ios
def _add_data_def_variables(
    data_def: suite.DataDef, vars: List[Tuple[str, TX]], probe: bool
) -> List[suite.LocalVariable]:
    """Core function to create scope local variables."""
    proc_name = '_add_data_def_variables'
    _check_object(data_def, proc_name, 'datadef', suite.DataDef)

    variables = []
    for name, tree in vars:
        type_ = _build_type(tree, data_def)
        variable = suite.LocalVariable(data_def)
        variable.name = name
        variable.probe = probe
        data_def.locals.append(variable)
        _object_link_type(variable, type_)
        variables.append(variable)

    _link_pendings()
    _set_modified(data_def)
    return variables


def add_data_def_locals(
    data_def: suite.DataDef, vars: List[Tuple[str, TX]]
) -> List[suite.LocalVariable]:
    """
    Add local variables to a scope.

    Notes
    -----
    This is an interface change with respect to the *SCADE Creation Library*.
    The pairs "name"/"type tree" are now embedded in a list of tuples.

    Parameters
    ----------
    data_def : suite.DataDef
        Input scope, which is an operator, state, or action.
    vars : List[Tuple[str, TX]]
        Name/type expression trees.

    Returns
    -------
    List[suite.LocalVariable]
        List of added variables.
    """
    return _add_data_def_variables(data_def, vars, False)


def add_data_def_probes(
    data_def: suite.DataDef, vars: List[Tuple[str, TX]]
) -> List[suite.LocalVariable]:
    """
    Add probes to a scope.

    Notes
    -----
    This is an interface change with respect to the *SCADE Creation Library*.
    The pairs "name"/"type tree" are now embedded in a list of tuples.

    Parameters
    ----------
    data_def : suite.DataDef
        Input scope, which is an operator, state, or action.
    vars : List[Tuple[str, TX]]
        Name/type expression trees.

    Returns
    -------
    List[suite.LocalVariable]
        List of added probes.
    """
    return _add_data_def_variables(data_def, vars, True)


# ----------------------------------------------------------------------------
# variables


def set_variable_default(variable: suite.LocalVariable, tree: EX) -> suite.Expression:
    """
    Set the default value of a variable.

    Parameters
    ----------
    variable : suite.LocalVariable
        Input variable.
    tree : EX
        Default value expressed as an extended expression tree.

    Returns
    -------
    suite.Expression
    """
    return _set_variable_expression(variable, 'default', tree)


def set_variable_last(variable: suite.LocalVariable, tree: EX) -> suite.Expression:
    """
    Set the last value of a variable.

    Parameters
    ----------
    variable : suite.LocalVariable
        Input variable.
    tree : EX
        Last value expressed as an extended expression tree.

    Returns
    -------
    suite.Expression
    """
    return _set_variable_expression(variable, 'last', tree)


def _set_variable_when(variable: suite.LocalVariable, tree: EX) -> suite.Expression:
    """Private: clocks not supported."""
    return _set_variable_expression(variable, 'when', tree)


def _set_variable_expression(variable, attr, tree):
    """Core function to set an expression to a variable."""
    _check_object(variable, 'set_variable_expression', 'variable', suite.LocalVariable)
    expression = _build_expression(tree, variable.owner)
    setattr(variable, attr, expression)
    _link_pendings()
    _set_modified(variable)
    return expression


# ----------------------------------------------------------------------------
# diagrams


def _add_data_def_diagram(data_def: suite.DataDef, class_: type, name: str) -> suite.Diagram:
    """Core creation function for a diagram."""
    _check_object(data_def, 'add_data_def_diagram', 'data_def', suite.DataDef)
    diagram = class_(data_def)
    diagram.name = name
    data_def.diagrams.append(diagram)
    if isinstance(data_def, (suite.Action, suite.State)):
        # the display of the scope is no longer embedded
        if data_def.presentation_element:
            data_def.presentation_element.display = DK.SPLIT.value

    _set_modified(data_def)
    return diagram


def add_data_def_text_diagram(data_def: suite.DataDef, name: str) -> suite.TextDiagram:
    """
    Add a textal diagram to a scope.

    Parameters
    ----------
    data_def : suite.DataDef
        Input scope, which is an operator, state, or action.
    name : str
        Name of the diagram.

    Returns
    -------
    suite.TextDiagram
    """
    diagram = _add_data_def_diagram(data_def, suite.TextDiagram, name)
    diagram.landscape = False
    return diagram


def add_data_def_net_diagram(data_def: suite.DataDef, name: str) -> suite.NetDiagram:
    """
    Add a graphical diagram to a scope.

    Parameters
    ----------
    data_def : suite.DataDef
        Input scope, which is an operator, state, or action.
    name : str
        Name of the diagram.

    Returns
    -------
    suite.NetDiagram
    """
    diagram = _add_data_def_diagram(data_def, suite.NetDiagram, name)
    diagram.landscape = True
    return diagram


# ----------------------------------------------------------------------------
# equations and edges


def _num_to_str(values: Sequence[Union[int, float]]) -> List[str]:
    """SCADE graphical coordinates are strings: position, size, points."""
    return [str(_) for _ in values]


def _create_internal(data_def: suite.DataDef, tree: TX) -> suite.LocalVariable:
    """
    Create an internal variable for an operator.

    Notes
    -----
    The algorithm is inefficient. You should compute the name
    of the internal variables with a cache in the client code.

    """
    # default name for the internal variable
    index = len(data_def.internals) + 1
    name = '_L' + str(index)
    while next((_ for _ in data_def.internals if _.name == name), None) is not None:
        index = index + 1
        name = '_L' + str(index)

    variable = suite.LocalVariable(data_def)
    variable.name = name
    data_def.internals.append(variable)
    _object_link_type(variable, _build_type(tree, data_def))

    _link_pendings()
    _set_modified(data_def)
    return variable


def add_data_def_equation(
    data_def: suite.DataDef,
    diagram: Optional[suite.Diagram],
    lefts: Sequence[Union[suite.LocalVariable, TX]],
    right: Optional[EX],
    position: Tuple[float, float] = (0, 0),
    size: Tuple[float, float] = (0, 0),
    symmetrical: bool = False,
    rotation: int = 0,
    textual: bool = False,
) -> suite.Equation:
    """
    Create an equation in a scope.

    Parameters
    ----------
    data_def : suite.DataDef
        Input scope, which is an operator, state, or action.
    diagram : suite.Diagram | None
        Diagram containing the equation. The diagram specified can be either graphical
        or textual, or it can be ``None``. However, it cannot be ``None`` if the scope
        contains at least one diagram.
    lefts : Sequence[Union[suite.LocalVariable, TX]]
        List of variables defined by the equation. The elements can be either an
        existing local variable or a type tree to create an internal
        variable on the fly when the diagram is a graphical diagram.
    right : EX | None
        Expression of the equation.
    position : Tuple[float, float], default: (0, 0))
        Position of the equation, expressed in 1/100th of mm.
        This value is ignored if the diagram is not a graphical diagram.
        Otherwise, it must be specified.
    size : Tuple[float, float], default: (0, 0)
        Size of the equation, expressed in 1/100th of mm.
        This value is ignored if the diagram is not a graphical diagram.
        Otherwise, it must be specified.
    symmetrical : bool, default: False
        Whether the graphical representation is symmetrical.
    rotation : int, default: 0
        Rotation angle of the equation, expressed in degrees.
        Options are ``0``, ``90``, ``180``, and ``270``.
    textual : bool, default: False
        Whether the equation is a textual. If ``False``, the equation is
        a graphical representation.

    Returns
    -------
    suite.Equation
    """
    _check_object(data_def, 'add_data_def_equation', 'datadef', suite.DataDef)
    if diagram is not None:
        _check_object(
            diagram, 'add_data_def_equation', 'diagram', (suite.NetDiagram, suite.TextDiagram)
        )
    else:
        # internal variables allowed only for graphical diagrams
        [
            _check_object(_, 'add_data_def_equation', 'lefts', suite.LocalVariable)
            for _ in lefts
            if _ != '_'
        ]

    equation = suite.Equation(data_def)
    for left in lefts:
        if left == '_':
            variable = suite.Variable(data_def)
            variable.name = '_'
            # TODO: raise an error if len(lefts) != 1
            equation.terminator = True
        else:
            if isinstance(left, suite.LocalVariable):
                # left is an existing local variable
                variable = left
            else:
                # left is expected to be a type tree
                variable = _create_internal(data_def, left)

        equation.lefts.append(variable)

    if right is not None:
        equation.right = _build_expression(right, data_def)

    # graphical part
    if diagram and not isinstance(data_def, suite.Operator):
        pe = data_def.presentation_element
        if not pe or pe.display == DK.TEXTUAL:
            # ignore the graphical information
            diagram = None
    if diagram is not None:
        if isinstance(diagram, suite.NetDiagram):
            pe = suite.EquationGE(data_def)
            # graphical properties
            pe.position = _num_to_str(position)
            pe.size = _num_to_str(size)
            pe.symmetrical = symmetrical
            pe.rotation = rotation
            pe.kind = 'OBJ_LIT' if textual else 'FI_EQUATION'
        else:
            # text diagram
            pe = suite.FlowTE(data_def)
            # not other properties
        equation.presentation_element = pe
        diagram.presentation_elements.append(pe)

    # no exception raised: add the equation to its owner
    data_def.flows.append(equation)

    _link_pendings()
    _set_modified(data_def)
    return equation


def add_diagram_edge(
    diagram: suite.NetDiagram,
    src: suite.Equation,
    left: suite.LocalVariable,
    dst: suite.Equation,
    expr: Union[int, suite.Expression],
    points: Optional[List[Tuple[int, int]]] = None,
) -> suite.Edge:
    """
    Add a graphical edge between two equations in a graphical diagram.

    * The source of the edge is identified by the local variable defined
      in the source equation.

    * The destination of the edge is identified by the parameter of the
      expression of the target equation. It is an ``ExprId`` instance
      referring to the left variable.

      To ease the creation of graphical diagrams, the destination of the edge
      can be specified with an integer, representing the input pin index of
      the target equation.

    Parameters
    ----------
    diagram : suite.NetDiagram
        Diagram containing the source and destination equations. The diagram specified
        can be either graphical or textual, or it can be ``None``. However, it cannot be
        ``None`` if the scope contains at least one diagram.
    src : suite.Equation
        Source equation of the edge.
    left : suite.LocalVariable
        Local variable associated with the edge.
    dst : suite.Equation
        Target equation of the edge.
    expr: Union[suite.Expression]
        Parameter to connect to the edge or the input pin index of the target equation.
    points : List[Tuple(int, int)] | None, default: None
        Coordinates of the segments composing the edge, expressed in 1/100th of mm.
        When ``None``, the value is set to ``[(0, 0), (0, 0)]`` so that the SCADE Editor
        computes default positions when the model is loaded.

    Returns
    -------
    suite.Edge
    """
    _check_object(diagram, 'add_data_def_edge', 'diagram', suite.NetDiagram)
    _check_object(src, 'add_data_def_edge', 'src', suite.Equation)
    _check_object(dst, 'add_data_def_edge', 'dst', suite.Equation)
    _check_object(left, 'add_data_def_edge', 'left', suite.LocalVariable)
    if isinstance(expr, int):
        # searches the equation for the corresponding expression
        index = expr
        expr = _find_expr_id(dst.right, index)
    _check_object(expr, 'add_data_def_edge', 'expr', suite.ExprId)

    # a flow is only graphical
    pesrc = src.presentation_element
    pedst = dst.presentation_element
    diagram = pesrc.diagram
    edge = suite.Edge(diagram)
    diagram.presentation_elements.append(edge)
    edge.src_equation = pesrc
    edge.dst_equation = pedst
    edge.left_var = left
    edge.right_expression = expr

    variables = src.lefts
    index = variables.index(left)
    # 1 based index
    edge.left_var_index = index + 1

    # graphical properties
    if not points:
        values = [0] * 4
    else:
        values = [_ for point in points for _ in point]
    edge.points = _num_to_str(values)

    _set_modified(diagram.data_def)
    return edge


def add_diagram_missing_edges(diagram: suite.NetDiagram) -> List[suite.Edge]:
    """
    Add the missing edges in a graphical diagram with default positions.

    Parameters
    ----------
    diagram : suite.NetDiagram
        Input diagram.

    Returns
    -------
    List[suite.Edge]
    """
    _check_object(diagram, 'add_missing_edges', 'diagram', suite.NetDiagram)

    # cache the existing edges
    cache = {
        (_.left_var, _.right_expression)
        for _ in diagram.presentation_elements
        if isinstance(_, suite.Edge)
    }
    # find the not connected expressions of the graphical equations
    pairs = set()
    for pe in diagram.presentation_elements:
        if isinstance(pe, suite.EquationGE) and pe.kind == 'FI_EQUATION':
            # not a textual expression
            pairs |= {(_.reference, _) for _ in pe.equation.right.sub_expr_ids if _.reference}
    pairs -= cache
    # create the graphical edges
    edges = []
    for const_var, expr in pairs:
        if not isinstance(const_var, suite.LocalVariable):
            continue
        left = const_var
        # get the owning equation of the expression
        dst = expr.owner
        while not isinstance(dst, suite.Equation):
            dst = dst.owner
        # find the first equation defining the variable,
        # in the same scope/diagram
        for src in left.definitions:
            pe = src.presentation_element
            if src.data_def != dst.data_def or not pe or pe.diagram != diagram:
                continue
            # create the edge
            edge = add_diagram_edge(diagram, src, left, dst, expr)
            edges.append(edge)

    return edges


# ----------------------------------------------------------------------------
# assertions


class AK(Enum):
    """Provides an enum of assertion kinds."""

    ASSUME = 'Assume'
    GUARANTEE = 'Guarantee'


def add_data_def_assertion(
    data_def: suite.DataDef,
    diagram: Optional[suite.Diagram],
    name: str,
    expr: EX,
    kind: AK = AK.ASSUME,
    position: Tuple[float, float] = (0, 0),
) -> suite.Assertion:
    """
    Create an assertion in a scope.

    Parameters
    ----------
    data_def : suite.DataDef
        Input scope, which is an operator, state, or action.
    diagram : suite.Diagram | None
        Diagram containing the equation. The diagram specified can be either graphical
        or textual, or it can be ``None``. However, it cannot be ``None`` if the scope
        contains at least one diagram.
    name : str
        Name of the assertion.
    expr : EX
        Expression of the assertion.
    kind : AK, default: ASSUME
        Kind of the assertion.
    position : Tuple[float, float], default: (0, 0)
        Position of the assertion, expressed in 1/100th of mm.
        This value is ignored if the diagram is not a graphical diagram.
        Otherwise, it must be specified.

    Returns
    -------
    suite.Assertion
    """
    _check_object(data_def, 'add_data_def_assertion', 'datadef', suite.DataDef)
    if diagram:
        _check_object(
            diagram, 'add_data_def_assertion', 'diagram', (suite.NetDiagram, suite.TextDiagram)
        )

    assertion = suite.Assertion(data_def)
    assertion.name = name
    assertion.expression = _build_expression(expr, data_def)
    assertion.assume = kind == AK.ASSUME

    data_def.flows.append(assertion)

    if diagram:
        # graphical part
        if isinstance(diagram, suite.NetDiagram):
            pe = suite.AssertionGE(data_def)
            # graphical properties
            pe.position = _num_to_str(position)
        else:
            # text diagram
            pe = suite.FlowTE(data_def)
            # no other properties
        assertion.presentation_element = pe
        diagram.presentation_elements.append(pe)

    _link_pendings()
    _set_modified(data_def)
    return assertion


# ----------------------------------------------------------------------------
# state machines


def add_data_def_state_machine(
    data_def: suite.DataDef,
    name: str,
    diagram: suite.Diagram,
    position: Tuple[float, float] = (0, 0),
    size: Tuple[float, float] = (0, 0),
) -> suite.StateMachine:
    """
    Create a state machine in a scope.

    Parameters
    ----------
    data_def : suite.DataDef
        Input scope, which is an operator, state, or action.
    name : str
        Name of the state machine.
    diagram : suite.Diagram
        Diagram containing the equation. The diagram specified can be either graphical
        or textual, or it can be ``None``. However, it cannot be ``None`` if the scope
        contains at least one diagram.
    position : Tuple[float, float], default: None
        Position of the state machine, expressed in 1/100th of mm.
        This value is ignored if the diagram is not a graphical diagram.
        Otherwise, it must be specified.
    size : Tuple[float, float], default: None
        Size of the state machine, expressed in 1/100th of mm.
        This value is ignored if your diagram is not a graphical diagram.
        Otherwise, it must be specified.

    Returns
    -------
    suite.StateMachine
    """
    _check_object(data_def, 'add_data_def_state_machine', 'data_def', suite.DataDef)
    if diagram is not None:
        _check_object(
            diagram, 'add_data_def_state_machine', 'diagram', (suite.NetDiagram, suite.TextDiagram)
        )

    sm = suite.StateMachine(data_def)
    sm.name = name

    data_def.flows.append(sm)

    # graphical part
    if diagram is not None:
        # graphical part
        if isinstance(diagram, suite.NetDiagram):
            pe = suite.StateMachineGE(data_def)
            # graphical properties
            pe.position = _num_to_str(position)
            pe.size = _num_to_str(size)
        else:
            # text diagram
            pe = suite.FlowTE(data_def)
            # no other properties
        sm.presentation_element = pe
        diagram.presentation_elements.append(pe)

    _link_pendings()
    _set_modified(data_def)
    return sm


class SK(Enum):
    """Provides an enum of state kinds."""

    NORMAL = 'Normal'
    INITIAL = 'Initial'
    FINAL = 'Final'


class DK(Enum):
    """Provides an enum of display kinds."""

    GRAPHICAL = 'EmbeddedGraphical'
    TEXTUAL = 'EmbeddedTextual'
    SPLIT = 'Split'


def add_state_machine_state(
    sm: suite.StateMachine,
    name: str,
    position: Tuple[float, float] = (0, 0),
    size: Tuple[float, float] = (0, 0),
    kind: SK = SK.NORMAL,
    display: DK = DK.GRAPHICAL,
) -> suite.State:
    """
    Create a state in a state machine.

    Parameters
    ----------
    sm : suite.StateMachine
        Input state machine.
    name : str.StateMachine
        Name of the state.
    position : Tuple[float, float], default: (0, 0)
        Position of the state, expressed in 1/100th of mm.
        This value is considered if and only if the state machine
        has a graphical representation.
    size : Tuple[float, float], default: (0, 0)
        Size of the state, expressed in 1/100th of mm.
        This value is considered if and only if the state machine
        has a graphical representation.
    kind : SK, default: NORMAL
        Kind of the state.
    display : DK, default: GRAPHICAL
        Layout of the state.

    Returns
    -------
    suite.State
    """
    _check_object(sm, 'add_state_machine_state', 'sm', suite.StateMachine)

    state = suite.State(sm)
    state.name = name
    if kind == SK.INITIAL:
        state.initial = True
    elif kind == SK.FINAL:
        state.final = True

    sm.states.append(state)

    # graphical part
    pesm = sm.presentation_element
    diagram = pesm.diagram if pesm is not None else None
    if isinstance(diagram, suite.NetDiagram):
        pe = suite.StateGE(diagram.data_def)
        # graphical properties
        pe.position = _num_to_str(position)
        pe.size = _num_to_str(size)
        if display == DK.SPLIT:
            add_data_def_net_diagram(state, state.name)
        pe.display = display.value
        state.presentation_element = pe
        diagram.presentation_elements.append(pe)
    # no presentation elements for text diagrams: only for owning state machine

    _link_pendings()
    _set_modified(sm)
    return state


# transition trees
class TransitionDestination:
    """Provides the top-level abstract class for transition destinations."""

    pass


TD = TransitionDestination
"""Short name for a ``TransitionDestination`` instance to simplify the declarations."""


class TransitionTree:
    """Provides the intermediate class for transitions."""

    def __init__(
        self,
        trigger: Optional[EX],
        target: TD,
        priority: int,
        points: Optional[List[Tuple[float, float]]] = None,
        label_position: Tuple[float, float] = (0, 0),
        label_size: Tuple[float, float] = (0, 0),
        slash_position: Tuple[float, float] = (0, 0),
        polyline: bool = True,
    ):
        """Store the attributes."""
        self.trigger = trigger
        self.target = target
        self.priority = priority
        # the points must be provided for graphical representations
        self.points = points if points else []
        # the positions and sizes are optional
        self.label_position = label_position
        self.label_size = label_size
        self.slash_position = slash_position
        self.polyline = polyline


TR = TransitionTree
"""Short name for a ``TransitionTree`` instance to simplify the declarations."""


class _State(TD):
    """Provides the destination state."""

    def __init__(self, state: suite.State, reset: bool):
        """Store the attributes."""
        self.state = state
        self.reset = reset


class _Fork(TD):
    """Provides forked transitions."""

    def __init__(self, transitions: List[TransitionTree]):
        """Store the attributes."""
        self.transitions = transitions


class TK(Enum):
    """Provides an enum of transition kinds."""

    WEAK = 'Weak'
    STRONG = 'Strong'
    SYNCHRO = 'Synchro'


def create_transition_state(
    trigger: Optional[EX],
    state: suite.State,
    reset: bool,
    priority: int,
    points: Optional[List[Tuple[float, float]]] = None,
    label_position: Tuple[float, float] = (0, 0),
    label_size: Tuple[float, float] = (0, 0),
    slash_position: Tuple[float, float] = (0, 0),
    polyline: bool = True,
) -> TR:
    """
    Create an intermediate transition structure that targets a state.

    The graphical properties are expressed 1/100th of mm.

    They are considered if and only if the owning state machine
    has a graphical representation.

    Parameters
    ----------
    trigger : EX | None
        Extended expression tree defining the trigger of the transition.
    state : suite.State
        Target state of the transition.
    reset : bool
        Whether the transition resets the targtet state.
    priority : int
        Priority of the transition.
    points : List[Tuple[float, float]] | None, default: None
        Points of the transition.
    label_position : Tuple[float, float], default: (0, 0)
        Position of the label.
    label_size : Tuple[float, float], default: (0, 0)
        Size of the label.
    slash_position : Tuple[float, float], default: (0, 0)
        Position of the separator between the trigger and the action
        of the transition.
    polyline : bool, default: True
        Whether the representation is a list of segments. If ``False``,
        the representation is a Bezier curve.

    Returns
    -------
    TR
    """
    td = _State(state, reset)
    return TR(trigger, td, priority, points, label_position, label_size, slash_position, polyline)


def create_transition_fork(
    trigger: Optional[EX],
    forks: List[TR],
    priority: int,
    points: Optional[List[Tuple[float, float]]] = None,
    label_position: Tuple[float, float] = (0, 0),
    label_size: Tuple[float, float] = (0, 0),
    slash_position: Tuple[float, float] = (0, 0),
    polyline: bool = True,
) -> TR:
    """
    Create an intermediate transition structure with forked transitions.

    The graphical properties are expressed 1/100th of mm.

    They are considered if and only if the owning state machine
    has a graphical representation.

    Parameters
    ----------
    trigger : EX | None
        Extended expression tree defining the trigger of the transition.
    forks : List[TR]
        Transitions forked from this transition.
    priority : int
        Priority of the transition.
    points : List[Tuple[float, float]] | None, default: None
        Points of the transition.
    label_position : Tuple[float, float], default: (0, 0)
        Position of the label.
    label_size : Tuple[float, float], default: (0, 0)
        Size of the label, default: None
    slash_position : Tuple[float, float], default: (0, 0)
        Position of the separator between the trigger and the action
        of the transition.
    polyline : bool, default: True
        Indicates whether the representation is a list of segments. If ``False``,
        the representation is a Bezier curve.

    Returns
    -------
    TR
    """
    td = _Fork(forks)
    return TR(trigger, td, priority, points, label_position, label_size, slash_position, polyline)


def add_state_transition(state: suite.State, kind: TK, tree: TR) -> suite.Transition:
    """
    Add a new transition starting from a state.

    Parameters
    ----------
    state : EX
        Source of the transition.
    kind : TK
        Kind of transition.
    tree : TR
        Transition tree, which is the intermediate structure describing the transition.

    Returns
    -------
    suite.Transition
    """
    _check_object(state, '_add_state_transition', 'state', suite.State)

    transition = _build_transition(state, tree)
    transition.transition_kind = kind.value

    _link_pendings()
    _set_modified(state)
    return transition


def _build_transition(src: Union[suite.State, suite.Transition], tree: TR) -> suite.Transition:
    """Build a transition from the intermediate tree."""
    _check_object(src, '_build_transition', 'src', (suite.State, suite.Transition))

    if isinstance(src, suite.State):
        # main transition
        transition = suite.MainTransition(src)
        src.outgoings.append(transition)
    else:
        # forked transition
        transition = suite.ForkedTransition(src)
        src.forked_transitions.append(transition)

    if tree.trigger is None:
        transition._else = True
    else:
        transition.condition = _build_expression(tree.trigger, src)
    # do not create automatically an action: this is the behavior of the SCADE Editor
    # transition.effect = suite.Action(transition)
    transition.priority = tree.priority

    # graphical part
    pesrc = src.presentation_element
    diagram = pesrc.diagram if pesrc is not None else None
    pe = None  # default
    if isinstance(diagram, suite.NetDiagram):
        pe = suite.TransitionGE(diagram.data_def)
        # graphical properties
        values = [_ for point in tree.points for _ in point]
        pe.points = _num_to_str(values)
        pe.label_position = _num_to_str(tree.label_position)
        pe.label_size = _num_to_str(tree.label_size)
        pe.slash_position = _num_to_str(tree.slash_position)
        pe.polyline = tree.polyline
        transition.presentation_element = pe
        diagram.presentation_elements.append(pe)
    # no presentation elements for text diagrams: only for owning state machine

    td = tree.target
    if isinstance(td, _State):
        transition.target = td.state
        transition.reset_target = td.reset
    else:
        assert isinstance(td, _Fork)  # nosec B101  # addresses linter
        for fork in td.transitions:
            _build_transition(transition, fork)

    return transition


def add_transition_equation(
    transition: suite.Transition,
    lefts: List[Union[suite.LocalVariable, TX]],
    right: Optional[EX],
) -> suite.Equation:
    """
    Create an equation in a transition.

    Notes
    -----
    This function ensures the availability of a scope before creating the
    equation. Indeed, the transitions do not have a scope, suite.DataDef, by default.

    Parameters
    ----------
    transition : suite.Transition
        Input transition.
    lefts : List[suite.LocalVariable]
        List of variables defined by the equation.
    right : EX | None
        Expression of the equation.

    Returns
    -------
    suite.Equation
    """
    _check_object(transition, 'add_transition_equation', 'transition', suite.Transition)

    # make sure the transition has a scope
    if not transition.effect:
        transition.effect = suite.Action(transition)

    return add_data_def_equation(transition.effect, None, lefts, right)


# ----------------------------------------------------------------------------
# if blocks


class IfTree(ABC):
    """Provides an intermediate structure for describing the structure of an if block."""

    def __init__(self, position: Tuple[float, float] = (0, 0)):
        """Store the attributes."""
        self.position = position
        # name to be used if a diagram needs to be created
        self.name = ''

    @abstractmethod
    def _build(self, context: suite.Object, diagram: suite.Diagram) -> suite.IfBranch:
        """Build an if branch from the tree."""
        raise NotImplementedError  # pragma no cover


IT = IfTree
"""Short name for an ``IfTree`` instance to simplify the declarations."""


class _Node(IT):
    """Provides an intermediate structure to describe a decision of an if tree."""

    def __init__(
        self,
        expression: EX,
        then: IT,
        else_: IT,
        position: Tuple[float, float] = (0, 0),
        label_width: int = 0,
    ):
        """Store the attributes."""
        super().__init__(position)
        self.expression = expression
        self.then = then
        self.then.name = 'Then'
        self.else_ = else_
        self.else_.name = 'Else'
        self.label_width = label_width

    def _build(self, owner: suite.Object, diagram: suite.Diagram) -> suite.IfBranch:
        """Build an if node from the tree."""
        _check_object(owner, '_build', 'owner', (suite.IfBlock, suite.IfNode))

        node = suite.IfNode(owner)
        node.expression = _build_expression(self.expression, node)
        node.then = self.then._build(node, diagram)
        node._else = self.else_._build(node, diagram)

        # graphical part
        if isinstance(diagram, suite.NetDiagram):
            pe = suite.IfNodeGE(diagram.data_def)
            # graphical properties
            pe.position = _num_to_str(self.position)
            pe.label_width = self.label_width
            node.presentation_element = pe
            diagram.presentation_elements.append(pe)

        return node


class _Action(IT):
    """Provides the leaf action of an if tree."""

    def __init__(
        self,
        position: Tuple[float, float] = (0, 0),
        size: Tuple[float, float] = (0, 0),
        display: DK = DK.GRAPHICAL,
    ):
        """Store the attributes."""
        super().__init__(position)
        self.size = size if size else (0, 0)
        self.display = display

    def _build(self, owner: suite.Object, diagram: suite.Diagram) -> suite.IfBranch:
        """Build an if action from the tree."""
        _check_object(owner, '_build', 'owner', suite.IfNode)

        ia = suite.IfAction(owner)
        ia.action = suite.Action(owner)

        # graphical part
        if isinstance(diagram, suite.NetDiagram):
            pe = suite.ActionGE(diagram.data_def)
            # graphical properties
            pe.position = _num_to_str(self.position)
            pe.size = _num_to_str(self.size)
            if self.display == DK.SPLIT:
                add_data_def_net_diagram(ia.action, self.name)
            pe.display = self.display.value
            ia.action.presentation_element = pe
            diagram.presentation_elements.append(pe)

        return ia


def create_if_action(
    position: Tuple[float, float] = (0, 0),
    size: Tuple[float, float] = (0, 0),
    display: DK = DK.GRAPHICAL,
) -> IT:
    """
    Create a leaf action in the intermediate structure if it is a tree structure.

    The graphical properties are expressed 1/100th of mm.

    They are considered if and only if the owning if block
    has a graphical representation.

    Parameters
    ----------
    position : Tuple[float, float], default: (0, 0)
        Position of the action.
    size : Tuple[float, float], default: (0, 0)
        Size of the action.
    display : DK, default: GRAPHICAL
        Layout of the action.


    Returns
    -------
    IT
    """
    return _Action(position, size, display)


def create_if_tree(
    expression: EX,
    then: IT,
    else_: IT,
    position: Tuple[float, float] = (0, 0),
    label_width: int = 0,
) -> IT:
    r"""
    Create a decision in the intermediate structure if it is a tree structure.

    The graphical properties are expressed 1/100th of mm.

    They are considered if and only if the owning if block
    has a graphical representation.

    Hint for the graphical properties: The size of a node is 80x80. Consider
    this offset to have consistent values between if nodes and actions.

    Parameters
    ----------
    expression : EX
        Extended expression tree defining the condition of the decision.
    then : IT
        Sub-decision tree to consider when the condition is ``True``.
    else\_ : IT
        Sub-decision tree to consider when the condition is ``False``.
    position : Tuple[float, float], default: (0, 0)
        Position of the decision.
    label_width : int, default: 0
        Size of the label.

    Returns
    -------
    IT
    """
    return _Node(expression, then, else_, position, label_width)


def add_data_def_if_block(
    data_def: suite.DataDef,
    name: str,
    if_tree: IfTree,
    diagram: suite.Diagram,
    position: Tuple[float, float] = (0, 0),
    size: Tuple[float, float] = (0, 0),
) -> suite.IfBlock:
    """
    Create an if block in a scope.

    The graphical properties are expressed 1/100th of mm.

    They are considered if and only if diagram is a graphical diagram.

    Parameters
    ----------
    data_def : suite.DataDef
        Input scope, which is an operator, state, or action.
    name : str
        Name of the if block.
    if_tree : IfTree
        Intermediate tree to describe the structure of the if block.
    diagram : suite.Diagram
        Diagram containing the equation. The diagram specified can be either graphical
        or textual, or it can be ``None``. However, it cannot be ``None`` if the scope
        contains at least one diagram.
    position : Tuple[float, float], default: (0, 0)
        Position of the if block.
    size : Tuple[float, float], default: (0, 0)
        Size of the if block.

    Returns
    -------
    suite.IfBlock
    """
    _check_object(data_def, 'add_data_def_if_block', 'data_def', suite.DataDef)
    if diagram is not None:
        _check_object(
            diagram, 'add_data_def_if_block', 'diagram', (suite.NetDiagram, suite.TextDiagram)
        )

    ib = suite.IfBlock(data_def)
    ib.name = name
    data_def.flows.append(ib)
    ib.if_node = if_tree._build(ib, diagram)

    # graphical part
    pe = None  # default
    if diagram is not None:
        if isinstance(diagram, suite.NetDiagram):
            pe = suite.IfBlockGE(data_def)
            # graphical properties
            pe.position = _num_to_str(position)
            pe.size = _num_to_str(size)
        else:
            # text diagram
            pe = suite.FlowTE(data_def)
            # no other properties
        ib.presentation_element = pe
        diagram.presentation_elements.append(pe)

    _link_pendings()
    _set_modified(data_def)
    return ib


# ----------------------------------------------------------------------------
# when blocks


class WhenBranch:
    """Provides the intermediate class for when branches."""

    def __init__(
        self,
        pattern: EX,
        position: Tuple[float, float] = (0, 0),
        size: Tuple[float, float] = (0, 0),
        display: DK = DK.GRAPHICAL,
        label_width: int = 0,
    ):
        """Store the attributes."""
        self.pattern = pattern
        self.position = position
        self.size = size
        self.display = display
        self.label_width = label_width


def create_when_branch(
    pattern: EX,
    position: Tuple[float, float] = (0, 0),
    size: Tuple[float, float] = (0, 0),
    display: DK = DK.GRAPHICAL,
    label_width: int = 0,
) -> WhenBranch:
    """
    Create an intermediate structure for a when branch.

    The graphical properties are expressed 1/100th of mm.

    They are considered if and only if the owning when block
    has a graphical representation.

    Parameters
    ----------
    pattern : EX
        Value of the branch.
    position : Tuple[float, float], default: (0, 0)
        Position of the action.
    size : Tuple[float, float], default: (0, 0)
        Size of the action.
    display : DK, default: GRAPHICAL
        Layout of the action.
    label_width : int
        Optional width of the label containing the pattern.

    Returns
    -------
    WhenBranch
    """
    return WhenBranch(pattern, position, size, display, label_width)


def add_data_def_when_block(
    data_def: suite.DataDef,
    name: str,
    when: EX,
    branches: List[WhenBranch],
    diagram: Optional[suite.Diagram] = None,
    position: Tuple[float, float] = (0, 0),
    size: Tuple[float, float] = (0, 0),
    start_position: Tuple[float, float] = (450, 582),
    label_width: int = 0,
) -> suite.WhenBlock:
    """
    Add a new when block in a scope.

    The graphical properties are expressed 1/100th of mm.

    They are considered if and only if the owning when block
    has a graphical representation.

    Parameters
    ----------
    data_def : suite.DataDef
        Input scope, which is an operator, state, or action.
    name : str
        Name of the block.
    when : EX
        Pattern of the block.
    branches : List[WhenBranch]
        List of intermediate structures describing the branches.
        There must be at least one branch.
    diagram : suite.Diagram | None, default: None
        Diagram containing the equation. The diagram specified can be either graphical
        or textual, or it can be ``None``. However, it cannot be ``None`` if the scope
        contains at least one diagram.
    position : Tuple[float, float] default: (0, 0))
        Position of the block.
    size : Tuple[float, float] default: (0, 0)
        Size of the block.
    start_position : Tuple[float, float], default: (450, 582)
        Start position of the branches relative to the block.
    label_width : int, default: 0
        Width of the label containing the pattern.

    Returns
    -------
    suite.WhenBlock
    """
    _check_object(data_def, 'add_data_def_when_block', 'datadef', suite.DataDef)
    if diagram is not None:
        _check_object(
            diagram, 'add_data_def_when_block', 'diagram', (suite.NetDiagram, suite.TextDiagram)
        )

    if not branches:
        raise ValueError('add_data_def_when_block: The block must have at least one branch')

    wb = suite.WhenBlock(data_def)
    wb.name = name
    data_def.flows.append(wb)
    wb.when = _build_expression(when, wb)

    # graphical part
    pe = None  # default
    if diagram is not None:
        if isinstance(diagram, suite.NetDiagram):
            pe = suite.WhenBlockGE(data_def)
            # graphical properties
            pe.start_pos = _num_to_str(start_position)
            pe.label_width = label_width
            pe.position = _num_to_str(position)
            pe.size = _num_to_str(size)
        else:
            # text diagram
            pe = suite.FlowTE(data_def)
            # no other properties
        wb.presentation_element = pe
        diagram.presentation_elements.append(pe)

    add_when_block_branches(wb, branches)

    _link_pendings()
    _set_modified(data_def)
    return wb


def add_when_block_branches(
    when_block: suite.WhenBlock,
    branches: List[WhenBranch],
) -> List[suite.WhenBranch]:
    """
    Add new branches to a when block.

    Parameters
    ----------
    when_block : suite.WhenBlock
        Input block.
    branches : List[WhenBranch]
        List of intermediate structures describing the branches.

    Returns
    -------
    List[suite.WhenBranch]
    """
    _check_object(when_block, 'add_when_block_branches', 'when_block', suite.WhenBlock)

    diagram = when_block.presentation_element.diagram if when_block.presentation_element else None

    when_branches = []
    for branch in branches:
        _check_object(branch, 'add_when_block_branches', 'branch', WhenBranch)

        when_branch = suite.WhenBranch(when_block)
        when_block.when_branches.append(when_branch)
        when_branch.pattern = _build_expression(branch.pattern, when_branch)
        when_branch.action = suite.Action(when_block)
        when_branches.append(when_branch)
        _link_pendings()

        # graphical part: a bit complex since two PE for one branch
        peb = None  # default
        pea = None  # default
        if diagram is not None:
            if isinstance(diagram, suite.NetDiagram):
                pew = when_block.presentation_element
                peb = suite.WhenBranchGE(when_block)
                pea = suite.ActionGE(when_block)
                # graphical properties
                # apply a fixed offset from the block's left and the action's top
                # the following offsets are reversed engineered and rounded from model files
                start = (pew.position[0] + pew.start_pos[0] + 80, branch.position[1] + 80)
                peb.position = _num_to_str(start)
                peb.label_width = branch.label_width
                pea.position = _num_to_str(branch.position)
                pea.size = _num_to_str(branch.size)
                if branch.display == DK.SPLIT:
                    name = when_branch.pattern.to_string()
                    add_data_def_net_diagram(when_branch.action, name)
                pea.display = branch.display.value
                when_branch.presentation_element = peb
                when_branch.action.presentation_element = pea
                diagram.presentation_elements.append(peb)
                diagram.presentation_elements.append(pea)

    _set_modified(when_block)
    return when_branches


# ----------------------------------------------------------------------------
# equation sets


def add_diagram_equation_set(
    diagram: suite.NetDiagram, name: str, elements: Optional[List[suite.Presentable]] = None
) -> suite.EquationSet:
    """
    Add a new equation set to a graphical diagram.

    Parameters
    ----------
    diagram : suite.NetDiagram
        Input diagram.
    name : str
        Name of the equation set.
    elements : List[suite.Presentable] | None, default: None
        List of elements to add to the equation set.

    Returns
    -------
    suite.EquationSet
    """
    _check_object(diagram, 'add_diagram_equation_set', 'diagram', suite.NetDiagram)
    # make sure the elements can be added to the equation set
    if elements is None:
        elements = []
    for index, element in enumerate(elements):
        pe = element.presentation_element
        if not pe or pe.diagram != diagram:
            raise ValueError("%s: element #%d can't be added" % (diagram, index + 1))

    eqs = suite.EquationSet(diagram)
    eqs.name = name
    eqs.presentables.extend(elements)
    diagram.equation_sets.append(eqs)

    _set_modified(diagram)
    return eqs
