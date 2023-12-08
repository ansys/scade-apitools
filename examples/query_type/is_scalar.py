# Copyright (C) 2023 ANSYS, Inc. and/or its affiliates.

"""
Example for ansys.scade.apitools.query.is_scalar.

Project: ./QueryType.etp
"""

from scade import output
from scade.model.suite import get_roots as get_sessions

from ansys.scade.apitools.query import is_scalar

# load the Scade model
model = get_sessions()[0].model
# retrieve the type Speed which resolves to float32
speed = model.get_object_from_path('Types::Speed/')
# the result shall be True
output('%s is scalar: %s\n' % (speed.name, is_scalar(speed)))
# retrieve the type Vector which is an array of float32
vector = model.get_object_from_path('Types::Vector/')
# the result shall be False
output('%s is scalar: %s\n' % (vector.name, is_scalar(vector)))
# retrieve the type ImportedScalar which is tagged as scalar for C
imported = model.get_object_from_path('Types::ImportedScalar/')
# the result shall be True
output('%s is scalar: %s\n' % (imported.name, is_scalar(imported, 'C')))
