"""
Example for ansys.scade.apitools.expr.IteratorOp.

Project: ./ExprAccess.etp
"""

from scade import output
from scade.model.suite import get_roots as get_sessions

from ansys.scade.apitools.expr import IteratorOp, accessor

# load the Scade model
model = get_sessions()[0].model
# retrieve the equation defining 'expression'
equation = model.get_object_from_path('Access::IteratorOp/expression=')
# get an accessor for the equation's expression
ex = accessor(equation.right)
# check the type of the wrapped expression
assert isinstance(ex, IteratorOp)
# dump the fields of the higher order expression
output('kind: %s\n' % ex.code)
output('instance name: %s\n' % ex.name)
# the size is a literal, dump the value
output('size: %s\n' % ex.size.value)
# the count is a literal, dump the value
output('accumulator count: %s\n' % ex.accumulator_count.value)
# dump the fields of the operator call
call = ex.operator
# dump the name of the operator
output('operator: %s\n' % call.operator.name)
# the parameters are local variables, dump the name
output('parameters: [%s]\n' % ','.join([_.path.name for _ in call.call_parameters]))
# the instance parameters are literals, dump the value
output('instance parameters: [%s]\n' % ','.join([_.value for _ in call.instance_parameters]))
