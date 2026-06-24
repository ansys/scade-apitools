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
Example for ansys.scade.apitools.prop.sdyaccess.

Project: ./Properties.etp
"""

from pathlib import Path

from scade.model.project.stdproject import get_roots as get_projects

import ansys.scade.apitools.prop.sdyaccess as display

# load the project
project = get_projects()[0]
project_dir = Path(project.pathname).parent

# load Circle.sgfx
path = project_dir / 'Circle.sgfx'
spec = display.load_sgfx(str(path))

# single layer with single object
circle = spec.layers[0].children[0]
assert isinstance(circle, display.Circle)

# print radius using standard API
print(f'circle.radius <{type(circle.radius).__name__} object>')
print('circle.radius.init', circle.radius.init)
# update and print radius using property accessor
circle.p_radius *= 2.0
print('circle.p_radius', circle.p_radius)
