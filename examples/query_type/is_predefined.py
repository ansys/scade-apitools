# Copyright (C) 2023 - 2024 ANSYS, Inc. and/or its affiliates.

"""
Example for ansys.scade.apitools.query.is_predefined.

Project: ./QueryType.etp
"""

from scade import output
from scade.model.suite import get_roots as get_sessions

from ansys.scade.apitools.query import is_predefined

# load the Scade model
model = get_sessions()[0].model
# retrieve the type Speed which resolves to float32
speed = model.get_object_from_path('Types::Speed/')
# the result shall be TRue
output('%s is predefined: %s\n' % (speed.name, is_predefined(speed)))
# retrieve the type Vector which is an array
vector = model.get_object_from_path('Types::Vector/')
# the result shall be False
output('%s is predefined: %s\n' % (vector.name, is_predefined(vector)))
