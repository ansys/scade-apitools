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

"""Generation of accessors for SCADE Display properties."""

from typing import override

from sdytools import SdyService

from ansys.eseg.lbsjv.ecore.ecore import EClass, EReference
from ansys.eseg.lbsjv.services import lower_name
from ansys.eseg.lbsjv.vgl import IBlockStream


class AccessFunctionsService(SdyService):
    """Access functions generation."""

    NAME = 'sdy_access_fct'

    def __init__(self):
        super().__init__(self.NAME, 'classes')

    @override
    def extend_files(self):  # numpydoc ignore=GL08
        assert self.manager is not None  # nosec B101  # addresses linter
        path = self.manager.target_dir / 'prop' / f'{self.model_name}access.py'
        self.manager.add_file(path)
        self.files[path] = None
        # self.filename = path

    @override
    def flush_block(
        self, ident: str, ext: str, data: object, bs: IBlockStream
    ):  # numpydoc ignore=GL08
        bs.begin_block()

        # data is None
        self.flush_functions(bs)

        bs.end_block()

        if bs.new:
            bs.print()
            bs.print()

    def flush_functions(self, bs: IBlockStream):
        """Generate access functions."""
        # opposite composition roles not available in ecore
        #   -> pass to determine if a property is used as scalar and/or list
        many = {}
        scalar = {}

        for cls in self.model.all_classifiers:
            if not isinstance(cls, EClass):
                continue
            property: EReference
            for property in cls.sdy__properties:
                if property.upper_bound == -1:
                    many[property.e_type] = True
                else:
                    scalar[property.e_type] = True

        for cls in self.model.all_classifiers:
            if not isinstance(cls, EClass):
                continue
            comment_flushed = False
            cls_lower_name = lower_name(cls.name)

            if cls.sdy__is_property:
                features = cls.sdy__flatten_features
                if len(features) == 0:
                    continue

                var = 'property'
                map = {
                    'class': cls.name,
                    'lower': cls_lower_name,
                    'var': var,
                    'type_name': cls.sdy__prop_typing_name,
                }
                if cls in many:
                    if not comment_flushed:
                        bs.print()
                        bs.print(f'# {cls.name}')
                        comment_flushed = True

                    map['value'] = 'values'
                    map['props'] = ', '.join(
                        ['self.{0}'.format(feature.sdy__accessor) for feature in features]
                    )
                    map['gprops'] = ', '.join(
                        [var + '.' + feature.sdy__accessor for feature in features]
                    )
                    map['sprops'] = ', '.join([feature.sdy__ident for feature in features])
                    code = (
                        'def _new_{lower}({value}: {type_name}) -> {class}:\n'
                        '    self = {class}()\n'
                        '    {props} = {value}\n'
                        '    return self\n'
                        '\n'
                        '\n'
                        'def _get_list_{lower}(self, attribute: str) -> List[{type_name}]:\n'
                        '    return [({gprops}) for {var} in self.__dict__[attribute]]\n'
                        '\n'
                        '\n'
                        'def _set_list_{lower}(self, attribute: str, {value}: List[{type_name}]):\n'
                        '    self.__dict__[attribute] = [_new_{lower}(({sprops})) for {sprops} in {value}]\n'
                    )
                    bs.print(code.format_map(map))
                if cls in scalar:
                    if not comment_flushed:
                        bs.print()
                        bs.print(f'# {cls.name}')
                        comment_flushed = True

                    map['value'] = 'value'
                    props = ', '.join([f'{var}.{feature.sdy__accessor}' for feature in features])
                    dprops = cls.sdy__prop_default_value
                    if len(features) > 1:
                        map['dprops'] = '(' + dprops + ')'
                        map['props'] = '(' + props + ')'
                    else:
                        map['dprops'] = dprops
                        map['props'] = props
                    code = (
                        'def _get_{lower}(self, attribute: str) -> {type_name}:\n'
                        '    {var} = self.__dict__[attribute]\n'
                        '    return {props} if {var} is not None else {dprops}\n'
                        '\n'
                        '\n'
                        'def _set_{lower}(self, attribute: str, {value}: {type_name}):\n'
                        '    if self.__dict__[attribute] is None:\n'
                        '        self.__dict__[attribute] = {class}()\n'
                        '    {var} = self.__dict__[attribute]\n'
                        '    {props} = {value}\n'
                    )
                    bs.print(code.format_map(map))


class AccessDeclarationsService(SdyService):
    """Declarations generation."""

    NAME = 'sdy_access_dcl'

    def __init__(self):
        super().__init__(self.NAME, 'classes')

    # redefine Sdy.ExtendFiles
    @override
    def extend_files(self):  # numpydoc ignore=GL08
        assert self.manager is not None  # nosec B101  # addresses linter
        path = self.manager.target_dir / 'prop' / f'{self.model_name}access.py'
        self.manager.add_file(path)
        self.files[path] = None
        # self.filename = filename

    @override
    def flush_block(
        self, ident: str, ext: str, data: object, bs: IBlockStream
    ):  # numpydoc ignore=GL08
        bs.begin_block()

        # data is None
        self.flush_declarations(bs)

        bs.end_block()

        if bs.new:
            bs.print()
            bs.print()

    def flush_declarations(self, bs: IBlockStream):
        """Generate declarations."""
        for cls in self.model.all_classifiers:
            if not isinstance(cls, EClass):
                continue
            comment_flushed = False

            empty = True
            property: EReference
            for property in cls.sdy__properties:
                type = property.e_type
                features = type.sdy__flatten_features
                if len(features) == 0:
                    continue

                if not comment_flushed:
                    bs.print()
                    bs.print(f'# {cls.name}')
                    comment_flushed = True

                map = {
                    'class': cls.name,
                    'lower': lower_name(type.name),
                    'attribute': property.sdy__attribute,
                    'accessor': property.sdy__accessor,
                    'prefix': 'list_' if property.upper_bound == -1 else '',
                }
                code = "{class}.{accessor} = _Property('{attribute}', _get_{prefix}{lower}, _set_{prefix}{lower})"
                bs.print(code.format_map(map))
                empty = False

            if not empty:
                bs.print()
