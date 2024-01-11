# Copyright (C) 2023 - 2024 ANSYS, Inc. and/or its affiliates.

"""
Example for ansys.scade.apitools.info.get_scade_home.

Project: ./Info.etp
"""

from scade import output

from ansys.scade.apitools.info import get_scade_home

output('SCADE installation directory: %s\n' % get_scade_home())
