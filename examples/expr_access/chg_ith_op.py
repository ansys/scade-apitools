# Copyright (C) 2023 ANSYS, Inc. and/or its affiliates.

"""
Example for ansys.scade.apitools.expr.ChgIthOp.

Project: ./ExprAccess.etp
"""

from scade import output
from scade.model.suite import get_roots as get_sessions

from ansys.scade.apitools.expr import ChgIthOp, accessor

# load the Scade model
model = get_sessions()[0].model
# retrieve the equation defining 'expression'
equation = model.get_object_from_path('Access::ChgIthOp/expression=')
# get an accessor for the equation's expression
ex = accessor(equation.right)
# check the type of the wrapped expression
assert isinstance(ex, ChgIthOp)
# dump the fields of the expression
output('kind: %s\n' % ex.code)
output('instance name: %s\n' % ex.name)
# the parameter is a local variable, dump the name
output('flow: %s\n' % ex.flow.path.name)
# the parameter is a local variable, dump the name
output('value: %s\n' % ex.value.path.name)
# the indexes or labels are literals, dump the value
output('with: [%s]\n' % ','.join([_.value for _ in ex.with_]))
