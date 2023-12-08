# Copyright (C) 2023 ANSYS, Inc. and/or its affiliates.

"""
Example for ansys.scade.apitools.query.is_enum.

Project: ./QueryType.etp
"""

from scade import output
from scade.model.suite import get_roots as get_sessions

from ansys.scade.apitools.query import is_enum

# load the Scade model
model = get_sessions()[0].model
# retrieve the type Vector which resolves to an enumeration
color = model.get_object_from_path('Types::Color/')
# the result shall be True
output('%s is enum: %s\n' % (color.name, is_enum(color)))
# retrieve the type Speed which is scalar
speed = model.get_object_from_path('Types::Speed/')
# the result shall be False
output('%s is enum: %s\n' % (speed.name, is_enum(speed)))
