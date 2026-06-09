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

"""Generation of Python classes from ecore for scade display: enumerations."""

from typing import override

from sdytools import SdyService

from ansys.eseg.lbsjv.ecore.ecore import EEnum
from ansys.eseg.lbsjv.services import lower_name, upper_name
from ansys.eseg.lbsjv.vgl import IBlockStream


class EnumService(SdyService):
    """Enumerations generation."""

    NAME = 'sdy_enums'

    def __init__(self):
        super().__init__(self.NAME, 'types')

    @override
    def flush_block(
        self, ident: str, ext: str, data: object, bs: IBlockStream
    ):  # numpydoc ignore=GL08
        bs.begin_block()

        # data is None
        blanks = ''
        for type_ in self.model.e_classifiers:
            if not isinstance(type_, EEnum):
                continue
            bs.write(blanks)
            literals = type_.e_literals
            map = {
                'type': type_.name,
                'values': ', '.join([upper_name(literal.name) for literal in literals]),
                'count': len(literals),
            }
            code = 'class {type}(Enum):'
            bs.print(code.format_map(map))
            annotation = type_.get_e_annotation('http://www.eclipse.org/emf/2002/GenModel')
            doc = annotation.details.get('documentation', '') if annotation else ''
            self.flush_doc(doc, '    ', type_.name, bs)
            code = '    {values} = range({count})'
            bs.print(code.format_map(map))
            ub = 'init_' + lower_name(type_.name)
            bs.flush_user_block(ub, '        ', False)
            blanks = '\n\n'

        bs.end_block()

        if bs.new:
            bs.print()
            bs.print()
