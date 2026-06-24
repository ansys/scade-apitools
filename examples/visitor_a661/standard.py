# Copyright (C) 2023 - 2026 ANSYS, Inc. and/or its affiliates.
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
Example for ansys.scade.apitools.visitor.StandardVisitor.

Project: ./TwoDF.etp
"""

import scade.model.a661 as a661
from scade.model.project.stdproject import get_roots as get_projects

from ansys.scade.apitools.visitor import StandardVisitor


class Metrics(StandardVisitor):
    """Some metrics on the ARINC 661 configuration file."""

    def __init__(self):
        # widgets + extension widgets
        self.widgets = 0
        # symbol commands
        self.commands = 0

    def visit_a661_widget(self, a661_widget: a661.A661Widget, *args):
        """Increment the counter."""
        self.widgets += 1
        super().visit_a661_widget(a661_widget, *args)

    def visit_symbol_command(self, symbol_command: a661.SymbolCommand, *args):
        """Increment the counter."""
        self.commands += 1
        super().visit_symbol_command(symbol_command, *args)


# load the project
project = get_projects()[0]

# load the A661 standard
conf = next(
    _
    for _ in project.file_refs
    if _.get_scalar_tool_prop_def('SDY', 'FILETYPE', '', None) == 'a661standardConf'
)
std = a661.load_standard(conf.pathname)

# compute some metrics
v = Metrics()
v.visit(std)
# print the results
print('wigets:', v.widgets)
print('commands:', v.commands)
