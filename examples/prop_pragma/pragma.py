# Copyright (C) 2023 - 2024 ANSYS, Inc. and/or its affiliates.

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
