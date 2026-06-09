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

"""Common classes for display API: SdyModel and SdyService."""

from pathlib import Path
from typing import override

from ansys.eseg.lbsjv.ecore.ecore import EClass, EClassifier, EDataType, EEnum, EPackage
from ansys.eseg.lbsjv.services import PythonModel, lower_name, upper_name
from ansys.eseg.lbsjv.vgl import IBlockManager, IBlockStream, IManager
from ansys.eseg.lbsjv.vgl.defaults import Service


class SdyModel(PythonModel):
    """Model provider for VGL."""

    @override
    def prepare_model(self):  # numpydoc ignore=GL08
        self._fix_containments()

        super().prepare_model()

    @override
    def prepare_oids(self):  # numpydoc ignore=GL08
        # do not generate VGL oids
        # return super().prepare_oids()
        pass

    @override
    def prepare_types(self):  # numpydoc ignore=GL08
        super().prepare_types()

        # add additional properties to the types
        assert isinstance(self.root, EPackage)
        for type in self.root.e_classifiers:
            if isinstance(type, EDataType):
                self.prepare_type(type)
        for cls in self.root.e_classifiers:
            if isinstance(cls, EClass):
                self.prepare_class(cls)

    def prepare_type(self, type_: EClassifier):
        """
        Add additional properties to type instances.

        * sdy__is_property: whether cls is or inherits from Property
        * sdy__default: default value for the type, either None or a new instance for properties
        """
        type_.sdy__is_property = False
        if isinstance(type_, EEnum):
            type_.sdy__default = f'{type_.name}.{upper_name(type_.e_literals[0].name)}'
        else:
            type_.sdy__default = type_.vgl_py_init_value

    def prepare_class(self, cls: EClass):
        """
        Add additional properties to class instances.

        * sdy__is_property: whether cls is or inherits from Property
        * sdy__default: default value for the type, either None or a new instance for properties
        * sdy__properties: list of contained references typed by a property
        * sdy__flatten_features: list of all the attributes/properties of a Property including the inherited ones
        * sdy__prop_typing_name: typing annotation of the class
        * sdy__prop_default_value:  default value of the flattened class
        * _prepared: marker to avoid recursion on the same class
        """
        try:
            if cls._prepared:
                return
        except BaseException:
            pass

        cls._prepared = True

        # prepare ancestors first
        cls.sdy__is_property = cls.name == 'Property'
        cls.sdy__flatten_features = []
        for parent in cls.e_super_types:
            self.prepare_class(parent)
            cls.sdy__is_property |= parent.sdy__is_property
            cls.sdy__flatten_features += parent.sdy__flatten_features

        # prepare children
        for reference in cls.e_references:
            if reference.containment and reference.e_type:
                # reference.e_type might be None with a661.ecore
                self.prepare_class(reference.e_type)

        cls.sdy__default = cls.name + '()' if cls.sdy__is_property else 'None'
        cls.vgl_py_name = cls.name

        """
        additional feature attributes (feature means attribute or reference)

        * sdy__ident: generic name of the feature
        * sdy__attribute: name of the class member
        * sdy__accessor: name of the accessor
        * sdy__default: default value of the feature: default value of the type combined with
          the multipliticy unless a default value is specified in the ecore model
        * sdy__is_property: true when the reference is a composition of a property
        * sdy__typing_name: typing annotation
        * sdy__prop_typing_name: typing annotation of the flattened property
        * sdy__prop_default_value: default value of the flattened property
        """

        for attribute in cls.e_attributes:
            attribute.sdy__is_property = False

        # properties: all references typed by a property
        cls.sdy__properties = []
        for reference in cls.e_references:
            reference.sdy__is_property = (
                reference.containment and reference.e_type and reference.e_type.sdy__is_property
            )
            if reference.sdy__is_property:
                cls.sdy__properties.append(reference)
        if cls.sdy__is_property:
            cls.sdy__flatten_features += cls.e_attributes + cls.sdy__properties

        typing_names = []
        defaults = []
        for feature in cls.e_attributes + cls.e_references:
            feature.sdy__ident = lower_name(feature.name)
            type_ = feature.e_type
            try:
                type_default = type_.sdy__default
                type_target_name = type_.vgl_py_name
            except BaseException:
                # classes referenced through an association might have not been prepared yet
                # this is not an issue
                type_default = 'None'
                type_target_name = type_.name if type_ is not None else None

            if type_ is None:
                continue
            feature.sdy__typing_name = type_target_name
            if feature.sdy__is_property:
                feature.sdy__attribute = feature.sdy__ident
                feature.sdy__accessor = 'p_' + feature.sdy__ident
                feature.sdy__prop_typing_name = type_.sdy__prop_typing_name
                feature.sdy__prop_default_value = type_.sdy__prop_default_value
            else:
                feature.sdy__attribute = feature.sdy__ident
                feature.sdy__accessor = feature.sdy__ident
                feature.sdy__prop_typing_name = type_target_name
                feature.sdy__prop_default_value = type_default
            # TODO: be smarter with multiplicities: for now, only 1..1, 0..* or 1..*
            #       provided they are consistent in the ecore model
            if feature.upper_bound == -1:
                feature.sdy__default = '[]'
                feature.sdy__prop_default_value = '[]'
                feature.sdy__prop_typing_name = f'List[{feature.sdy__prop_typing_name}]'
                feature.sdy__typing_name = f'List[{feature.sdy__typing_name}]'
            else:
                if feature.default_value_literal != '':
                    feature.sdy__default = feature.default_value_literal
                    if isinstance(type_, EEnum):
                        feature.sdy__default = f'{type_.name}.{upper_name(feature.sdy__default)}'
                else:
                    feature.sdy__default = type_default
                    if feature.sdy__default is None:
                        print(f'{feature.e_container.name}::{feature.name}: Unknown type {type_}')
                        feature.sdy__default = 'None'
        typing_names = []
        defaults = []
        for feature in cls.sdy__flatten_features:
            typing_names.append(feature.sdy__prop_typing_name)
            defaults.append(feature.sdy__prop_default_value)

        if len(typing_names) == 1:
            cls.sdy__prop_typing_name = typing_names[0]
            cls.sdy__prop_default_value = defaults[0]
        else:
            cls.sdy__prop_typing_name = 'Tuple[' + ', '.join(typing_names) + ']'
            cls.sdy__prop_default_value = '(' + ', '.join(defaults) + ')'

    def _fix_containments(self):
        """
        Declare all references to properties as containment.

        Rationale: the containment attribute is not always set in sdy.ecore

        Note: the implementation is not the best one, to not interfere with
        the main algorithm.
        """
        prop_classes = {}
        for cls in self.root.all_classifiers:
            # classes are (partially) sorted with respect to the inheritance graph
            if isinstance(cls, EClass):
                if cls.name == 'Property' or (
                    len(cls.e_super_types) > 0 and cls.e_super_types[0] in prop_classes
                ):
                    prop_classes[cls] = True

        for cls in self.root.all_classifiers:
            if isinstance(cls, EClass):
                for reference in cls.e_references:
                    if not reference.containment and reference.e_type in prop_classes:
                        reference.containment = True


class SdyService(Service):
    """
    Base SCADE Display service for VGL.

    Creates one file per model assuming one and only one model.
    """

    def __init__(self, name, anchor):
        self.anchor = anchor
        self.files = {}
        return super().__init__(name)

    # IService interface
    @override
    def init(self, manager: IManager):  # numpydoc ignore=GL08
        super().init(manager)
        for model in manager.models:
            if isinstance(model, SdyModel):
                # should be one and only one SDY model
                if model.library:
                    continue
                path = model.path
                self.model_name = path.stem
                self.basename = path.with_suffix('.py').name
                self.sdy_model = model
                self.model = model.root
                return True
        return False

    @override
    def extend_files(self):  # numpydoc ignore=GL08
        assert self.manager is not None  # nosec B101  # addresses linter
        path = self.manager.target_dir / self.basename
        self.manager.add_file(path)
        self.files[path] = None
        # self.filename = path

    @override
    def subscribe(self):  # numpydoc ignore=GL08
        # subscribe to all declared files
        assert self.manager is not None  # nosec B101  # addresses linter
        for file in self.files.keys():
            self.manager.subscribe_file(file, self)

    @override
    def create_blocks(self, bm: IBlockManager, path: Path):  # numpydoc ignore=GL08
        assert isinstance(self.manager, IManager)  # nosec B101  # addresses linter
        # one unique block
        if not self.manager.is_block_present(self.name, self.sdy_model.ident, ''):
            bm.create_block(
                self.name, self.sdy_model.ident, '', None, anchor=self.anchor, bottom=True
            )

    @override
    def accept_block(self, ident: str, ext: str) -> tuple[bool, object]:  # numpydoc ignore=GL08
        # one unique block
        return ident == self.sdy_model.ident, None

    # helpers
    def flush_doc(self, doc: str, tab: str, ident: str, bs: IBlockStream):
        """Flush the optional documentation user block."""
        ub = 'doc_' + lower_name(ident)
        empty = doc == ''
        present = bs.user_block_present(ub)
        if empty and not present:
            return
        bs.print(tab + '"""')
        if not empty:
            bs.print(tab + doc)
        if present:
            if not empty:
                bs.print()
            bs.flush_user_block(ub, tab, False)
        bs.print(tab + '"""')
