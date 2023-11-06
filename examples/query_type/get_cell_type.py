# Copyright (C) 2023 ANSYS, Inc. and/or its affiliates.

"""
Example for ansys.scade.apitools.query.get_cell_type.

Project: ./QueryType.etp
"""

from scade import output
from scade.model.suite import get_roots as get_sessions

from ansys.scade.apitools.query import get_cell_type

# load the Scade model
model = get_sessions()[0].model
# retrieve the type Matrix which is an array of Vector
matrix = model.get_object_from_path('Types::Matrix/')
# direct type of the array
cell_type = get_cell_type(matrix)
# the result shall be Vector
output('direct cell type: %s\n' % cell_type.name)
# leaf type of the array
cell_type = get_cell_type(matrix, True)
# the result shall be Real
output('leaf cell type: %s\n' % cell_type.name)
