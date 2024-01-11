# Copyright (C) 2023 - 2024 ANSYS, Inc. and/or its affiliates.

"""
Example for ansys.scade.apitools.expr.NAryOp.

Project: ./ExprAccess.etp
"""

from scade import output
from scade.model.suite import get_roots as get_sessions

from ansys.scade.apitools.expr import NAryOp, accessor

# load the Scade model
model = get_sessions()[0].model
# retrieve the equation defining 'expression'
equation = model.get_object_from_path('Access::NAryOp/expression=')
# get an accessor for the equation's expression
ex = accessor(equation.right)
# check the type of the wrapped expression
assert isinstance(ex, NAryOp)
# dump the fields of the expression
output('kind: %s\n' % ex.code)
output('instance name: %s\n' % ex.name)
# the parameters are local variables, dump the name
output('parameters: [%s]\n' % ','.join([_.path.name for _ in ex.operands]))
