# Copyright (C) 2023 - 2024 ANSYS, Inc. and/or its affiliates.

"""
Example for creating a when block.

Usage::

    scade.exe -script <project> create_when_block.py

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
    # retrieve the variable used for the selector
    e = model.get_object_from_path('P::O/e/')

    # hard coded WB with three actions
    positions = [(2300, 2000), (7000, 3500), (2300, 4500)]
    size = [4000, 1000]
    branches = []
    for pattern, position in zip(e.type.type.values, positions):
        branch = create.create_when_branch(pattern.name, position, size)
        branches.append(branch)
    # create the block with two branches
    block = create.add_data_def_when_block(
        operator, 'WB', e, branches[:2], diagram, (500, 500), (11000, 6000)
    )

    # add the third branch
    create.add_when_block_branches(block, branches[2:])

    create.save_all()


if __name__ == "__main__":
    # launched from scade -script
    main()
