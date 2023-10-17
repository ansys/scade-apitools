"""
Example for creating a state machine.

Usage::

    scade.exe -script <project> create_state_machine.py

"""

import scade.model.suite as suite

import ansys.scade.apitools.create as create


def main():
    """Create a graphical state machine."""
    # assume one and only one loaded project
    model = suite.get_roots()[0].model
    # add a state machine to the first operator found, assuming there is at least one
    operator = model.sub_operators[0]
    # assume the operator has a graphical diagram
    diagram = operator.diagrams[0]
    # hard coded SM with three states
    position = [500, 500]
    size = [15000, 5000]
    sm = create.add_data_def_state_machine(operator, 'SM', diagram, position, size)
    # states
    positions = [[6000, 1000], [1000, 4000], [11000, 4000]]
    size = [4000, 1000]
    states = []
    for kind, display, position in zip(create.SK, create.DK, positions):
        state = create.add_state_machine_state(sm, kind.value, position, size, kind, display)
        states.append(state)
    # retrieve the created states
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
    # create a signal and add an action to emit it
    signal = create.add_data_def_signals(operator, ['signal'])[0]
    create.add_transition_equation(main, [signal], None)

    create.save_all()


if __name__ == "__main__":
    # launched from scade -script
    main()
