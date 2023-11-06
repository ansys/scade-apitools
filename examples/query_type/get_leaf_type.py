# Copyright (C) 2023 ANSYS, Inc. and/or its affiliates.

"""
Example for ansys.scade.apitools.query.get_leaf_type.

Project: ./QueryType.etp
"""

from scade import output
from scade.model.suite import get_roots as get_sessions

from ansys.scade.apitools.query import get_leaf_type

# load the Scade model
model = get_sessions()[0].model
# retrieve the type Speed which resolves to float32
speed = model.get_object_from_path('Types::Speed/')
leaf_type = get_leaf_type(speed)
# the result shall be float32
output('leaf type: %s\n' % leaf_type.name)
# retrieve the type Vector which resolves to an array
vector = model.get_object_from_path('Types::Vector/')
leaf_type = get_leaf_type(vector)
# the result shall be an instance of Table
output('leaf type: %s\n' % type(leaf_type))
