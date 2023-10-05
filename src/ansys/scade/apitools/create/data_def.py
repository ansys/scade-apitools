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
Creation functions for Scade operator definitions.

* Interface
* Behavior
"""

from enum import Enum
from typing import List, Tuple, Union

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

    Return the added signals.

    Parameters
    ----------
        data_def : suite.DataDef
            Input scope, either an operator, a state or an action.

        names : List[str]
            Names of the signals to be created.

    Returns
    -------
        List[suite.LocalVariable]
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

    Return the added variables.

    Note: interface change with respect to the SCADE Creation Library,
    the pairs name/type tree are now embedded in a list of tuples.

    Parameters
    ----------
        data_def : suite.DataDef
            Input scope, either an operator, a state or an action.

        vars : List[Tuple[str, TX]]
            Name/type expression trees.

    Returns
    -------
        List[suite.LocalVariable]
    """
    return _add_data_def_variables(data_def, vars, False)


def add_data_def_probes(
    data_def: suite.DataDef, vars: List[Tuple[str, TX]]
) -> List[suite.LocalVariable]:
    """
    Add probes to a scope.

    Return the added probes.

    Note: interface change with respect to the SCADE Creation Library,
    the pairs name/type tree are now embedded in a list of tuples.

    Parameters
    ----------
        data_def : suite.DataDef
            Input scope, either an operator, a state or an action.

        vars : List[Tuple[str, TX]]
            Name/type expression trees.

    Returns
    -------
        List[suite.LocalVariable]
    """
    return _add_data_def_variables(data_def, vars, True)


# ----------------------------------------------------------------------------
# variables


def set_variable_default(variable: suite.LocalVariable, tree: EX) -> suite.Expression:
    """
    Set the default value of a variable.

    Return the expression.

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

    Return the expression.

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
    if isinstance(data_def, suite.Action):
        # internal IDE structure not consistent, an additional property is required
        if data_def.presentation_element:
            data_def.presentation_element.display = 'Split'

    _set_modified(data_def)
    return diagram


def add_data_def_text_diagram(data_def: suite.DataDef, name: str) -> suite.TextDiagram:
    """
    Add a textal diagram to a scope.

    Return the diagram.

    Parameters
    ----------
        data_def : suite.DataDef
            Input scope, either an operator, a state or an action.

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

    Return the diagram.

    Parameters
    ----------
        data_def : suite.DataDef
            Input scope, either an operator, a state or an action.

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


def _num_to_str(values: List[Union[int, float]]) -> List[str]:
    """SCADE graphical coordinates shall be strings: position, size, points."""
    return [str(_) for _ in values]


def _create_internal(data_def: suite.DataDef, tree: TX) -> suite.LocalVariable:
    """
    Create an internal variable for an operator.

    Note: the algorithm is inefficient, it is adivsed the name
    of the internal variables is computed with a cache in the client code.

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
    diagram: suite.Diagram,
    lefts: List[Union[suite.LocalVariable, TX]],
    right: EX,
    position: Tuple[float, float] = None,
    size: Tuple[float, float] = None,
    symmetrical: bool = False,
    rotation: int = 0,
    textual: bool = False,
) -> suite.Equation:
    """
    Create an equation in a scope.

    Parameters
    ----------
        data_def : suite.DataDef
            Input scope, either an operator, a state or an action.

        diagram : suite.Diagram
            Diagram containing the equation: either graphical, textual or None.

            Note: the diagram can't be None if the scope contains at least one diagram.

        lefts : List[Union[suite.LocalVariable, TX]]
            List of variables defined by the equation. The elements can be either an
            existing local variable or a type tree, to create on the fly a new internal
            variable.

        right : EX
            Expression of the equation.

        position : Tuple[float, float]
            Position of the equation, expressed in 1/100th of mm.
            This value is ignored if diagram is not a graphical diagram,
            otherwise it must be specified.

        size : Tuple[float, float]
            Size of the equation, expressed in 1/100th of mm.
            This value is ignored if diagram is not a graphical diagram,
            otherwise it must be specified.

        symmetrical : bool
            Indicates whether the graphical representation is symmetrical.

        rotation : int
            Rotation angle of the equation, expressed in degrees.
            The value shall be one of 0, 90, 180 or 270.

        textual : bool
            Indicates whether the equation is a textual or has a graphical representation.

    Returns
    -------
        suite.Equation
    """
    _check_object(data_def, 'add_data_def_equation', 'datadef', suite.DataDef)
    if diagram is not None:
        _check_object(
            diagram, 'add_data_def_equation', 'diagram', (suite.NetDiagram, suite.TextDiagram)
        )

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

    equation.right = _build_expression(right, data_def)

    # graphical part
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
    points: List[Tuple[int, int]] = None,
) -> suite.Edge:
    """
    Add a graphical edge between two equations in a graphical diagram.

    * The source of the edge is identified by the local variable defined
      in the source equation.

    * The destination of the edge is identified by the parameter of the
      expression of the target equation. It shall be an instance of ExprId
      referring to the left variable.

      To ease the creation of graphical diagrams, the destination of the edge
      can be specified with an integer, representing the input pin index of
      the target equation.

    Parameters
    ----------
        diagram : suite.NetDiagram
            Diagram containing the source and destination equations.

            Note: the diagram can't be None if the scope contains at least one diagram.

        src : suite.Equation
            Source equation of the edge.

        left : suite.LocalVariable
            Local variable associated of the edge.

        dst : suite.Equation
            Target equation of the edge.

        expr: Union[suite.Expression]
            Parameter to be connected to the edge, or input pin index.

        points : List[Tuple(int, int)]
            Coordinates of the segments composing the edge, expressed in 1/100th of mm.
            When None, the value is set to [(0, 0), (0, 0)], so that the SCADE Editor
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
    for left, expr in pairs:
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
    """Assertion kind: either assume or guarantee."""

    ASSUME = 'Assume'
    GUARANTEE = 'Guarantee'


def add_data_def_assertion(
    data_def: suite.DataDef,
    diagram: suite.Diagram,
    name: str,
    expr: EX,
    kind: AK = AK.ASSUME,
    position: Tuple[float, float] = None,
) -> suite.Assertion:
    """
    Create an assertion in a scope.

    Parameters
    ----------
        data_def : suite.DataDef
            Input scope, either an operator, a state or an action.

        diagram : suite.Diagram
            Diagram containing the equation: either graphical, textual or None.

            Note: the diagram can't be None if the scope contains at least one diagram.

        name : str
            Name of the assertion.

        expr : EX
            Expression of the assertion.

        kind : VK
            Kind of the assertion, either assume or guarantee.

        position : Tuple[float, float]
            Position of the assertion, expressed in 1/100th of mm.
            This value is ignored if diagram is not a graphical diagram,
            otherwise it must be specified.

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
    diagram: suite.Diagram,
    name: str,
    position: Tuple[float, float] = None,
    size: Tuple[float, float] = None,
) -> suite.StateMachine:
    """
    Create a state machine in a scope.

    Parameters
    ----------
        data_def : suite.DataDef
            Input scope, either an operator, a state or an action.

        diagram : suite.Diagram
            Diagram containing the equation: either graphical, textual or None.

            Note: the diagram can't be None if the scope contains at least one diagram.

        position : Tuple[float, float]
            Position of the state machine, expressed in 1/100th of mm.
            This value is ignored if diagram is not a graphical diagram,
            otherwise it must be specified.

        size : Tuple[float, float]
            Size of the state machine, expressed in 1/100th of mm.
            This value is ignored if diagram is not a graphical diagram,
            otherwise it must be specified.

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
    """State kind: either normal, initial, or final."""

    NORMAL = 'Normal'
    INITIAL = 'Initial'
    FINAL = 'Final'


class DK(Enum):
    """Display kind: either normal, initial, or final."""

    GRAPHICAL = 'EmbeddedGraphical'
    TEXTUAL = 'EmbeddedTextual'
    SPLIT = 'Split'


def add_state_machine_state(
    sm: suite.StateMachine,
    name: str,
    position: Tuple[float, float] = None,
    size: Tuple[float, float] = None,
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

        position : Tuple[float, float]
            Position of the state, expressed in 1/100th of mm.
            This value is considered if and only if the state machine
            has a graphical representation.

        size : Tuple[float, float]
            Size of the state, expressed in 1/100th of mm.
            This value is considered if and only if the state machine
            has a graphical representation.

        kind : SK
            Kind of the state, either normal, initial, or final.

        display : DK
            Display kind of the state, either graphical, textual, or split.

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
        state.presentation_element = pe
        diagram.presentation_elements.append(pe)
    # no presentation elements for text diagrams: only for owning state machine

    _link_pendings()
    _set_modified(sm)
    return state


# transition trees
class TransitionDestination:
    """Top-level abstract class for transition destinations."""

    pass


TD = TransitionDestination
"""Short name for TransitionDestination to simplify the declarations."""


class TransitionTree:
    """Intermediate class for transitions."""

    def __init__(
        self,
        trigger: EX,
        target: TD,
        priority: int,
        points: List[Tuple[float, float]] = None,
        label_position: Tuple[float, float] = None,
        label_size: Tuple[float, float] = None,
        slash_position: Tuple[float, float] = None,
        polyline: bool = True,
    ):
        """Store the attributes."""
        self.trigger = trigger
        self.target = target
        self.priority = priority
        # the points must be provided for graphical representations
        self.points = points
        # the positions and sizes are optional
        self.label_position = label_position if label_position else [0, 0]
        self.label_size = label_size if label_size else [0, 0]
        self.slash_position = slash_position if slash_position else [0, 0]
        self.polyline = polyline

    def _build_transition(self, context: suite.Object) -> suite.Transition:
        """Build a transition from the transition tree."""
        # must be overridden
        assert False  # pragma no cover


TR = TransitionTree
"""Short name for TransitionTree to simplify the declarations."""


class _State(TD):
    """Destination state."""

    def __init__(self, state: suite.State, reset: bool):
        """Store the attributes."""
        self.state = state
        self.reset = reset


class _Fork(TD):
    """Forked Transitions."""

    def __init__(self, transitions: List[TransitionTree]):
        """Store the attributes."""
        self.transitions = transitions


class TK(Enum):
    """Transition kind: either weak, strong, or synchro."""

    WEAK = 'Weak'
    STRONG = 'Strong'
    SYNCHRO = 'Synchro'


def create_transition_state(
    trigger: EX,
    state: suite.State,
    reset: bool,
    priority: int,
    points: List[Tuple[float, float]] = None,
    label_position: Tuple[float, float] = None,
    label_size: Tuple[float, float] = None,
    slash_position: Tuple[float, float] = None,
    polyline: bool = True,
) -> TR:
    """
    Create an intermediate transition structure which targets a state.

    The graphical properties are expressed  1/100th of mm.

    They are considered if and only if the owning state machine
    has a graphical representation.

    Parameters
    ----------
        trigger : EX
            Extended expression tree defining the trigger of the transition.

        state : suite.State
            Target state of the transition.

        reset : bool
            Indicates whether the transition resets the targtet state.

        priority : int
            Priority of the transition.

        points : List[Tuple[float, float]]
            Points of the transition.

        label_position : Tuple[float, float]
            Position of the label.

        label_size : Tuple[float, float]
            Size of the label.

        slash_position : Tuple[float, float]
            Position of the separator between the trigger and the action
            of the transition.

        polyline : bool.
            Indicates whether the representation is a list of segments or
            a Bezier curve.

    Returns
    -------
        TR
    """
    td = _State(state, reset)
    return TR(trigger, td, priority, points, label_position, label_size, slash_position, polyline)


def create_transition_fork(
    trigger: EX,
    forks: List[TR],
    priority: int,
    points: List[Tuple[float, float]] = None,
    label_position: Tuple[float, float] = None,
    label_size: Tuple[float, float] = None,
    slash_position: Tuple[float, float] = None,
    polyline: bool = True,
) -> TR:
    """
    Create an intermediate transition structure with forked transitions.

    The graphical properties are expressed  1/100th of mm.

    They are considered if and only if the owning state machine
    has a graphical representation.

    Parameters
    ----------
        trigger : EX
            Extended expression tree defining the trigger of the transition.

        forks : List[TR]
            Transitions forked from this transition.

        priority : int
            Priority of the transition.

        points : List[Tuple[float, float]]
            Points of the transition.

        label_position : Tuple[float, float]
            Position of the label.

        label_size : Tuple[float, float]
            Size of the label.

        slash_position : Tuple[float, float]
            Position of the separator between the trigger and the action
            of the transition.

        polyline : bool.
            Indicates whether the representation is a list of segments or
            a Bezier curve.

    Returns
    -------
        TR
    """
    td = _Fork(forks)
    return TR(trigger, td, priority, points, label_position, label_size, slash_position, polyline)


def add_state_transition(state: suite.State, kind: TK, tree: TR) -> suite.Transition:
    """
    Add a new transition from a state.

    Note : the transition is created without action. To add equations, the following
    statement must be added::

        transition.effect = suite.Action(transition)

    Parameters
    ----------
        state : EX
            Source of the transition.

        kind : TK
            Kind of the transition, either weak, strong, or synchro.

        tree : TR
            Transition tree: intermediate structure describing the transition.

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
        assert isinstance(td, _Fork)
        for fork in td.transitions:
            _build_transition(transition, fork)

    return transition


# ----------------------------------------------------------------------------
# if blocks
#
#'''
# <diagram>: Diagram the block has to be linked to. This shall be either a diagram of <datadef>
#            or an empty diagram when <datadef> is for example the action of a transition.
# <if_tree>: Tree describing the block hierarchy. This tree is defined as follow:
#        <if_tree> :: = { if <expr_tree> <then> <else> <if_props> }
#        <then> ::= <action_props> | <if_tree>
#        <else> ::= <action_prop> | <if_tree>
# <block_props>: Properties set of the block.
# 	* position (¤): Pair of integers defining the position of the block ({ <int> <int> })
# 	* size (¤): Pair of integers defining the size of the block ({ <int> <int> })
# <if_props>: Properties set of the decision node.
# 	* position (¤): Pair of integers defining the position of the node ({ <int> <int> })
# 	* labelWidth (¤): Integer defining the width of the label containing the condition
# <action_props>: Properties set of the action.
# 	* position (¤): Pair of integers defining the position of the action ({ <int> <int> })
# 	* size (¤): Pair of integers defining the size of the action ({ <int> <int> })
# 	* display (¤): Layout of the action, EmbeddedGraphical, EmbeddedTextual or Split
#'''
#
#
# def AddDataDefIfBlock(datadef, diagram, name, if_tree, **keywords):
#    _check_object(datadef, 'AddDataDefIfBlock', 'datadef', suite.DataDef)
#    if diagram is not None:
#        _check_object(
#            diagram, 'AddDataDefIfBlock', 'diagram', (suite.NetDiagram, suite.TextDiagram)
#        )
#
#    ib = suite.IfBlock(datadef)
#    ib.name = name
#    _scade_api.add(datadef, 'flow', ib)
#    ib.if_node = BuildIfTree(ib, diagram, if_tree)
#
#    # graphical part
#    pe = None  # default
#    if diagram is not None:
#        if isinstance(diagram, suite.NetDiagram):
#            pe = suite.IfBlockGE(datadef)
#        else:
#            # text diagram
#            pe = suite.FlowTE(datadef)
#        ib.presentation_element = pe
#        _scade_api.add(diagram, 'presentationElement', pe)
#
#    ApplyGraphicalPropSet(ib, pe, 'AddDataDefIfBlock', keywords)
#
#    LinkPendings()
#    SetModified(datadef)
#    return ib
#
#
## -----------------------------------------------------------------------------
## when blocks
#
#'''
# <diagram>: Diagram the block has to be linked to. This shall be either a diagram of <datadef>
#            or an empty diagram when <datadef> is for example the action of a transition.
# <when>: Expression tree that should resolve to
# <branches>: List of branches; each branch is made of an expression tree and a properties set
#             ({ [ <exp_tree> [ <br_props> ] ]+ })
# <wh_props>: Properties set of the block.
# 	* position (¤): Pair of integers defining the position of the block ({ <int> <int> })
# 	* size (¤): Pair of integers defining the size of the block ({ <int> <int> })
# 	* startPos (¤): Pair of integers defining the branch position ({ <int> <int> })
# 	* labelWidth (¤): Integer defining the width of the label containing expression
# <br_props>: Properties set of the branch.
# 	* startPos (¤): Pair of integers defining the branch position ({ <int> <int> })
# 	* labelWidth (¤): Integer defining the width of the label containing the pattern
# 	* position (¤): Pair of integers defining the position of the action ({ <int> <int> })
# 	* size (¤): Pair of integers defining the size of the action ({ <int> <int> })
# 	* display (¤): Layout of the action, EmbeddedGraphical, EmbeddedTextual or Split
#'''
#
#
# def AddDataDefWhenBlock(datadef, diagram, name, when, branches, **keywords):
#    _check_object(datadef, 'AddDataDefWhenBlock', 'datadef', suite.DataDef)
#    if diagram is not None:
#        _check_object(
#            diagram, 'AddDataDefWhenBlock', 'diagram', (suite.NetDiagram, suite.TextDiagram)
#        )
#
#    if not branches:
#        raise (
#            WhenBlockSyntaxError('AddDataDefWhenBlock', 'The block must have at least one branch')
#        )
#
#    wb = suite.WhenBlock(datadef)
#    wb.name = name
#    _scade_api.add(datadef, 'flow', wb)
#    wb.when = BuildExpressionTree(wb, when)
#
#    # graphical part
#    pe = None  # default
#    if diagram is not None:
#        if isinstance(diagram, suite.NetDiagram):
#            pe = suite.WhenBlockGE(datadef)
#        else:
#            # text diagram
#            pe = suite.FlowTE(datadef)
#        wb.presentation_element = pe
#        _scade_api.add(diagram, 'presentationElement', pe)
#
#    ApplyGraphicalPropSet(wb, pe, 'AddDataDefWhenBlock', keywords)
#
#    AddWhenBlockBranches(wb, branches)
#
#    LinkPendings()
#    SetModified(datadef)
#    return wb
#
#
# def AddWhenBlockBranches(when_block, branches):
#    _check_object(when_block, 'AddWhenBlockBranches', 'wb', suite.WhenBlock)
#
#    diagram = when_block.presentation_element.diagram if when_block.presentation_element else None
#
#    for branch in branches:
#        # each branch must be a tuple with 1 or 2 elements
#        if not isinstance(branch, tuple) and (len(branches) != 1 or len(branches) != 2):
#            raise (WhenBlockSyntaxError('AddWhenBlockBranches', 'Branch syntax error'))
#
#        when_branch = suite.WhenBranch(when_block)
#        _scade_api.add(when_block, 'whenBranch', when_branch)
#        when_branch.pattern = BuildExpressionTree(when_branch, branch[0])
#        when_branch.action = suite.Action(when_block)
#
#        # graphical part: a bit complex since two PE for one branch
#        args = branch[1] if len(branch) == 2 else {}
#        branch_props = {}
#        lw = args.pop('labelWidth', None)
#        if lw:
#            branch_props['labelWidth'] = lw
#        lw = args.pop('startPos', None)
#        if lw:
#            # not the same name
#            branch_props['position'] = lw
#        # remaining props for the action
#        action_props = args
#
#        peb = None  # default
#        pea = None  # default
#        if diagram is not None:
#            if isinstance(diagram, suite.NetDiagram):
#                peb = suite.WhenBranchGE(when_block)
#                pea = suite.ActionGE(when_block)
#            else:
#                # text diagram
#                peb = suite.FlowTE(when_block)
#                pea = suite.FlowTE(when_block)
#            when_branch.presentation_element = peb
#            when_branch.action.presentation_element = pea
#            _scade_api.add(diagram, 'presentationElement', peb)
#            _scade_api.add(diagram, 'presentationElement', pea)
#
#        ApplyGraphicalPropSet(when_branch, peb, 'AddDataDefWhenBlock', branch_props)
#        ApplyGraphicalPropSet(when_branch.action, pea, 'AddDataDefWhenBlock', action_props)
#
#
## -----------------------------------------------------------------------------
## Helpers
#
#
# class WhenBlockSyntaxError(Exception):
#    def __init__(self, context, message):
#        self.context = context
#        self.message = message
#
#    def __str__(self):
#        return '%s: %s' % (self.context, self.message)
#
#
#'''
# <if_tree> :: = { if <expr_tree> <then> <else> <if_props> }
# <then> ::= <action_props> | <if_tree>
# <else> ::= <action_prop> | <if_tree>
# <if_props>: Properties set of the decision node.
# 	* position (¤): Pair of integers defining the position of the node ({ <int> <int> })
# 	* labelWidth (¤): Integer defining the width of the label containing the condition
# <action_props>: Properties set of the action.
# 	* position (¤): Pair of integers defining the position of the action ({ <int> <int> })
# 	* size (¤): Pair of integers defining the size of the action ({ <int> <int> })
# 	* display (¤): Layout of the action, EmbeddedGraphical, EmbeddedTextual or Split
#'''
#
#
# def BuildIfTree(owner, diagram, tree):
#    _check_object(owner, 'BuildTransitionTree', 'node', (suite.IfBlock, suite.IfNode))
#
#    pe = None  # default
#    peclass = None  # either ActionGE, IfNodeGE or FlowTE
#    presentable = None  # either IfNode or Action instance
#    result = None  # IfBranch
#
#    if isinstance(tree, tuple) and len(tree) >= 1 and tree[0] == 'if':
#        if len(tree) != 5:
#            raise (TreeSyntaxError('BuildIfTree', "'if': Syntax error"))
#        # if tree
#        _, expression, then, else_, args = tree
#        node = suite.IfNode(owner)
#        node.expression = BuildExpressionTree(node, expression)
#        node.then = BuildIfTree(node, diagram, then)
#        node._else = BuildIfTree(node, diagram, else_)
#        peclass = suite.IfNodeGE
#        presentable = node
#        result = node
#    else:
#        # must be an action
#        args = tree
#        ia = suite.IfAction(owner)
#        ia.action = suite.Action(owner)
#        peclass = suite.ActionGE
#        presentable = ia.action
#        result = ia
#
#    # graphical part
#    if diagram:
#        if isinstance(diagram, suite.NetDiagram):
#            pe = peclass(diagram.data_def)
#        else:
#            # text diagram
#            pe = suite.FlowTE(diagram.data_def)
#        presentable.presentation_element = pe
#        _scade_api.add(diagram, 'presentationElement', pe)
#
#    ApplyGraphicalPropSet(presentable, pe, 'BuildIfTree', args)
#
#    return result
#
#
# def ApplyGraphicalPropSet(object, pe, context, props):
#    for name, value in props.items():
#        if object is None:
#            # try on the presentation element
#            try:
#                _scade_api.set(pe, name, value)
#            except:
#                # can't raise an error since calling function
#                # is successful and shall return a value
#                print('warning: ' + context + ': Illegal attribute ' + name + '\n')
#        else:
#            try:
#                _scade_api.set(object, name, value)
#            except:
#                # try on the presentation element
#                try:
#                    _scade_api.set(pe, name, value)
#                except:
#                    # can't raise an error since calling function
#                    # is successful and shall return a value
#                    print('warning: ' + context + ': Illegal attribute ' + name + '\n')
