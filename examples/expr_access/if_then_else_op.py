# Copyright (C) 2023 - 2024 ANSYS, Inc. and/or its affiliates.

"""
Example for ansys.scade.apitools.expr.IfThenElseOp.

Project: ./ExprAccess.etp
"""

from scade import output
from scade.model.suite import get_roots as get_sessions

from ansys.scade.apitools.expr import IfThenElseOp, accessor

# load the Scade model
model = get_sessions()[0].model
# retrieve the equation defining 'expression'
equation = model.get_object_from_path('Access::IfThenElseOp/expression=')
# get an accessor for the equation's expression
ex = accessor(equation.right)
# check the type of the wrapped expression
assert isinstance(ex, IfThenElseOp)
# dump the fields of the expression
output('kind: %s\n' % ex.code)
output('instance name: %s\n' % ex.name)
# the 'if' flow is a local variable, dump the name
output('condition: %s\n' % ex.if_.path.name)
# the 'then' flows are local variables, dump the name
output('then: [%s]\n' % ','.join([_.path.name for _ in ex.then]))
# the 'else' flows are local variables, dump the name
output('else: [%s]\n' % ','.join([_.path.name for _ in ex.else_]))
