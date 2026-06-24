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
Example for ansys.scade.apitools.visitor.SdyVisitor.

Project: ./TwoCounters.etp
"""

from pathlib import Path

import scade.model.display as display
from scade.model.project.stdproject import get_roots as get_projects

from ansys.scade.apitools.visitor import SdyVisitor


class ReferenceVisitor(SdyVisitor):
    """Gathers the pathnames of contained reference objects."""

    def __init__(self):
        # path of referenced objects
        self.references = set()

    def visit_reference_container(self, reference_container: display.ReferenceContainer, *args):
        """Register the path of the reference Object."""
        path = Path(reference_container.file.file).relative_to(project_dir)
        self.references.add(str(path))
        super().visit_reference_container(reference_container, *args)


# load the project
project = get_projects()[0]
project_dir = Path(project.pathname).parent

# retrieve the specifications files
files = [_ for _ in project.file_refs if Path(_.pathname).suffix == '.sgfx']

# create a visitor instance
v = ReferenceVisitor()

# visit the specifications
for file in files:
    # load the specification
    spec = display.load_sgfx(file.pathname)
    v.visit(spec)

# print references
print('\n'.join(sorted(v.references, key=lambda n: n.lower())))
