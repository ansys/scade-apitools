"""
Example for ansys.scade.apitools.query.is_imported.

Project: ./QueryType.etp
"""

from scade import output
from scade.model.suite import get_roots as get_sessions

from ansys.scade.apitools.query import is_imported

# load the Scade model
model = get_sessions()[0].model
# retrieve the type Imported which is imported
imported = model.get_object_from_path('Types::Imported/')
# the result shall be True
output('%s is imported: %s\n' % (imported.name, is_imported(imported)))
# retrieve the type Speed which resolves to float32
speed = model.get_object_from_path('Types::Speed/')
# the result shall be False
output('%s is imported: %s\n' % (speed.name, is_imported(speed)))
