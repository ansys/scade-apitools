# for debug purposes and quick tests
# (breakpoints can't be always hit with VS/pytest)

import ansys.scade.apitools.create as create
from conftest import load_session
from test_utils import get_resources_dir

if __name__ == '__main__':
    session = load_session(get_resources_dir() / 'resources' / 'EmptySession' / 'EmptySession.etp')
    try:
        tree = create.create_case(True, [("'A'", 65)])
        ex = create._build_expression_tree(None, tree)
        print(ex)
    except create.EmptyTreeError:
        print('got it')
