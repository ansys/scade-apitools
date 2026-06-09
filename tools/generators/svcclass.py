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

"""Generation of Python classes from ecore for scade display: classes."""

from typing import override

from sdytools import SdyService

from ansys.eseg.lbsjv.ecore.ecore import EClass, EReference
from ansys.eseg.lbsjv.services import lower_name, title_name
from ansys.eseg.lbsjv.vgl import IBlockStream


class ClassService(SdyService):
    """Classes generation."""

    NAME = 'sdy_classes'

    def __init__(self):
        super().__init__(self.NAME, 'classes')

    @override
    def flush_block(
        self, ident: str, ext: str, data: object, bs: IBlockStream
    ):  # numpydoc ignore=GL08
        bs.begin_block()

        # data is a None
        blanks = ''
        for cls in self.model.all_classifiers:
            if isinstance(cls, EClass):
                bs.write(blanks)
                self.flush_class(cls, bs)
                blanks = '\n\n'

        bs.end_block()

        if bs.new:
            bs.print()
            bs.print()

    def flush_class(self, cls: EClass, bs: IBlockStream):
        """Generate the class."""
        bs.write(f'class {cls.name}(')
        if len(cls.e_super_types) != 0:
            bs.write(', '.join([parent.name for parent in cls.e_super_types]))
        else:
            bs.write('object')
        bs.print('):')
        annotation = cls.get_e_annotation('http://www.eclipse.org/emf/2002/GenModel')
        if not annotation:
            pass
        else:
            doc = annotation.details.get('documentation', '')
            self.flush_doc(doc, '    ', cls.name, bs)
        self.flush_init(cls, bs)
        self.flush_accessors(cls, bs)
        self.flush_properties(cls, bs)

        ub = 'cls_' + lower_name(cls.name)
        if bs.user_block_present(ub):
            bs.print()
            bs.flush_user_block(ub, '    ', False)

    def flush_init(self, cls: EClass, bs: IBlockStream):
        """
        Generate ``__init__`` function.

        The class has construction parameters if it is a ``Property``.
        The parameters correspond to the flatten features, possibly empty.
        The parameters of the inherited features must be passed to ``super().__init__``.
        The initial value of a class member is either the default value or a parameter.
        """
        # TODO JH: ignore derived features (none for now in sdy.ecore)
        # compute the default values of the attribute/properties (applies to Property only)
        features = cls.sdy__flatten_features
        bs.write('    def __init__(self')
        if len(features) > 0:
            bs.write(', ')
            bs.write(
                ', '.join(
                    [
                        "{0}: {1} = {2}".format(
                            feature.sdy__ident,
                            feature.sdy__prop_typing_name,
                            feature.sdy__prop_default_value,
                        )
                        for feature in features
                    ]
                )
            )
        bs.print('):')
        if len(cls.e_super_types) != 0:
            # consider only the first parent (don't know how to call super() for multiple inheritance)
            parent = cls.e_super_types[0]
            parameters = ', '.join([_.sdy__ident for _ in parent.sdy__flatten_features])
        else:
            parameters = ''
        bs.print('        super().__init__({0})'.format(parameters))
        for feature in cls.e_attributes + cls.e_references:
            if feature in features:
                # equivalent to cls.isProperty and (isinstance(feature, EAttribute) or feature.isProperty):
                if feature.sdy__is_property:
                    sub_type = feature.e_type
                    sub_features = sub_type.sdy__flatten_features
                    if len(sub_features) > 1:
                        params = ', '.join([_.sdy__ident for _ in sub_features])
                    else:
                        params = feature.sdy__ident
                    if feature.upper_bound == -1:
                        # code similar to setter
                        bs.print(
                            '        self.{0} = [{3}({4}) for {4} in {1}] # type: {2}'.format(
                                feature.sdy__attribute,
                                feature.sdy__ident,
                                feature.sdy__typing_name,
                                sub_type.name,
                                params,
                            )
                        )
                    else:
                        # call constructor with the parameter
                        bs.print(
                            '        self.{0} = {3}({1}) # type: {2}'.format(
                                feature.sdy__attribute,
                                params,
                                feature.sdy__typing_name,
                                feature.e_type.name,
                            )
                        )
                else:
                    bs.print(
                        '        self.{0} = {1}  # type: {2}'.format(
                            feature.sdy__attribute, feature.sdy__ident, feature.sdy__typing_name
                        )
                    )
            else:
                bs.print(
                    '        self.{0} = {1}  # type: {2}'.format(
                        feature.sdy__attribute, feature.sdy__default, feature.sdy__typing_name
                    )
                )
        ub = 'init_' + lower_name(cls.name)
        bs.flush_user_block(ub, '        ', False)

    def flush_properties(self, cls: EClass, bs: IBlockStream):
        """Generate the properties."""
        properties = cls.sdy__properties
        if len(properties) == 0:
            return
        bs.print('')
        bs.print('    def getProperties(self):')
        dict = ', '.join(
            [
                "'{1}': ('{0}', {2})".format(
                    prop.sdy__attribute, title_name(prop.name), prop.e_type.name
                )
                for prop in properties
            ]
        )
        bs.print('        return {' + dict + '}')

    def flush_accessors(self, cls: EClass, bs: IBlockStream):
        """Generate the property accessors."""
        property: EReference
        for property in cls.sdy__properties:
            type = property.e_type
            features = type.sdy__flatten_features
            if len(features) == 0:
                continue
            map = {
                'ident': property.sdy__ident,
                'attribute': property.sdy__attribute,
                'accessor': property.sdy__accessor,
                'type': type.name,
                'typeName': property.sdy__prop_typing_name,
            }
            if property.upper_bound == -1:
                map['gprops'] = ', '.join(
                    [property.sdy__accessor + '.' + feature.sdy__accessor for feature in features]
                )
                map['sprops'] = ', '.join([feature.sdy__accessor for feature in features])
                code = (
                    '\n'
                    '    @property\n'
                    '    def {accessor}(self) -> {typeName}:\n'
                    '        return [({gprops}) for {accessor} in self.{attribute}]\n'
                    '\n'
                    '    @{accessor}.setter\n'
                    '    def {accessor}(self, {ident}: {typeName}):\n'
                    '        self.{attribute} = [{type}({sprops}) for {sprops} in {ident}]'
                )
                bs.print(code.format_map(map))
            else:
                map['props'] = ', '.join(
                    [
                        'self.' + property.sdy__attribute + '.' + feature.sdy__accessor
                        for feature in features
                    ]
                )
                code = (
                    '\n'
                    '    @property\n'
                    '    def {accessor}(self) -> {typeName}:\n'
                    '        return {props}\n'
                    '\n'
                    '    @{accessor}.setter\n'
                    '    def {accessor}(self, {ident}: {typeName}):\n'
                    '        {props} = {ident}'
                )
                bs.print(code.format_map(map))
