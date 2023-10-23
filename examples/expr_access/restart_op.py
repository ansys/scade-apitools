"""
Example for ansys.scade.apitools.expr.RestartOp.

Project: ./ExprAccess.etp
"""

from scade import output
from scade.model.suite import get_roots as get_sessions

from ansys.scade.apitools.expr import RestartOp, accessor

# load the Scade model
model = get_sessions()[0].model
# retrieve the equation defining 'expression'
equation = model.get_object_from_path('Access::RestartOp/expression=')
# get an accessor for the equation's expression
ex = accessor(equation.right)
# check the type of the wrapped expression
assert isinstance(ex, RestartOp)
# dump the fields of the higher order expression
output('kind: %s\n' % ex.code)
output('instance name: %s\n' % ex.name)
# the condition is a local variable, dump the name
output('every: %s\n' % ex.every.path.name)
# dump the fields of the operator call
call = ex.operator
# dump the name of the operator
output('operator: %s\n' % call.operator.name)
# the parameters are local variables, dump the name
output('parameters: [%s]\n' % ','.join([_.path.name for _ in call.call_parameters]))
# the instance parameters are literals, dump the value
output('instance parameters: [%s]\n' % ','.join([_.value for _ in call.instance_parameters]))
