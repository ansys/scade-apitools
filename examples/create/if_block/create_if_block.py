"""
Example for creating a if block.

Usage::

    scade.exe -script <project> create_if_block.py

"""

import scade.model.suite as suite

import ansys.scade.apitools.create as create


def main():
    """Create a graphical state machine."""
    # assume one and only one loaded project
    model = suite.get_roots()[0].model
    # retrieve the operator P::O/
    operator = model.get_object_from_path('P::O/')
    # assume the operator has a graphical diagram
    diagram = operator.diagrams[0]

    # hard coded IB with three nodes
    # retrieve the variables used for the selector
    a, b, c = [model.get_object_from_path('P::O/%s/' % _) for _ in 'a b c'.split()]
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

    block = create.add_data_def_if_block(operator, 'IB', na, diagram, block_position, block_size)

    create.save_all()


if __name__ == "__main__":
    # launched from scade -script
    main()
