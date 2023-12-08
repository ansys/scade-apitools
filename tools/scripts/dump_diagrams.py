# Copyright (C) 2023 ANSYS, Inc. and/or its affiliates.
# SPDX-FileCopyrightText: 2021 ANSYS, Inc. All rights reserved.
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

"""Print the diagrams to png files into the documentation directory."""

from pathlib import Path

import scade
from scade.model.suite import get_roots as get_sessions
from scade.model.suite.visitors import Visit


class Diagrams(Visit):
    """Visit and print the net diagrams."""

    def __init__(self, dir: Path, suffix: str):
        """Store the parameters."""
        self.dir = dir
        self.suffix = suffix

    def visit_net_diagram(self, diagram, *args):
        """Print the diagram to a png file."""
        file = str(self.dir / ('%s%s' % (diagram.name, self.suffix)))
        scade.print(diagram, file, 'png')
        scade.output(file + '\n')


def dump_diagrams(dir: str = '', suffix: str = '.png'):
    """Print the project's diagrams to png files."""
    for session in get_sessions():
        model = session.model
        project = model.project
        if not dir:
            dir = Path(project.pathname).parent / 'diagrams'
            dir.mkdir(exist_ok='True')
        else:
            dir = Path(dir)
        Diagrams(dir, suffix).visit(model)
