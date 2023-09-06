"""
Example for ansys.scade.apitools.query.is_array.

Project: ./QueryType.etp
"""

from scade import output
from scade.model.suite import get_roots as get_sessions

from ansys.scade.apitools.query import is_array

# load the Scade model
model = get_sessions()[0].model
# retrieve the type Vector which resolves to an array
vector = model.get_object_from_path('Types::Vector/')
# the result shall be True
output('%s is array: %s\n' % (vector.name, is_array(vector)))
# retrieve the type Speed which is scalar
speed = model.get_object_from_path('Types::Speed/')
# the result shall be False
output('%s is array: %s\n' % (speed.name, is_array(speed)))
