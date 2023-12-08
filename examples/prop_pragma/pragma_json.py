# Copyright (C) 2023 ANSYS, Inc. and/or its affiliates.

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
