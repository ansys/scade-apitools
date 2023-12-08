# Copyright (C) 2023 ANSYS, Inc. and/or its affiliates.

"""
Example for ansys.scade.apitools.expr.Last.

Project: ./ExprAccess.etp
"""

from scade import output
from scade.model.suite import get_roots as get_sessions

from ansys.scade.apitools.expr import Last, accessor

# load the Scade model
model = get_sessions()[0].model
# retrieve the equation defining 'expression'
equation = model.get_object_from_path('Access::Last/expression=')
# get an accessor for the equation's expression
ex = accessor(equation.right)
# check the type of the wrapped expression
assert isinstance(ex, Last)
# dump the name of the local variable
output('name: %s\n' % ex.variable.name)
