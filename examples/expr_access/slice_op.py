# Copyright (C) 2023 ANSYS, Inc. and/or its affiliates.

"""
Example for ansys.scade.apitools.expr.SliceOp.

Project: ./ExprAccess.etp
"""

from scade import output
from scade.model.suite import get_roots as get_sessions

from ansys.scade.apitools.expr import SliceOp, accessor

# load the Scade model
model = get_sessions()[0].model
# retrieve the equation defining 'expression'
equation = model.get_object_from_path('Access::SliceOp/expression=')
# get an accessor for the equation's expression
ex = accessor(equation.right)
# check the type of the wrapped expression
assert isinstance(ex, SliceOp)
# dump the fields of the expression
output('kind: %s\n' % ex.code)
output('instance name: %s\n' % ex.name)
# the parameters is a local variable, dump the name
output('array: %s\n' % ex.array.path.name)
# from is a literal, dump the value
output('from index: %s\n' % ex.from_index.value)
# to is a literal, dump the value
output('to index: %s\n' % ex.to_index.value)
