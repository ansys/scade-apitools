"""
Example for ansys.scade.apitools.expr.PrjDynOp.

Project: ./ExprAccess.etp
"""

from scade import output
from scade.model.suite import get_roots as get_sessions

from ansys.scade.apitools.expr import PrjDynOp, accessor

# load the Scade model
model = get_sessions()[0].model
# retrieve the equation defining 'expression'
equation = model.get_object_from_path('Access::PrjDynOp/expression=')
# get an accessor for the equation's expression
ex = accessor(equation.right)
# check the type of the wrapped expression
assert isinstance(ex, PrjDynOp)
# dump the fields of the expression
output('kind: %s\n' % ex.code)
output('instance name: %s\n' % ex.name)
# the parameter is a local variable, dump the name
output('array: %s\n' % ex.array.path.name)
# the indexes or labels are literals, dump the value
output('indexes: [%s]\n' % ','.join([_.value for _ in ex.indexes]))
# default is a literal, dump the value
output('default: %s\n' % ex.default.value)
