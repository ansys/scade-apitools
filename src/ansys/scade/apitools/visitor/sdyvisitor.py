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
        """Stub for SCADE Display 2023 R1."""
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

    def visit_angle_array_prop(self, angle_array_prop: AngleArrayProp, class_name: str, reference_name: str):
        self.visit_pluggable_property(angle_array_prop, class_name, reference_name)

    def visit_angle_prop(self, angle_prop: AngleProp, class_name: str, reference_name: str):
        self.visit_property(angle_prop, class_name, reference_name)

        reference = angle_prop.angle
        if reference:
            self.visit(reference, 'AngleProp', 'angle')

    def visit_arc(self, arc: Arc, class_name: str, reference_name: str):
        self.visit_graphic_object(arc, class_name, reference_name)

        reference = arc.center
        if reference:
            self.visit(reference, 'Arc', 'center')
        reference = arc.end_angle
        if reference:
            self.visit(reference, 'Arc', 'endAngle')
        reference = arc.fill_color
        if reference:
            self.visit(reference, 'Arc', 'fillColor')
        reference = arc.fill_opacity
        if reference:
            self.visit(reference, 'Arc', 'fillOpacity')
        reference = arc.gradient
        if reference:
            self.visit(reference, 'Arc', 'gradient')
        reference = arc.halo_color
        if reference:
            self.visit(reference, 'Arc', 'haloColor')
        reference = arc.haloing
        if reference:
            self.visit(reference, 'Arc', 'haloing')
        reference = arc.line_cap
        if reference:
            self.visit(reference, 'Arc', 'lineCap')
        reference = arc.line_stipple
        if reference:
            self.visit(reference, 'Arc', 'lineStipple')
        reference = arc.line_width
        if reference:
            self.visit(reference, 'Arc', 'lineWidth')
        reference = arc.modulate
        if reference:
            self.visit(reference, 'Arc', 'modulate')
        reference = arc.orientation
        if reference:
            self.visit(reference, 'Arc', 'orientation')
        reference = arc.outline_color
        if reference:
            self.visit(reference, 'Arc', 'outlineColor')
        reference = arc.outline_opacity
        if reference:
            self.visit(reference, 'Arc', 'outlineOpacity')
        reference = arc.polygon_smooth
        if reference:
            self.visit(reference, 'Arc', 'polygonSmooth')
        reference = arc.radius
        if reference:
            self.visit(reference, 'Arc', 'radius')
        reference = arc.start_angle
        if reference:
            self.visit(reference, 'Arc', 'startAngle')
        reference = arc.texture
        if reference:
            self.visit(reference, 'Arc', 'texture')
        reference = arc.visible
        if reference:
            self.visit(reference, 'Arc', 'visible')

    def visit_arc_ellipse(self, arc_ellipse: ArcEllipse, class_name: str, reference_name: str):
        self.visit_graphic_object(arc_ellipse, class_name, reference_name)

        reference = arc_ellipse.center
        if reference:
            self.visit(reference, 'ArcEllipse', 'center')
        reference = arc_ellipse.end_angle
        if reference:
            self.visit(reference, 'ArcEllipse', 'endAngle')
        reference = arc_ellipse.fill_color
        if reference:
            self.visit(reference, 'ArcEllipse', 'fillColor')
        reference = arc_ellipse.fill_opacity
        if reference:
            self.visit(reference, 'ArcEllipse', 'fillOpacity')
        reference = arc_ellipse.gradient
        if reference:
            self.visit(reference, 'ArcEllipse', 'gradient')
        reference = arc_ellipse.halo_color
        if reference:
            self.visit(reference, 'ArcEllipse', 'haloColor')
        reference = arc_ellipse.haloing
        if reference:
            self.visit(reference, 'ArcEllipse', 'haloing')
        reference = arc_ellipse.horz_radius
        if reference:
            self.visit(reference, 'ArcEllipse', 'horzRadius')
        reference = arc_ellipse.line_cap
        if reference:
            self.visit(reference, 'ArcEllipse', 'lineCap')
        reference = arc_ellipse.line_stipple
        if reference:
            self.visit(reference, 'ArcEllipse', 'lineStipple')
        reference = arc_ellipse.line_width
        if reference:
            self.visit(reference, 'ArcEllipse', 'lineWidth')
        reference = arc_ellipse.modulate
        if reference:
            self.visit(reference, 'ArcEllipse', 'modulate')
        reference = arc_ellipse.orientation
        if reference:
            self.visit(reference, 'ArcEllipse', 'orientation')
        reference = arc_ellipse.outline_color
        if reference:
            self.visit(reference, 'ArcEllipse', 'outlineColor')
        reference = arc_ellipse.outline_opacity
        if reference:
            self.visit(reference, 'ArcEllipse', 'outlineOpacity')
        reference = arc_ellipse.polygon_smooth
        if reference:
            self.visit(reference, 'ArcEllipse', 'polygonSmooth')
        reference = arc_ellipse.start_angle
        if reference:
            self.visit(reference, 'ArcEllipse', 'startAngle')
        reference = arc_ellipse.texture
        if reference:
            self.visit(reference, 'ArcEllipse', 'texture')
        reference = arc_ellipse.vert_radius
        if reference:
            self.visit(reference, 'ArcEllipse', 'vertRadius')
        reference = arc_ellipse.visible
        if reference:
            self.visit(reference, 'ArcEllipse', 'visible')

    def visit_arc_segment_prop(self, arc_segment_prop: ArcSegmentProp, class_name: str, reference_name: str):
        self.visit_property(arc_segment_prop, class_name, reference_name)

        reference = arc_segment_prop.angle
        if reference:
            self.visit(reference, 'ArcSegmentProp', 'angle')
        reference = arc_segment_prop.orientation
        if reference:
            self.visit(reference, 'ArcSegmentProp', 'orientation')

    def visit_array_expr(self, array_expr: ArrayExpr, class_name: str, reference_name: str):
        self.visit_expr(array_expr, class_name, reference_name)

    def visit_array_type(self, array_type: ArrayType, class_name: str, reference_name: str):
        self.visit_type(array_type, class_name, reference_name)

    def visit_assignment(self, assignment: Assignment, class_name: str, reference_name: str):
        self.visit_graphic_object(assignment, class_name, reference_name)

        reference = assignment.enable
        if reference:
            self.visit(reference, 'Assignment', 'enable')
        reference = assignment.input
        if reference:
            self.visit(reference, 'Assignment', 'input')
        reference = assignment.output
        if reference:
            self.visit(reference, 'Assignment', 'output')

    def visit_assignment_output_prop(self, assignment_output_prop: AssignmentOutputProp, class_name: str, reference_name: str):
        self.visit_property(assignment_output_prop, class_name, reference_name)

        reference = assignment_output_prop.expr
        if reference:
            self.visit(reference, 'AssignmentOutputProp', 'expr')

    def visit_behavior(self, behavior: Behavior, class_name: str, reference_name: str):
        self.visit_graphic_object(behavior, class_name, reference_name)

        reference = behavior.enable
        if reference:
            self.visit(reference, 'Behavior', 'enable')
        reference = behavior.file
        if reference:
            self.visit(reference, 'Behavior', 'file')
        reference = behavior.function
        if reference:
            self.visit(reference, 'Behavior', 'function')
        reference = behavior.input_parameters
        if reference:
            self.visit(reference, 'Behavior', 'inputParameters')
        reference = behavior.output_parameters
        if reference:
            self.visit(reference, 'Behavior', 'outputParameters')

    def visit_bi_font(self, bi_font: BiFont, class_name: str, reference_name: str):
        self.visit_graphic_object(bi_font, class_name, reference_name)

        reference = bi_font.first_font
        if reference:
            self.visit(reference, 'BiFont', 'firstFont')
        reference = bi_font.first_line_width
        if reference:
            self.visit(reference, 'BiFont', 'firstLineWidth')
        reference = bi_font.format
        if reference:
            self.visit(reference, 'BiFont', 'format')
        reference = bi_font.halo_color
        if reference:
            self.visit(reference, 'BiFont', 'haloColor')
        reference = bi_font.haloing
        if reference:
            self.visit(reference, 'BiFont', 'haloing')
        reference = bi_font.horiz_align
        if reference:
            self.visit(reference, 'BiFont', 'horizAlign')
        reference = bi_font.outline_color
        if reference:
            self.visit(reference, 'BiFont', 'outlineColor')
        reference = bi_font.position
        if reference:
            self.visit(reference, 'BiFont', 'position')
        reference = bi_font.second_font
        if reference:
            self.visit(reference, 'BiFont', 'secondFont')
        reference = bi_font.second_line_width
        if reference:
            self.visit(reference, 'BiFont', 'secondLineWidth')
        reference = bi_font.value
        if reference:
            self.visit(reference, 'BiFont', 'value')
        reference = bi_font.vert_align
        if reference:
            self.visit(reference, 'BiFont', 'vertAlign')
        reference = bi_font.visible
        if reference:
            self.visit(reference, 'BiFont', 'visible')

    def visit_bi_font_display_sign_prop(self, bi_font_display_sign_prop: BiFontDisplaySignProp, class_name: str, reference_name: str):
        self.visit_pluggable_property(bi_font_display_sign_prop, class_name, reference_name)

    def visit_binary_op_expr(self, binary_op_expr: BinaryOpExpr, class_name: str, reference_name: str):
        self.visit_expr(binary_op_expr, class_name, reference_name)

    def visit_bitmap(self, bitmap: Bitmap, class_name: str, reference_name: str):
        self.visit_graphic_object(bitmap, class_name, reference_name)

        reference = bitmap.position
        if reference:
            self.visit(reference, 'Bitmap', 'position')
        reference = bitmap.texture_id
        if reference:
            self.visit(reference, 'Bitmap', 'textureId')
        reference = bitmap.visible
        if reference:
            self.visit(reference, 'Bitmap', 'visible')

    def visit_boolean_array_prop(self, boolean_array_prop: BooleanArrayProp, class_name: str, reference_name: str):
        self.visit_pluggable_property(boolean_array_prop, class_name, reference_name)

    def visit_boolean_prop(self, boolean_prop: BooleanProp, class_name: str, reference_name: str):
        self.visit_pluggable_property(boolean_prop, class_name, reference_name)

    def visit_circle(self, circle: Circle, class_name: str, reference_name: str):
        self.visit_graphic_object(circle, class_name, reference_name)

        reference = circle.center
        if reference:
            self.visit(reference, 'Circle', 'center')
        reference = circle.fill_color
        if reference:
            self.visit(reference, 'Circle', 'fillColor')
        reference = circle.fill_opacity
        if reference:
            self.visit(reference, 'Circle', 'fillOpacity')
        reference = circle.gradient
        if reference:
            self.visit(reference, 'Circle', 'gradient')
        reference = circle.halo_color
        if reference:
            self.visit(reference, 'Circle', 'haloColor')
        reference = circle.haloing
        if reference:
            self.visit(reference, 'Circle', 'haloing')
        reference = circle.line_cap
        if reference:
            self.visit(reference, 'Circle', 'lineCap')
        reference = circle.line_stipple
        if reference:
            self.visit(reference, 'Circle', 'lineStipple')
        reference = circle.line_width
        if reference:
            self.visit(reference, 'Circle', 'lineWidth')
        reference = circle.modulate
        if reference:
            self.visit(reference, 'Circle', 'modulate')
        reference = circle.outline_color
        if reference:
            self.visit(reference, 'Circle', 'outlineColor')
        reference = circle.outline_opacity
        if reference:
            self.visit(reference, 'Circle', 'outlineOpacity')
        reference = circle.polygon_smooth
        if reference:
            self.visit(reference, 'Circle', 'polygonSmooth')
        reference = circle.radius
        if reference:
            self.visit(reference, 'Circle', 'radius')
        reference = circle.texture
        if reference:
            self.visit(reference, 'Circle', 'texture')
        reference = circle.visible
        if reference:
            self.visit(reference, 'Circle', 'visible')

    def visit_circle_area(self, circle_area: CircleArea, class_name: str, reference_name: str):
        self.visit_graphic_object(circle_area, class_name, reference_name)

        reference = circle_area.angle
        if reference:
            self.visit(reference, 'CircleArea', 'angle')
        reference = circle_area.center
        if reference:
            self.visit(reference, 'CircleArea', 'center')
        reference = circle_area.enable
        if reference:
            self.visit(reference, 'CircleArea', 'enable')
        reference = circle_area.inside
        if reference:
            self.visit(reference, 'CircleArea', 'inside')
        reference = circle_area.percent
        if reference:
            self.visit(reference, 'CircleArea', 'percent')
        reference = circle_area.pointer_id
        if reference:
            self.visit(reference, 'CircleArea', 'pointerId')
        reference = circle_area.radius
        if reference:
            self.visit(reference, 'CircleArea', 'radius')

    def visit_clip_box(self, clip_box: ClipBox, class_name: str, reference_name: str):
        self.visit_graphic_object(clip_box, class_name, reference_name)

        reference = clip_box.clip_inside
        if reference:
            self.visit(reference, 'ClipBox', 'clipInside')
        reference = clip_box.first_point
        if reference:
            self.visit(reference, 'ClipBox', 'firstPoint')
        reference = clip_box.mask_activity
        if reference:
            self.visit(reference, 'ClipBox', 'maskActivity')
        reference = clip_box.third_point
        if reference:
            self.visit(reference, 'ClipBox', 'thirdPoint')

    def visit_clip_plane(self, clip_plane: ClipPlane, class_name: str, reference_name: str):
        self.visit_graphic_object(clip_plane, class_name, reference_name)

        reference = clip_plane.clip_angle
        if reference:
            self.visit(reference, 'ClipPlane', 'clipAngle')
        reference = clip_plane.clip_start_point
        if reference:
            self.visit(reference, 'ClipPlane', 'clipStartPoint')
        reference = clip_plane.mask_activity
        if reference:
            self.visit(reference, 'ClipPlane', 'maskActivity')
        reference = clip_plane.orientation
        if reference:
            self.visit(reference, 'ClipPlane', 'orientation')

    def visit_close_path(self, close_path: ClosePath, class_name: str, reference_name: str):
        self.visit_command(close_path, class_name, reference_name)

    def visit_color_element(self, color_element: ColorElement, class_name: str, reference_name: str):
        pass

    def visit_color_table(self, color_table: ColorTable, class_name: str, reference_name: str):
        for reference in color_table.elements:
            self.visit(reference, 'ColorTable', 'Elements')

    def visit_command(self, command: Command, class_name: str, reference_name: str):
        pass

    def visit_commands_prop(self, commands_prop: CommandsProp, class_name: str, reference_name: str):
        self.visit_property(commands_prop, class_name, reference_name)

    def visit_comment(self, comment: Comment, class_name: str, reference_name: str):
        pass

    def visit_cond_container(self, cond_container: CondContainer, class_name: str, reference_name: str):
        self.visit_a_container(cond_container, class_name, reference_name)

        reference = cond_container.index
        if reference:
            self.visit(reference, 'CondContainer', 'index')
        reference = cond_container.indexes
        if reference:
            self.visit(reference, 'CondContainer', 'indexes')
        reference = cond_container.orientation
        if reference:
            self.visit(reference, 'CondContainer', 'orientation')
        reference = cond_container.origin
        if reference:
            self.visit(reference, 'CondContainer', 'origin')
        reference = cond_container.priority
        if reference:
            self.visit(reference, 'CondContainer', 'priority')
        reference = cond_container.rotate
        if reference:
            self.visit(reference, 'CondContainer', 'rotate')
        reference = cond_container.scale
        if reference:
            self.visit(reference, 'CondContainer', 'scale')
        reference = cond_container.visible
        if reference:
            self.visit(reference, 'CondContainer', 'visible')

    def visit_conditional_expr(self, conditional_expr: ConditionalExpr, class_name: str, reference_name: str):
        self.visit_expr(conditional_expr, class_name, reference_name)

    def visit_conditional_index_prop(self, conditional_index_prop: ConditionalIndexProp, class_name: str, reference_name: str):
        self.visit_pluggable_property(conditional_index_prop, class_name, reference_name)

    def visit_constant_definition(self, constant_definition: ConstantDefinition, class_name: str, reference_name: str):
        self.visit_global_definition(constant_definition, class_name, reference_name)

        reference = constant_definition.definition
        if reference:
            self.visit(reference, 'ConstantDefinition', 'definition')

    def visit_container(self, container: Container, class_name: str, reference_name: str):
        self.visit_a_container(container, class_name, reference_name)

        reference = container.orientation
        if reference:
            self.visit(reference, 'Container', 'orientation')
        reference = container.origin
        if reference:
            self.visit(reference, 'Container', 'origin')
        reference = container.priority
        if reference:
            self.visit(reference, 'Container', 'priority')
        reference = container.rotate
        if reference:
            self.visit(reference, 'Container', 'rotate')
        reference = container.scale
        if reference:
            self.visit(reference, 'Container', 'scale')
        reference = container.static
        if reference:
            self.visit(reference, 'Container', 'static')
        reference = container.visible
        if reference:
            self.visit(reference, 'Container', 'visible')

    def visit_coordinate_point(self, coordinate_point: CoordinatePoint, class_name: str, reference_name: str):
        self.visit_property(coordinate_point, class_name, reference_name)

        reference = coordinate_point.x
        if reference:
            self.visit(reference, 'CoordinatePoint', 'x')
        reference = coordinate_point.y
        if reference:
            self.visit(reference, 'CoordinatePoint', 'y')

    def visit_crown(self, crown: Crown, class_name: str, reference_name: str):
        self.visit_graphic_object(crown, class_name, reference_name)

        reference = crown.center
        if reference:
            self.visit(reference, 'Crown', 'center')
        reference = crown.end_angle
        if reference:
            self.visit(reference, 'Crown', 'endAngle')
        reference = crown.fill_color
        if reference:
            self.visit(reference, 'Crown', 'fillColor')
        reference = crown.fill_opacity
        if reference:
            self.visit(reference, 'Crown', 'fillOpacity')
        reference = crown.gradient
        if reference:
            self.visit(reference, 'Crown', 'gradient')
        reference = crown.halo_color
        if reference:
            self.visit(reference, 'Crown', 'haloColor')
        reference = crown.haloing
        if reference:
            self.visit(reference, 'Crown', 'haloing')
        reference = crown.line_cap
        if reference:
            self.visit(reference, 'Crown', 'lineCap')
        reference = crown.line_stipple
        if reference:
            self.visit(reference, 'Crown', 'lineStipple')
        reference = crown.line_width
        if reference:
            self.visit(reference, 'Crown', 'lineWidth')
        reference = crown.modulate
        if reference:
            self.visit(reference, 'Crown', 'modulate')
        reference = crown.orientation
        if reference:
            self.visit(reference, 'Crown', 'orientation')
        reference = crown.outline_color
        if reference:
            self.visit(reference, 'Crown', 'outlineColor')
        reference = crown.outline_opacity
        if reference:
            self.visit(reference, 'Crown', 'outlineOpacity')
        reference = crown.polygon_smooth
        if reference:
            self.visit(reference, 'Crown', 'polygonSmooth')
        reference = crown.radius
        if reference:
            self.visit(reference, 'Crown', 'radius')
        reference = crown.start_angle
        if reference:
            self.visit(reference, 'Crown', 'startAngle')
        reference = crown.texture
        if reference:
            self.visit(reference, 'Crown', 'texture')
        reference = crown.thickness
        if reference:
            self.visit(reference, 'Crown', 'thickness')
        reference = crown.visible
        if reference:
            self.visit(reference, 'Crown', 'visible')

    def visit_cursor_pos_request(self, cursor_pos_request: CursorPosRequest, class_name: str, reference_name: str):
        self.visit_graphic_object(cursor_pos_request, class_name, reference_name)

        reference = cursor_pos_request.cursor_id
        if reference:
            self.visit(reference, 'CursorPosRequest', 'cursorId')
        reference = cursor_pos_request.cursor_position
        if reference:
            self.visit(reference, 'CursorPosRequest', 'cursorPosition')
        reference = cursor_pos_request.enable
        if reference:
            self.visit(reference, 'CursorPosRequest', 'enable')

    def visit_curve_to(self, curve_to: CurveTo, class_name: str, reference_name: str):
        self.visit_command(curve_to, class_name, reference_name)

        reference = curve_to.end_point
        if reference:
            self.visit(reference, 'CurveTo', 'endPoint')
        reference = curve_to.first_control_point
        if reference:
            self.visit(reference, 'CurveTo', 'firstControlPoint')
        reference = curve_to.second_control_point
        if reference:
            self.visit(reference, 'CurveTo', 'secondControlPoint')

    def visit_ellipse(self, ellipse: Ellipse, class_name: str, reference_name: str):
        self.visit_graphic_object(ellipse, class_name, reference_name)

        reference = ellipse.center
        if reference:
            self.visit(reference, 'Ellipse', 'center')
        reference = ellipse.fill_color
        if reference:
            self.visit(reference, 'Ellipse', 'fillColor')
        reference = ellipse.fill_opacity
        if reference:
            self.visit(reference, 'Ellipse', 'fillOpacity')
        reference = ellipse.gradient
        if reference:
            self.visit(reference, 'Ellipse', 'gradient')
        reference = ellipse.halo_color
        if reference:
            self.visit(reference, 'Ellipse', 'haloColor')
        reference = ellipse.haloing
        if reference:
            self.visit(reference, 'Ellipse', 'haloing')
        reference = ellipse.horz_radius
        if reference:
            self.visit(reference, 'Ellipse', 'horzRadius')
        reference = ellipse.line_cap
        if reference:
            self.visit(reference, 'Ellipse', 'lineCap')
        reference = ellipse.line_stipple
        if reference:
            self.visit(reference, 'Ellipse', 'lineStipple')
        reference = ellipse.line_width
        if reference:
            self.visit(reference, 'Ellipse', 'lineWidth')
        reference = ellipse.modulate
        if reference:
            self.visit(reference, 'Ellipse', 'modulate')
        reference = ellipse.outline_color
        if reference:
            self.visit(reference, 'Ellipse', 'outlineColor')
        reference = ellipse.outline_opacity
        if reference:
            self.visit(reference, 'Ellipse', 'outlineOpacity')
        reference = ellipse.polygon_smooth
        if reference:
            self.visit(reference, 'Ellipse', 'polygonSmooth')
        reference = ellipse.texture
        if reference:
            self.visit(reference, 'Ellipse', 'texture')
        reference = ellipse.vert_radius
        if reference:
            self.visit(reference, 'Ellipse', 'vertRadius')
        reference = ellipse.visible
        if reference:
            self.visit(reference, 'Ellipse', 'visible')

    def visit_elliptical_arc(self, elliptical_arc: EllipticalArc, class_name: str, reference_name: str):
        self.visit_command(elliptical_arc, class_name, reference_name)

        reference = elliptical_arc.end_point
        if reference:
            self.visit(reference, 'EllipticalArc', 'endPoint')
        reference = elliptical_arc.large_arc_flag
        if reference:
            self.visit(reference, 'EllipticalArc', 'largeArcFlag')
        reference = elliptical_arc.sweep_flag
        if reference:
            self.visit(reference, 'EllipticalArc', 'sweepFlag')
        reference = elliptical_arc.x_axis_rotation
        if reference:
            self.visit(reference, 'EllipticalArc', 'xAxisRotation')
        reference = elliptical_arc.x_radius
        if reference:
            self.visit(reference, 'EllipticalArc', 'xRadius')
        reference = elliptical_arc.y_radius
        if reference:
            self.visit(reference, 'EllipticalArc', 'yRadius')

    def visit_enum_type(self, enum_type: EnumType, class_name: str, reference_name: str):
        self.visit_global_type(enum_type, class_name, reference_name)

    def visit_enum_value(self, enum_value: EnumValue, class_name: str, reference_name: str):
        pass

    def visit_expr(self, expr: Expr, class_name: str, reference_name: str):
        self.visit_global_constant(expr, class_name, reference_name)

    def visit_field_expr(self, field_expr: FieldExpr, class_name: str, reference_name: str):
        self.visit_expr(field_expr, class_name, reference_name)

    def visit_file_prop(self, file_prop: FileProp, class_name: str, reference_name: str):
        self.visit_property(file_prop, class_name, reference_name)

    def visit_filter_rotation_container(self, filter_rotation_container: FilterRotationContainer, class_name: str, reference_name: str):
        self.visit_a_container(filter_rotation_container, class_name, reference_name)

        reference = filter_rotation_container.end_rotation_angle
        if reference:
            self.visit(reference, 'FilterRotationContainer', 'endRotationAngle')
        reference = filter_rotation_container.end_rotation_locked
        if reference:
            self.visit(reference, 'FilterRotationContainer', 'endRotationLocked')
        reference = filter_rotation_container.end_rotation_value
        if reference:
            self.visit(reference, 'FilterRotationContainer', 'endRotationValue')
        reference = filter_rotation_container.orientation
        if reference:
            self.visit(reference, 'FilterRotationContainer', 'orientation')
        reference = filter_rotation_container.origin
        if reference:
            self.visit(reference, 'FilterRotationContainer', 'origin')
        reference = filter_rotation_container.priority
        if reference:
            self.visit(reference, 'FilterRotationContainer', 'priority')
        reference = filter_rotation_container.start_rotation_angle
        if reference:
            self.visit(reference, 'FilterRotationContainer', 'startRotationAngle')
        reference = filter_rotation_container.start_rotation_locked
        if reference:
            self.visit(reference, 'FilterRotationContainer', 'startRotationLocked')
        reference = filter_rotation_container.start_rotation_value
        if reference:
            self.visit(reference, 'FilterRotationContainer', 'startRotationValue')
        reference = filter_rotation_container.visible
        if reference:
            self.visit(reference, 'FilterRotationContainer', 'visible')

    def visit_filter_translation_container(self, filter_translation_container: FilterTranslationContainer, class_name: str, reference_name: str):
        self.visit_a_container(filter_translation_container, class_name, reference_name)

        reference = filter_translation_container.end_translation_locked
        if reference:
            self.visit(reference, 'FilterTranslationContainer', 'endTranslationLocked')
        reference = filter_translation_container.end_translation_point
        if reference:
            self.visit(reference, 'FilterTranslationContainer', 'endTranslationPoint')
        reference = filter_translation_container.end_translation_value
        if reference:
            self.visit(reference, 'FilterTranslationContainer', 'endTranslationValue')
        reference = filter_translation_container.origin
        if reference:
            self.visit(reference, 'FilterTranslationContainer', 'origin')
        reference = filter_translation_container.priority
        if reference:
            self.visit(reference, 'FilterTranslationContainer', 'priority')
        reference = filter_translation_container.start_translation_locked
        if reference:
            self.visit(reference, 'FilterTranslationContainer', 'startTranslationLocked')
        reference = filter_translation_container.start_translation_point
        if reference:
            self.visit(reference, 'FilterTranslationContainer', 'startTranslationPoint')
        reference = filter_translation_container.start_translation_value
        if reference:
            self.visit(reference, 'FilterTranslationContainer', 'startTranslationValue')
        reference = filter_translation_container.visible
        if reference:
            self.visit(reference, 'FilterTranslationContainer', 'visible')

    def visit_font_definition(self, font_definition: FontDefinition, class_name: str, reference_name: str):
        pass

    def visit_font_table(self, font_table: FontTable, class_name: str, reference_name: str):
        for reference in font_table.elements:
            self.visit(reference, 'FontTable', 'elements')

    def visit_format_prop(self, format_prop: FormatProp, class_name: str, reference_name: str):
        self.visit_property(format_prop, class_name, reference_name)

        reference = format_prop.display_sign
        if reference:
            self.visit(reference, 'FormatProp', 'displaySign')
        reference = format_prop.fractional_part
        if reference:
            self.visit(reference, 'FormatProp', 'fractionalPart')
        reference = format_prop.integral_part
        if reference:
            self.visit(reference, 'FormatProp', 'integralPart')
        reference = format_prop.leading_zeros
        if reference:
            self.visit(reference, 'FormatProp', 'leadingZeros')
        reference = format_prop.second_font_pos
        if reference:
            self.visit(reference, 'FormatProp', 'secondFontPos')

    def visit_function_prop(self, function_prop: FunctionProp, class_name: str, reference_name: str):
        self.visit_property(function_prop, class_name, reference_name)

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
        reference = graphic_object.oid
        if reference:
            self.visit(reference, 'GraphicObject', 'oid')

    def visit_hook(self, hook: Hook, class_name: str, reference_name: str):
        self.visit_graphic_object(hook, class_name, reference_name)

        reference = hook.index
        if reference:
            self.visit(reference, 'Hook', 'index')
        reference = hook.visible
        if reference:
            self.visit(reference, 'Hook', 'visible')

    def visit_horizontal_line_to(self, horizontal_line_to: HorizontalLineTo, class_name: str, reference_name: str):
        self.visit_command(horizontal_line_to, class_name, reference_name)

        reference = horizontal_line_to.end_x
        if reference:
            self.visit(reference, 'HorizontalLineTo', 'endX')

    def visit_identifier_expr(self, identifier_expr: IdentifierExpr, class_name: str, reference_name: str):
        self.visit_expr(identifier_expr, class_name, reference_name)

    def visit_imported(self, imported: Imported, class_name: str, reference_name: str):
        self.visit_graphic_object(imported, class_name, reference_name)

        reference = imported.enable
        if reference:
            self.visit(reference, 'Imported', 'enable')
        reference = imported.function
        if reference:
            self.visit(reference, 'Imported', 'function')
        reference = imported.input_parameters
        if reference:
            self.visit(reference, 'Imported', 'inputParameters')
        reference = imported.memory
        if reference:
            self.visit(reference, 'Imported', 'memory')
        reference = imported.output_parameters
        if reference:
            self.visit(reference, 'Imported', 'outputParameters')
        reference = imported.restore_states
        if reference:
            self.visit(reference, 'Imported', 'restoreStates')

    def visit_imported_constant(self, imported_constant: ImportedConstant, class_name: str, reference_name: str):
        self.visit_global_constant(imported_constant, class_name, reference_name)

    def visit_imported_type(self, imported_type: ImportedType, class_name: str, reference_name: str):
        self.visit_global_type(imported_type, class_name, reference_name)

    def visit_index_expr(self, index_expr: IndexExpr, class_name: str, reference_name: str):
        self.visit_expr(index_expr, class_name, reference_name)

    def visit_index_texture_point(self, index_texture_point: IndexTexturePoint, class_name: str, reference_name: str):
        reference = index_texture_point.arc_segment
        if reference:
            self.visit(reference, 'IndexTexturePoint', 'arcSegment')
        reference = index_texture_point.point
        if reference:
            self.visit(reference, 'IndexTexturePoint', 'point')

    def visit_indexed_point(self, indexed_point: IndexedPoint, class_name: str, reference_name: str):
        reference = indexed_point.arc_segment
        if reference:
            self.visit(reference, 'IndexedPoint', 'arcSegment')
        reference = indexed_point.point
        if reference:
            self.visit(reference, 'IndexedPoint', 'point')

    def visit_indexed_points_prop(self, indexed_points_prop: IndexedPointsProp, class_name: str, reference_name: str):
        self.visit_property(indexed_points_prop, class_name, reference_name)

        for reference in indexed_points_prop.points:
            self.visit(reference, 'IndexedPointsProp', 'points')

    def visit_indexed_texture_points_prop(self, indexed_texture_points_prop: IndexedTexturePointsProp, class_name: str, reference_name: str):
        self.visit_property(indexed_texture_points_prop, class_name, reference_name)

        for reference in indexed_texture_points_prop.points:
            self.visit(reference, 'IndexedTexturePointsProp', 'points')

    def visit_indexes_prop(self, indexes_prop: IndexesProp, class_name: str, reference_name: str):
        self.visit_property(indexes_prop, class_name, reference_name)

    def visit_input_param_prop(self, input_param_prop: InputParamProp, class_name: str, reference_name: str):
        self.visit_param_prop(input_param_prop, class_name, reference_name)

        reference = input_param_prop.init
        if reference:
            self.visit(reference, 'InputParamProp', 'init')

    def visit_input_parameters_prop(self, input_parameters_prop: InputParametersProp, class_name: str, reference_name: str):
        self.visit_property(input_parameters_prop, class_name, reference_name)

        for reference in input_parameters_prop.parameters:
            self.visit(reference, 'InputParametersProp', 'parameters')

    def visit_input_prop(self, input_prop: InputProp, class_name: str, reference_name: str):
        self.visit_pluggable_property(input_prop, class_name, reference_name)

        reference = input_prop.init
        if reference:
            self.visit(reference, 'InputProp', 'init')

    def visit_integer_prop(self, integer_prop: IntegerProp, class_name: str, reference_name: str):
        self.visit_pluggable_property(integer_prop, class_name, reference_name)

    def visit_keyboard_event_listener(self, keyboard_event_listener: KeyboardEventListener, class_name: str, reference_name: str):
        self.visit_graphic_object(keyboard_event_listener, class_name, reference_name)

        reference = keyboard_event_listener.enable
        if reference:
            self.visit(reference, 'KeyboardEventListener', 'enable')
        reference = keyboard_event_listener.event_id
        if reference:
            self.visit(reference, 'KeyboardEventListener', 'eventId')
        reference = keyboard_event_listener.key_code
        if reference:
            self.visit(reference, 'KeyboardEventListener', 'keyCode')
        reference = keyboard_event_listener.modifiers
        if reference:
            self.visit(reference, 'KeyboardEventListener', 'modifiers')
        reference = keyboard_event_listener.pressed
        if reference:
            self.visit(reference, 'KeyboardEventListener', 'pressed')
        reference = keyboard_event_listener.released
        if reference:
            self.visit(reference, 'KeyboardEventListener', 'released')

    def visit_layer(self, layer: Layer, class_name: str, reference_name: str):
        self.visit_a_container(layer, class_name, reference_name)

        reference = layer.declaration
        if reference:
            self.visit(reference, 'Layer', 'declaration')
        reference = layer.id
        if reference:
            self.visit(reference, 'Layer', 'id')
        reference = layer.origin
        if reference:
            self.visit(reference, 'Layer', 'origin')
        reference = layer.visible
        if reference:
            self.visit(reference, 'Layer', 'visible')

    def visit_line(self, line: Line, class_name: str, reference_name: str):
        self.visit_graphic_object(line, class_name, reference_name)

        reference = line.halo_color
        if reference:
            self.visit(reference, 'Line', 'haloColor')
        reference = line.haloing
        if reference:
            self.visit(reference, 'Line', 'haloing')
        reference = line.line_cap
        if reference:
            self.visit(reference, 'Line', 'lineCap')
        reference = line.line_stipple
        if reference:
            self.visit(reference, 'Line', 'lineStipple')
        reference = line.line_width
        if reference:
            self.visit(reference, 'Line', 'lineWidth')
        reference = line.outline_color
        if reference:
            self.visit(reference, 'Line', 'outlineColor')
        reference = line.outline_opacity
        if reference:
            self.visit(reference, 'Line', 'outlineOpacity')
        reference = line.points
        if reference:
            self.visit(reference, 'Line', 'points')
        reference = line.visible
        if reference:
            self.visit(reference, 'Line', 'visible')

    def visit_line_cap_prop(self, line_cap_prop: LineCapProp, class_name: str, reference_name: str):
        self.visit_pluggable_property(line_cap_prop, class_name, reference_name)

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

        reference = line_to.end_point
        if reference:
            self.visit(reference, 'LineTo', 'endPoint')

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

        reference = mask_container.clip_inside
        if reference:
            self.visit(reference, 'MaskContainer', 'clipInside')
        reference = mask_container.mask_activity
        if reference:
            self.visit(reference, 'MaskContainer', 'maskActivity')
        reference = mask_container.orientation
        if reference:
            self.visit(reference, 'MaskContainer', 'orientation')
        reference = mask_container.origin
        if reference:
            self.visit(reference, 'MaskContainer', 'origin')
        reference = mask_container.rotate
        if reference:
            self.visit(reference, 'MaskContainer', 'rotate')
        reference = mask_container.scale
        if reference:
            self.visit(reference, 'MaskContainer', 'scale')

    def visit_mem_variable(self, mem_variable: MemVariable, class_name: str, reference_name: str):
        self.visit_variable(mem_variable, class_name, reference_name)

    def visit_move_to(self, move_to: MoveTo, class_name: str, reference_name: str):
        self.visit_command(move_to, class_name, reference_name)

        reference = move_to.start_point
        if reference:
            self.visit(reference, 'MoveTo', 'startPoint')

    def visit_named_type(self, named_type: NamedType, class_name: str, reference_name: str):
        self.visit_type(named_type, class_name, reference_name)

    def visit_node_function_prop(self, node_function_prop: NodeFunctionProp, class_name: str, reference_name: str):
        self.visit_property(node_function_prop, class_name, reference_name)

    def visit_nplicator_container(self, nplicator_container: NplicatorContainer, class_name: str, reference_name: str):
        self.visit_a_container(nplicator_container, class_name, reference_name)

        reference = nplicator_container.constant_parameters
        if reference:
            self.visit(reference, 'NplicatorContainer', 'constantParameters')
        reference = nplicator_container.file
        if reference:
            self.visit(reference, 'NplicatorContainer', 'file')
        reference = nplicator_container.input_parameters
        if reference:
            self.visit(reference, 'NplicatorContainer', 'inputParameters')
        reference = nplicator_container.orientation
        if reference:
            self.visit(reference, 'NplicatorContainer', 'orientation')
        reference = nplicator_container.origin
        if reference:
            self.visit(reference, 'NplicatorContainer', 'origin')
        reference = nplicator_container.output_parameters
        if reference:
            self.visit(reference, 'NplicatorContainer', 'outputParameters')
        reference = nplicator_container.replication
        if reference:
            self.visit(reference, 'NplicatorContainer', 'replication')
        reference = nplicator_container.rotate
        if reference:
            self.visit(reference, 'NplicatorContainer', 'rotate')
        reference = nplicator_container.scale
        if reference:
            self.visit(reference, 'NplicatorContainer', 'scale')
        reference = nplicator_container.visible
        if reference:
            self.visit(reference, 'NplicatorContainer', 'visible')

    def visit_oid(self, oid: Oid, class_name: str, reference_name: str):
        pass

    def visit_orientation_prop(self, orientation_prop: OrientationProp, class_name: str, reference_name: str):
        self.visit_property(orientation_prop, class_name, reference_name)

    def visit_output_param_prop(self, output_param_prop: OutputParamProp, class_name: str, reference_name: str):
        self.visit_param_prop(output_param_prop, class_name, reference_name)

    def visit_output_parameters_prop(self, output_parameters_prop: OutputParametersProp, class_name: str, reference_name: str):
        self.visit_property(output_parameters_prop, class_name, reference_name)

        for reference in output_parameters_prop.output_parameters:
            self.visit(reference, 'OutputParametersProp', 'outputParameters')

    def visit_output_point_prop(self, output_point_prop: OutputPointProp, class_name: str, reference_name: str):
        self.visit_property(output_point_prop, class_name, reference_name)

        reference = output_point_prop.point
        if reference:
            self.visit(reference, 'OutputPointProp', 'point')
        reference = output_point_prop.x
        if reference:
            self.visit(reference, 'OutputPointProp', 'x')
        reference = output_point_prop.y
        if reference:
            self.visit(reference, 'OutputPointProp', 'y')

    def visit_output_prop(self, output_prop: OutputProp, class_name: str, reference_name: str):
        self.visit_assignment_output_prop(output_prop, class_name, reference_name)

    def visit_panel_container(self, panel_container: PanelContainer, class_name: str, reference_name: str):
        self.visit_a_container(panel_container, class_name, reference_name)

        reference = panel_container.height
        if reference:
            self.visit(reference, 'PanelContainer', 'height')
        reference = panel_container.origin
        if reference:
            self.visit(reference, 'PanelContainer', 'origin')
        reference = panel_container.priority
        if reference:
            self.visit(reference, 'PanelContainer', 'priority')
        reference = panel_container.visible
        if reference:
            self.visit(reference, 'PanelContainer', 'visible')
        reference = panel_container.width
        if reference:
            self.visit(reference, 'PanelContainer', 'width')

    def visit_param_prop(self, param_prop: ParamProp, class_name: str, reference_name: str):
        self.visit_pluggable_property(param_prop, class_name, reference_name)

        reference = param_prop.type
        if reference:
            self.visit(reference, 'ParamProp', 'type')

    def visit_path(self, path: Path, class_name: str, reference_name: str):
        self.visit_graphic_object(path, class_name, reference_name)

        reference = path.commands
        if reference:
            self.visit(reference, 'Path', 'commands')
        reference = path.fill_color
        if reference:
            self.visit(reference, 'Path', 'fillColor')
        reference = path.fill_opacity
        if reference:
            self.visit(reference, 'Path', 'fillOpacity')
        reference = path.gradient
        if reference:
            self.visit(reference, 'Path', 'gradient')
        reference = path.halo_color
        if reference:
            self.visit(reference, 'Path', 'haloColor')
        reference = path.haloing
        if reference:
            self.visit(reference, 'Path', 'haloing')
        reference = path.line_cap
        if reference:
            self.visit(reference, 'Path', 'lineCap')
        reference = path.line_stipple
        if reference:
            self.visit(reference, 'Path', 'lineStipple')
        reference = path.line_width
        if reference:
            self.visit(reference, 'Path', 'lineWidth')
        reference = path.modulate
        if reference:
            self.visit(reference, 'Path', 'modulate')
        reference = path.outline_color
        if reference:
            self.visit(reference, 'Path', 'outlineColor')
        reference = path.outline_opacity
        if reference:
            self.visit(reference, 'Path', 'outlineOpacity')
        reference = path.polygon_smooth
        if reference:
            self.visit(reference, 'Path', 'polygonSmooth')
        reference = path.tessellate
        if reference:
            self.visit(reference, 'Path', 'tessellate')
        reference = path.texture
        if reference:
            self.visit(reference, 'Path', 'texture')
        reference = path.visible
        if reference:
            self.visit(reference, 'Path', 'visible')

    def visit_pluggable_property(self, pluggable_property: PluggableProperty, class_name: str, reference_name: str):
        self.visit_property(pluggable_property, class_name, reference_name)

        reference = pluggable_property.addr
        if reference:
            self.visit(reference, 'PluggableProperty', 'addr')
        reference = pluggable_property.expr
        if reference:
            self.visit(reference, 'PluggableProperty', 'expr')

    def visit_point_array_prop(self, point_array_prop: PointArrayProp, class_name: str, reference_name: str):
        self.visit_property(point_array_prop, class_name, reference_name)

        reference = point_array_prop.x
        if reference:
            self.visit(reference, 'PointArrayProp', 'x')
        reference = point_array_prop.y
        if reference:
            self.visit(reference, 'PointArrayProp', 'y')

    def visit_point_property(self, point_property: PointProperty, class_name: str, reference_name: str):
        self.visit_coordinate_point(point_property, class_name, reference_name)

        reference = point_property.interp
        if reference:
            self.visit(reference, 'PointProperty', 'interp')

    def visit_point_texture_prop(self, point_texture_prop: PointTextureProp, class_name: str, reference_name: str):
        self.visit_coordinate_point(point_texture_prop, class_name, reference_name)

        reference = point_texture_prop.interp
        if reference:
            self.visit(reference, 'PointTextureProp', 'interp')
        reference = point_texture_prop.u
        if reference:
            self.visit(reference, 'PointTextureProp', 'u')
        reference = point_texture_prop.v
        if reference:
            self.visit(reference, 'PointTextureProp', 'v')

    def visit_pointer_event_listener(self, pointer_event_listener: PointerEventListener, class_name: str, reference_name: str):
        self.visit_graphic_object(pointer_event_listener, class_name, reference_name)

        reference = pointer_event_listener.button
        if reference:
            self.visit(reference, 'PointerEventListener', 'button')
        reference = pointer_event_listener.enable
        if reference:
            self.visit(reference, 'PointerEventListener', 'enable')
        reference = pointer_event_listener.event_id
        if reference:
            self.visit(reference, 'PointerEventListener', 'eventId')
        reference = pointer_event_listener.modifiers
        if reference:
            self.visit(reference, 'PointerEventListener', 'modifiers')
        reference = pointer_event_listener.pointer_position
        if reference:
            self.visit(reference, 'PointerEventListener', 'pointerPosition')
        reference = pointer_event_listener.pressed
        if reference:
            self.visit(reference, 'PointerEventListener', 'pressed')
        reference = pointer_event_listener.relative
        if reference:
            self.visit(reference, 'PointerEventListener', 'relative')
        reference = pointer_event_listener.released
        if reference:
            self.visit(reference, 'PointerEventListener', 'released')

    def visit_points_prop(self, points_prop: PointsProp, class_name: str, reference_name: str):
        self.visit_property(points_prop, class_name, reference_name)

        for reference in points_prop.point:
            self.visit(reference, 'PointsProp', 'point')

    def visit_predef_type(self, predef_type: PredefType, class_name: str, reference_name: str):
        self.visit_type(predef_type, class_name, reference_name)

    def visit_priority_prop(self, priority_prop: PriorityProp, class_name: str, reference_name: str):
        self.visit_pluggable_property(priority_prop, class_name, reference_name)

    def visit_property(self, property: Property, class_name: str, reference_name: str):
        pass

    def visit_quadratic_curve_to(self, quadratic_curve_to: QuadraticCurveTo, class_name: str, reference_name: str):
        self.visit_command(quadratic_curve_to, class_name, reference_name)

        reference = quadratic_curve_to.control_point
        if reference:
            self.visit(reference, 'QuadraticCurveTo', 'controlPoint')
        reference = quadratic_curve_to.end_point
        if reference:
            self.visit(reference, 'QuadraticCurveTo', 'endPoint')

    def visit_radial_gradient_element(self, radial_gradient_element: RadialGradientElement, class_name: str, reference_name: str):
        self.visit_gradient_element(radial_gradient_element, class_name, reference_name)

    def visit_real_array_prop(self, real_array_prop: RealArrayProp, class_name: str, reference_name: str):
        self.visit_pluggable_property(real_array_prop, class_name, reference_name)

    def visit_real_prop(self, real_prop: RealProp, class_name: str, reference_name: str):
        self.visit_pluggable_property(real_prop, class_name, reference_name)

    def visit_rectangle(self, rectangle: Rectangle, class_name: str, reference_name: str):
        self.visit_graphic_object(rectangle, class_name, reference_name)

        reference = rectangle.fill_color
        if reference:
            self.visit(reference, 'Rectangle', 'fillColor')
        reference = rectangle.fill_opacity
        if reference:
            self.visit(reference, 'Rectangle', 'fillOpacity')
        reference = rectangle.first_arc
        if reference:
            self.visit(reference, 'Rectangle', 'firstArc')
        reference = rectangle.first_point
        if reference:
            self.visit(reference, 'Rectangle', 'firstPoint')
        reference = rectangle.fourth_arc
        if reference:
            self.visit(reference, 'Rectangle', 'fourthArc')
        reference = rectangle.gradient
        if reference:
            self.visit(reference, 'Rectangle', 'gradient')
        reference = rectangle.halo_color
        if reference:
            self.visit(reference, 'Rectangle', 'haloColor')
        reference = rectangle.haloing
        if reference:
            self.visit(reference, 'Rectangle', 'haloing')
        reference = rectangle.line_cap
        if reference:
            self.visit(reference, 'Rectangle', 'lineCap')
        reference = rectangle.line_stipple
        if reference:
            self.visit(reference, 'Rectangle', 'lineStipple')
        reference = rectangle.line_width
        if reference:
            self.visit(reference, 'Rectangle', 'lineWidth')
        reference = rectangle.modulate
        if reference:
            self.visit(reference, 'Rectangle', 'modulate')
        reference = rectangle.outline_color
        if reference:
            self.visit(reference, 'Rectangle', 'outlineColor')
        reference = rectangle.outline_opacity
        if reference:
            self.visit(reference, 'Rectangle', 'outlineOpacity')
        reference = rectangle.polygon_smooth
        if reference:
            self.visit(reference, 'Rectangle', 'polygonSmooth')
        reference = rectangle.second_arc
        if reference:
            self.visit(reference, 'Rectangle', 'secondArc')
        reference = rectangle.tessellate
        if reference:
            self.visit(reference, 'Rectangle', 'tessellate')
        reference = rectangle.texture
        if reference:
            self.visit(reference, 'Rectangle', 'texture')
        reference = rectangle.texture_control
        if reference:
            self.visit(reference, 'Rectangle', 'textureControl')
        reference = rectangle.third_arc
        if reference:
            self.visit(reference, 'Rectangle', 'thirdArc')
        reference = rectangle.third_point
        if reference:
            self.visit(reference, 'Rectangle', 'thirdPoint')
        reference = rectangle.visible
        if reference:
            self.visit(reference, 'Rectangle', 'visible')

    def visit_rectangle_area(self, rectangle_area: RectangleArea, class_name: str, reference_name: str):
        self.visit_graphic_object(rectangle_area, class_name, reference_name)

        reference = rectangle_area.enable
        if reference:
            self.visit(reference, 'RectangleArea', 'enable')
        reference = rectangle_area.first_point
        if reference:
            self.visit(reference, 'RectangleArea', 'firstPoint')
        reference = rectangle_area.inside
        if reference:
            self.visit(reference, 'RectangleArea', 'inside')
        reference = rectangle_area.percent_height
        if reference:
            self.visit(reference, 'RectangleArea', 'percentHeight')
        reference = rectangle_area.percent_width
        if reference:
            self.visit(reference, 'RectangleArea', 'percentWidth')
        reference = rectangle_area.pointer_id
        if reference:
            self.visit(reference, 'RectangleArea', 'pointerId')
        reference = rectangle_area.third_point
        if reference:
            self.visit(reference, 'RectangleArea', 'thirdPoint')

    def visit_reference_container(self, reference_container: ReferenceContainer, class_name: str, reference_name: str):
        self.visit_a_container(reference_container, class_name, reference_name)

        reference = reference_container.constant_parameters
        if reference:
            self.visit(reference, 'ReferenceContainer', 'constantParameters')
        reference = reference_container.file
        if reference:
            self.visit(reference, 'ReferenceContainer', 'file')
        reference = reference_container.input_parameters
        if reference:
            self.visit(reference, 'ReferenceContainer', 'inputParameters')
        reference = reference_container.orientation
        if reference:
            self.visit(reference, 'ReferenceContainer', 'orientation')
        reference = reference_container.origin
        if reference:
            self.visit(reference, 'ReferenceContainer', 'origin')
        reference = reference_container.output_parameters
        if reference:
            self.visit(reference, 'ReferenceContainer', 'outputParameters')
        reference = reference_container.rotate
        if reference:
            self.visit(reference, 'ReferenceContainer', 'rotate')
        reference = reference_container.scale
        if reference:
            self.visit(reference, 'ReferenceContainer', 'scale')
        reference = reference_container.visible
        if reference:
            self.visit(reference, 'ReferenceContainer', 'visible')

    def visit_reference_object(self, reference_object: ReferenceObject, class_name: str, reference_name: str):
        reference = reference_object.children
        if reference:
            self.visit(reference, 'ReferenceObject', 'children')
        reference = reference_object.declaration
        if reference:
            self.visit(reference, 'ReferenceObject', 'declaration')

    def visit_rich_text(self, rich_text: RichText, class_name: str, reference_name: str):
        self.visit_graphic_object(rich_text, class_name, reference_name)

        reference = rich_text.font
        if reference:
            self.visit(reference, 'RichText', 'font')
        reference = rich_text.horiz_align
        if reference:
            self.visit(reference, 'RichText', 'horizAlign')
        reference = rich_text.line_width
        if reference:
            self.visit(reference, 'RichText', 'lineWidth')
        reference = rich_text.max_length
        if reference:
            self.visit(reference, 'RichText', 'maxLength')
        reference = rich_text.outline_color
        if reference:
            self.visit(reference, 'RichText', 'outlineColor')
        reference = rich_text.position
        if reference:
            self.visit(reference, 'RichText', 'position')
        reference = rich_text.text_value
        if reference:
            self.visit(reference, 'RichText', 'textValue')
        reference = rich_text.vert_align
        if reference:
            self.visit(reference, 'RichText', 'vertAlign')
        reference = rich_text.visible
        if reference:
            self.visit(reference, 'RichText', 'visible')

    def visit_rotation_container(self, rotation_container: RotationContainer, class_name: str, reference_name: str):
        self.visit_a_container(rotation_container, class_name, reference_name)

        reference = rotation_container.end_rotation_angle
        if reference:
            self.visit(reference, 'RotationContainer', 'endRotationAngle')
        reference = rotation_container.end_rotation_locked
        if reference:
            self.visit(reference, 'RotationContainer', 'endRotationLocked')
        reference = rotation_container.end_rotation_value
        if reference:
            self.visit(reference, 'RotationContainer', 'endRotationValue')
        reference = rotation_container.functional_rotation_value
        if reference:
            self.visit(reference, 'RotationContainer', 'functionalRotationValue')
        reference = rotation_container.orientation
        if reference:
            self.visit(reference, 'RotationContainer', 'orientation')
        reference = rotation_container.origin
        if reference:
            self.visit(reference, 'RotationContainer', 'origin')
        reference = rotation_container.priority
        if reference:
            self.visit(reference, 'RotationContainer', 'priority')
        reference = rotation_container.ref_angle
        if reference:
            self.visit(reference, 'RotationContainer', 'refAngle')
        reference = rotation_container.start_rotation_angle
        if reference:
            self.visit(reference, 'RotationContainer', 'startRotationAngle')
        reference = rotation_container.start_rotation_locked
        if reference:
            self.visit(reference, 'RotationContainer', 'startRotationLocked')
        reference = rotation_container.start_rotation_value
        if reference:
            self.visit(reference, 'RotationContainer', 'startRotationValue')
        reference = rotation_container.visible
        if reference:
            self.visit(reference, 'RotationContainer', 'visible')

    def visit_shape(self, shape: Shape, class_name: str, reference_name: str):
        self.visit_graphic_object(shape, class_name, reference_name)

        reference = shape.fill_color
        if reference:
            self.visit(reference, 'Shape', 'fillColor')
        reference = shape.fill_opacity
        if reference:
            self.visit(reference, 'Shape', 'fillOpacity')
        reference = shape.gradient
        if reference:
            self.visit(reference, 'Shape', 'gradient')
        reference = shape.halo_color
        if reference:
            self.visit(reference, 'Shape', 'haloColor')
        reference = shape.haloing
        if reference:
            self.visit(reference, 'Shape', 'haloing')
        reference = shape.line_cap
        if reference:
            self.visit(reference, 'Shape', 'lineCap')
        reference = shape.line_stipple
        if reference:
            self.visit(reference, 'Shape', 'lineStipple')
        reference = shape.line_width
        if reference:
            self.visit(reference, 'Shape', 'lineWidth')
        reference = shape.modulate
        if reference:
            self.visit(reference, 'Shape', 'modulate')
        reference = shape.outline_color
        if reference:
            self.visit(reference, 'Shape', 'outlineColor')
        reference = shape.outline_opacity
        if reference:
            self.visit(reference, 'Shape', 'outlineOpacity')
        reference = shape.points
        if reference:
            self.visit(reference, 'Shape', 'points')
        reference = shape.polygon_smooth
        if reference:
            self.visit(reference, 'Shape', 'polygonSmooth')
        reference = shape.tessellate
        if reference:
            self.visit(reference, 'Shape', 'tessellate')
        reference = shape.texture
        if reference:
            self.visit(reference, 'Shape', 'texture')
        reference = shape.texture_control
        if reference:
            self.visit(reference, 'Shape', 'textureControl')
        reference = shape.visible
        if reference:
            self.visit(reference, 'Shape', 'visible')

    def visit_shape_area(self, shape_area: ShapeArea, class_name: str, reference_name: str):
        self.visit_graphic_object(shape_area, class_name, reference_name)

        reference = shape_area.enable
        if reference:
            self.visit(reference, 'ShapeArea', 'enable')
        reference = shape_area.inside
        if reference:
            self.visit(reference, 'ShapeArea', 'inside')
        reference = shape_area.pointer_id
        if reference:
            self.visit(reference, 'ShapeArea', 'pointerId')
        reference = shape_area.points
        if reference:
            self.visit(reference, 'ShapeArea', 'points')

    def visit_smooth_curve_to(self, smooth_curve_to: SmoothCurveTo, class_name: str, reference_name: str):
        self.visit_command(smooth_curve_to, class_name, reference_name)

        reference = smooth_curve_to.end_point
        if reference:
            self.visit(reference, 'SmoothCurveTo', 'endPoint')
        reference = smooth_curve_to.second_control_point
        if reference:
            self.visit(reference, 'SmoothCurveTo', 'secondControlPoint')

    def visit_smooth_quadratic_curve_to(self, smooth_quadratic_curve_to: SmoothQuadraticCurveTo, class_name: str, reference_name: str):
        self.visit_command(smooth_quadratic_curve_to, class_name, reference_name)

        reference = smooth_quadratic_curve_to.end_point
        if reference:
            self.visit(reference, 'SmoothQuadraticCurveTo', 'endPoint')

    def visit_specification(self, specification: Specification, class_name: str, reference_name: str):
        for reference in specification.layers:
            self.visit(reference, 'Specification', 'layers')

    def visit_static_bitmap(self, static_bitmap: StaticBitmap, class_name: str, reference_name: str):
        pass

    def visit_static_container_prop(self, static_container_prop: StaticContainerProp, class_name: str, reference_name: str):
        self.visit_property(static_container_prop, class_name, reference_name)

        reference = static_container_prop.bitmap
        if reference:
            self.visit(reference, 'StaticContainerProp', 'bitmap')

    def visit_stencil(self, stencil: Stencil, class_name: str, reference_name: str):
        self.visit_graphic_object(stencil, class_name, reference_name)

        reference = stencil.mask_activity
        if reference:
            self.visit(reference, 'Stencil', 'maskActivity')
        reference = stencil.points
        if reference:
            self.visit(reference, 'Stencil', 'points')
        reference = stencil.tessellate
        if reference:
            self.visit(reference, 'Stencil', 'tessellate')

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

        reference = text.font
        if reference:
            self.visit(reference, 'Text', 'font')
        reference = text.halo_color
        if reference:
            self.visit(reference, 'Text', 'haloColor')
        reference = text.haloing
        if reference:
            self.visit(reference, 'Text', 'haloing')
        reference = text.horiz_align
        if reference:
            self.visit(reference, 'Text', 'horizAlign')
        reference = text.line_width
        if reference:
            self.visit(reference, 'Text', 'lineWidth')
        reference = text.max_length
        if reference:
            self.visit(reference, 'Text', 'maxLength')
        reference = text.outline_color
        if reference:
            self.visit(reference, 'Text', 'outlineColor')
        reference = text.position
        if reference:
            self.visit(reference, 'Text', 'position')
        reference = text.text_value
        if reference:
            self.visit(reference, 'Text', 'textValue')
        reference = text.vert_align
        if reference:
            self.visit(reference, 'Text', 'vertAlign')
        reference = text.visible
        if reference:
            self.visit(reference, 'Text', 'visible')

    def visit_text_area(self, text_area: TextArea, class_name: str, reference_name: str):
        self.visit_graphic_object(text_area, class_name, reference_name)

        reference = text_area.first_point
        if reference:
            self.visit(reference, 'TextArea', 'firstPoint')
        reference = text_area.font
        if reference:
            self.visit(reference, 'TextArea', 'font')
        reference = text_area.halo_color
        if reference:
            self.visit(reference, 'TextArea', 'haloColor')
        reference = text_area.haloing
        if reference:
            self.visit(reference, 'TextArea', 'haloing')
        reference = text_area.horiz_align
        if reference:
            self.visit(reference, 'TextArea', 'horizAlign')
        reference = text_area.line_width
        if reference:
            self.visit(reference, 'TextArea', 'lineWidth')
        reference = text_area.max_length
        if reference:
            self.visit(reference, 'TextArea', 'maxLength')
        reference = text_area.outline_color
        if reference:
            self.visit(reference, 'TextArea', 'outlineColor')
        reference = text_area.text_value
        if reference:
            self.visit(reference, 'TextArea', 'textValue')
        reference = text_area.third_point
        if reference:
            self.visit(reference, 'TextArea', 'thirdPoint')
        reference = text_area.vert_align
        if reference:
            self.visit(reference, 'TextArea', 'vertAlign')
        reference = text_area.visible
        if reference:
            self.visit(reference, 'TextArea', 'visible')

    def visit_text_horiz_align_prop(self, text_horiz_align_prop: TextHorizAlignProp, class_name: str, reference_name: str):
        self.visit_pluggable_property(text_horiz_align_prop, class_name, reference_name)

    def visit_text_prop(self, text_prop: TextProp, class_name: str, reference_name: str):
        self.visit_pluggable_property(text_prop, class_name, reference_name)

    def visit_text_vert_align_prop(self, text_vert_align_prop: TextVertAlignProp, class_name: str, reference_name: str):
        self.visit_pluggable_property(text_vert_align_prop, class_name, reference_name)

    def visit_texture_element(self, texture_element: TextureElement, class_name: str, reference_name: str):
        pass

    def visit_texture_prop(self, texture_prop: TextureProp, class_name: str, reference_name: str):
        self.visit_property(texture_prop, class_name, reference_name)

        reference = texture_prop.texture_id
        if reference:
            self.visit(reference, 'TextureProp', 'textureId')

    def visit_texture_table(self, texture_table: TextureTable, class_name: str, reference_name: str):
        for reference in texture_table.elements:
            self.visit(reference, 'TextureTable', 'Elements')

    def visit_translation_container(self, translation_container: TranslationContainer, class_name: str, reference_name: str):
        self.visit_a_container(translation_container, class_name, reference_name)

        reference = translation_container.end_translation_locked
        if reference:
            self.visit(reference, 'TranslationContainer', 'endTranslationLocked')
        reference = translation_container.end_translation_point
        if reference:
            self.visit(reference, 'TranslationContainer', 'endTranslationPoint')
        reference = translation_container.end_translation_value
        if reference:
            self.visit(reference, 'TranslationContainer', 'endTranslationValue')
        reference = translation_container.functional_translation_value
        if reference:
            self.visit(reference, 'TranslationContainer', 'functionalTranslationValue')
        reference = translation_container.origin
        if reference:
            self.visit(reference, 'TranslationContainer', 'origin')
        reference = translation_container.priority
        if reference:
            self.visit(reference, 'TranslationContainer', 'priority')
        reference = translation_container.ref_point
        if reference:
            self.visit(reference, 'TranslationContainer', 'refPoint')
        reference = translation_container.start_translation_locked
        if reference:
            self.visit(reference, 'TranslationContainer', 'startTranslationLocked')
        reference = translation_container.start_translation_point
        if reference:
            self.visit(reference, 'TranslationContainer', 'startTranslationPoint')
        reference = translation_container.start_translation_value
        if reference:
            self.visit(reference, 'TranslationContainer', 'startTranslationValue')
        reference = translation_container.visible
        if reference:
            self.visit(reference, 'TranslationContainer', 'visible')

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

        reference = vertical_line_to.end_y
        if reference:
            self.visit(reference, 'VerticalLineTo', 'endY')

    #<<visitor
    def visit_traceable(self, traceable: Traceable, class_name: str, reference_name: str):
        pass
    #>>visitor


_map_visit_functions = {
    AngleArrayProp: 'visit_angle_array_prop',
    AngleProp: 'visit_angle_prop',
    Arc: 'visit_arc',
    ArcEllipse: 'visit_arc_ellipse',
    ArcSegmentProp: 'visit_arc_segment_prop',
    ArrayExpr: 'visit_array_expr',
    ArrayType: 'visit_array_type',
    Assignment: 'visit_assignment',
    AssignmentOutputProp: 'visit_assignment_output_prop',
    Behavior: 'visit_behavior',
    BiFont: 'visit_bi_font',
    BiFontDisplaySignProp: 'visit_bi_font_display_sign_prop',
    BinaryOpExpr: 'visit_binary_op_expr',
    Bitmap: 'visit_bitmap',
    BooleanArrayProp: 'visit_boolean_array_prop',
    BooleanProp: 'visit_boolean_prop',
    Circle: 'visit_circle',
    CircleArea: 'visit_circle_area',
    ClipBox: 'visit_clip_box',
    ClipPlane: 'visit_clip_plane',
    ClosePath: 'visit_close_path',
    ColorElement: 'visit_color_element',
    ColorTable: 'visit_color_table',
    CommandsProp: 'visit_commands_prop',
    Comment: 'visit_comment',
    CondContainer: 'visit_cond_container',
    ConditionalExpr: 'visit_conditional_expr',
    ConditionalIndexProp: 'visit_conditional_index_prop',
    ConstantDefinition: 'visit_constant_definition',
    Container: 'visit_container',
    CoordinatePoint: 'visit_coordinate_point',
    Crown: 'visit_crown',
    CursorPosRequest: 'visit_cursor_pos_request',
    CurveTo: 'visit_curve_to',
    Ellipse: 'visit_ellipse',
    EllipticalArc: 'visit_elliptical_arc',
    EnumType: 'visit_enum_type',
    EnumValue: 'visit_enum_value',
    FieldExpr: 'visit_field_expr',
    FileProp: 'visit_file_prop',
    FilterRotationContainer: 'visit_filter_rotation_container',
    FilterTranslationContainer: 'visit_filter_translation_container',
    FontDefinition: 'visit_font_definition',
    FontTable: 'visit_font_table',
    FormatProp: 'visit_format_prop',
    FunctionProp: 'visit_function_prop',
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
    IndexedPointsProp: 'visit_indexed_points_prop',
    IndexedTexturePointsProp: 'visit_indexed_texture_points_prop',
    IndexesProp: 'visit_indexes_prop',
    InputParamProp: 'visit_input_param_prop',
    InputParametersProp: 'visit_input_parameters_prop',
    InputProp: 'visit_input_prop',
    IntegerProp: 'visit_integer_prop',
    KeyboardEventListener: 'visit_keyboard_event_listener',
    Layer: 'visit_layer',
    Line: 'visit_line',
    LineCapProp: 'visit_line_cap_prop',
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
    NodeFunctionProp: 'visit_node_function_prop',
    NplicatorContainer: 'visit_nplicator_container',
    Oid: 'visit_oid',
    OrientationProp: 'visit_orientation_prop',
    OutputParamProp: 'visit_output_param_prop',
    OutputParametersProp: 'visit_output_parameters_prop',
    OutputPointProp: 'visit_output_point_prop',
    OutputProp: 'visit_output_prop',
    PanelContainer: 'visit_panel_container',
    ParamProp: 'visit_param_prop',
    Path: 'visit_path',
    PointArrayProp: 'visit_point_array_prop',
    PointProperty: 'visit_point_property',
    PointTextureProp: 'visit_point_texture_prop',
    PointerEventListener: 'visit_pointer_event_listener',
    PointsProp: 'visit_points_prop',
    PredefType: 'visit_predef_type',
    PriorityProp: 'visit_priority_prop',
    QuadraticCurveTo: 'visit_quadratic_curve_to',
    RadialGradientElement: 'visit_radial_gradient_element',
    RealArrayProp: 'visit_real_array_prop',
    RealProp: 'visit_real_prop',
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
    StaticContainerProp: 'visit_static_container_prop',
    Stencil: 'visit_stencil',
    StructExpr: 'visit_struct_expr',
    StructFieldExpr: 'visit_struct_field_expr',
    StructFieldType: 'visit_struct_field_type',
    StructType: 'visit_struct_type',
    Text: 'visit_text',
    TextArea: 'visit_text_area',
    TextHorizAlignProp: 'visit_text_horiz_align_prop',
    TextProp: 'visit_text_prop',
    TextVertAlignProp: 'visit_text_vert_align_prop',
    TextureElement: 'visit_texture_element',
    TextureProp: 'visit_texture_prop',
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
