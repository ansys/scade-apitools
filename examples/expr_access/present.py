# Copyright (C) 2023 ANSYS, Inc. and/or its affiliates.

"""
Example for ansys.scade.apitools.expr.Present.

Project: ./ExprAccess.etp
"""

from scade import output
from scade.model.suite import get_roots as get_sessions

from ansys.scade.apitools.expr import Present, accessor

# load the Scade model
model = get_sessions()[0].model
# retrieve the equation defining 'expression'
equation = model.get_object_from_path('Access::Present/expression=')
# get an accessor for the equation's expression
ex = accessor(equation.right)
# check the type of the wrapped expression
assert isinstance(ex, Present)
# dump the name of the signal
output('name: %s\n' % ex.signal.name)
