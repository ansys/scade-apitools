# for debug purposes and quick tests
# (breakpoints can't be always hit with VS/pytest)

import ansys.scade.apitools.create as create
from ansys.scade.apitools.create.scade import suite
from conftest import load_session
from test_utils import get_resources_dir

if __name__ == '__main__':
    session = load_session(get_resources_dir() / 'resources' / 'EmptySession' / 'EmptySession.etp')
    try:
        operator = suite.Operator()
        operator.name = 'Op'
        modifier = create.create_map(1)
        tree = create.create_higher_order_call(operator, [], [modifier], [])
        # ex = tree._build_expression(session.model)
        ex = tree._build_expression(None)
        print(ex, ex.to_string())
    except BaseException as e:
        print(e)
