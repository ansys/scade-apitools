# Copyright (C) 2023 ANSYS, Inc. and/or its affiliates.

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
