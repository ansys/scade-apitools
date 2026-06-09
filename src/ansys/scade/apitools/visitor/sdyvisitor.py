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
Visitor for SCADE Display models (from 2023 R1 to 2026 R1).

The visitor corresponds to SCADE Display 2026 R1.
It provides stubs for former releases.
"""

# required for supporting several versions
from scade.model.common.traceability import Traceable
from scade.model.display import *  # noqa: F403  # type: ignore[reportAssignmentType]

#%% classes

try:
    # FontTable can't be compatbible with stub defined hereafter
    from scade.model.display import FontTable  # type: ignore[reportAssignmentType]
except ImportError:
    # provide stubs to fix type annotations and linter errors ONLY
    class FontDefinition:
        pass

    class FontTable:
        def __init__(self):
            # warning: attribute name not consistent with ecore model
            self.elements = []  # type: List[FontDefinition]

#{{visit(sdy)
class SdyVisitor:
    def visit(self, item: object, class_name: str = '', reference_name: str  = ''):
        fct = getattr(type(self), _map_visit_functions[type(item)])
        fct(self, item, class_name, reference_name)


    def visit_a_container(self, a_container: AContainer, class_name: str, reference_name: str):
        self.visit_graphic_object(a_container, class_name, reference_name)

        for reference in a_container.children:
            self.visit(reference, 'AContainer', 'children')

    def visit_arc(self, arc: Arc, class_name: str, reference_name: str):
        self.visit_graphic_object(arc, class_name, reference_name)

    def visit_arc_ellipse(self, arc_ellipse: ArcEllipse, class_name: str, reference_name: str):
        self.visit_graphic_object(arc_ellipse, class_name, reference_name)

    def visit_array_expr(self, array_expr: ArrayExpr, class_name: str, reference_name: str):
        self.visit_expr(array_expr, class_name, reference_name)

    def visit_array_type(self, array_type: ArrayType, class_name: str, reference_name: str):
        self.visit_type(array_type, class_name, reference_name)

    def visit_assignment(self, assignment: Assignment, class_name: str, reference_name: str):
        self.visit_graphic_object(assignment, class_name, reference_name)

    def visit_behavior(self, behavior: Behavior, class_name: str, reference_name: str):
        self.visit_graphic_object(behavior, class_name, reference_name)

    def visit_bi_font(self, bi_font: BiFont, class_name: str, reference_name: str):
        self.visit_graphic_object(bi_font, class_name, reference_name)

    def visit_binary_op_expr(self, binary_op_expr: BinaryOpExpr, class_name: str, reference_name: str):
        self.visit_expr(binary_op_expr, class_name, reference_name)

    def visit_bitmap(self, bitmap: Bitmap, class_name: str, reference_name: str):
        self.visit_graphic_object(bitmap, class_name, reference_name)

    def visit_circle(self, circle: Circle, class_name: str, reference_name: str):
        self.visit_graphic_object(circle, class_name, reference_name)

    def visit_circle_area(self, circle_area: CircleArea, class_name: str, reference_name: str):
        self.visit_graphic_object(circle_area, class_name, reference_name)

    def visit_clip_box(self, clip_box: ClipBox, class_name: str, reference_name: str):
        self.visit_graphic_object(clip_box, class_name, reference_name)

    def visit_clip_plane(self, clip_plane: ClipPlane, class_name: str, reference_name: str):
        self.visit_graphic_object(clip_plane, class_name, reference_name)

    def visit_close_path(self, close_path: ClosePath, class_name: str, reference_name: str):
        self.visit_command(close_path, class_name, reference_name)

    def visit_color_element(self, color_element: ColorElement, class_name: str, reference_name: str):
        pass

    def visit_color_table(self, color_table: ColorTable, class_name: str, reference_name: str):
        for reference in color_table.elements:
            self.visit(reference, 'ColorTable', 'Elements')

    def visit_command(self, command: Command, class_name: str, reference_name: str):
        pass

    def visit_comment(self, comment: Comment, class_name: str, reference_name: str):
        pass

    def visit_cond_container(self, cond_container: CondContainer, class_name: str, reference_name: str):
        self.visit_a_container(cond_container, class_name, reference_name)

    def visit_conditional_expr(self, conditional_expr: ConditionalExpr, class_name: str, reference_name: str):
        self.visit_expr(conditional_expr, class_name, reference_name)

    def visit_constant_definition(self, constant_definition: ConstantDefinition, class_name: str, reference_name: str):
        self.visit_global_definition(constant_definition, class_name, reference_name)

        reference = constant_definition.definition
        if reference:
            self.visit(reference, 'ConstantDefinition', 'definition')

    def visit_container(self, container: Container, class_name: str, reference_name: str):
        self.visit_a_container(container, class_name, reference_name)

    def visit_crown(self, crown: Crown, class_name: str, reference_name: str):
        self.visit_graphic_object(crown, class_name, reference_name)

    def visit_cursor_pos_request(self, cursor_pos_request: CursorPosRequest, class_name: str, reference_name: str):
        self.visit_graphic_object(cursor_pos_request, class_name, reference_name)

    def visit_curve_to(self, curve_to: CurveTo, class_name: str, reference_name: str):
        self.visit_command(curve_to, class_name, reference_name)

    def visit_ellipse(self, ellipse: Ellipse, class_name: str, reference_name: str):
        self.visit_graphic_object(ellipse, class_name, reference_name)

    def visit_elliptical_arc(self, elliptical_arc: EllipticalArc, class_name: str, reference_name: str):
        self.visit_command(elliptical_arc, class_name, reference_name)

    def visit_enum_type(self, enum_type: EnumType, class_name: str, reference_name: str):
        self.visit_global_type(enum_type, class_name, reference_name)

    def visit_enum_value(self, enum_value: EnumValue, class_name: str, reference_name: str):
        pass

    def visit_expr(self, expr: Expr, class_name: str, reference_name: str):
        self.visit_global_constant(expr, class_name, reference_name)

    def visit_field_expr(self, field_expr: FieldExpr, class_name: str, reference_name: str):
        self.visit_expr(field_expr, class_name, reference_name)

    def visit_filter_rotation_container(self, filter_rotation_container: FilterRotationContainer, class_name: str, reference_name: str):
        self.visit_a_container(filter_rotation_container, class_name, reference_name)

    def visit_filter_translation_container(self, filter_translation_container: FilterTranslationContainer, class_name: str, reference_name: str):
        self.visit_a_container(filter_translation_container, class_name, reference_name)

    def visit_font_definition(self, font_definition: FontDefinition, class_name: str, reference_name: str):
        pass

    def visit_font_table(self, font_table: FontTable, class_name: str, reference_name: str):
        for reference in font_table.elements:
            self.visit(reference, 'FontTable', 'elements')

    def visit_global_constant(self, global_constant: GlobalConstant, class_name: str, reference_name: str):
        pass

    def visit_global_definition(self, global_definition: GlobalDefinition, class_name: str, reference_name: str):
        pass

    def visit_global_definitions(self, global_definitions: GlobalDefinitions, class_name: str, reference_name: str):
        for reference in global_definitions.definitions:
            self.visit(reference, 'GlobalDefinitions', 'definitions')

    def visit_global_type(self, global_type: GlobalType, class_name: str, reference_name: str):
        pass

    def visit_gradient_element(self, gradient_element: GradientElement, class_name: str, reference_name: str):
        for reference in gradient_element.stop_colors:
            self.visit(reference, 'GradientElement', 'StopColors')

    def visit_gradient_stop_color(self, gradient_stop_color: GradientStopColor, class_name: str, reference_name: str):
        pass

    def visit_gradient_table(self, gradient_table: GradientTable, class_name: str, reference_name: str):
        for reference in gradient_table.elements:
            self.visit(reference, 'GradientTable', 'Elements')

    def visit_graphic_object(self, graphic_object: GraphicObject, class_name: str, reference_name: str):
        self.visit_traceable(graphic_object, class_name, reference_name)

        reference = graphic_object.comment
        if reference:
            self.visit(reference, 'GraphicObject', 'comment')

    def visit_hook(self, hook: Hook, class_name: str, reference_name: str):
        self.visit_graphic_object(hook, class_name, reference_name)

    def visit_horizontal_line_to(self, horizontal_line_to: HorizontalLineTo, class_name: str, reference_name: str):
        self.visit_command(horizontal_line_to, class_name, reference_name)

    def visit_identifier_expr(self, identifier_expr: IdentifierExpr, class_name: str, reference_name: str):
        self.visit_expr(identifier_expr, class_name, reference_name)

    def visit_imported(self, imported: Imported, class_name: str, reference_name: str):
        self.visit_graphic_object(imported, class_name, reference_name)

    def visit_imported_constant(self, imported_constant: ImportedConstant, class_name: str, reference_name: str):
        self.visit_global_constant(imported_constant, class_name, reference_name)

    def visit_imported_type(self, imported_type: ImportedType, class_name: str, reference_name: str):
        self.visit_global_type(imported_type, class_name, reference_name)

    def visit_index_expr(self, index_expr: IndexExpr, class_name: str, reference_name: str):
        self.visit_expr(index_expr, class_name, reference_name)

    def visit_index_texture_point(self, index_texture_point: IndexTexturePoint, class_name: str, reference_name: str):
        pass

    def visit_indexed_point(self, indexed_point: IndexedPoint, class_name: str, reference_name: str):
        pass

    def visit_keyboard_event_listener(self, keyboard_event_listener: KeyboardEventListener, class_name: str, reference_name: str):
        self.visit_graphic_object(keyboard_event_listener, class_name, reference_name)

    def visit_layer(self, layer: Layer, class_name: str, reference_name: str):
        self.visit_a_container(layer, class_name, reference_name)

        reference = layer.declaration
        if reference:
            self.visit(reference, 'Layer', 'declaration')

    def visit_line(self, line: Line, class_name: str, reference_name: str):
        self.visit_graphic_object(line, class_name, reference_name)

    def visit_line_stipple_element(self, line_stipple_element: LineStippleElement, class_name: str, reference_name: str):
        for reference in line_stipple_element.segments:
            self.visit(reference, 'LineStippleElement', 'Segments')

    def visit_line_stipple_segment(self, line_stipple_segment: LineStippleSegment, class_name: str, reference_name: str):
        pass

    def visit_line_stipple_table(self, line_stipple_table: LineStippleTable, class_name: str, reference_name: str):
        for reference in line_stipple_table.elements:
            self.visit(reference, 'LineStippleTable', 'Elements')

    def visit_line_to(self, line_to: LineTo, class_name: str, reference_name: str):
        self.visit_command(line_to, class_name, reference_name)

    def visit_line_width_element(self, line_width_element: LineWidthElement, class_name: str, reference_name: str):
        pass

    def visit_line_width_table(self, line_width_table: LineWidthTable, class_name: str, reference_name: str):
        for reference in line_width_table.elements:
            self.visit(reference, 'LineWidthTable', 'Elements')

    def visit_linear_gradient_element(self, linear_gradient_element: LinearGradientElement, class_name: str, reference_name: str):
        self.visit_gradient_element(linear_gradient_element, class_name, reference_name)

    def visit_literal_expr(self, literal_expr: LiteralExpr, class_name: str, reference_name: str):
        self.visit_expr(literal_expr, class_name, reference_name)

    def visit_mask_container(self, mask_container: MaskContainer, class_name: str, reference_name: str):
        self.visit_a_container(mask_container, class_name, reference_name)

    def visit_mem_variable(self, mem_variable: MemVariable, class_name: str, reference_name: str):
        self.visit_variable(mem_variable, class_name, reference_name)

    def visit_move_to(self, move_to: MoveTo, class_name: str, reference_name: str):
        self.visit_command(move_to, class_name, reference_name)

    def visit_named_type(self, named_type: NamedType, class_name: str, reference_name: str):
        self.visit_type(named_type, class_name, reference_name)

    def visit_nplicator_container(self, nplicator_container: NplicatorContainer, class_name: str, reference_name: str):
        self.visit_a_container(nplicator_container, class_name, reference_name)

    def visit_panel_container(self, panel_container: PanelContainer, class_name: str, reference_name: str):
        self.visit_a_container(panel_container, class_name, reference_name)

    def visit_path(self, path: Path, class_name: str, reference_name: str):
        self.visit_graphic_object(path, class_name, reference_name)

    def visit_pointer_event_listener(self, pointer_event_listener: PointerEventListener, class_name: str, reference_name: str):
        self.visit_graphic_object(pointer_event_listener, class_name, reference_name)

    def visit_predef_type(self, predef_type: PredefType, class_name: str, reference_name: str):
        self.visit_type(predef_type, class_name, reference_name)

    def visit_quadratic_curve_to(self, quadratic_curve_to: QuadraticCurveTo, class_name: str, reference_name: str):
        self.visit_command(quadratic_curve_to, class_name, reference_name)

    def visit_radial_gradient_element(self, radial_gradient_element: RadialGradientElement, class_name: str, reference_name: str):
        self.visit_gradient_element(radial_gradient_element, class_name, reference_name)

    def visit_rectangle(self, rectangle: Rectangle, class_name: str, reference_name: str):
        self.visit_graphic_object(rectangle, class_name, reference_name)

    def visit_rectangle_area(self, rectangle_area: RectangleArea, class_name: str, reference_name: str):
        self.visit_graphic_object(rectangle_area, class_name, reference_name)

    def visit_reference_container(self, reference_container: ReferenceContainer, class_name: str, reference_name: str):
        self.visit_a_container(reference_container, class_name, reference_name)

    def visit_reference_object(self, reference_object: ReferenceObject, class_name: str, reference_name: str):
        reference = reference_object.children
        if reference:
            self.visit(reference, 'ReferenceObject', 'children')
        reference = reference_object.declaration
        if reference:
            self.visit(reference, 'ReferenceObject', 'declaration')

    def visit_rich_text(self, rich_text: RichText, class_name: str, reference_name: str):
        self.visit_graphic_object(rich_text, class_name, reference_name)

    def visit_rotation_container(self, rotation_container: RotationContainer, class_name: str, reference_name: str):
        self.visit_a_container(rotation_container, class_name, reference_name)

    def visit_shape(self, shape: Shape, class_name: str, reference_name: str):
        self.visit_graphic_object(shape, class_name, reference_name)

    def visit_shape_area(self, shape_area: ShapeArea, class_name: str, reference_name: str):
        self.visit_graphic_object(shape_area, class_name, reference_name)

    def visit_smooth_curve_to(self, smooth_curve_to: SmoothCurveTo, class_name: str, reference_name: str):
        self.visit_command(smooth_curve_to, class_name, reference_name)

    def visit_smooth_quadratic_curve_to(self, smooth_quadratic_curve_to: SmoothQuadraticCurveTo, class_name: str, reference_name: str):
        self.visit_command(smooth_quadratic_curve_to, class_name, reference_name)

    def visit_specification(self, specification: Specification, class_name: str, reference_name: str):
        for reference in specification.layers:
            self.visit(reference, 'Specification', 'layers')

    def visit_static_bitmap(self, static_bitmap: StaticBitmap, class_name: str, reference_name: str):
        pass

    def visit_stencil(self, stencil: Stencil, class_name: str, reference_name: str):
        self.visit_graphic_object(stencil, class_name, reference_name)

    def visit_struct_expr(self, struct_expr: StructExpr, class_name: str, reference_name: str):
        self.visit_expr(struct_expr, class_name, reference_name)

    def visit_struct_field_expr(self, struct_field_expr: StructFieldExpr, class_name: str, reference_name: str):
        pass

    def visit_struct_field_type(self, struct_field_type: StructFieldType, class_name: str, reference_name: str):
        pass

    def visit_struct_type(self, struct_type: StructType, class_name: str, reference_name: str):
        self.visit_type(struct_type, class_name, reference_name)

    def visit_text(self, text: Text, class_name: str, reference_name: str):
        self.visit_graphic_object(text, class_name, reference_name)

    def visit_text_area(self, text_area: TextArea, class_name: str, reference_name: str):
        self.visit_graphic_object(text_area, class_name, reference_name)

    def visit_texture_element(self, texture_element: TextureElement, class_name: str, reference_name: str):
        pass

    def visit_texture_table(self, texture_table: TextureTable, class_name: str, reference_name: str):
        for reference in texture_table.elements:
            self.visit(reference, 'TextureTable', 'Elements')

    def visit_translation_container(self, translation_container: TranslationContainer, class_name: str, reference_name: str):
        self.visit_a_container(translation_container, class_name, reference_name)

    def visit_type(self, type: Type, class_name: str, reference_name: str):
        self.visit_global_type(type, class_name, reference_name)

    def visit_type_definition(self, type_definition: TypeDefinition, class_name: str, reference_name: str):
        self.visit_global_definition(type_definition, class_name, reference_name)

        reference = type_definition.definition
        if reference:
            self.visit(reference, 'TypeDefinition', 'definition')

    def visit_unary_op_expr(self, unary_op_expr: UnaryOpExpr, class_name: str, reference_name: str):
        self.visit_expr(unary_op_expr, class_name, reference_name)

    def visit_variable(self, variable: Variable, class_name: str, reference_name: str):
        self.visit_traceable(variable, class_name, reference_name)

        reference = variable.comment
        if reference:
            self.visit(reference, 'Variable', 'comment')
        reference = variable.init
        if reference:
            self.visit(reference, 'Variable', 'init')
        reference = variable.type
        if reference:
            self.visit(reference, 'Variable', 'type')

    def visit_variable_table(self, variable_table: VariableTable, class_name: str, reference_name: str):
        for reference in variable_table.constant:
            self.visit(reference, 'VariableTable', 'constant')
        for reference in variable_table.input:
            self.visit(reference, 'VariableTable', 'input')
        for reference in variable_table.local:
            self.visit(reference, 'VariableTable', 'local')
        for reference in variable_table.local_constant:
            self.visit(reference, 'VariableTable', 'localConstant')
        for reference in variable_table.output:
            self.visit(reference, 'VariableTable', 'output')
        for reference in variable_table.probe:
            self.visit(reference, 'VariableTable', 'probe')

    def visit_vertical_line_to(self, vertical_line_to: VerticalLineTo, class_name: str, reference_name: str):
        self.visit_command(vertical_line_to, class_name, reference_name)

    #<<visitor
    def visit_traceable(self, traceable: Traceable, class_name: str, reference_name: str):
        pass
    #>>visitor


_map_visit_functions = {
    Arc: 'visit_arc',
    ArcEllipse: 'visit_arc_ellipse',
    ArrayExpr: 'visit_array_expr',
    ArrayType: 'visit_array_type',
    Assignment: 'visit_assignment',
    Behavior: 'visit_behavior',
    BiFont: 'visit_bi_font',
    BinaryOpExpr: 'visit_binary_op_expr',
    Bitmap: 'visit_bitmap',
    Circle: 'visit_circle',
    CircleArea: 'visit_circle_area',
    ClipBox: 'visit_clip_box',
    ClipPlane: 'visit_clip_plane',
    ClosePath: 'visit_close_path',
    ColorElement: 'visit_color_element',
    ColorTable: 'visit_color_table',
    Comment: 'visit_comment',
    CondContainer: 'visit_cond_container',
    ConditionalExpr: 'visit_conditional_expr',
    ConstantDefinition: 'visit_constant_definition',
    Container: 'visit_container',
    Crown: 'visit_crown',
    CursorPosRequest: 'visit_cursor_pos_request',
    CurveTo: 'visit_curve_to',
    Ellipse: 'visit_ellipse',
    EllipticalArc: 'visit_elliptical_arc',
    EnumType: 'visit_enum_type',
    EnumValue: 'visit_enum_value',
    FieldExpr: 'visit_field_expr',
    FilterRotationContainer: 'visit_filter_rotation_container',
    FilterTranslationContainer: 'visit_filter_translation_container',
    FontDefinition: 'visit_font_definition',
    FontTable: 'visit_font_table',
    GlobalDefinitions: 'visit_global_definitions',
    GradientStopColor: 'visit_gradient_stop_color',
    GradientTable: 'visit_gradient_table',
    Hook: 'visit_hook',
    HorizontalLineTo: 'visit_horizontal_line_to',
    IdentifierExpr: 'visit_identifier_expr',
    Imported: 'visit_imported',
    ImportedConstant: 'visit_imported_constant',
    ImportedType: 'visit_imported_type',
    IndexExpr: 'visit_index_expr',
    IndexTexturePoint: 'visit_index_texture_point',
    IndexedPoint: 'visit_indexed_point',
    KeyboardEventListener: 'visit_keyboard_event_listener',
    Layer: 'visit_layer',
    Line: 'visit_line',
    LineStippleElement: 'visit_line_stipple_element',
    LineStippleSegment: 'visit_line_stipple_segment',
    LineStippleTable: 'visit_line_stipple_table',
    LineTo: 'visit_line_to',
    LineWidthElement: 'visit_line_width_element',
    LineWidthTable: 'visit_line_width_table',
    LinearGradientElement: 'visit_linear_gradient_element',
    LiteralExpr: 'visit_literal_expr',
    MaskContainer: 'visit_mask_container',
    MemVariable: 'visit_mem_variable',
    MoveTo: 'visit_move_to',
    NamedType: 'visit_named_type',
    NplicatorContainer: 'visit_nplicator_container',
    PanelContainer: 'visit_panel_container',
    Path: 'visit_path',
    PointerEventListener: 'visit_pointer_event_listener',
    PredefType: 'visit_predef_type',
    QuadraticCurveTo: 'visit_quadratic_curve_to',
    RadialGradientElement: 'visit_radial_gradient_element',
    Rectangle: 'visit_rectangle',
    RectangleArea: 'visit_rectangle_area',
    ReferenceContainer: 'visit_reference_container',
    ReferenceObject: 'visit_reference_object',
    RichText: 'visit_rich_text',
    RotationContainer: 'visit_rotation_container',
    Shape: 'visit_shape',
    ShapeArea: 'visit_shape_area',
    SmoothCurveTo: 'visit_smooth_curve_to',
    SmoothQuadraticCurveTo: 'visit_smooth_quadratic_curve_to',
    Specification: 'visit_specification',
    StaticBitmap: 'visit_static_bitmap',
    Stencil: 'visit_stencil',
    StructExpr: 'visit_struct_expr',
    StructFieldExpr: 'visit_struct_field_expr',
    StructFieldType: 'visit_struct_field_type',
    StructType: 'visit_struct_type',
    Text: 'visit_text',
    TextArea: 'visit_text_area',
    TextureElement: 'visit_texture_element',
    TextureTable: 'visit_texture_table',
    TranslationContainer: 'visit_translation_container',
    TypeDefinition: 'visit_type_definition',
    UnaryOpExpr: 'visit_unary_op_expr',
    Variable: 'visit_variable',
    VariableTable: 'visit_variable_table',
    VerticalLineTo: 'visit_vertical_line_to',
}
#}}visit

#%% end
