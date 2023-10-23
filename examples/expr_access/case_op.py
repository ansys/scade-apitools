"""
Example for ansys.scade.apitools.expr.CaseOp.

Project: ./ExprAccess.etp
"""

from scade import output
from scade.model.suite import get_roots as get_sessions

from ansys.scade.apitools.expr import CaseOp, accessor

# load the Scade model
model = get_sessions()[0].model
# retrieve the equation defining 'expression'
equation = model.get_object_from_path('Access::CaseOp/expression=')
# get an accessor for the equation's expression
ex = accessor(equation.right)
# check the type of the wrapped expression
assert isinstance(ex, CaseOp)
# dump the fields of the expression
output('kind: %s\n' % ex.code)
output('instance name: %s\n' % ex.name)
# the selector is a local variable, dump the name
output('switch: %s\n' % ex.switch.path.name)
# the parameters are local variables, dump the pairs
output('cases: {%s}\n' % ','.join(['%s: %s' % (v, f.path.name) for v, f in ex.cases]))
# the default is a local variable, dump the name
output('default: %s\n' % ex.default.path.name)
