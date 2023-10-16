"""
Example for ansys.scade.apitools.expr.InitOp.

Project: ./ExprAccess.etp
"""

from scade import output
from scade.model.suite import get_roots as get_sessions

from ansys.scade.apitools.expr import InitOp, accessor

# load the Scade model
model = get_sessions()[0].model
# retrieve the equation defining 'expression'
equation = model.get_object_from_path('Access::InitOp/expression=')
# get an accessor for the equation's expression
ex = accessor(equation.right)
# check the type of the wrapped expression
assert isinstance(ex, InitOp)
# dump the fields of the expression
output('kind: %s\n' % ex.code)
output('instance name: %s\n' % ex.name)
# the parameters are local variables, dump the name
output('flows: [%s]\n' % ','.join([_.path.name for _ in ex.flows]))
# the initial values are literals, dump the value
output('init values: [%s]\n' % ','.join([_.value for _ in ex.inits]))
