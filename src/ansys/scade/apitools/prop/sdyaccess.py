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

from typing import List, Tuple

# allows importing this module instead of scade.model.display
from scade.model.display import *  # noqa: F403

#%% classes

class _Property(object):
    """Variant from PyProperty_Type() in cpython/Objects/descrobject.c"""

    def __init__(self, attribute, fget=None, fset=None, fdel=None, doc=None):
        self.attribute = attribute
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        if doc is None and fget is not None:
            doc = fget.__doc__
        self.__doc__ = doc

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError('unreadable attribute')
        return self.fget(obj, self.attribute)

    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError("can't set attribute")
        self.fset(obj, self.attribute, value)

    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        self.fdel(obj, self.attribute)


#{{sdy_access_fct(sdy)

# AngleProp
def _get_angle_prop(self, attribute: str) -> float:
    property = getattr(self, attribute)
    return property.p_angle if property is not None else 0.


def _set_angle_prop(self, attribute: str, value: float):
    if getattr(self, attribute) is None:
        setattr(self, attribute, AngleProp())
    property = getattr(self, attribute)
    property.p_angle = value


# ArcSegmentProp
def _get_arc_segment_prop(self, attribute: str) -> Tuple[bool, float]:
    property = getattr(self, attribute)
    return (property.p_orientation, property.p_angle) if property is not None else ((False, 0.))


def _set_arc_segment_prop(self, attribute: str, value: Tuple[bool, float]):
    if getattr(self, attribute) is None:
        setattr(self, attribute, ArcSegmentProp())
    property = getattr(self, attribute)
    (property.p_orientation, property.p_angle) = value


# CoordinatePoint
def _get_coordinate_point(self, attribute: str) -> Tuple[float, float]:
    property = getattr(self, attribute)
    return (property.p_x, property.p_y) if property is not None else ((0., 0.))


def _set_coordinate_point(self, attribute: str, value: Tuple[float, float]):
    if getattr(self, attribute) is None:
        setattr(self, attribute, CoordinatePoint())
    property = getattr(self, attribute)
    (property.p_x, property.p_y) = value


# FileProp
def _get_file_prop(self, attribute: str) -> str:
    property = getattr(self, attribute)
    return property.file if property is not None else ''


def _set_file_prop(self, attribute: str, value: str):
    if getattr(self, attribute) is None:
        setattr(self, attribute, FileProp())
    property = getattr(self, attribute)
    property.file = value


# FormatProp
def _get_format_prop(self, attribute: str) -> Tuple[int, int, int, int, bool, DisplaySignEnum]:
    property = getattr(self, attribute)
    return (property.separator, property.p_integral_part, property.p_fractional_part, property.p_second_font_pos, property.p_leading_zeros, property.p_display_sign) if property is not None else ((0, 0, 0, 0, False, DisplaySignEnum.ALWAYS))


def _set_format_prop(self, attribute: str, value: Tuple[int, int, int, int, bool, DisplaySignEnum]):
    if getattr(self, attribute) is None:
        setattr(self, attribute, FormatProp())
    property = getattr(self, attribute)
    (property.separator, property.p_integral_part, property.p_fractional_part, property.p_second_font_pos, property.p_leading_zeros, property.p_display_sign) = value


# FunctionProp
def _get_function_prop(self, attribute: str) -> str:
    property = getattr(self, attribute)
    return property.name if property is not None else ''


def _set_function_prop(self, attribute: str, value: str):
    if getattr(self, attribute) is None:
        setattr(self, attribute, FunctionProp())
    property = getattr(self, attribute)
    property.name = value


# IndexesProp
def _get_indexes_prop(self, attribute: str) -> bool:
    property = getattr(self, attribute)
    return property.default_is_other if property is not None else False


def _set_indexes_prop(self, attribute: str, value: bool):
    if getattr(self, attribute) is None:
        setattr(self, attribute, IndexesProp())
    property = getattr(self, attribute)
    property.default_is_other = value


# InputParametersProp
def _get_input_parameters_prop(self, attribute: str) -> List[Tuple[str, Representation]]:
    property = getattr(self, attribute)
    return property.p_parameters if property is not None else []


def _set_input_parameters_prop(self, attribute: str, value: List[Tuple[str, Representation]]):
    if getattr(self, attribute) is None:
        setattr(self, attribute, InputParametersProp())
    property = getattr(self, attribute)
    property.p_parameters = value


# NodeFunctionProp
def _get_node_function_prop(self, attribute: str) -> Tuple[bool, str]:
    property = getattr(self, attribute)
    return (property.is_node, property.name) if property is not None else ((False, ''))


def _set_node_function_prop(self, attribute: str, value: Tuple[bool, str]):
    if getattr(self, attribute) is None:
        setattr(self, attribute, NodeFunctionProp())
    property = getattr(self, attribute)
    (property.is_node, property.name) = value


# OrientationProp
def _get_orientation_prop(self, attribute: str) -> bool:
    property = getattr(self, attribute)
    return property.clockwise if property is not None else False


def _set_orientation_prop(self, attribute: str, value: bool):
    if getattr(self, attribute) is None:
        setattr(self, attribute, OrientationProp())
    property = getattr(self, attribute)
    property.clockwise = value


# OutputParametersProp
def _get_output_parameters_prop(self, attribute: str) -> List[Tuple[str, Representation]]:
    property = getattr(self, attribute)
    return property.p_output_parameters if property is not None else []


def _set_output_parameters_prop(self, attribute: str, value: List[Tuple[str, Representation]]):
    if getattr(self, attribute) is None:
        setattr(self, attribute, OutputParametersProp())
    property = getattr(self, attribute)
    property.p_output_parameters = value


# PointArrayProp
def _get_point_array_prop(self, attribute: str) -> Tuple[List[float], List[float]]:
    property = getattr(self, attribute)
    return (property.p_x, property.p_y) if property is not None else (([], []))


def _set_point_array_prop(self, attribute: str, value: Tuple[List[float], List[float]]):
    if getattr(self, attribute) is None:
        setattr(self, attribute, PointArrayProp())
    property = getattr(self, attribute)
    (property.p_x, property.p_y) = value


# PointsProp
def _get_points_prop(self, attribute: str) -> List[Tuple[float, float]]:
    property = getattr(self, attribute)
    return property.p_point if property is not None else []


def _set_points_prop(self, attribute: str, value: List[Tuple[float, float]]):
    if getattr(self, attribute) is None:
        setattr(self, attribute, PointsProp())
    property = getattr(self, attribute)
    property.p_point = value


# StaticContainerProp
def _get_static_container_prop(self, attribute: str) -> Tuple[bool, float, float, float, float, bool]:
    property = getattr(self, attribute)
    return (property.init, property.min_x, property.max_x, property.min_y, property.max_y, property.generate_static_sequence) if property is not None else ((False, 0., 0., 0., 0., False))


def _set_static_container_prop(self, attribute: str, value: Tuple[bool, float, float, float, float, bool]):
    if getattr(self, attribute) is None:
        setattr(self, attribute, StaticContainerProp())
    property = getattr(self, attribute)
    (property.init, property.min_x, property.max_x, property.min_y, property.max_y, property.generate_static_sequence) = value


# TextureProp
def _get_texture_prop(self, attribute: str) -> Tuple[HorizAlignEnum, VertAlignEnum, float, float, int]:
    property = getattr(self, attribute)
    return (property.horiz_align, property.vert_align, property.horiz_pattern, property.vert_pattern, property.p_texture_id) if property is not None else ((HorizAlignEnum.LEFT, VertAlignEnum.TOP, 0., 0., 0))


def _set_texture_prop(self, attribute: str, value: Tuple[HorizAlignEnum, VertAlignEnum, float, float, int]):
    if getattr(self, attribute) is None:
        setattr(self, attribute, TextureProp())
    property = getattr(self, attribute)
    (property.horiz_align, property.vert_align, property.horiz_pattern, property.vert_pattern, property.p_texture_id) = value


# AngleArrayProp
def _get_angle_array_prop(self, attribute: str) -> List[float]:
    property = getattr(self, attribute)
    return property.init if property is not None else []


def _set_angle_array_prop(self, attribute: str, value: List[float]):
    if getattr(self, attribute) is None:
        setattr(self, attribute, AngleArrayProp())
    property = getattr(self, attribute)
    property.init = value


# BiFontDisplaySignProp
def _get_bi_font_display_sign_prop(self, attribute: str) -> DisplaySignEnum:
    property = getattr(self, attribute)
    return property.init if property is not None else DisplaySignEnum.ALWAYS


def _set_bi_font_display_sign_prop(self, attribute: str, value: DisplaySignEnum):
    if getattr(self, attribute) is None:
        setattr(self, attribute, BiFontDisplaySignProp())
    property = getattr(self, attribute)
    property.init = value


# BooleanArrayProp
def _get_boolean_array_prop(self, attribute: str) -> List[bool]:
    property = getattr(self, attribute)
    return property.init if property is not None else []


def _set_boolean_array_prop(self, attribute: str, value: List[bool]):
    if getattr(self, attribute) is None:
        setattr(self, attribute, BooleanArrayProp())
    property = getattr(self, attribute)
    property.init = value


# BooleanProp
def _get_boolean_prop(self, attribute: str) -> bool:
    property = getattr(self, attribute)
    return property.init if property is not None else False


def _set_boolean_prop(self, attribute: str, value: bool):
    if getattr(self, attribute) is None:
        setattr(self, attribute, BooleanProp())
    property = getattr(self, attribute)
    property.init = value


# ConditionalIndexProp
def _get_conditional_index_prop(self, attribute: str) -> Tuple[IndexPropEnum, bool]:
    property = getattr(self, attribute)
    return (property.index_prop_enum, property.all_visible) if property is not None else ((IndexPropEnum.NUMERIC, False))


def _set_conditional_index_prop(self, attribute: str, value: Tuple[IndexPropEnum, bool]):
    if getattr(self, attribute) is None:
        setattr(self, attribute, ConditionalIndexProp())
    property = getattr(self, attribute)
    (property.index_prop_enum, property.all_visible) = value


# IntegerProp
def _get_integer_prop(self, attribute: str) -> int:
    property = getattr(self, attribute)
    return property.init if property is not None else 0


def _set_integer_prop(self, attribute: str, value: int):
    if getattr(self, attribute) is None:
        setattr(self, attribute, IntegerProp())
    property = getattr(self, attribute)
    property.init = value


# LineCapProp
def _get_line_cap_prop(self, attribute: str) -> LineCapEnum:
    property = getattr(self, attribute)
    return property.init if property is not None else LineCapEnum.SQUARE


def _set_line_cap_prop(self, attribute: str, value: LineCapEnum):
    if getattr(self, attribute) is None:
        setattr(self, attribute, LineCapProp())
    property = getattr(self, attribute)
    property.init = value


# PointProperty
def _new_point_property(values: Tuple[float, float]) -> PointProperty:
    self = PointProperty()
    self.p_x, self.p_y = values
    return self


def _get_list_point_property(self, attribute: str) -> List[Tuple[float, float]]:
    return [(property.p_x, property.p_y) for property in getattr(self, attribute)]


def _set_list_point_property(self, attribute: str, values: List[Tuple[float, float]]):
    setattr(self, attribute, [_new_point_property((x, y)) for x, y in values])

def _get_point_property(self, attribute: str) -> Tuple[float, float]:
    property = getattr(self, attribute)
    return (property.p_x, property.p_y) if property is not None else ((0., 0.))


def _set_point_property(self, attribute: str, value: Tuple[float, float]):
    if getattr(self, attribute) is None:
        setattr(self, attribute, PointProperty())
    property = getattr(self, attribute)
    (property.p_x, property.p_y) = value


# PointTextureProp
def _get_point_texture_prop(self, attribute: str) -> Tuple[float, float, float, float]:
    property = getattr(self, attribute)
    return (property.p_x, property.p_y, property.p_u, property.p_v) if property is not None else ((0., 0., 0., 0.))


def _set_point_texture_prop(self, attribute: str, value: Tuple[float, float, float, float]):
    if getattr(self, attribute) is None:
        setattr(self, attribute, PointTextureProp())
    property = getattr(self, attribute)
    (property.p_x, property.p_y, property.p_u, property.p_v) = value


# PriorityProp
def _get_priority_prop(self, attribute: str) -> int:
    property = getattr(self, attribute)
    return property.init if property is not None else 0


def _set_priority_prop(self, attribute: str, value: int):
    if getattr(self, attribute) is None:
        setattr(self, attribute, PriorityProp())
    property = getattr(self, attribute)
    property.init = value


# RealArrayProp
def _get_real_array_prop(self, attribute: str) -> List[float]:
    property = getattr(self, attribute)
    return property.init if property is not None else []


def _set_real_array_prop(self, attribute: str, value: List[float]):
    if getattr(self, attribute) is None:
        setattr(self, attribute, RealArrayProp())
    property = getattr(self, attribute)
    property.init = value


# RealProp
def _get_real_prop(self, attribute: str) -> float:
    property = getattr(self, attribute)
    return property.init if property is not None else 0.


def _set_real_prop(self, attribute: str, value: float):
    if getattr(self, attribute) is None:
        setattr(self, attribute, RealProp())
    property = getattr(self, attribute)
    property.init = value


# TextHorizAlignProp
def _get_text_horiz_align_prop(self, attribute: str) -> HorizAlignEnum:
    property = getattr(self, attribute)
    return property.init if property is not None else HorizAlignEnum.LEFT


def _set_text_horiz_align_prop(self, attribute: str, value: HorizAlignEnum):
    if getattr(self, attribute) is None:
        setattr(self, attribute, TextHorizAlignProp())
    property = getattr(self, attribute)
    property.init = value


# TextProp
def _get_text_prop(self, attribute: str) -> Tuple[TextTypeEnum, List[int]]:
    property = getattr(self, attribute)
    return (property.type, property.init) if property is not None else ((TextTypeEnum.CHAR, []))


def _set_text_prop(self, attribute: str, value: Tuple[TextTypeEnum, List[int]]):
    if getattr(self, attribute) is None:
        setattr(self, attribute, TextProp())
    property = getattr(self, attribute)
    (property.type, property.init) = value


# TextVertAlignProp
def _get_text_vert_align_prop(self, attribute: str) -> VertAlignEnum:
    property = getattr(self, attribute)
    return property.init if property is not None else VertAlignEnum.TOP


def _set_text_vert_align_prop(self, attribute: str, value: VertAlignEnum):
    if getattr(self, attribute) is None:
        setattr(self, attribute, TextVertAlignProp())
    property = getattr(self, attribute)
    property.init = value


# InputParamProp
def _new_input_param_prop(values: Tuple[str, Representation]) -> InputParamProp:
    self = InputParamProp()
    self.name, self.representation = values
    return self


def _get_list_input_param_prop(self, attribute: str) -> List[Tuple[str, Representation]]:
    return [(property.name, property.representation) for property in getattr(self, attribute)]


def _set_list_input_param_prop(self, attribute: str, values: List[Tuple[str, Representation]]):
    setattr(self, attribute, [_new_input_param_prop((name, representation)) for name, representation in values])


# OutputParamProp
def _new_output_param_prop(values: Tuple[str, Representation]) -> OutputParamProp:
    self = OutputParamProp()
    self.name, self.representation = values
    return self


def _get_list_output_param_prop(self, attribute: str) -> List[Tuple[str, Representation]]:
    return [(property.name, property.representation) for property in getattr(self, attribute)]


def _set_list_output_param_prop(self, attribute: str, values: List[Tuple[str, Representation]]):
    setattr(self, attribute, [_new_output_param_prop((name, representation)) for name, representation in values])

#}}sdy_access_fct


#{{sdy_access_dcl(sdy)

# IndexTexturePoint
IndexTexturePoint.p_point = _Property('point', _get_point_texture_prop, _set_point_texture_prop)
IndexTexturePoint.p_arc_segment = _Property('arc_segment', _get_arc_segment_prop, _set_arc_segment_prop)


# IndexedPoint
IndexedPoint.p_point = _Property('point', _get_point_property, _set_point_property)
IndexedPoint.p_arc_segment = _Property('arc_segment', _get_arc_segment_prop, _set_arc_segment_prop)


# AngleProp
AngleProp.p_angle = _Property('angle', _get_real_prop, _set_real_prop)


# ArcSegmentProp
ArcSegmentProp.p_orientation = _Property('orientation', _get_orientation_prop, _set_orientation_prop)
ArcSegmentProp.p_angle = _Property('angle', _get_angle_prop, _set_angle_prop)


# CoordinatePoint
CoordinatePoint.p_x = _Property('x', _get_real_prop, _set_real_prop)
CoordinatePoint.p_y = _Property('y', _get_real_prop, _set_real_prop)


# CurveTo
CurveTo.p_first_control_point = _Property('first_control_point', _get_point_property, _set_point_property)
CurveTo.p_second_control_point = _Property('second_control_point', _get_point_property, _set_point_property)
CurveTo.p_end_point = _Property('end_point', _get_point_property, _set_point_property)


# EllipticalArc
EllipticalArc.p_x_radius = _Property('x_radius', _get_real_prop, _set_real_prop)
EllipticalArc.p_y_radius = _Property('y_radius', _get_real_prop, _set_real_prop)
EllipticalArc.p_x_axis_rotation = _Property('x_axis_rotation', _get_real_prop, _set_real_prop)
EllipticalArc.p_large_arc_flag = _Property('large_arc_flag', _get_boolean_prop, _set_boolean_prop)
EllipticalArc.p_sweep_flag = _Property('sweep_flag', _get_boolean_prop, _set_boolean_prop)
EllipticalArc.p_end_point = _Property('end_point', _get_point_property, _set_point_property)


# FormatProp
FormatProp.p_integral_part = _Property('integral_part', _get_integer_prop, _set_integer_prop)
FormatProp.p_fractional_part = _Property('fractional_part', _get_integer_prop, _set_integer_prop)
FormatProp.p_second_font_pos = _Property('second_font_pos', _get_integer_prop, _set_integer_prop)
FormatProp.p_leading_zeros = _Property('leading_zeros', _get_boolean_prop, _set_boolean_prop)
FormatProp.p_display_sign = _Property('display_sign', _get_bi_font_display_sign_prop, _set_bi_font_display_sign_prop)


# HorizontalLineTo
HorizontalLineTo.p_end_x = _Property('end_x', _get_real_prop, _set_real_prop)


# InputParametersProp
InputParametersProp.p_parameters = _Property('parameters', _get_list_input_param_prop, _set_list_input_param_prop)


# LineTo
LineTo.p_end_point = _Property('end_point', _get_point_property, _set_point_property)


# MoveTo
MoveTo.p_start_point = _Property('start_point', _get_point_property, _set_point_property)


# OutputParametersProp
OutputParametersProp.p_output_parameters = _Property('output_parameters', _get_list_output_param_prop, _set_list_output_param_prop)


# PointArrayProp
PointArrayProp.p_x = _Property('x', _get_real_array_prop, _set_real_array_prop)
PointArrayProp.p_y = _Property('y', _get_real_array_prop, _set_real_array_prop)


# PointsProp
PointsProp.p_point = _Property('point', _get_list_point_property, _set_list_point_property)


# QuadraticCurveTo
QuadraticCurveTo.p_control_point = _Property('control_point', _get_point_property, _set_point_property)
QuadraticCurveTo.p_end_point = _Property('end_point', _get_point_property, _set_point_property)


# SmoothCurveTo
SmoothCurveTo.p_second_control_point = _Property('second_control_point', _get_point_property, _set_point_property)
SmoothCurveTo.p_end_point = _Property('end_point', _get_point_property, _set_point_property)


# SmoothQuadraticCurveTo
SmoothQuadraticCurveTo.p_end_point = _Property('end_point', _get_point_property, _set_point_property)


# TextureProp
TextureProp.p_texture_id = _Property('texture_id', _get_integer_prop, _set_integer_prop)


# VerticalLineTo
VerticalLineTo.p_end_y = _Property('end_y', _get_real_prop, _set_real_prop)


# Arc
Arc.p_visible = _Property('visible', _get_boolean_prop, _set_boolean_prop)
Arc.p_center = _Property('center', _get_point_property, _set_point_property)
Arc.p_radius = _Property('radius', _get_real_prop, _set_real_prop)
Arc.p_start_angle = _Property('start_angle', _get_angle_prop, _set_angle_prop)
Arc.p_end_angle = _Property('end_angle', _get_angle_prop, _set_angle_prop)
Arc.p_orientation = _Property('orientation', _get_orientation_prop, _set_orientation_prop)
Arc.p_haloing = _Property('haloing', _get_boolean_prop, _set_boolean_prop)
Arc.p_line_width = _Property('line_width', _get_integer_prop, _set_integer_prop)
Arc.p_line_stipple = _Property('line_stipple', _get_integer_prop, _set_integer_prop)
Arc.p_outline_color = _Property('outline_color', _get_integer_prop, _set_integer_prop)
Arc.p_halo_color = _Property('halo_color', _get_integer_prop, _set_integer_prop)
Arc.p_fill_color = _Property('fill_color', _get_integer_prop, _set_integer_prop)
Arc.p_outline_opacity = _Property('outline_opacity', _get_integer_prop, _set_integer_prop)
Arc.p_fill_opacity = _Property('fill_opacity', _get_integer_prop, _set_integer_prop)
Arc.p_line_cap = _Property('line_cap', _get_line_cap_prop, _set_line_cap_prop)
Arc.p_polygon_smooth = _Property('polygon_smooth', _get_boolean_prop, _set_boolean_prop)
Arc.p_texture = _Property('texture', _get_texture_prop, _set_texture_prop)
Arc.p_modulate = _Property('modulate', _get_boolean_prop, _set_boolean_prop)
Arc.p_gradient = _Property('gradient', _get_integer_prop, _set_integer_prop)


# ArcEllipse
ArcEllipse.p_visible = _Property('visible', _get_boolean_prop, _set_boolean_prop)
ArcEllipse.p_center = _Property('center', _get_point_property, _set_point_property)
ArcEllipse.p_horz_radius = _Property('horz_radius', _get_real_prop, _set_real_prop)
ArcEllipse.p_vert_radius = _Property('vert_radius', _get_real_prop, _set_real_prop)
ArcEllipse.p_start_angle = _Property('start_angle', _get_angle_prop, _set_angle_prop)
ArcEllipse.p_end_angle = _Property('end_angle', _get_angle_prop, _set_angle_prop)
ArcEllipse.p_orientation = _Property('orientation', _get_orientation_prop, _set_orientation_prop)
ArcEllipse.p_haloing = _Property('haloing', _get_boolean_prop, _set_boolean_prop)
ArcEllipse.p_line_width = _Property('line_width', _get_integer_prop, _set_integer_prop)
ArcEllipse.p_line_stipple = _Property('line_stipple', _get_integer_prop, _set_integer_prop)
ArcEllipse.p_outline_color = _Property('outline_color', _get_integer_prop, _set_integer_prop)
ArcEllipse.p_halo_color = _Property('halo_color', _get_integer_prop, _set_integer_prop)
ArcEllipse.p_fill_color = _Property('fill_color', _get_integer_prop, _set_integer_prop)
ArcEllipse.p_outline_opacity = _Property('outline_opacity', _get_integer_prop, _set_integer_prop)
ArcEllipse.p_fill_opacity = _Property('fill_opacity', _get_integer_prop, _set_integer_prop)
ArcEllipse.p_line_cap = _Property('line_cap', _get_line_cap_prop, _set_line_cap_prop)
ArcEllipse.p_polygon_smooth = _Property('polygon_smooth', _get_boolean_prop, _set_boolean_prop)
ArcEllipse.p_texture = _Property('texture', _get_texture_prop, _set_texture_prop)
ArcEllipse.p_modulate = _Property('modulate', _get_boolean_prop, _set_boolean_prop)
ArcEllipse.p_gradient = _Property('gradient', _get_integer_prop, _set_integer_prop)


# Assignment
Assignment.p_enable = _Property('enable', _get_boolean_prop, _set_boolean_prop)


# Behavior
Behavior.p_enable = _Property('enable', _get_boolean_prop, _set_boolean_prop)
Behavior.p_file = _Property('file', _get_file_prop, _set_file_prop)
Behavior.p_function = _Property('function', _get_node_function_prop, _set_node_function_prop)
Behavior.p_input_parameters = _Property('input_parameters', _get_input_parameters_prop, _set_input_parameters_prop)
Behavior.p_output_parameters = _Property('output_parameters', _get_output_parameters_prop, _set_output_parameters_prop)


# BiFont
BiFont.p_visible = _Property('visible', _get_boolean_prop, _set_boolean_prop)
BiFont.p_position = _Property('position', _get_point_property, _set_point_property)
BiFont.p_value = _Property('value', _get_real_prop, _set_real_prop)
BiFont.p_format = _Property('format', _get_format_prop, _set_format_prop)
BiFont.p_haloing = _Property('haloing', _get_boolean_prop, _set_boolean_prop)
BiFont.p_first_line_width = _Property('first_line_width', _get_integer_prop, _set_integer_prop)
BiFont.p_first_font = _Property('first_font', _get_integer_prop, _set_integer_prop)
BiFont.p_outline_color = _Property('outline_color', _get_integer_prop, _set_integer_prop)
BiFont.p_halo_color = _Property('halo_color', _get_integer_prop, _set_integer_prop)
BiFont.p_horiz_align = _Property('horiz_align', _get_text_horiz_align_prop, _set_text_horiz_align_prop)
BiFont.p_vert_align = _Property('vert_align', _get_text_vert_align_prop, _set_text_vert_align_prop)
BiFont.p_second_font = _Property('second_font', _get_integer_prop, _set_integer_prop)
BiFont.p_second_line_width = _Property('second_line_width', _get_integer_prop, _set_integer_prop)


# Bitmap
Bitmap.p_visible = _Property('visible', _get_boolean_prop, _set_boolean_prop)
Bitmap.p_position = _Property('position', _get_point_property, _set_point_property)
Bitmap.p_texture_id = _Property('texture_id', _get_integer_prop, _set_integer_prop)


# Circle
Circle.p_visible = _Property('visible', _get_boolean_prop, _set_boolean_prop)
Circle.p_center = _Property('center', _get_point_property, _set_point_property)
Circle.p_radius = _Property('radius', _get_real_prop, _set_real_prop)
Circle.p_haloing = _Property('haloing', _get_boolean_prop, _set_boolean_prop)
Circle.p_line_width = _Property('line_width', _get_integer_prop, _set_integer_prop)
Circle.p_line_stipple = _Property('line_stipple', _get_integer_prop, _set_integer_prop)
Circle.p_outline_color = _Property('outline_color', _get_integer_prop, _set_integer_prop)
Circle.p_halo_color = _Property('halo_color', _get_integer_prop, _set_integer_prop)
Circle.p_fill_color = _Property('fill_color', _get_integer_prop, _set_integer_prop)
Circle.p_outline_opacity = _Property('outline_opacity', _get_integer_prop, _set_integer_prop)
Circle.p_fill_opacity = _Property('fill_opacity', _get_integer_prop, _set_integer_prop)
Circle.p_line_cap = _Property('line_cap', _get_line_cap_prop, _set_line_cap_prop)
Circle.p_polygon_smooth = _Property('polygon_smooth', _get_boolean_prop, _set_boolean_prop)
Circle.p_texture = _Property('texture', _get_texture_prop, _set_texture_prop)
Circle.p_modulate = _Property('modulate', _get_boolean_prop, _set_boolean_prop)
Circle.p_gradient = _Property('gradient', _get_integer_prop, _set_integer_prop)


# CircleArea
CircleArea.p_enable = _Property('enable', _get_boolean_prop, _set_boolean_prop)
CircleArea.p_pointer_id = _Property('pointer_id', _get_integer_prop, _set_integer_prop)
CircleArea.p_center = _Property('center', _get_point_property, _set_point_property)
CircleArea.p_radius = _Property('radius', _get_real_prop, _set_real_prop)


# ClipBox
ClipBox.p_mask_activity = _Property('mask_activity', _get_boolean_prop, _set_boolean_prop)
ClipBox.p_clip_inside = _Property('clip_inside', _get_boolean_prop, _set_boolean_prop)
ClipBox.p_first_point = _Property('first_point', _get_point_property, _set_point_property)
ClipBox.p_third_point = _Property('third_point', _get_point_property, _set_point_property)


# ClipPlane
ClipPlane.p_mask_activity = _Property('mask_activity', _get_boolean_prop, _set_boolean_prop)
ClipPlane.p_clip_start_point = _Property('clip_start_point', _get_point_property, _set_point_property)
ClipPlane.p_clip_angle = _Property('clip_angle', _get_angle_prop, _set_angle_prop)
ClipPlane.p_orientation = _Property('orientation', _get_orientation_prop, _set_orientation_prop)


# Crown
Crown.p_visible = _Property('visible', _get_boolean_prop, _set_boolean_prop)
Crown.p_center = _Property('center', _get_point_property, _set_point_property)
Crown.p_radius = _Property('radius', _get_real_prop, _set_real_prop)
Crown.p_start_angle = _Property('start_angle', _get_angle_prop, _set_angle_prop)
Crown.p_end_angle = _Property('end_angle', _get_angle_prop, _set_angle_prop)
Crown.p_orientation = _Property('orientation', _get_orientation_prop, _set_orientation_prop)
Crown.p_thickness = _Property('thickness', _get_real_prop, _set_real_prop)
Crown.p_haloing = _Property('haloing', _get_boolean_prop, _set_boolean_prop)
Crown.p_line_width = _Property('line_width', _get_integer_prop, _set_integer_prop)
Crown.p_line_stipple = _Property('line_stipple', _get_integer_prop, _set_integer_prop)
Crown.p_outline_color = _Property('outline_color', _get_integer_prop, _set_integer_prop)
Crown.p_halo_color = _Property('halo_color', _get_integer_prop, _set_integer_prop)
Crown.p_fill_color = _Property('fill_color', _get_integer_prop, _set_integer_prop)
Crown.p_outline_opacity = _Property('outline_opacity', _get_integer_prop, _set_integer_prop)
Crown.p_fill_opacity = _Property('fill_opacity', _get_integer_prop, _set_integer_prop)
Crown.p_line_cap = _Property('line_cap', _get_line_cap_prop, _set_line_cap_prop)
Crown.p_polygon_smooth = _Property('polygon_smooth', _get_boolean_prop, _set_boolean_prop)
Crown.p_texture = _Property('texture', _get_texture_prop, _set_texture_prop)
Crown.p_modulate = _Property('modulate', _get_boolean_prop, _set_boolean_prop)
Crown.p_gradient = _Property('gradient', _get_integer_prop, _set_integer_prop)


# CursorPosRequest
CursorPosRequest.p_enable = _Property('enable', _get_boolean_prop, _set_boolean_prop)
CursorPosRequest.p_cursor_id = _Property('cursor_id', _get_integer_prop, _set_integer_prop)
CursorPosRequest.p_cursor_position = _Property('cursor_position', _get_point_property, _set_point_property)


# Ellipse
Ellipse.p_visible = _Property('visible', _get_boolean_prop, _set_boolean_prop)
Ellipse.p_center = _Property('center', _get_point_property, _set_point_property)
Ellipse.p_horz_radius = _Property('horz_radius', _get_real_prop, _set_real_prop)
Ellipse.p_vert_radius = _Property('vert_radius', _get_real_prop, _set_real_prop)
Ellipse.p_haloing = _Property('haloing', _get_boolean_prop, _set_boolean_prop)
Ellipse.p_line_width = _Property('line_width', _get_integer_prop, _set_integer_prop)
Ellipse.p_line_stipple = _Property('line_stipple', _get_integer_prop, _set_integer_prop)
Ellipse.p_outline_color = _Property('outline_color', _get_integer_prop, _set_integer_prop)
Ellipse.p_halo_color = _Property('halo_color', _get_integer_prop, _set_integer_prop)
Ellipse.p_fill_color = _Property('fill_color', _get_integer_prop, _set_integer_prop)
Ellipse.p_outline_opacity = _Property('outline_opacity', _get_integer_prop, _set_integer_prop)
Ellipse.p_fill_opacity = _Property('fill_opacity', _get_integer_prop, _set_integer_prop)
Ellipse.p_line_cap = _Property('line_cap', _get_line_cap_prop, _set_line_cap_prop)
Ellipse.p_polygon_smooth = _Property('polygon_smooth', _get_boolean_prop, _set_boolean_prop)
Ellipse.p_texture = _Property('texture', _get_texture_prop, _set_texture_prop)
Ellipse.p_modulate = _Property('modulate', _get_boolean_prop, _set_boolean_prop)
Ellipse.p_gradient = _Property('gradient', _get_integer_prop, _set_integer_prop)


# Hook
Hook.p_visible = _Property('visible', _get_boolean_prop, _set_boolean_prop)
Hook.p_index = _Property('index', _get_integer_prop, _set_integer_prop)


# Imported
Imported.p_enable = _Property('enable', _get_boolean_prop, _set_boolean_prop)
Imported.p_restore_states = _Property('restore_states', _get_boolean_prop, _set_boolean_prop)
Imported.p_function = _Property('function', _get_function_prop, _set_function_prop)
Imported.p_memory = _Property('memory', _get_boolean_prop, _set_boolean_prop)
Imported.p_input_parameters = _Property('input_parameters', _get_input_parameters_prop, _set_input_parameters_prop)
Imported.p_output_parameters = _Property('output_parameters', _get_output_parameters_prop, _set_output_parameters_prop)


# KeyboardEventListener
KeyboardEventListener.p_enable = _Property('enable', _get_boolean_prop, _set_boolean_prop)
KeyboardEventListener.p_event_id = _Property('event_id', _get_integer_prop, _set_integer_prop)


# Line
Line.p_visible = _Property('visible', _get_boolean_prop, _set_boolean_prop)
Line.p_line_width = _Property('line_width', _get_integer_prop, _set_integer_prop)
Line.p_line_stipple = _Property('line_stipple', _get_integer_prop, _set_integer_prop)
Line.p_haloing = _Property('haloing', _get_boolean_prop, _set_boolean_prop)
Line.p_outline_color = _Property('outline_color', _get_integer_prop, _set_integer_prop)
Line.p_halo_color = _Property('halo_color', _get_integer_prop, _set_integer_prop)
Line.p_outline_opacity = _Property('outline_opacity', _get_integer_prop, _set_integer_prop)
Line.p_line_cap = _Property('line_cap', _get_line_cap_prop, _set_line_cap_prop)


# Path
Path.p_visible = _Property('visible', _get_boolean_prop, _set_boolean_prop)
Path.p_line_width = _Property('line_width', _get_integer_prop, _set_integer_prop)
Path.p_line_stipple = _Property('line_stipple', _get_integer_prop, _set_integer_prop)
Path.p_line_cap = _Property('line_cap', _get_line_cap_prop, _set_line_cap_prop)
Path.p_haloing = _Property('haloing', _get_boolean_prop, _set_boolean_prop)
Path.p_halo_color = _Property('halo_color', _get_integer_prop, _set_integer_prop)
Path.p_outline_color = _Property('outline_color', _get_integer_prop, _set_integer_prop)
Path.p_outline_opacity = _Property('outline_opacity', _get_integer_prop, _set_integer_prop)
Path.p_fill_color = _Property('fill_color', _get_integer_prop, _set_integer_prop)
Path.p_fill_opacity = _Property('fill_opacity', _get_integer_prop, _set_integer_prop)
Path.p_polygon_smooth = _Property('polygon_smooth', _get_boolean_prop, _set_boolean_prop)
Path.p_texture = _Property('texture', _get_texture_prop, _set_texture_prop)
Path.p_gradient = _Property('gradient', _get_integer_prop, _set_integer_prop)
Path.p_modulate = _Property('modulate', _get_boolean_prop, _set_boolean_prop)
Path.p_tessellate = _Property('tessellate', _get_boolean_prop, _set_boolean_prop)


# PointTextureProp
PointTextureProp.p_u = _Property('u', _get_real_prop, _set_real_prop)
PointTextureProp.p_v = _Property('v', _get_real_prop, _set_real_prop)


# PointerEventListener
PointerEventListener.p_enable = _Property('enable', _get_boolean_prop, _set_boolean_prop)
PointerEventListener.p_event_id = _Property('event_id', _get_integer_prop, _set_integer_prop)
PointerEventListener.p_relative = _Property('relative', _get_boolean_prop, _set_boolean_prop)


# Rectangle
Rectangle.p_visible = _Property('visible', _get_boolean_prop, _set_boolean_prop)
Rectangle.p_first_point = _Property('first_point', _get_point_texture_prop, _set_point_texture_prop)
Rectangle.p_third_point = _Property('third_point', _get_point_texture_prop, _set_point_texture_prop)
Rectangle.p_first_arc = _Property('first_arc', _get_arc_segment_prop, _set_arc_segment_prop)
Rectangle.p_second_arc = _Property('second_arc', _get_arc_segment_prop, _set_arc_segment_prop)
Rectangle.p_third_arc = _Property('third_arc', _get_arc_segment_prop, _set_arc_segment_prop)
Rectangle.p_fourth_arc = _Property('fourth_arc', _get_arc_segment_prop, _set_arc_segment_prop)
Rectangle.p_haloing = _Property('haloing', _get_boolean_prop, _set_boolean_prop)
Rectangle.p_line_width = _Property('line_width', _get_integer_prop, _set_integer_prop)
Rectangle.p_line_stipple = _Property('line_stipple', _get_integer_prop, _set_integer_prop)
Rectangle.p_outline_color = _Property('outline_color', _get_integer_prop, _set_integer_prop)
Rectangle.p_halo_color = _Property('halo_color', _get_integer_prop, _set_integer_prop)
Rectangle.p_fill_color = _Property('fill_color', _get_integer_prop, _set_integer_prop)
Rectangle.p_outline_opacity = _Property('outline_opacity', _get_integer_prop, _set_integer_prop)
Rectangle.p_fill_opacity = _Property('fill_opacity', _get_integer_prop, _set_integer_prop)
Rectangle.p_line_cap = _Property('line_cap', _get_line_cap_prop, _set_line_cap_prop)
Rectangle.p_polygon_smooth = _Property('polygon_smooth', _get_boolean_prop, _set_boolean_prop)
Rectangle.p_texture = _Property('texture', _get_texture_prop, _set_texture_prop)
Rectangle.p_texture_control = _Property('texture_control', _get_boolean_prop, _set_boolean_prop)
Rectangle.p_modulate = _Property('modulate', _get_boolean_prop, _set_boolean_prop)
Rectangle.p_tessellate = _Property('tessellate', _get_boolean_prop, _set_boolean_prop)
Rectangle.p_gradient = _Property('gradient', _get_integer_prop, _set_integer_prop)


# RectangleArea
RectangleArea.p_enable = _Property('enable', _get_boolean_prop, _set_boolean_prop)
RectangleArea.p_pointer_id = _Property('pointer_id', _get_integer_prop, _set_integer_prop)
RectangleArea.p_first_point = _Property('first_point', _get_point_property, _set_point_property)
RectangleArea.p_third_point = _Property('third_point', _get_point_property, _set_point_property)


# RichText
RichText.p_visible = _Property('visible', _get_boolean_prop, _set_boolean_prop)
RichText.p_position = _Property('position', _get_point_property, _set_point_property)
RichText.p_max_length = _Property('max_length', _get_integer_prop, _set_integer_prop)
RichText.p_text_value = _Property('text_value', _get_text_prop, _set_text_prop)
RichText.p_line_width = _Property('line_width', _get_integer_prop, _set_integer_prop)
RichText.p_font = _Property('font', _get_integer_prop, _set_integer_prop)
RichText.p_outline_color = _Property('outline_color', _get_integer_prop, _set_integer_prop)
RichText.p_horiz_align = _Property('horiz_align', _get_text_horiz_align_prop, _set_text_horiz_align_prop)
RichText.p_vert_align = _Property('vert_align', _get_text_vert_align_prop, _set_text_vert_align_prop)


# Shape
Shape.p_visible = _Property('visible', _get_boolean_prop, _set_boolean_prop)
Shape.p_haloing = _Property('haloing', _get_boolean_prop, _set_boolean_prop)
Shape.p_line_width = _Property('line_width', _get_integer_prop, _set_integer_prop)
Shape.p_line_stipple = _Property('line_stipple', _get_integer_prop, _set_integer_prop)
Shape.p_outline_color = _Property('outline_color', _get_integer_prop, _set_integer_prop)
Shape.p_halo_color = _Property('halo_color', _get_integer_prop, _set_integer_prop)
Shape.p_fill_color = _Property('fill_color', _get_integer_prop, _set_integer_prop)
Shape.p_outline_opacity = _Property('outline_opacity', _get_integer_prop, _set_integer_prop)
Shape.p_fill_opacity = _Property('fill_opacity', _get_integer_prop, _set_integer_prop)
Shape.p_line_cap = _Property('line_cap', _get_line_cap_prop, _set_line_cap_prop)
Shape.p_polygon_smooth = _Property('polygon_smooth', _get_boolean_prop, _set_boolean_prop)
Shape.p_texture_control = _Property('texture_control', _get_boolean_prop, _set_boolean_prop)
Shape.p_texture = _Property('texture', _get_texture_prop, _set_texture_prop)
Shape.p_modulate = _Property('modulate', _get_boolean_prop, _set_boolean_prop)
Shape.p_tessellate = _Property('tessellate', _get_boolean_prop, _set_boolean_prop)
Shape.p_gradient = _Property('gradient', _get_integer_prop, _set_integer_prop)


# ShapeArea
ShapeArea.p_enable = _Property('enable', _get_boolean_prop, _set_boolean_prop)
ShapeArea.p_pointer_id = _Property('pointer_id', _get_integer_prop, _set_integer_prop)
ShapeArea.p_points = _Property('points', _get_points_prop, _set_points_prop)


# Stencil
Stencil.p_mask_activity = _Property('mask_activity', _get_boolean_prop, _set_boolean_prop)
Stencil.p_tessellate = _Property('tessellate', _get_boolean_prop, _set_boolean_prop)


# Text
Text.p_visible = _Property('visible', _get_boolean_prop, _set_boolean_prop)
Text.p_position = _Property('position', _get_point_property, _set_point_property)
Text.p_max_length = _Property('max_length', _get_integer_prop, _set_integer_prop)
Text.p_text_value = _Property('text_value', _get_text_prop, _set_text_prop)
Text.p_haloing = _Property('haloing', _get_boolean_prop, _set_boolean_prop)
Text.p_line_width = _Property('line_width', _get_integer_prop, _set_integer_prop)
Text.p_font = _Property('font', _get_integer_prop, _set_integer_prop)
Text.p_outline_color = _Property('outline_color', _get_integer_prop, _set_integer_prop)
Text.p_halo_color = _Property('halo_color', _get_integer_prop, _set_integer_prop)
Text.p_horiz_align = _Property('horiz_align', _get_text_horiz_align_prop, _set_text_horiz_align_prop)
Text.p_vert_align = _Property('vert_align', _get_text_vert_align_prop, _set_text_vert_align_prop)


# TextArea
TextArea.p_visible = _Property('visible', _get_boolean_prop, _set_boolean_prop)
TextArea.p_first_point = _Property('first_point', _get_point_property, _set_point_property)
TextArea.p_third_point = _Property('third_point', _get_point_property, _set_point_property)
TextArea.p_max_length = _Property('max_length', _get_integer_prop, _set_integer_prop)
TextArea.p_text_value = _Property('text_value', _get_text_prop, _set_text_prop)
TextArea.p_haloing = _Property('haloing', _get_boolean_prop, _set_boolean_prop)
TextArea.p_line_width = _Property('line_width', _get_integer_prop, _set_integer_prop)
TextArea.p_font = _Property('font', _get_integer_prop, _set_integer_prop)
TextArea.p_outline_color = _Property('outline_color', _get_integer_prop, _set_integer_prop)
TextArea.p_halo_color = _Property('halo_color', _get_integer_prop, _set_integer_prop)
TextArea.p_horiz_align = _Property('horiz_align', _get_text_horiz_align_prop, _set_text_horiz_align_prop)
TextArea.p_vert_align = _Property('vert_align', _get_text_vert_align_prop, _set_text_vert_align_prop)


# CondContainer
CondContainer.p_visible = _Property('visible', _get_boolean_prop, _set_boolean_prop)
CondContainer.p_priority = _Property('priority', _get_priority_prop, _set_priority_prop)
CondContainer.p_origin = _Property('origin', _get_point_property, _set_point_property)
CondContainer.p_rotate = _Property('rotate', _get_angle_prop, _set_angle_prop)
CondContainer.p_orientation = _Property('orientation', _get_orientation_prop, _set_orientation_prop)
CondContainer.p_scale = _Property('scale', _get_coordinate_point, _set_coordinate_point)
CondContainer.p_index = _Property('index', _get_conditional_index_prop, _set_conditional_index_prop)
CondContainer.p_indexes = _Property('indexes', _get_indexes_prop, _set_indexes_prop)


# Container
Container.p_visible = _Property('visible', _get_boolean_prop, _set_boolean_prop)
Container.p_priority = _Property('priority', _get_priority_prop, _set_priority_prop)
Container.p_origin = _Property('origin', _get_point_property, _set_point_property)
Container.p_rotate = _Property('rotate', _get_angle_prop, _set_angle_prop)
Container.p_orientation = _Property('orientation', _get_orientation_prop, _set_orientation_prop)
Container.p_scale = _Property('scale', _get_coordinate_point, _set_coordinate_point)
Container.p_static = _Property('static', _get_static_container_prop, _set_static_container_prop)


# FilterRotationContainer
FilterRotationContainer.p_visible = _Property('visible', _get_boolean_prop, _set_boolean_prop)
FilterRotationContainer.p_origin = _Property('origin', _get_point_property, _set_point_property)
FilterRotationContainer.p_orientation = _Property('orientation', _get_orientation_prop, _set_orientation_prop)
FilterRotationContainer.p_start_rotation_angle = _Property('start_rotation_angle', _get_angle_prop, _set_angle_prop)
FilterRotationContainer.p_end_rotation_angle = _Property('end_rotation_angle', _get_angle_prop, _set_angle_prop)
FilterRotationContainer.p_start_rotation_value = _Property('start_rotation_value', _get_real_prop, _set_real_prop)
FilterRotationContainer.p_end_rotation_value = _Property('end_rotation_value', _get_real_prop, _set_real_prop)
FilterRotationContainer.p_start_rotation_locked = _Property('start_rotation_locked', _get_boolean_prop, _set_boolean_prop)
FilterRotationContainer.p_end_rotation_locked = _Property('end_rotation_locked', _get_boolean_prop, _set_boolean_prop)
FilterRotationContainer.p_priority = _Property('priority', _get_priority_prop, _set_priority_prop)


# FilterTranslationContainer
FilterTranslationContainer.p_visible = _Property('visible', _get_boolean_prop, _set_boolean_prop)
FilterTranslationContainer.p_origin = _Property('origin', _get_point_property, _set_point_property)
FilterTranslationContainer.p_start_translation_point = _Property('start_translation_point', _get_point_property, _set_point_property)
FilterTranslationContainer.p_end_translation_point = _Property('end_translation_point', _get_point_property, _set_point_property)
FilterTranslationContainer.p_start_translation_value = _Property('start_translation_value', _get_real_prop, _set_real_prop)
FilterTranslationContainer.p_end_translation_value = _Property('end_translation_value', _get_real_prop, _set_real_prop)
FilterTranslationContainer.p_start_translation_locked = _Property('start_translation_locked', _get_boolean_prop, _set_boolean_prop)
FilterTranslationContainer.p_end_translation_locked = _Property('end_translation_locked', _get_boolean_prop, _set_boolean_prop)
FilterTranslationContainer.p_priority = _Property('priority', _get_priority_prop, _set_priority_prop)


# Layer
Layer.p_visible = _Property('visible', _get_boolean_prop, _set_boolean_prop)
Layer.p_origin = _Property('origin', _get_coordinate_point, _set_coordinate_point)
Layer.p_id = _Property('id', _get_integer_prop, _set_integer_prop)


# MaskContainer
MaskContainer.p_mask_activity = _Property('mask_activity', _get_boolean_prop, _set_boolean_prop)
MaskContainer.p_origin = _Property('origin', _get_point_property, _set_point_property)
MaskContainer.p_rotate = _Property('rotate', _get_angle_prop, _set_angle_prop)
MaskContainer.p_orientation = _Property('orientation', _get_orientation_prop, _set_orientation_prop)
MaskContainer.p_scale = _Property('scale', _get_coordinate_point, _set_coordinate_point)
MaskContainer.p_clip_inside = _Property('clip_inside', _get_boolean_prop, _set_boolean_prop)


# NplicatorContainer
NplicatorContainer.p_file = _Property('file', _get_file_prop, _set_file_prop)
NplicatorContainer.p_replication = _Property('replication', _get_integer_prop, _set_integer_prop)
NplicatorContainer.p_visible = _Property('visible', _get_boolean_array_prop, _set_boolean_array_prop)
NplicatorContainer.p_origin = _Property('origin', _get_point_array_prop, _set_point_array_prop)
NplicatorContainer.p_rotate = _Property('rotate', _get_angle_array_prop, _set_angle_array_prop)
NplicatorContainer.p_orientation = _Property('orientation', _get_orientation_prop, _set_orientation_prop)
NplicatorContainer.p_scale = _Property('scale', _get_point_array_prop, _set_point_array_prop)
NplicatorContainer.p_constant_parameters = _Property('constant_parameters', _get_input_parameters_prop, _set_input_parameters_prop)
NplicatorContainer.p_input_parameters = _Property('input_parameters', _get_input_parameters_prop, _set_input_parameters_prop)
NplicatorContainer.p_output_parameters = _Property('output_parameters', _get_output_parameters_prop, _set_output_parameters_prop)


# PanelContainer
PanelContainer.p_visible = _Property('visible', _get_boolean_prop, _set_boolean_prop)
PanelContainer.p_origin = _Property('origin', _get_point_property, _set_point_property)
PanelContainer.p_width = _Property('width', _get_real_prop, _set_real_prop)
PanelContainer.p_height = _Property('height', _get_real_prop, _set_real_prop)
PanelContainer.p_priority = _Property('priority', _get_priority_prop, _set_priority_prop)


# ReferenceContainer
ReferenceContainer.p_file = _Property('file', _get_file_prop, _set_file_prop)
ReferenceContainer.p_visible = _Property('visible', _get_boolean_prop, _set_boolean_prop)
ReferenceContainer.p_origin = _Property('origin', _get_point_property, _set_point_property)
ReferenceContainer.p_rotate = _Property('rotate', _get_angle_prop, _set_angle_prop)
ReferenceContainer.p_orientation = _Property('orientation', _get_orientation_prop, _set_orientation_prop)
ReferenceContainer.p_scale = _Property('scale', _get_coordinate_point, _set_coordinate_point)
ReferenceContainer.p_constant_parameters = _Property('constant_parameters', _get_input_parameters_prop, _set_input_parameters_prop)
ReferenceContainer.p_input_parameters = _Property('input_parameters', _get_input_parameters_prop, _set_input_parameters_prop)
ReferenceContainer.p_output_parameters = _Property('output_parameters', _get_output_parameters_prop, _set_output_parameters_prop)


# RotationContainer
RotationContainer.p_visible = _Property('visible', _get_boolean_prop, _set_boolean_prop)
RotationContainer.p_origin = _Property('origin', _get_point_property, _set_point_property)
RotationContainer.p_ref_angle = _Property('ref_angle', _get_angle_prop, _set_angle_prop)
RotationContainer.p_orientation = _Property('orientation', _get_orientation_prop, _set_orientation_prop)
RotationContainer.p_start_rotation_angle = _Property('start_rotation_angle', _get_angle_prop, _set_angle_prop)
RotationContainer.p_end_rotation_angle = _Property('end_rotation_angle', _get_angle_prop, _set_angle_prop)
RotationContainer.p_start_rotation_value = _Property('start_rotation_value', _get_real_prop, _set_real_prop)
RotationContainer.p_end_rotation_value = _Property('end_rotation_value', _get_real_prop, _set_real_prop)
RotationContainer.p_start_rotation_locked = _Property('start_rotation_locked', _get_boolean_prop, _set_boolean_prop)
RotationContainer.p_end_rotation_locked = _Property('end_rotation_locked', _get_boolean_prop, _set_boolean_prop)
RotationContainer.p_functional_rotation_value = _Property('functional_rotation_value', _get_real_prop, _set_real_prop)
RotationContainer.p_priority = _Property('priority', _get_priority_prop, _set_priority_prop)


# TranslationContainer
TranslationContainer.p_visible = _Property('visible', _get_boolean_prop, _set_boolean_prop)
TranslationContainer.p_priority = _Property('priority', _get_priority_prop, _set_priority_prop)
TranslationContainer.p_origin = _Property('origin', _get_point_property, _set_point_property)
TranslationContainer.p_ref_point = _Property('ref_point', _get_point_property, _set_point_property)
TranslationContainer.p_start_translation_point = _Property('start_translation_point', _get_point_property, _set_point_property)
TranslationContainer.p_end_translation_point = _Property('end_translation_point', _get_point_property, _set_point_property)
TranslationContainer.p_start_translation_value = _Property('start_translation_value', _get_real_prop, _set_real_prop)
TranslationContainer.p_end_translation_value = _Property('end_translation_value', _get_real_prop, _set_real_prop)
TranslationContainer.p_start_translation_locked = _Property('start_translation_locked', _get_boolean_prop, _set_boolean_prop)
TranslationContainer.p_end_translation_locked = _Property('end_translation_locked', _get_boolean_prop, _set_boolean_prop)
TranslationContainer.p_functional_translation_value = _Property('functional_translation_value', _get_real_prop, _set_real_prop)

#}}sdy_access_dcl

#%% end
