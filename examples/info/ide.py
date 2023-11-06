# Copyright (C) 2023 ANSYS, Inc. and/or its affiliates.

"""
Example for ansys.scade.apitools.info.ide.

Project: ./Info.etp
"""

from scade import output

from ansys.scade.apitools.info import ide

output('Running in SCADE IDE: %s\n' % ide)
