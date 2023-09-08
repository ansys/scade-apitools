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
Generate the diagrams and outputs of the examples.

Walk through each example and update the content of doc/source/examples/<example>:

* Run all the scripts in the project's directory and store the standard output.
* Print all the diagrams as png files.

This script can be run independently or within a pre-commit handler.

The exit code is 0 if nothing is modified and if there are no obsolete file in
the documentation directory.
"""

import filecmp
import os
from pathlib import Path
import platform
from subprocess import CompletedProcess, run
import sys

# add <repo>/src to the path to access apitools
repo = Path(__file__).parent.parent.parent
sys.path.append(str(repo / 'src'))

if platform.system() == 'Windows':
    from ansys.scade.apitools.info import get_scade_home


def run_example(project: Path, script: Path) -> CompletedProcess:
    """Run the script on the project and retrieve stderr/stdout."""
    exe = get_scade_home() / 'SCADE' / 'bin' / 'scade.exe'

    cmd = [str(exe), '-script', script.as_posix(), project.as_posix()]
    cp = run(cmd, capture_output=True)
    return cp


def run_example(project: Path, script: Path) -> CompletedProcess:
    """
    Run the script on the project and retrieve stderr/stdout.

    Atlernative to the above command since, for some unknown reason,
    scade.exe fails to import ansys.scade.apitools in the context of tox.
    """
    cmd = [
        sys.executable,
        Path(__file__).with_name('run_example.py').as_posix(),
        project.as_posix(),
        script.as_posix(),
    ]
    cp = run(cmd, capture_output=True)
    if cp.stderr:
        print('failed to run', ' '.join(cmd))
        print(cp.stderr.decode())
    return cp


def update_file(context: str, tmp: Path, dst: Path) -> int:
    """
    Update the destination file with respect to the temporary one.

    Return 0 if no change occurs otherwise 1.
    """
    exit_code = 0
    if tmp.exists():
        if not dst.exists():
            print('%s: creating %s' % (context, dst.name))
            os.replace(tmp, dst)
            exit_code = 1
        elif not filecmp.cmp(dst, tmp):
            print('%s: updating %s' % (context, dst.name))
            os.replace(tmp, dst)
            exit_code = 1
        else:
            # nothing to update
            os.remove(tmp)
    else:
        if dst.exists():
            print('%s: removing %s' % (context, dst.name))
            os.remove(tmp)
            exit_code = 1

    return exit_code


def update_examples(root: Path) -> int:
    """
    Update the execution outputs and diagrams for the examples.

    Return 0 if no change occurs otherwise 1.
    """
    exit_code = 0

    exe = get_scade_home() / 'SCADE' / 'bin' / 'scade.exe'
    doc_dir = root / 'doc' / 'source' / 'examples'
    examples = sorted([_ for _ in root.glob('examples/*') if _.is_dir()])
    docs = {_.name: _ for _ in doc_dir.glob('*') if _.is_dir()}
    for example in examples:
        projects = [_ for _ in example.glob('*.etp')]
        if len(projects) != 1:
            print('skipping %s: no project' % example.name)
            continue
        scripts = sorted([_ for _ in example.glob('*.py')])
        if not scripts:
            print('skipping %s: no scripts' % example.name)
            continue
        project = projects[0]
        try:
            doc = docs.pop(example.name)
        except KeyError:
            print('%s: no doc directory' % example.name)
            exit_code = 1
            doc = doc_dir / example.name
            doc.mkdir(exist_ok=True)
        # make sure there is no trailing temporary file
        for tmp in doc.glob('*.tmp'):
            os.remove(tmp)
        old_txts = {_.stem for _ in doc.glob('output_*.txt')}
        txts = set()
        for script in scripts:
            tmp = doc / ('output_%s.tmp' % script.stem)
            txt = tmp.with_suffix('.txt')
            txts.add(txt.stem)

            # run the script on the current project and retrieve the output
            cp = run_example(project, script)
            if cp.stderr:
                # print('failed to run', ' '.join(cmd))
                # print(cp.stderr.decode())
                exit_code = 1
                continue
            if cp.stdout:
                with tmp.open('w') as f:
                    f.write(cp.stdout.decode())

            if update_file(example.name, tmp, txt):
                exit_code = 1

        # generate the diagrams
        old_pngs = {_.stem for _ in doc.glob('*.png')}
        pngs = set()
        script = Path(__file__).with_name('dump_diagrams.py')
        cmd = [
            str(exe),
            '-script',
            script.as_posix(),
            project.as_posix(),
            "dump_diagrams('%s', '.tmp')" % doc.as_posix(),
        ]
        cp = run(cmd, capture_output=True)
        if cp.stderr:
            print('failed to run', ' '.join(cmd))
            print(cp.stderr.decode())
            exit_code = 1
            continue
        for tmp in cp.stdout.decode().split('\n'):
            if not tmp:
                continue
            tmp = Path(tmp)
            pngs.add(tmp.stem)
            if update_file(example.name, tmp, tmp.with_suffix('.png')):
                exit_code = 1

        for txt in sorted(old_txts - txts):
            exit_code = 1
            print('%s/%s: no script' % (doc.name, txt))
        for png in sorted(old_pngs - pngs):
            exit_code = 1
            print('%s/%s: no diagram' % (doc.name, png))

    return exit_code


if __name__ == '__main__':
    # can be run only on Windows
    if platform.system() == 'Windows':
        sys.exit(update_examples(repo))
    else:
        # nothing to do
        sys.exit(0)
