# Copyright (C) 2023 - 2024 ANSYS, Inc. and/or its affiliates.
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
