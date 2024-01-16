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
Example for the 'tool' functions of ansys.scade.apitools.prop.pragma.

* find_pragma_tool
* get_pragma_tool_text
* remove_pragma_tool
* set_pragma_tool_text

Project: ./PropPragma.etp
"""

from scade import output
from scade.model.suite import get_roots as get_sessions

from ansys.scade.apitools.prop import (
    find_pragma_tool,
    get_pragma_tool_text,
    remove_pragma_tool,
    set_pragma_tool_text,
)

# load the Scade model
model = get_sessions()[0].model
# retrieve the sensor sandbox
sensor = model.get_object_from_path('P::sandbox/')
# set the pragma 'kcg C:name'
set_pragma_tool_text(sensor, 'kcg', 'C:name', 'c_name')
# retrieve and delete the pragma name for the target languages C and Ada
for language in 'C', 'Ada':
    key = language + ':name'
    pragma = find_pragma_tool(sensor, 'kcg', key)
    output('pragma kcg %s found for %s: %s\n' % (key, sensor.name, pragma is not None))
    text = get_pragma_tool_text(sensor, 'kcg', key)
    output('pragma kcg %s for %s: %s\n' % (key, sensor.name, text))
    modified = set_pragma_tool_text(sensor, 'kcg', key, 'c_new_name')
    output('pragma kcg %s modified for %s: %s\n' % (key, sensor.name, modified))
    found = remove_pragma_tool(sensor, 'kcg', key)
    output('pragma kcg %s deleted for %s: %s\n' % (key, sensor.name, found))
