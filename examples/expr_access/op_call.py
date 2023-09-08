"""
Example for ansys.scade.apitools.expr.OpCall.

Project: ./ExprAccess.etp
"""

from scade import output
from scade.model.suite import get_roots as get_sessions

from ansys.scade.apitools.expr import OpCall, accessor

# load the Scade model
model = get_sessions()[0].model
# retrieve the equation defining 'expression'
equation = model.get_object_from_path('Access::OpCall/expression=')
# get an accessor for the equation's expression
ex = accessor(equation.right)
# check the type of the wrapped expression
assert isinstance(ex, OpCall)
# dump the fields of the expression
output('kind: %s\n' % ex.code)
output('instance name: %s\n' % ex.name)
# dump the name of the operator
output('operator: %s\n' % ex.operator.name)
# the parameters are local variables, dump the name
output('parameters: [%s]\n' % ','.join([_.path.name for _ in ex.call_parameters]))
# the instance parameters are literals, dump the value
output('instance parameters: [%s]\n' % ','.join([_.value for _ in ex.instance_parameters]))