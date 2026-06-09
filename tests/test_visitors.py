# Copyright (C) 2023 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
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
Test suite for visitors.

Test strategy:

* retrieve the model elements with the visitor and compare to a reference
"""

from pathlib import Path
from typing import List

import pytest
import scade.model.display as sdy

from ansys.scade.apitools.visitor import SdyVisitor
from tests.conftest import cmp_ref_text

res_dir = Path(__file__).parent / 'resources'
ref_dir = Path(__file__).parent / 'ref'


class HierarchyVisitor(SdyVisitor):
    def __init__(self):
        self.visits: List[str] = []

    def visit_graphic_object(self, graphic_object: sdy.GraphicObject, class_name, reference_name):
        e = graphic_object
        self.visits.append(
            f'{e.oid.oid} {e.name} {type(e).__name__} ({class_name}, {reference_name})'
        )
        return super().visit_graphic_object(graphic_object, class_name, reference_name)


sdy_visitor_data = [
    (res_dir / 'VisitDisplay' / 'Nominal.sgfx', 'VisitDisplayNominal.txt'),
]


@pytest.mark.parametrize(
    'path, ref',
    sdy_visitor_data,
    ids=[Path(_[0]).name for _ in sdy_visitor_data],
)
def test_sdy_visitor(path: Path, ref: str):
    spec = sdy.load_sgfx(str(path))
    v = HierarchyVisitor()
    v.visit(spec)
    text = '\n'.join(v.visits) + '\n'
    # debug
    # print(text)

    failure = cmp_ref_text(ref_dir / ref, text)
    assert not failure
