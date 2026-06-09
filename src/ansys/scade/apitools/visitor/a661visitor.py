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

import scade.model.a661.df as model
import scade.model.a661.standard as a661

#%% classes

#{{visit(a661)
class A661Visitor:
    def visit(self, item: object, class_name: str = '', reference_name: str  = ''):
        fct = getattr(type(self), _map_visit_functions[type(item)])
        fct(self, item, class_name, reference_name)


    def visit_a661_constant(self, a661_constant: a661.A661Constant, class_name: str, reference_name: str):
        pass

    def visit_a661_constants(self, a661_constants: a661.A661Constants, class_name: str, reference_name: str):
        for reference in a661_constants.constants:
            self.visit(reference, 'A661Constants', 'constants')

    def visit_a661_hierarchy(self, a661_hierarchy: a661.A661Hierarchy, class_name: str, reference_name: str):
        for reference in a661_hierarchy.hierarchies:
            self.visit(reference, 'A661Hierarchy', 'hierarchies')

    def visit_a661_layer(self, a661_layer: a661.A661Layer, class_name: str, reference_name: str):
        for reference in a661_layer.events:
            self.visit(reference, 'A661Layer', 'events')
        for reference in a661_layer.runtime_messages:
            self.visit(reference, 'A661Layer', 'runtime_messages')

    def visit_a661_object(self, a661_object: a661.A661Object, class_name: str, reference_name: str):
        for reference in a661_object.definitions:
            self.visit(reference, 'A661Object', 'definitions')
        reference = a661_object.ide_info
        if reference:
            self.visit(reference, 'A661Object', 'ideInfo')

    def visit_a661_standard(self, a661_standard: a661.A661Standard, class_name: str, reference_name: str):
        reference = a661_standard.a661_hierarchy
        if reference:
            self.visit(reference, 'A661Standard', 'a661Hierarchy')
        reference = a661_standard.constants
        if reference:
            self.visit(reference, 'A661Standard', 'constants')
        reference = a661_standard.extension_hierarchy
        if reference:
            self.visit(reference, 'A661Standard', 'extensionHierarchy')
        reference = a661_standard.layer
        if reference:
            self.visit(reference, 'A661Standard', 'layer')
        for reference in a661_standard.symbol_commands:
            self.visit(reference, 'A661Standard', 'symbolCommands')
        reference = a661_standard.symbol_hierarchy
        if reference:
            self.visit(reference, 'A661Standard', 'symbolHierarchy')
        reference = a661_standard.types
        if reference:
            self.visit(reference, 'A661Standard', 'types')
        for reference in a661_standard.widget_extensions:
            self.visit(reference, 'A661Standard', 'widgetExtensions')
        for reference in a661_standard.widgets:
            self.visit(reference, 'A661Standard', 'widgets')

    def visit_a661_type(self, a661_type: a661.A661Type, class_name: str, reference_name: str):
        pass

    def visit_a661_types(self, a661_types: a661.A661Types, class_name: str, reference_name: str):
        for reference in a661_types.types:
            self.visit(reference, 'A661Types', 'types')

    def visit_a661_widget(self, a661_widget: a661.A661Widget, class_name: str, reference_name: str):
        self.visit_a661_object(a661_widget, class_name, reference_name)

        for reference in a661_widget.events:
            self.visit(reference, 'A661Widget', 'events')
        for reference in a661_widget.runtime_messages:
            self.visit(reference, 'A661Widget', 'runtimeMessages')
        for reference in a661_widget.types:
            self.visit(reference, 'A661Widget', 'types')

    def visit_a_struct_element(self, a_struct_element: a661.AStructElement, class_name: str, reference_name: str):
        pass

    def visit_align_element(self, align_element: a661.AlignElement, class_name: str, reference_name: str):
        self.visit_definition_field(align_element, class_name, reference_name)
        self.visit_msg_element(align_element, class_name, reference_name)

    def visit_array_element(self, array_element: a661.ArrayElement, class_name: str, reference_name: str):
        self.visit_a_struct_element(array_element, class_name, reference_name)

        for reference in array_element.elements:
            self.visit(reference, 'ArrayElement', 'elements')

    def visit_array_field(self, array_field: a661.ArrayField, class_name: str, reference_name: str):
        self.visit_msg_element(array_field, class_name, reference_name)

        for reference in array_field.field_elements:
            self.visit(reference, 'ArrayField', 'fieldElements')

    def visit_array_type(self, array_type: a661.ArrayType, class_name: str, reference_name: str):
        self.visit_a661_type(array_type, class_name, reference_name)

    def visit_bit_field(self, bit_field: a661.BitField, class_name: str, reference_name: str):
        pass

    def visit_built_in_type(self, built_in_type: a661.BuiltInType, class_name: str, reference_name: str):
        self.visit_a661_type(built_in_type, class_name, reference_name)

    def visit_data_element(self, data_element: a661.DataElement, class_name: str, reference_name: str):
        self.visit_a_struct_element(data_element, class_name, reference_name)

    def visit_definition_field(self, definition_field: a661.DefinitionField, class_name: str, reference_name: str):
        pass

    def visit_definition_prop(self, definition_prop: a661.DefinitionProp, class_name: str, reference_name: str):
        self.visit_definition_field(definition_prop, class_name, reference_name)

        reference = definition_prop.default
        if reference:
            self.visit(reference, 'DefinitionProp', 'default')
        reference = definition_prop.ide_info
        if reference:
            self.visit(reference, 'DefinitionProp', 'ideInfo')

    def visit_definition_prop_control(self, definition_prop_control: a661.DefinitionPropControl, class_name: str, reference_name: str):
        pass

    def visit_definition_prop_ide_info(self, definition_prop_ide_info: a661.DefinitionPropIDEInfo, class_name: str, reference_name: str):
        for reference in definition_prop_ide_info.selector:
            self.visit(reference, 'DefinitionPropIDEInfo', 'selector')

    def visit_definition_prop_selector(self, definition_prop_selector: a661.DefinitionPropSelector, class_name: str, reference_name: str):
        for reference in definition_prop_selector.bit_field:
            self.visit(reference, 'DefinitionPropSelector', 'bit_field')

    def visit_dimension(self, dimension: a661.Dimension, class_name: str, reference_name: str):
        for reference in dimension.dimension:
            self.visit(reference, 'Dimension', 'dimension')

    def visit_enum_type(self, enum_type: a661.EnumType, class_name: str, reference_name: str):
        self.visit_a661_type(enum_type, class_name, reference_name)

    def visit_extension_hierarchy(self, extension_hierarchy: a661.ExtensionHierarchy, class_name: str, reference_name: str):
        for reference in extension_hierarchy.widget_extensions:
            self.visit(reference, 'ExtensionHierarchy', 'widgetExtensions')

    def visit_fr_type(self, fr_type: a661.FRType, class_name: str, reference_name: str):
        self.visit_built_in_type(fr_type, class_name, reference_name)

    def visit_generic_dimension(self, generic_dimension: a661.GenericDimension, class_name: str, reference_name: str):
        pass

    def visit_generic_index(self, generic_index: a661.GenericIndex, class_name: str, reference_name: str):
        pass

    def visit_generic_type(self, generic_type: a661.GenericType, class_name: str, reference_name: str):
        pass

    def visit_message(self, message: a661.Message, class_name: str, reference_name: str):
        reference = message.msg_type
        if reference:
            self.visit(reference, 'Message', 'msgType')

    def visit_msg_element(self, msg_element: a661.MsgElement, class_name: str, reference_name: str):
        pass

    def visit_msg_field(self, msg_field: a661.MsgField, class_name: str, reference_name: str):
        self.visit_msg_element(msg_field, class_name, reference_name)

    def visit_msg_type(self, msg_type: a661.MsgType, class_name: str, reference_name: str):
        for reference in msg_type.subst:
            self.visit(reference, 'MsgType', 'subst')

    def visit_msg_type_subst(self, msg_type_subst: a661.MsgTypeSubst, class_name: str, reference_name: str):
        pass

    def visit_named_type(self, named_type: a661.NamedType, class_name: str, reference_name: str):
        self.visit_a661_type(named_type, class_name, reference_name)

    def visit_object_ide_info(self, object_ide_info: a661.ObjectIDEInfo, class_name: str, reference_name: str):
        pass

    def visit_padding_element(self, padding_element: a661.PaddingElement, class_name: str, reference_name: str):
        self.visit_definition_field(padding_element, class_name, reference_name)
        self.visit_msg_element(padding_element, class_name, reference_name)

    def visit_scalar_element(self, scalar_element: a661.ScalarElement, class_name: str, reference_name: str):
        self.visit_a_struct_element(scalar_element, class_name, reference_name)

    def visit_size_element(self, size_element: a661.SizeElement, class_name: str, reference_name: str):
        self.visit_a_struct_element(size_element, class_name, reference_name)

    def visit_str_type(self, str_type: a661.StrType, class_name: str, reference_name: str):
        self.visit_built_in_type(str_type, class_name, reference_name)

    def visit_struct_align_element(self, struct_align_element: a661.StructAlignElement, class_name: str, reference_name: str):
        self.visit_a_struct_element(struct_align_element, class_name, reference_name)

    def visit_struct_element(self, struct_element: a661.StructElement, class_name: str, reference_name: str):
        self.visit_a_struct_element(struct_element, class_name, reference_name)

    def visit_struct_padding_element(self, struct_padding_element: a661.StructPaddingElement, class_name: str, reference_name: str):
        self.visit_a_struct_element(struct_padding_element, class_name, reference_name)

    def visit_struct_type(self, struct_type: a661.StructType, class_name: str, reference_name: str):
        self.visit_a661_type(struct_type, class_name, reference_name)

        for reference in struct_type.elements:
            self.visit(reference, 'StructType', 'elements')

    def visit_symbol_command(self, symbol_command: a661.SymbolCommand, class_name: str, reference_name: str):
        self.visit_a661_object(symbol_command, class_name, reference_name)

    def visit_symbol_command_hierarchy(self, symbol_command_hierarchy: a661.SymbolCommandHierarchy, class_name: str, reference_name: str):
        pass

    def visit_symbol_hierarchy(self, symbol_hierarchy: a661.SymbolHierarchy, class_name: str, reference_name: str):
        pass

    def visit_union_type(self, union_type: a661.UnionType, class_name: str, reference_name: str):
        self.visit_a661_type(union_type, class_name, reference_name)

        for reference in union_type.alternatives:
            self.visit(reference, 'UnionType', 'alternatives')

    def visit_widget_extensions(self, widget_extensions: a661.WidgetExtensions, class_name: str, reference_name: str):
        pass

    def visit_widget_hierarchy(self, widget_hierarchy: a661.WidgetHierarchy, class_name: str, reference_name: str):
        pass

    #<<visitor
    # methods duplicated from modelvisitor.py
    def visit_array_prop_value(self, array_prop_value: model.ArrayPropValue, class_name: str, reference_name: str):
        self.visit_prop_value(array_prop_value, class_name, reference_name)

        for reference in array_prop_value.values:
            self.visit(reference, 'ArrayPropValue', 'values')

    def visit_definition_attribute(self, definition_attribute: model.DefinitionAttribute, class_name: str, reference_name: str):
        reference = definition_attribute.value
        if reference:
            self.visit(reference, 'DefinitionAttribute', 'value')

    def visit_enum_prop_value(self, enum_prop_value: model.EnumPropValue, class_name: str, reference_name: str):
        self.visit_prop_value(enum_prop_value, class_name, reference_name)

    def visit_float_prop_value(self, float_prop_value: model.FloatPropValue, class_name: str, reference_name: str):
        self.visit_prop_value(float_prop_value, class_name, reference_name)

    def visit_int_prop_value(self, int_prop_value: model.IntPropValue, class_name: str, reference_name: str):
        self.visit_prop_value(int_prop_value, class_name, reference_name)

    def visit_prop_value(self, prop_value: model.PropValue, class_name: str, reference_name: str):
        pass

    def visit_string_prop_value(self, string_prop_value: model.StringPropValue, class_name: str, reference_name: str):
        self.visit_prop_value(string_prop_value, class_name, reference_name)

    def visit_struct_prop_value(self, struct_prop_value: model.StructPropValue, class_name: str, reference_name: str):
        self.visit_prop_value(struct_prop_value, class_name, reference_name)

        for reference in struct_prop_value.values:
            self.visit(reference, 'StructPropValue', 'values')
    #>>visitor


_map_visit_functions = {
    a661.A661Constant: 'visit_a661_constant',
    a661.A661Constants: 'visit_a661_constants',
    a661.A661Hierarchy: 'visit_a661_hierarchy',
    a661.A661Layer: 'visit_a661_layer',
    a661.A661Standard: 'visit_a661_standard',
    a661.A661Types: 'visit_a661_types',
    a661.A661Widget: 'visit_a661_widget',
    a661.AStructElement: 'visit_a_struct_element',
    a661.AlignElement: 'visit_align_element',
    a661.ArrayElement: 'visit_array_element',
    a661.ArrayField: 'visit_array_field',
    a661.ArrayType: 'visit_array_type',
    a661.BitField: 'visit_bit_field',
    a661.BuiltInType: 'visit_built_in_type',
    a661.DataElement: 'visit_data_element',
    a661.DefinitionProp: 'visit_definition_prop',
    a661.DefinitionPropControl: 'visit_definition_prop_control',
    a661.DefinitionPropIDEInfo: 'visit_definition_prop_ide_info',
    a661.DefinitionPropSelector: 'visit_definition_prop_selector',
    a661.Dimension: 'visit_dimension',
    a661.EnumType: 'visit_enum_type',
    a661.ExtensionHierarchy: 'visit_extension_hierarchy',
    a661.FRType: 'visit_fr_type',
    a661.GenericDimension: 'visit_generic_dimension',
    a661.GenericIndex: 'visit_generic_index',
    a661.GenericType: 'visit_generic_type',
    a661.Message: 'visit_message',
    a661.MsgField: 'visit_msg_field',
    a661.MsgType: 'visit_msg_type',
    a661.MsgTypeSubst: 'visit_msg_type_subst',
    a661.NamedType: 'visit_named_type',
    a661.ObjectIDEInfo: 'visit_object_ide_info',
    a661.PaddingElement: 'visit_padding_element',
    a661.ScalarElement: 'visit_scalar_element',
    a661.SizeElement: 'visit_size_element',
    a661.StrType: 'visit_str_type',
    a661.StructAlignElement: 'visit_struct_align_element',
    a661.StructElement: 'visit_struct_element',
    a661.StructPaddingElement: 'visit_struct_padding_element',
    a661.StructType: 'visit_struct_type',
    a661.SymbolCommand: 'visit_symbol_command',
    a661.SymbolCommandHierarchy: 'visit_symbol_command_hierarchy',
    a661.SymbolHierarchy: 'visit_symbol_hierarchy',
    a661.UnionType: 'visit_union_type',
    a661.WidgetExtensions: 'visit_widget_extensions',
    a661.WidgetHierarchy: 'visit_widget_hierarchy',
    #<<map_visit_functions
    # entries duplicated from modelvisitor.py
    model.ArrayPropValue: 'visit_array_prop_value',
    model.EnumPropValue: 'visit_enum_prop_value',
    model.FloatPropValue: 'visit_float_prop_value',
    model.IntPropValue: 'visit_int_prop_value',
    model.StringPropValue: 'visit_string_prop_value',
    model.StructPropValue: 'visit_struct_prop_value',
    model.DefinitionAttribute: 'visit_definition_attribute',
    #>>map_visit_functions
}
#}}visit


# provide a more significant name
StandardVisitor = A661Visitor

#%% end
