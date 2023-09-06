# this extension triggers the script tools/update_doc/update_doc.py
# to copy the examples to the documentation directory

from pathlib import Path
import sys

# repository's root directory
# __file__ is <root>/doc/source/_ext/ex.py
root_dir = Path(__file__).parent.parent.parent.parent

# add tools/update_doc to the path
sys.path.append(str(root_dir / 'tools' / 'update_doc'))
from update_doc import update_doc


def process_examples(app, env, added, changed, removed):
    """
    Call update_doc.

    * Copy the scripts from examples/* to _examples
    * Create or update a rst file to include all the examples associated to a project

    Return the list of new/updated rst files
    """
    files = update_doc(root_dir)
    with open('c:/temp/ex.log', 'w') as f:
        f.write('\n'.join(files) + '\n')
    return []


def setup(app):
    """Initialize the extension."""
    # can not create documents in the following event handler
    # app.connect('env-get-outdated', process_examples)
    # lets do it at startup for now
    update_doc(root_dir)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
