# Copyright (C) 2023 ANSYS, Inc. and/or its affiliates.

"""
Example for ansys.scade.apitools.query.is_structure.

Project: ./QueryType.etp
"""

from scade import output
from scade.model.suite import get_roots as get_sessions

from ansys.scade.apitools.query import is_structure

# load the Scade model
model = get_sessions()[0].model
# retrieve the type Structure which resolves to a structure
structure = model.get_object_from_path('Types::Structure/')
# the result shall be True
output('%s is structure: %s\n' % (structure.name, is_structure(structure)))
# retrieve the type Speed which is scalar
speed = model.get_object_from_path('Types::Speed/')
# the result shall be False
output('%s is structure: %s\n' % (speed.name, is_structure(speed)))
