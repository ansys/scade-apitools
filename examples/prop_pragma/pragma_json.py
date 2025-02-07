# Copyright (C) 2023 - 2025 ANSYS, Inc. and/or its affiliates.
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
Example for the 'json' functions of ansys.scade.apitools.prop.pragma.

* get_pragma_json
* set_pragma_json

Project: ./PropPragma.etp
"""

from scade import output
from scade.model.suite import get_roots as get_sessions

from ansys.scade.apitools.prop import (
    find_pragma,
    get_pragma_json,
    get_pragma_text,
    set_pragma_json,
)

# load the Scade model
model = get_sessions()[0].model
# retrieve the sensor sandbox
sensor = model.get_object_from_path('P::sandbox/')
# create a pragma 'any' using json serialization
set_pragma_json(sensor, 'any', {'bool': True, 'text': 'some text'})
# check the serialization
text = get_pragma_text(sensor, 'any')
output('pragma any for %s: %s\n' % (sensor.name, text))
# retrieve the value as a Python object
value = get_pragma_json(sensor, 'any')
output('pragma any for %s: %s\n' % (sensor.name, value))
# remove the pragma
set_pragma_json(sensor, 'any', {})
assert not find_pragma(sensor, 'any')
