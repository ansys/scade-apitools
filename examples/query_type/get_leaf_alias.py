"""
Example for ansys.scade.apitools.query.get_leaf_alias.

Project: ./QueryType.etp
"""

from scade import output
from scade.model.suite import get_roots as get_sessions

from ansys.scade.apitools.query import get_leaf_alias

# load the Scade model
model = get_sessions()[0].model
# retrieve the type Speed which is an alias for Real
speed = model.get_object_from_path('Types::Speed/')
leaf_alias = get_leaf_alias(speed)
# the result shall be float32
output('leaf alias: %s\n' % leaf_alias.name)
