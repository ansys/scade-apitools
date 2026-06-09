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
from scade.model.common.traceability import Traceable

#%% classes

#{{visit(model)
class ModelVisitor:
    def visit(self, item: object, class_name: str = '', reference_name: str  = ''):
        fct = getattr(type(self), _map_visit_functions[type(item)])
        fct(self, item, class_name, reference_name)


    def visit_a661_object_instance(self, a661_object_instance: model.A661ObjectInstance, class_name: str, reference_name: str):
        self.visit_traceable(a661_object_instance, class_name, reference_name)

    def visit_array_prop_value(self, array_prop_value: model.ArrayPropValue, class_name: str, reference_name: str):
        self.visit_prop_value(array_prop_value, class_name, reference_name)

        for reference in array_prop_value.values:
            self.visit(reference, 'ArrayPropValue', 'values')

    def visit_connected_message(self, connected_message: model.ConnectedMessage, class_name: str, reference_name: str):
        pass

    def visit_definition_attribute(self, definition_attribute: model.DefinitionAttribute, class_name: str, reference_name: str):
        reference = definition_attribute.value
        if reference:
            self.visit(reference, 'DefinitionAttribute', 'value')

    def visit_definition_file(self, definition_file: model.DefinitionFile, class_name: str, reference_name: str):
        self.visit_definition_file_element(definition_file, class_name, reference_name)

        for reference in definition_file.layers:
            self.visit(reference, 'DefinitionFile', 'layers')

    def visit_definition_file_element(self, definition_file_element: model.DefinitionFileElement, class_name: str, reference_name: str):
        pass

    def visit_enum_prop_value(self, enum_prop_value: model.EnumPropValue, class_name: str, reference_name: str):
        self.visit_prop_value(enum_prop_value, class_name, reference_name)

    def visit_float_prop_value(self, float_prop_value: model.FloatPropValue, class_name: str, reference_name: str):
        self.visit_prop_value(float_prop_value, class_name, reference_name)

    def visit_int_prop_value(self, int_prop_value: model.IntPropValue, class_name: str, reference_name: str):
        self.visit_prop_value(int_prop_value, class_name, reference_name)

    def visit_layer_instance(self, layer_instance: model.LayerInstance, class_name: str, reference_name: str):
        self.visit_a661_object_instance(layer_instance, class_name, reference_name)

        for reference in layer_instance.children:
            self.visit(reference, 'LayerInstance', 'children')
        for reference in layer_instance.events:
            self.visit(reference, 'LayerInstance', 'events')
        for reference in layer_instance.runtime_messages:
            self.visit(reference, 'LayerInstance', 'runtimeMessages')

    def visit_picture_element(self, picture_element: model.PictureElement, class_name: str, reference_name: str):
        pass

    def visit_picture_table(self, picture_table: model.PictureTable, class_name: str, reference_name: str):
        for reference in picture_table.bitmaps:
            self.visit(reference, 'PictureTable', 'bitmaps')

    def visit_prop_value(self, prop_value: model.PropValue, class_name: str, reference_name: str):
        pass

    def visit_string_prop_value(self, string_prop_value: model.StringPropValue, class_name: str, reference_name: str):
        self.visit_prop_value(string_prop_value, class_name, reference_name)

    def visit_struct_prop_value(self, struct_prop_value: model.StructPropValue, class_name: str, reference_name: str):
        self.visit_prop_value(struct_prop_value, class_name, reference_name)

        for reference in struct_prop_value.values:
            self.visit(reference, 'StructPropValue', 'values')

    def visit_symbol_command_instance(self, symbol_command_instance: model.SymbolCommandInstance, class_name: str, reference_name: str):
        self.visit_a661_object_instance(symbol_command_instance, class_name, reference_name)

        for reference in symbol_command_instance.children:
            self.visit(reference, 'SymbolCommandInstance', 'children')
        for reference in symbol_command_instance.props:
            self.visit(reference, 'SymbolCommandInstance', 'props')

    def visit_symbol_instance(self, symbol_instance: model.SymbolInstance, class_name: str, reference_name: str):
        self.visit_definition_file_element(symbol_instance, class_name, reference_name)
        self.visit_traceable(symbol_instance, class_name, reference_name)

        for reference in symbol_instance.children:
            self.visit(reference, 'SymbolInstance', 'children')

    def visit_symbol_table(self, symbol_table: model.SymbolTable, class_name: str, reference_name: str):
        for reference in symbol_table.elements:
            self.visit(reference, 'SymbolTable', 'elements')

    def visit_symbol_table_element(self, symbol_table_element: model.SymbolTableElement, class_name: str, reference_name: str):
        reference = symbol_table_element.symbol
        if reference:
            self.visit(reference, 'SymbolTableElement', 'symbol')

    def visit_widget_element(self, widget_element: model.WidgetElement, class_name: str, reference_name: str):
        self.visit_a661_object_instance(widget_element, class_name, reference_name)

    def visit_widget_extension_instance(self, widget_extension_instance: model.WidgetExtensionInstance, class_name: str, reference_name: str):
        for reference in widget_extension_instance.props:
            self.visit(reference, 'WidgetExtensionInstance', 'props')

    def visit_widget_instance(self, widget_instance: model.WidgetInstance, class_name: str, reference_name: str):
        self.visit_widget_element(widget_instance, class_name, reference_name)

        for reference in widget_instance.children:
            self.visit(reference, 'WidgetInstance', 'children')
        for reference in widget_instance.events:
            self.visit(reference, 'WidgetInstance', 'events')
        for reference in widget_instance.extensions:
            self.visit(reference, 'WidgetInstance', 'extensions')
        for reference in widget_instance.props:
            self.visit(reference, 'WidgetInstance', 'props')
        for reference in widget_instance.runtime_messages:
            self.visit(reference, 'WidgetInstance', 'runtimeMessages')

    def visit_widget_set(self, widget_set: model.WidgetSet, class_name: str, reference_name: str):
        pass

    def visit_widget_set_reference_instance(self, widget_set_reference_instance: model.WidgetSetReferenceInstance, class_name: str, reference_name: str):
        self.visit_widget_element(widget_set_reference_instance, class_name, reference_name)

    #<<visitor
    def visit_traceable(self, traceable: Traceable, class_name: str, reference_name: str):
        pass
    #>>visitor


_map_visit_functions = {
    model.A661ObjectInstance: 'visit_a661_object_instance',
    model.ArrayPropValue: 'visit_array_prop_value',
    model.ConnectedMessage: 'visit_connected_message',
    model.DefinitionAttribute: 'visit_definition_attribute',
    model.DefinitionFile: 'visit_definition_file',
    model.EnumPropValue: 'visit_enum_prop_value',
    model.FloatPropValue: 'visit_float_prop_value',
    model.IntPropValue: 'visit_int_prop_value',
    model.LayerInstance: 'visit_layer_instance',
    model.PictureElement: 'visit_picture_element',
    model.PictureTable: 'visit_picture_table',
    model.StringPropValue: 'visit_string_prop_value',
    model.StructPropValue: 'visit_struct_prop_value',
    model.SymbolCommandInstance: 'visit_symbol_command_instance',
    model.SymbolInstance: 'visit_symbol_instance',
    model.SymbolTable: 'visit_symbol_table',
    model.SymbolTableElement: 'visit_symbol_table_element',
    model.WidgetExtensionInstance: 'visit_widget_extension_instance',
    model.WidgetInstance: 'visit_widget_instance',
    model.WidgetSet: 'visit_widget_set',
    model.WidgetSetReferenceInstance: 'visit_widget_set_reference_instance',
}
#}}visit

# provide a more significant name
DFVisitor = ModelVisitor

#%% end
