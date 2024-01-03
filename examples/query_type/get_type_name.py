# Copyright (C) 2023 - 2024 ANSYS, Inc. and/or its affiliates.

"""
Example for ansys.scade.apitools.query.get_type_name.

Project: ./QueryType.etp
"""

from scade import output
from scade.model.suite import get_roots as get_sessions

from ansys.scade.apitools.query import get_type_name

# load the Scade model
model = get_sessions()[0].model
# retrieve the named type Vector
vector = model.get_object_from_path('Types::Vector/')
# the result shall be Vector
output('name: %s\n' % get_type_name(vector))
# the type of vector is an array, its name shall be its definition
array = vector.type
output('definition: %s\n' % get_type_name(array))
# <null> for None
output('name: %s\n' % get_type_name(None))
