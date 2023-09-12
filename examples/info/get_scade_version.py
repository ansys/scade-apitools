"""
Example for ansys.scade.apitools.info.get_scade_version.

Project: ./Info.etp
"""

from scade import output

from ansys.scade.apitools.info import get_scade_version

output('SCADE version: %s\n' % get_scade_version())