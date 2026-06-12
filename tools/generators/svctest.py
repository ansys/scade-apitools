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

"""Generation of consistency checks for SCADE Display properties."""

from typing import override

from sdytools import SdyService

from ansys.eseg.lbsjv.ecore.ecore import EClass
from ansys.eseg.lbsjv.vgl import IBlockStream


class ConsistencyCheckService(SdyService):
    """Access functions generation."""

    NAME = 'sdy_access_ut'

    def __init__(self):
        super().__init__(self.NAME, 'classes')

    @override
    def extend_files(self):  # numpydoc ignore=GL08
        # no default file is created: generated block expected to be present
        # in a user file
        pass

    @override
    def flush_block(
        self, ident: str, ext: str, data: object, bs: IBlockStream
    ):  # numpydoc ignore=GL08
        bs.begin_block()

        # generate schema
        bs.print('classes = {')
        for cls in sorted(self.model.all_classifiers, key=lambda c: c.name):
            if not isinstance(cls, EClass):
                continue
            props = []
            for prop in cls.sdy__properties:
                features = prop.e_type.sdy__flatten_features
                if not features:
                    print('ignoring prop', cls.name, prop.name)
                    continue
                many = prop.upper_bound == -1
                props.append(f"('{prop.sdy__attribute}', sdy.{prop.e_type.name}, {many})")
            if props:
                bs.print(f'    sdy.{cls.name}: [')
                for prop in props:
                    bs.print(f'        {prop},')
                bs.flush_user_block('class', '        ')
                bs.print('    ],')

        bs.flush_user_block('classes', '    ')
        bs.print('}')
        bs.end_block()

        if bs.new:
            bs.print()
            bs.print()
