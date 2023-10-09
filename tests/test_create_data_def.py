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
Test suite for create/data_def.py.

Test strategy:

The tests of this module operate make a copy of a reference project and add Scade
elements. The project is saved once all the tests of a class are executed.

The status of the tests cases is assessed by ensuring the functions execute properly and
by testing a few properties of the created data: This gives enough confidence for the
correctness of the execution. Indeed, it is not easy to compare the resulting model
to some expected result, nor easy to maintain.

Anyways, the result models can be exmined after the execution of the tests, for a deep analysis.
"""

import pytest

import ansys.scade.apitools.create as create

# import suite from declaration to ensure import order: models after apitools
# import scade.model.suite as suite
from ansys.scade.apitools.create.declaration import suite
from test_utils import get_resources_dir

# project considered for the tests
project_path = get_resources_dir() / 'resources' / 'CreateDataDef' / 'CreateDataDef.etp'


@pytest.mark.project(project_path)
class TestCreateDataDef:
    data_def_scope_data = [
        (['P::Scopes/', 'op']),
        (['P::Scopes/SM:State:', 'st']),
        (['P::Scopes/WB:true:', 'ac']),
    ]

    data_def_variables_data = [
        ([('localInt', 'int32'), ('localBool', 'bool')], False),
        ([('probe', 'float64')], True),
    ]

    @pytest.mark.parametrize(
        'scope, kind',
        data_def_scope_data,
        ids=[_[0] for _ in data_def_scope_data],
    )
    @pytest.mark.parametrize(
        'vars, probe',
        data_def_variables_data,
        ids=[_[0][0][0] for _ in data_def_variables_data],
    )
    def test_add_data_def_variables(self, tmp_project_session, scope, kind, vars, probe):
        # project/session must have been duplicated to a temporary directory
        project, session = tmp_project_session
        scope = session.model.get_object_from_path(scope)
        # same path for branches and actions
        if isinstance(scope, suite.WhenBranch):
            scope = scope.action
        vars = [('%s%s%s' % (kind, _[0][0].capitalize(), _[0][1:]), _[1]) for _ in vars]
        fct = create.add_data_def_probes if probe else create.add_data_def_locals
        result = fct(scope, vars)
        assert [(_.name, _.type.name) for _ in result] == [_ for _ in vars]
        for var, _ in vars:
            # the created variable must be accessible
            var_path = '%s%s/' % (scope.get_full_path(), var)
            assert session.model.get_object_from_path(var_path) is not None
        create.save_all()

    data_def_signals_data = [
        (['event']),
    ]

    @pytest.mark.parametrize(
        'scope, kind',
        data_def_scope_data,
        ids=[_[0] for _ in data_def_scope_data],
    )
    @pytest.mark.parametrize(
        'signals',
        data_def_signals_data,
        ids=[_[0][0] for _ in data_def_signals_data],
    )
    def test_add_data_def_signals(self, tmp_project_session, scope, kind, signals):
        # project/session must have been duplicated to a temporary directory
        project, session = tmp_project_session
        scope = session.model.get_object_from_path(scope)
        # same path for branches and actions
        if isinstance(scope, suite.WhenBranch):
            scope = scope.action
        signals = ['%s%s%s' % (kind, _[0].capitalize(), _[1:]) for _ in signals]
        result = create.add_data_def_signals(scope, signals)
        assert [_.name for _ in result] == [_ for _ in signals]
        for signal in signals:
            # the created signal must be accessible
            signal_path = '%s%s/' % (scope.get_full_path(), signal)
            assert session.model.get_object_from_path(signal_path) is not None
        create.save_all()

    variable_expression_data = [
        ('P::Scopes/expressions/', 'default', True, 'true'),
        ('P::Scopes/expressions/', 'last', 3.14, '3.14'),
        ('P::Scopes/expressions/', 'when', False, 'false'),
        ('P::Scopes/', 'default', False, TypeError),
    ]

    @pytest.mark.parametrize(
        'variable, kind, tree, expected',
        variable_expression_data,
        ids=['%s-%s' % (_[0], _[1]) for _ in variable_expression_data],
    )
    def test_set_variable_expression(self, tmp_project_session, variable, kind, tree, expected):
        # project/session must have been duplicated to a temporary directory
        project, session = tmp_project_session
        variable = session.model.get_object_from_path(variable)
        fct = {
            'default': create.set_variable_default,
            'last': create.set_variable_last,
            'when': create.data_def._set_variable_when,
        }[kind]
        if isinstance(expected, str):
            result = fct(variable, tree)
            value = {
                'default': variable.default,
                'last': variable.last,
                'when': variable.when,
            }[kind]
            assert value == result
            assert value.to_string() == expected
            create.save_all()
        else:
            with pytest.raises(expected):
                fct(variable, tree)

    data_def_diagram_data = [
        ('Text', False),
        ('Net', True),
    ]

    @pytest.mark.parametrize(
        'scope, kind',
        data_def_scope_data,
        ids=[_[0] for _ in data_def_scope_data],
    )
    @pytest.mark.parametrize(
        'name, graphical',
        data_def_diagram_data,
        ids=[_[0] for _ in data_def_diagram_data],
    )
    def test_add_data_def_diagram(self, tmp_project_session, scope, kind, name, graphical):
        # project/session must have been duplicated to a temporary directory
        project, session = tmp_project_session
        scope = session.model.get_object_from_path(scope)
        # same path for branches and actions
        if isinstance(scope, suite.WhenBranch):
            scope = scope.action
        name = '%s%s' % (kind.capitalize(), name)
        fct = create.add_data_def_net_diagram if graphical else create.add_data_def_text_diagram
        result = fct(scope, name)
        assert result in scope.diagrams
        assert result.name == name
        create.save_all()

    def test_add_data_def_graphical_equation(self, tmp_project_session):
        # project/session must have been duplicated to a temporary directory
        project, session = tmp_project_session
        model = session.model
        # hard-coded test: create the missing equation and connections
        # in P::DataFLows/SM1:ToBeCompleted:
        path = 'P::DataFlows/SM1:ToBeCompleted:'
        scope = model.get_object_from_path(path)
        # semantic part:
        # - retrieve the input variables
        # - retrieve the produced local variables
        # - build the expression
        lefts = [model.get_object_from_path('%s%s' % (path, _)) for _ in 'cond a b c d'.split()]
        cond, a, b, c, d = lefts
        l1, l2 = [model.get_object_from_path('%s%s' % (path, _)) for _ in 'l1 l2'.split()]
        tree = create.create_if(cond, [a, b], [c, d])
        # graphical part
        diagram = scope.presentation_element.diagram
        position = [13864, 4763]
        size = [1006, 979]
        equation = create.add_data_def_equation(scope, diagram, [l1, l2], tree, position, size)

        # input edges: the source equation is the unique one defining the variable
        for index, left in enumerate(lefts):
            src = left.definitions[0]
            create.add_diagram_edge(diagram, src, left, equation, index, points=[(0, 0), (0, 0)])

        # output edges
        for left, name in (l1, 'o1'), (l2, 'o2'):
            # equation defining name
            dst = model.get_object_from_path('%s%s=' % (path, name))
            # must replace the expression, _null in the test model
            dst.right.reference = left
            create.add_diagram_edge(diagram, equation, left, dst, 0)

        # compare the equations (semantics only)
        reference = model.get_object_from_path('P::DataFlows/SM1:Reference:l1=')
        assert equation.to_string() == reference.to_string()

        create.save_all()

    missing_edges_data = [
        ('P::Edges/', 'Nominal', 3),
    ]

    @pytest.mark.parametrize(
        'scope, name, expected',
        missing_edges_data,
        ids=[_[0] for _ in missing_edges_data],
    )
    def test_add_missing_edges(self, tmp_project_session, scope, name, expected):
        # project/session must have been duplicated to a temporary directory
        project, session = tmp_project_session
        model = session.model
        scope = model.get_object_from_path(scope)
        diagram = next((_ for _ in scope.diagrams if _.name == name))
        # replace the _null references with the following convention:
        # the name of the variable identifying the equation is <token>[_<local>]+
        # assuming the local variable is defined in the same scope
        replaced_exprs = set()
        for pe in diagram.presentation_elements:
            if not isinstance(pe, suite.EquationGE) or not pe.equation.lefts:
                continue
            equation = pe.equation
            left = equation.lefts[0]
            path = left.owner.get_full_path()
            locals = [
                model.get_object_from_path('%s%s' % (path, _)) for _ in left.name.split('_')[1:]
            ]
            index = 0
            for expr in equation.right.sub_expr_ids:
                if not expr.reference:
                    expr.reference = locals[index]
                    replaced_exprs.add(expr)
                    index += 1
        # perform the test
        edges = create.add_diagram_missing_edges(diagram)
        assert len(edges) == expected
        # restore reference to None for pins which have not beeb connected,
        # else the model is wrong
        connected_exprs = {_.right_expression for _ in edges}
        for expr in replaced_exprs - connected_exprs:
            expr.reference = None
        create.save_all()

    def test_add_data_def_textual_equation(self, tmp_project_session):
        # project/session must have been duplicated to a temporary directory
        project, session = tmp_project_session
        model = session.model
        # hard-coded test: create the equation textOut = textIn;
        path = 'P::DataFlows/'
        scope = model.get_object_from_path(path)
        diagram = next((_ for _ in scope.diagrams if _.name == 'TextDiagram'))
        # retrieve the variables
        o, i = [model.get_object_from_path('%stext%s' % (path, _)) for _ in 'Out In'.split()]
        # create the equation
        equation = create.add_data_def_equation(scope, diagram, [o], i)
        # minimal test
        assert equation.to_string() == 'textOut = textIn'
        # take the opportunity if this test case to create an assertion
        assertion = create.add_data_def_assertion(
            scope, diagram, 'GuaranteeTrue', True, kind=create.AK.GUARANTEE
        )
        assert assertion.to_string() == 'guarantee GuaranteeTrue : true'

        create.save_all()

    def test_add_data_def_embedded_equation(self, tmp_project_session):
        # project/session must have been duplicated to a temporary directory
        project, session = tmp_project_session
        model = session.model
        # hard-coded test: create the equation textOut = textIn;
        path = 'P::DataFlows/SM2:Textual:'
        scope = model.get_object_from_path(path)
        # retrieve the variables
        o, i = [model.get_object_from_path('%s%s/' % (path, _)) for _ in 'out in'.split()]
        # create the equation
        equation = create.add_data_def_equation(scope, None, [o], i)
        # minimal test
        assert equation.to_string() == 'out = in'
        # take the opportunity if this test case to create an assertion
        assertion = create.add_data_def_assertion(scope, None, 'AssumeFalse', False)
        assert assertion.to_string() == 'assume AssumeFalse : false'

        create.save_all()

    def test_add_data_def_misc_equation(self, tmp_project_session):
        # project/session must have been duplicated to a temporary directory
        project, session = tmp_project_session
        model = session.model
        # hard-coded test: create the following equations
        # <_L??> = 0;
        # _ = <_L??>
        path = 'P::DataFlows/'
        scope = model.get_object_from_path(path)
        diagram = next((_ for _ in scope.diagrams if _.name == 'Misc'))
        # source equation, with default values for textual expression
        position = [3201, 2355]
        size = [212, 317]
        src = create.add_data_def_equation(scope, diagram, ['bool'], True, position, size)
        left = src.lefts[0]
        assert left.is_internal()
        # minimal test
        assert src.to_string() == '%s = true' % left.name
        # target equation, with default values for terminator
        position = [7832, 2222]
        size = [503, 503]
        dst = create.add_data_def_equation(scope, diagram, '_', left, position, size)
        assert dst.terminator
        # minimal test
        assert dst.to_string() == '_ = %s' % left.name
        # create missing edges
        edges = create.add_diagram_missing_edges(diagram)
        assert len(edges) == 1
        # take the opportunity if this test case to create an assertion
        position = [1799, 3361]
        assertion = create.add_data_def_assertion(scope, diagram, 'A1', True, position=position)
        assert assertion.to_string() == 'assume A1 : true'

        create.save_all()

    data_def_state_machine_data = [
        ('P::StateMachines/', 'NetDiagram'),
        ('P::StateMachines/', 'TextDiagram'),
        ('P::StateMachines/SM:NoDiagram:', None),
    ]

    @pytest.mark.parametrize(
        'scope, name',
        data_def_state_machine_data,
        ids=['%s%s' % (_[0], _[1]) for _ in data_def_state_machine_data],
    )
    def test_data_def_state_machine(self, tmp_project_session, scope, name):
        # project/session must have been duplicated to a temporary directory
        project, session = tmp_project_session
        scope = session.model.get_object_from_path(scope)
        # same path for branches and actions
        if isinstance(scope, suite.WhenBranch):
            scope = scope.action
        diagram = next((_ for _ in scope.diagrams if _.name == name)) if name else None
        # hard coded SM with three states
        position = [500, 500]
        size = [15000, 5000]
        name = 'SM%s' % diagram.name.replace('Diagram', '') if diagram else 'SM'
        sm = create.add_data_def_state_machine(scope, name, diagram, position, size)
        # states
        positions = [[6000, 1000], [1000, 4000], [11000, 4000]]
        size = [4000, 1000]
        states = []
        for kind, display, position in zip(create.SK, create.DK, positions):
            state = create.add_state_machine_state(sm, kind.value, position, size, kind, display)
            states.append(state)
        # retrieve the create states
        normal, initial, final = states

        # create a transition from initial to final
        # let the tool compute default positions/size for the label
        # no help from the tool for the points, we must provide consistent positions
        points = [(5000, 4500), (6000, 4000), (10000, 5000), (11000, 4500)]
        tree = create.create_transition_state(True, final, False, 1, points, polyline=False)
        create.add_state_transition(initial, create.TK.STRONG, tree)

        # create a forked transition from normal to initial and final
        points = [(8000, 3000), (0, 0), (0, 0), (13000, 4000)]
        to_final = create.create_transition_state(True, final, True, 1, points)
        # no trigger: 'else' transition
        points = [(8000, 3000), (0, 0), (0, 0), (3000, 4000)]
        to_initial = create.create_transition_state(None, initial, True, 2, points)
        points = [(8000, 2000), (0, 0), (0, 0), (8000, 3000)]
        fork = create.create_transition_fork(False, [to_final, to_initial], 1, points)
        main = create.add_state_transition(normal, create.TK.WEAK, fork)
        # add an action to the main transition
        signal = session.model.get_object_from_path('P::StateMachines/signal/')
        # a scope shall be added to the transition
        create.add_transition_equation(main, [signal], None)
        # add another action to make sure another scope is not created
        create.add_transition_equation(main, ['_'], 0)

        # compare the semantics of the state machine with the reference
        reference = session.model.get_object_from_path('P::StateMachines/Reference:')
        assert reference.to_string().replace('Reference', name) == sm.to_string()

        create.save_all()

    data_def_when_block_data = [
        ('P::WhenBlocks/', 'NetDiagram'),
        ('P::WhenBlocks/', 'TextDiagram'),
        ('P::WhenBlocks/SM:NoDiagram:', None),
    ]

    @pytest.mark.parametrize(
        'scope, name',
        data_def_when_block_data,
        ids=['%s%s' % (_[0], _[1]) for _ in data_def_when_block_data],
    )
    def test_data_def_when_block(self, tmp_project_session, scope, name):
        # project/session must have been duplicated to a temporary directory
        project, session = tmp_project_session
        scope = session.model.get_object_from_path(scope)
        # same path for branches and actions
        if isinstance(scope, suite.WhenBranch):
            scope = scope.action
        diagram = next((_ for _ in scope.diagrams if _.name == name)) if name else None
        # hard coded WB with three actions
        # retrieve the variable used for the selector
        e = session.model.get_object_from_path('P::WhenBlocks/e/')
        # create the branches
        positions = [[2300, 2000], [7000, 3500], [2300, 4500]]
        size = [4000, 1000]
        branches = []
        for pattern, display, position in zip(e.type.type.values, create.DK, positions):
            branch = create.create_when_branch(pattern.name, position, size, display)
            branches.append(branch)
        # create the block with two branches
        name = 'WB%s' % diagram.name.replace('Diagram', '') if diagram else 'WB'
        block_position = [500, 500]
        block_size = [11000, 6000]
        block = create.add_data_def_when_block(
            scope, name, e, branches[:2], diagram, block_position, block_size
        )

        # add a third branch
        create.add_when_block_branches(block, branches[2:])

        # compare the semantics of the state machine with the reference
        reference = session.model.get_object_from_path('P::WhenBlocks/Reference:')
        assert reference.to_string().replace('Reference', name) == block.to_string()

        create.save_all()

    data_def_if_block_data = [
        ('P::IfBlocks/', 'NetDiagram'),
        ('P::IfBlocks/', 'TextDiagram'),
        ('P::IfBlocks/SM:NoDiagram:', None),
    ]

    @pytest.mark.parametrize(
        'scope, name',
        data_def_if_block_data,
        ids=['%s%s' % (_[0], _[1]) for _ in data_def_if_block_data],
    )
    def test_data_def_if_block(self, tmp_project_session, scope, name):
        # project/session must have been duplicated to a temporary directory
        project, session = tmp_project_session
        scope = session.model.get_object_from_path(scope)
        # same path for branches and actions
        if isinstance(scope, suite.WhenBranch):
            scope = scope.action
        diagram = next((_ for _ in scope.diagrams if _.name == name)) if name else None
        # hard coded IB with three nodes
        # retrieve the variables used for the selector
        a, b, c = [
            session.model.get_object_from_path('P::IfBlocks/%s/' % _) for _ in 'a b c'.split()
        ]
        # create the actions
        block_position = (500, 700)
        block_size = (14000, 6000)
        # default offsets of the SCADE editor
        start_position = (block_position[0] + 450, block_position[1] + 500)

        displays = list(create.DK) + [create.DK.SPLIT]
        positions = [(10000, block_position[1] + 500), (10000, 2800), (2500, 3900), (2500, 5400)]
        size = (4000, 1000)
        actions = []
        for display, position in zip(displays, positions):
            action = create.create_if_action(position, size, display)
            actions.append(action)
        b1, b2, c1, c2 = actions
        # create the nodes
        nb = create.create_if_tree(b, b1, b2, (5000, positions[0][1] + 80))
        nc = create.create_if_tree(c, c1, c2, (start_position[0], positions[2][1] + 80))
        na = create.create_if_tree(a, nb, nc, (start_position[0], positions[0][1] + 80))

        name = 'IB%s' % diagram.name.replace('Diagram', '') if diagram else 'IB'
        block = create.add_data_def_if_block(scope, name, na, diagram, block_position, block_size)

        # compare the semantics of the state machine with the reference
        reference = session.model.get_object_from_path('P::IfBlocks/Reference:')
        assert reference.to_string().replace('Reference', name) == block.to_string()

        create.save_all()

    diagram_equation_set_data = [
        ('P::EquationSets/', 'NetDiagram', 'a, b', ['a', 'b'], None),
        ('P::EquationSets/', 'TextDiagram', 'd', ['d'], TypeError),
        ('P::EquationSets/', 'NetDiagram', 'c', ['c'], ValueError),
        ('P::EquationSets/', 'NetDiagram', 'empty', [], None),
    ]

    @pytest.mark.parametrize(
        'scope, diagram, name, vars, exception',
        diagram_equation_set_data,
        ids=[_[2] for _ in diagram_equation_set_data],
    )
    def test_diagram_equation_set(
        self, tmp_project_session, scope, diagram, name, vars, exception
    ):
        # project/session must have been duplicated to a temporary directory
        project, session = tmp_project_session
        path = scope
        scope = session.model.get_object_from_path(scope)
        # same path for branches and actions
        if isinstance(scope, suite.WhenBranch):
            scope = scope.action
        diagram = next((_ for _ in scope.diagrams if _.name == diagram))
        # retrieve the variables and then their definition
        vars = [session.model.get_object_from_path('%s%s/' % (path, _)) for _ in vars]
        equations = [_.definitions[0] for _ in vars]
        if exception:
            with pytest.raises(exception):
                eqs = create.add_diagram_equation_set(diagram, name, equations)
        else:
            if equations:
                eqs = create.add_diagram_equation_set(diagram, name, equations)
            else:
                eqs = create.add_diagram_equation_set(diagram, name)
            # minimal verification
            for equation in equations:
                assert eqs in equation.equation_sets

        create.save_all()
