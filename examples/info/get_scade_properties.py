# Copyright (C) 2023 - 2024 ANSYS, Inc. and/or its affiliates.

"""
Example for ansys.scade.apitools.info.get_scade_properties.

Project: ./Info.etp
"""

from scade import output

from ansys.scade.apitools.info.install import get_scade_properties

for property, value in get_scade_properties().items():
    output('%s: %s\n' % (property, value))
