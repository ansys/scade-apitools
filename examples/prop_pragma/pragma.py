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
Example for the basic functions of ansys.scade.apitools.prop.pragma.

* find_pragma
* get_pragma_text
* remove_pragma
* set_pragma_text

Project: ./PropPragma.etp
"""

from scade import output
from scade.model.suite import get_roots as get_sessions

from ansys.scade.apitools.prop import find_pragma, get_pragma_text, remove_pragma, set_pragma_text

# load the Scade model
model = get_sessions()[0].model
# retrieve the sensor sandbox
sensor = model.get_object_from_path('P::sandbox/')
# create a pragma 'any' to initialize the test
set_pragma_text(sensor, 'any', 'some text')
# retrieve the pragma
pragma = find_pragma(sensor, 'any')
# its text shall be identical to the value returned by get_pragma_text
assert pragma.text == get_pragma_text(sensor, 'any')
output('pragma any for %s: %s\n' % (sensor.name, pragma.text))
for _ in range(2):
    found = remove_pragma(sensor, 'any')
    output('pragma any deleted for %s: %s\n' % (sensor.name, found))
