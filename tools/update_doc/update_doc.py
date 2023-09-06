# -*- coding: utf-8 -*-
# MIT License
#
# Copyright (c) 2021 ANSYS, Inc. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Copy the Python examples to the documentation directory.

Generate the intermediate lists: one per example project.
"""

__author__ = "Jean Henry"
__email__ = "scade-support@ansys.com"
__copyright__ = "Copyright 2023, ANSYS Inc."

import filecmp
from pathlib import Path
import shutil
import sys
from typing import List


def update_doc(root: Path) -> List[str]:
    """Return the list of new/updated rst files."""
    files = []

    target_dir = root / 'doc' / 'source' / '_examples'
    target_dir.mkdir(exist_ok=True)
    projects = sorted([_ for _ in root.glob('examples/*/*.etp')])
    for project in projects:
        # create the catalog
        dir = project.parent
        name = dir.name
        examples = sorted([_ for _ in dir.glob('*.py')])
        doc = (target_dir / name).with_suffix('.rst')
        tmp = doc.with_suffix('.rst.tmp')
        with tmp.open('w') as f:
            f.write('%s\n%s\n\n' % (name, '-' * len(name)))
            f.write("project: %s\n\n" % project.name)
            for example in examples:
                # copy the file to the documentation hierarchy
                shutil.copy(example, target_dir)

                # add an entry to the file
                entry = '\n'.join(
                    [
                        "",
                        ".. _ex__%s:" % example.stem,
                        "",
                        ".. raw:: html",
                        "",
                        "  <details>",
                        "  <summary><a>%s</a></summary>" % example.stem,
                        "",
                        ".. literalinclude :: /_examples/%s" % example.name,
                        "",
                        ".. raw:: html",
                        "",
                        "  </details>",
                        "",
                    ]
                )
                f.write(entry)
        if not doc.exists() or not filecmp.cmp(doc, tmp):
            shutil.copy(tmp, doc)
            files.append(str(doc))

    return files


if __name__ == '__main__':
    # dir must be the root of the repository
    dir = Path(sys.argv[1]) if len(sys.argv) == 2 else Path(__file__).parent.parent.parent
    update_doc(dir)
    sys.exit(0)
