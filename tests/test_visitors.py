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
import scade.model.a661 as a661
import scade.model.display as sdy

from ansys.scade.apitools.info import get_scade_home
from ansys.scade.apitools.visitor import DFVisitor, SdyVisitor, StandardVisitor
from tests.conftest import cmp_ref_text

res_dir = Path(__file__).parent / 'resources'
ref_dir = Path(__file__).parent / 'ref'


class DisplayHierarchyVisitor(SdyVisitor):
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
    v = DisplayHierarchyVisitor()
    v.visit(spec)
    text = '\n'.join(v.visits) + '\n'
    # debug
    # print(text)

    failure = cmp_ref_text(ref_dir / ref, text)
    assert not failure


class WidgetVisitor(DFVisitor):
    def __init__(self):
        self.visits: List[str] = []

    def visit_a661_object_instance(self, a661_object_instance: a661.A661ObjectInstance, *args):
        self.visits.append(a661_object_instance.name)
        super().visit_a661_object_instance(a661_object_instance, *args)


df_visitor_data = [
    (res_dir / 'VisitDF' / 'Two.sgfx', 'VisitDFTwo.txt'),
]


@pytest.mark.parametrize(
    'path, ref',
    df_visitor_data,
    ids=[Path(_[0]).name for _ in df_visitor_data],
)
def test_df_visitor(path: Path, ref: str):
    std = a661.load_standard(
        str(get_scade_home() / 'SCADE A661' / 'server' / 'a661_description/a661.xml')
    )
    spec = a661.load_sgfx(str(path), std)
    v = WidgetVisitor()
    v.visit(spec)
    text = '\n'.join(v.visits) + '\n'
    # debug
    # print(text)

    failure = cmp_ref_text(ref_dir / ref, text)
    assert not failure


class StandardCounter(StandardVisitor):
    def __init__(self):
        self.count = 0

    def visit_a661_object(self, a661_object, *args):
        self.count += 1
        return super().visit_a661_object(a661_object, *args)


def test_std_visitor():
    std = a661.load_standard(
        str(get_scade_home() / 'SCADE A661' / 'server' / 'a661_description/a661.xml')
    )
    v = StandardCounter()
    # dry visit, verify there is no runtime error
    v.visit(std)
    # some feedback
    print(v.count)
    assert v.count > 0
