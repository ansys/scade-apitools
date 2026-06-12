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
Test suite for sdyaccess.py.

Test strategy:

* Test at least one instance of property class

    * Assess read access
    * Assess write access

* Check accessors, produced from sdy.ecore, are consistent with SCADE Display API
"""

import ansys.scade.apitools.prop.sdyaccess as sdy


def test_angle_prop():
    # one of sdy.Arc, sdy.ArcEllipse, sdy.ClipPlane...
    angle = 1.991
    c = sdy.Arc(
        # one of start_angle, end_angle...
        start_angle=angle,
    )
    assert c.p_start_angle == angle
    angle = 2.026
    c.p_start_angle = angle
    assert c.start_angle.angle.init == angle


def test_arc_segment_prop():
    # one of sdy.Rectangle, sdy.IndexTexturePoint, sdy.IndexedPoint...
    c = sdy.Rectangle()
    # one of first_arc, second_arc, third_arc, fourth_arc
    assert c.first_arc is None
    assert c.p_first_arc == (False, 0.0)
    flag = True
    angle = 3.14
    value = (flag, angle)
    c.p_first_arc = value
    assert c.first_arc.orientation.clockwise == flag
    assert c.first_arc.angle.angle.init == angle


# N/A
# def test_assignment_output_prop():
#     pass


def test_coordinate_point():
    # one of sdy.MaskContainer, sdy.ReferenceContainer...
    c = sdy.MaskContainer(scale=(1.2, 3.4))
    assert c.p_scale == (c.scale.x.init, c.scale.y.init)
    x = 5.6
    y = 7.7
    c.p_scale = (x, y)
    assert c.scale.x.init == x
    assert c.scale.y.init == y


def test_file_prop():
    # one of sdy.Behavior, sdy.NplicatorContainer, sdy.ReferenceContainer...
    c = sdy.Behavior(file='project.etp')
    assert c.p_file == c.file.file
    value = 'project_ex.etp'
    c.p_file = value
    assert c.file.file == value


def test_format_prop():
    # one of sdy.BiFont...
    c = sdy.BiFont()
    assert c.p_format == (
        c.format.separator,
        c.format.integral_part.init,
        c.format.fractional_part.init,
        c.format.second_font_pos.init,
        c.format.leading_zeros.init,
        c.format.display_sign.init,
    )

    s = 3
    ip = 1
    fp = 2
    sfp = 4
    lz = True
    ds = sdy.DisplaySignEnum.WHENNEGATIVE
    c.p_format = (s, ip, fp, sfp, lz, ds)
    assert c.format.integral_part.init == ip
    assert c.format.fractional_part.init == fp
    assert c.format.separator == s
    assert c.format.second_font_pos.init == sfp
    assert c.format.leading_zeros.init == lz
    assert c.format.display_sign.init == ds


def test_function_prop():
    # one of sdy.Imported...
    c = sdy.Imported(function='f')
    assert c.p_function == c.function.name
    value = 'g'
    c.p_function = value
    assert c.function.name == value


def test_indexed_points_prop():
    points = [(1.0, 2.0), (3.0, 4.0), (5.0, 6.0)]
    # one of sdy.Line, sdy.Stencil...
    c = sdy.Line(points=points)
    for index, point in enumerate(points):
        assert c.points.points[index].p_point == point
        assert c.points.points[index].p_arc_segment == (False, 0.0)


def test_indexes_prop():
    # one of sdy.CondContainer...
    c = sdy.CondContainer()
    assert c.p_indexes == c.indexes.default_is_other
    dis = not c.p_indexes
    c.p_indexes = dis
    assert c.indexes.default_is_other == dis


def test_input_parameters_prop():
    bool_type = sdy.PredefType(sdy.SimpleType.BOOL)
    inputs = [('I0', bool_type)]
    # one of sdy.Behavior, sdy.Imported, sdy.NplicatorContainer...
    c = sdy.NplicatorContainer(
        # one of input_parameters, constant_parameters...
        inputs=inputs,  # type: ignore
    )
    values = [(_.name, _.representation) for _ in c.input_parameters.parameters]
    assert c.p_input_parameters == values
    inputs = [('color', sdy.Representation.COLOR), ('font', sdy.Representation.FONT)]
    c.p_input_parameters = inputs
    assert c.input_parameters.parameters[0].name == inputs[0][0]
    assert c.input_parameters.parameters[0].representation == inputs[0][1]
    assert c.input_parameters.parameters[1].name == inputs[1][0]
    assert c.input_parameters.parameters[1].representation == inputs[1][1]

    # for index, name in enumerate(opts):
    #     prop_name = f'p_{name}'
    #     value = getattr(c, name)
    #     assert value is None
    #     assert getattr(c, prop_name) == []  # ('', sdy.Representation.NONE)
    #     param = f'C{index}'
    #     representation = sdy.Representation.GRADIENT
    #     value = [(param, representation)]
    #     setattr(c, prop_name, value)
    #     assert getattr(c, prop_name) == value
    #     assert len(getattr(c, name).parameters) == 1
    #     assert getattr(c, name).parameters[0].name == param
    #     assert getattr(c, name).parameters[0].representation == representation


def test_node_function_prop():
    # one of sdy.Behavior...
    c = sdy.Behavior(function='F')
    is_node = c.function.is_node
    assert c.p_function == (c.function.is_node, c.function.name)
    is_node = not c.function.is_node
    name = 'G'
    c.p_function = (is_node, name)
    assert c.function.is_node == is_node
    assert c.function.name == name


def test_orientation_property():
    # one of sdy.Arc, sdy.ArcEllipse, sdy.ClipPlane...
    c = sdy.Arc(clockwise=False)

    assert not c.p_orientation
    c.p_orientation = True
    assert c.orientation.clockwise


def test_output_parameters_prop():
    bool_type = sdy.PredefType(sdy.SimpleType.BOOL)
    outputs = [('O1', bool_type)]
    # one of sdy.Behavior, sdy.Imported, sdy.NplicatorContainer...
    c = sdy.NplicatorContainer(
        # one of input_parameters, constant_parameters...
        outputs=outputs,  # type: ignore
    )
    values = [(_.name, _.representation) for _ in c.output_parameters.output_parameters]
    assert c.p_output_parameters == values
    outputs = [('color', sdy.Representation.COLOR), ('font', sdy.Representation.FONT)]
    c.p_output_parameters = outputs
    assert c.output_parameters.output_parameters[0].name == outputs[0][0]
    assert c.output_parameters.output_parameters[0].representation == outputs[0][1]
    assert c.output_parameters.output_parameters[1].name == outputs[1][0]
    assert c.output_parameters.output_parameters[1].representation == outputs[1][1]


# N/A
# def test_output_point_prop():
#     pass


# N/A
# def test_pluggable_property():
#     pass


def test_point_array_prop():
    # one of sdy.NplicatorContainer...
    c = sdy.NplicatorContainer(
        # one of origin, scale...
        origin=[(1.0, 2.0), (3.0, 4.0), (5.0, 6.0)],
    )
    assert c.p_origin == ([1.0, 3.0, 5.0], [2.0, 4.0, 6.0])
    c.p_origin = ([5.0, 6.0, 7.0], [8.0, 9.0, 0.0])
    assert c.origin.x.init[0] == 5.0
    assert c.origin.x.init[1] == 6.0
    assert c.origin.x.init[2] == 7.0
    assert c.origin.y.init[0] == 8.0
    assert c.origin.y.init[1] == 9.0
    assert c.origin.y.init[2] == 0.0


def test_points_prop():
    points = [(1.0, 2.0), (3.0, 4.0)]
    # one of sdy.ShapeArea...
    c = sdy.ShapeArea(
        # one of points...
        points=points,
    )
    assert c.p_points == points
    c.p_points = [(5.0, 6.0)]
    assert len(c.points.point) == 1
    assert c.points.point[0].x.init == 5.0
    assert c.points.point[0].y.init == 6.0


def test_static_container_prop():
    # one of sdy.Container...
    c = sdy.Container()
    assert c.static is None
    assert c.p_static == (False, 0.0, 0.0, 0.0, 0.0, False)
    init = False
    min_x = 4.0
    max_x = 3.0
    min_y = 2.0
    max_y = 1.0
    gss = True
    c.p_static = (init, min_x, max_x, min_y, max_y, gss)
    assert c.static.init == init
    assert c.static.min_x == min_x
    assert c.static.max_x == max_x
    assert c.static.min_y == min_y
    assert c.static.max_y == max_y
    assert c.static.generate_static_sequence == gss


def test_texture_prop():
    # one of sdy.Arc, sdy.ArcEllipse, sdy.Circle...
    c = sdy.Arc()
    assert c.texture is None
    assert c.p_texture == (
        sdy.HorizAlignEnum.LEFT,
        sdy.VertAlignEnum.TOP,
        0.0,
        0.0,
        0,
    )
    ha = sdy.HorizAlignEnum.CENTER
    va = sdy.VertAlignEnum.MIDDLE
    hp = 1.0
    vp = 2.0
    id = 31
    c.p_texture = (ha, va, hp, vp, id)
    assert c.texture.horiz_align == ha
    assert c.texture.vert_align == va
    assert c.texture.horiz_pattern == hp
    assert c.texture.vert_pattern == vp
    assert c.texture.texture_id.init == id


def test_angle_array_prop():
    # one of sdy.NplicatorContainer...
    c = sdy.NplicatorContainer()
    values = [1.0, 2.0]
    c.p_rotate = values
    assert c.p_rotate == values
    assert c.rotate.init == values


def test_boolean_array_prop():
    # one of sdy.NplicatorContainer...
    c = sdy.NplicatorContainer()
    values = [True, False]
    c.p_visible = values
    assert c.p_visible == values
    assert c.visible.init == values


def test_boolean_prop():
    # one of sdy.Arc, sdy.ArcEllipse, sdy.BiFont...
    c = sdy.Arc(
        # one of haloing...
        haloing=True,
    )
    assert c.p_haloing
    c.p_haloing = False
    assert not c.haloing.init


def test_conditionnal_index_prop():
    # one of sdy.CondContainer...
    c = sdy.CondContainer()
    assert c.p_index == (c.index.index_prop_enum, c.index.all_visible)
    index = sdy.IndexPropEnum.OTHER
    all_visible = not c.index.all_visible
    c.p_index = (index, all_visible)
    assert c.index.index_prop_enum == index
    assert c.index.all_visible == all_visible


# N/A
# def test_input_prop():
#     pass


def test_integer_prop():
    # one of sdy.Arc, sdy.ArcEllipse, sdy.BiFont...
    c = sdy.Arc(
        # one of line_width, line_stipple, outline_color...
        line_width=9,
    )
    assert c.p_line_width == c.line_width.init
    value = c.line_width.init + 1
    c.p_line_width = value
    assert c.line_width.init == value


def test_line_cap_prop():
    # one of sdy.Arc, sdy.ArcEllipse, sdy.BiFont...
    c = sdy.Arc()
    assert c.line_cap is None
    assert c.p_line_cap in sdy.LineCapEnum
    value = sdy.LineCapEnum.ROUND
    c.p_line_cap = value
    assert c.line_cap.init == value


# N/A
# def test_param_prop():
#     pass


def test_priority_prop():
    # one of sdy.CondContainer, sdy.Container, sdy.FilterRotationContainer...
    c = sdy.CondContainer()
    assert c.priority is None
    assert c.p_priority == 0
    value = 31
    c.p_priority = value
    assert c.priority.init == value


def test_real_array_prop():
    # one of sdy.PointArrayProp...
    c = sdy.PointArrayProp()
    values = [-2.0, 3.14]
    # one of x, y...
    c.p_x = values
    assert c.p_x == values
    assert c.x.init == values


def test_real_prop():
    # one of sdy.EllipticalArc, sdy.HorizontalLineTo, sdy.VerticalLineTo...
    c = sdy.EllipticalArc(
        # one of x_radius, y_radius, x_axis_rotation...
        x_radius=0.9,
    )
    assert c.p_x_radius == c.x_radius.init
    value = 31.0
    c.p_x_radius = value
    assert c.x_radius.init == value


def test_text_horiz_align_prop():
    # one of sdy.BiFont, sdy.RichText, sdy.Text...
    c = sdy.BiFont()
    for value in sdy.HorizAlignEnum:
        c.p_horiz_align = value
        assert c.p_horiz_align == value
        assert c.horiz_align.init == value


def test_text_vert_align_prop():
    # one of sdy.BiFont, sdy.RichText, sdy.Text...
    c = sdy.BiFont()
    for value in sdy.VertAlignEnum:
        c.p_vert_align = value
        assert c.p_vert_align == value
        assert c.vert_align.init == value


def test_text_prop():
    # one of sdy.RichText, sdy.Text, sdy.TextArea...
    c = sdy.RichText()
    type_ = sdy.TextTypeEnum.INT
    init = [9, 31]
    value = (type_, init)
    c.p_text_value = value
    assert c.p_text_value == value
    assert c.text_value.type == type_
    assert c.text_value.init == init


def test_point_texture_prop():
    # one of sdy.Rectangle, sdy.IndexTexturePoint...
    c = sdy.Rectangle(
        # one of first_point, third_point
        first_point=(1.0, 2.0)
    )

    x = c.first_point.x.init
    y = c.first_point.y.init
    assert c.first_point.u is None
    assert c.first_point.v is None
    assert c.p_first_point == (x, y, 0.0, 0.0)
    x *= 2.0
    y *= 3.0
    u = -x
    v = -y
    c.p_first_point = (x, y, u, v)
    assert c.first_point.x.init == x
    assert c.first_point.y.init == y
    assert c.first_point.u.init == u
    assert c.first_point.v.init == v


# no white space required for markers
# fmt: off
#{{sdy_access_ut(sdy)
classes = {
    sdy.AngleProp: [
        ('angle', sdy.RealProp, False),
    ],
    sdy.Arc: [
        ('visible', sdy.BooleanProp, False),
        ('center', sdy.PointProperty, False),
        ('radius', sdy.RealProp, False),
        ('start_angle', sdy.AngleProp, False),
        ('end_angle', sdy.AngleProp, False),
        ('orientation', sdy.OrientationProp, False),
        ('haloing', sdy.BooleanProp, False),
        ('line_width', sdy.IntegerProp, False),
        ('line_stipple', sdy.IntegerProp, False),
        ('outline_color', sdy.IntegerProp, False),
        ('halo_color', sdy.IntegerProp, False),
        ('fill_color', sdy.IntegerProp, False),
        ('outline_opacity', sdy.IntegerProp, False),
        ('fill_opacity', sdy.IntegerProp, False),
        ('line_cap', sdy.LineCapProp, False),
        ('polygon_smooth', sdy.BooleanProp, False),
        ('texture', sdy.TextureProp, False),
        ('modulate', sdy.BooleanProp, False),
        ('gradient', sdy.IntegerProp, False),
    ],
    sdy.ArcEllipse: [
        ('visible', sdy.BooleanProp, False),
        ('center', sdy.PointProperty, False),
        ('horz_radius', sdy.RealProp, False),
        ('vert_radius', sdy.RealProp, False),
        ('start_angle', sdy.AngleProp, False),
        ('end_angle', sdy.AngleProp, False),
        ('orientation', sdy.OrientationProp, False),
        ('haloing', sdy.BooleanProp, False),
        ('line_width', sdy.IntegerProp, False),
        ('line_stipple', sdy.IntegerProp, False),
        ('outline_color', sdy.IntegerProp, False),
        ('halo_color', sdy.IntegerProp, False),
        ('fill_color', sdy.IntegerProp, False),
        ('outline_opacity', sdy.IntegerProp, False),
        ('fill_opacity', sdy.IntegerProp, False),
        ('line_cap', sdy.LineCapProp, False),
        ('polygon_smooth', sdy.BooleanProp, False),
        ('texture', sdy.TextureProp, False),
        ('modulate', sdy.BooleanProp, False),
        ('gradient', sdy.IntegerProp, False),
    ],
    sdy.ArcSegmentProp: [
        ('orientation', sdy.OrientationProp, False),
        ('angle', sdy.AngleProp, False),
    ],
    sdy.Assignment: [
        ('enable', sdy.BooleanProp, False),
    ],
    sdy.Behavior: [
        ('enable', sdy.BooleanProp, False),
        ('file', sdy.FileProp, False),
        ('function', sdy.NodeFunctionProp, False),
        ('input_parameters', sdy.InputParametersProp, False),
        ('output_parameters', sdy.OutputParametersProp, False),
    ],
    sdy.BiFont: [
        ('visible', sdy.BooleanProp, False),
        ('position', sdy.PointProperty, False),
        ('value', sdy.RealProp, False),
        ('format', sdy.FormatProp, False),
        ('haloing', sdy.BooleanProp, False),
        ('first_line_width', sdy.IntegerProp, False),
        ('first_font', sdy.IntegerProp, False),
        ('outline_color', sdy.IntegerProp, False),
        ('halo_color', sdy.IntegerProp, False),
        ('horiz_align', sdy.TextHorizAlignProp, False),
        ('vert_align', sdy.TextVertAlignProp, False),
        ('second_font', sdy.IntegerProp, False),
        ('second_line_width', sdy.IntegerProp, False),
    ],
    sdy.Bitmap: [
        ('visible', sdy.BooleanProp, False),
        ('position', sdy.PointProperty, False),
        ('texture_id', sdy.IntegerProp, False),
    ],
    sdy.Circle: [
        ('visible', sdy.BooleanProp, False),
        ('center', sdy.PointProperty, False),
        ('radius', sdy.RealProp, False),
        ('haloing', sdy.BooleanProp, False),
        ('line_width', sdy.IntegerProp, False),
        ('line_stipple', sdy.IntegerProp, False),
        ('outline_color', sdy.IntegerProp, False),
        ('halo_color', sdy.IntegerProp, False),
        ('fill_color', sdy.IntegerProp, False),
        ('outline_opacity', sdy.IntegerProp, False),
        ('fill_opacity', sdy.IntegerProp, False),
        ('line_cap', sdy.LineCapProp, False),
        ('polygon_smooth', sdy.BooleanProp, False),
        ('texture', sdy.TextureProp, False),
        ('modulate', sdy.BooleanProp, False),
        ('gradient', sdy.IntegerProp, False),
    ],
    sdy.CircleArea: [
        ('enable', sdy.BooleanProp, False),
        ('pointer_id', sdy.IntegerProp, False),
        ('center', sdy.PointProperty, False),
        ('radius', sdy.RealProp, False),
    ],
    sdy.ClipBox: [
        ('mask_activity', sdy.BooleanProp, False),
        ('clip_inside', sdy.BooleanProp, False),
        ('first_point', sdy.PointProperty, False),
        ('third_point', sdy.PointProperty, False),
    ],
    sdy.ClipPlane: [
        ('mask_activity', sdy.BooleanProp, False),
        ('clip_start_point', sdy.PointProperty, False),
        ('clip_angle', sdy.AngleProp, False),
        ('orientation', sdy.OrientationProp, False),
    ],
    sdy.CondContainer: [
        ('visible', sdy.BooleanProp, False),
        ('priority', sdy.PriorityProp, False),
        ('origin', sdy.PointProperty, False),
        ('rotate', sdy.AngleProp, False),
        ('orientation', sdy.OrientationProp, False),
        ('scale', sdy.CoordinatePoint, False),
        ('index', sdy.ConditionalIndexProp, False),
        ('indexes', sdy.IndexesProp, False),
    ],
    sdy.Container: [
        ('visible', sdy.BooleanProp, False),
        ('priority', sdy.PriorityProp, False),
        ('origin', sdy.PointProperty, False),
        ('rotate', sdy.AngleProp, False),
        ('orientation', sdy.OrientationProp, False),
        ('scale', sdy.CoordinatePoint, False),
        ('static', sdy.StaticContainerProp, False),
    ],
    sdy.CoordinatePoint: [
        ('x', sdy.RealProp, False),
        ('y', sdy.RealProp, False),
    ],
    sdy.Crown: [
        ('visible', sdy.BooleanProp, False),
        ('center', sdy.PointProperty, False),
        ('radius', sdy.RealProp, False),
        ('start_angle', sdy.AngleProp, False),
        ('end_angle', sdy.AngleProp, False),
        ('orientation', sdy.OrientationProp, False),
        ('thickness', sdy.RealProp, False),
        ('haloing', sdy.BooleanProp, False),
        ('line_width', sdy.IntegerProp, False),
        ('line_stipple', sdy.IntegerProp, False),
        ('outline_color', sdy.IntegerProp, False),
        ('halo_color', sdy.IntegerProp, False),
        ('fill_color', sdy.IntegerProp, False),
        ('outline_opacity', sdy.IntegerProp, False),
        ('fill_opacity', sdy.IntegerProp, False),
        ('line_cap', sdy.LineCapProp, False),
        ('polygon_smooth', sdy.BooleanProp, False),
        ('texture', sdy.TextureProp, False),
        ('modulate', sdy.BooleanProp, False),
        ('gradient', sdy.IntegerProp, False),
    ],
    sdy.CursorPosRequest: [
        ('enable', sdy.BooleanProp, False),
        ('cursor_id', sdy.IntegerProp, False),
        ('cursor_position', sdy.PointProperty, False),
    ],
    sdy.CurveTo: [
        ('first_control_point', sdy.PointProperty, False),
        ('second_control_point', sdy.PointProperty, False),
        ('end_point', sdy.PointProperty, False),
    ],
    sdy.Ellipse: [
        ('visible', sdy.BooleanProp, False),
        ('center', sdy.PointProperty, False),
        ('horz_radius', sdy.RealProp, False),
        ('vert_radius', sdy.RealProp, False),
        ('haloing', sdy.BooleanProp, False),
        ('line_width', sdy.IntegerProp, False),
        ('line_stipple', sdy.IntegerProp, False),
        ('outline_color', sdy.IntegerProp, False),
        ('halo_color', sdy.IntegerProp, False),
        ('fill_color', sdy.IntegerProp, False),
        ('outline_opacity', sdy.IntegerProp, False),
        ('fill_opacity', sdy.IntegerProp, False),
        ('line_cap', sdy.LineCapProp, False),
        ('polygon_smooth', sdy.BooleanProp, False),
        ('texture', sdy.TextureProp, False),
        ('modulate', sdy.BooleanProp, False),
        ('gradient', sdy.IntegerProp, False),
    ],
    sdy.EllipticalArc: [
        ('x_radius', sdy.RealProp, False),
        ('y_radius', sdy.RealProp, False),
        ('x_axis_rotation', sdy.RealProp, False),
        ('large_arc_flag', sdy.BooleanProp, False),
        ('sweep_flag', sdy.BooleanProp, False),
        ('end_point', sdy.PointProperty, False),
    ],
    sdy.FilterRotationContainer: [
        ('visible', sdy.BooleanProp, False),
        ('origin', sdy.PointProperty, False),
        ('orientation', sdy.OrientationProp, False),
        ('start_rotation_angle', sdy.AngleProp, False),
        ('end_rotation_angle', sdy.AngleProp, False),
        ('start_rotation_value', sdy.RealProp, False),
        ('end_rotation_value', sdy.RealProp, False),
        ('start_rotation_locked', sdy.BooleanProp, False),
        ('end_rotation_locked', sdy.BooleanProp, False),
        ('priority', sdy.PriorityProp, False),
    ],
    sdy.FilterTranslationContainer: [
        ('visible', sdy.BooleanProp, False),
        ('origin', sdy.PointProperty, False),
        ('start_translation_point', sdy.PointProperty, False),
        ('end_translation_point', sdy.PointProperty, False),
        ('start_translation_value', sdy.RealProp, False),
        ('end_translation_value', sdy.RealProp, False),
        ('start_translation_locked', sdy.BooleanProp, False),
        ('end_translation_locked', sdy.BooleanProp, False),
        ('priority', sdy.PriorityProp, False),
    ],
    sdy.FormatProp: [
        ('integral_part', sdy.IntegerProp, False),
        ('fractional_part', sdy.IntegerProp, False),
        ('second_font_pos', sdy.IntegerProp, False),
        ('leading_zeros', sdy.BooleanProp, False),
        ('display_sign', sdy.BiFontDisplaySignProp, False),
    ],
    sdy.Hook: [
        ('visible', sdy.BooleanProp, False),
        ('index', sdy.IntegerProp, False),
    ],
    sdy.HorizontalLineTo: [
        ('end_x', sdy.RealProp, False),
    ],
    sdy.Imported: [
        ('enable', sdy.BooleanProp, False),
        ('restore_states', sdy.BooleanProp, False),
        ('function', sdy.FunctionProp, False),
        ('memory', sdy.BooleanProp, False),
        ('input_parameters', sdy.InputParametersProp, False),
        ('output_parameters', sdy.OutputParametersProp, False),
    ],
    sdy.IndexTexturePoint: [
        ('point', sdy.PointTextureProp, False),
        ('arc_segment', sdy.ArcSegmentProp, False),
    ],
    sdy.IndexedPoint: [
        ('point', sdy.PointProperty, False),
        ('arc_segment', sdy.ArcSegmentProp, False),
    ],
    sdy.InputParametersProp: [
        ('parameters', sdy.InputParamProp, True),
    ],
    sdy.KeyboardEventListener: [
        ('enable', sdy.BooleanProp, False),
        ('event_id', sdy.IntegerProp, False),
    ],
    sdy.Layer: [
        ('visible', sdy.BooleanProp, False),
        ('origin', sdy.CoordinatePoint, False),
        ('id', sdy.IntegerProp, False),
    ],
    sdy.Line: [
        ('visible', sdy.BooleanProp, False),
        ('line_width', sdy.IntegerProp, False),
        ('line_stipple', sdy.IntegerProp, False),
        ('haloing', sdy.BooleanProp, False),
        ('outline_color', sdy.IntegerProp, False),
        ('halo_color', sdy.IntegerProp, False),
        ('outline_opacity', sdy.IntegerProp, False),
        ('line_cap', sdy.LineCapProp, False),
    ],
    sdy.LineTo: [
        ('end_point', sdy.PointProperty, False),
    ],
    sdy.MaskContainer: [
        ('mask_activity', sdy.BooleanProp, False),
        ('origin', sdy.PointProperty, False),
        ('rotate', sdy.AngleProp, False),
        ('orientation', sdy.OrientationProp, False),
        ('scale', sdy.CoordinatePoint, False),
        ('clip_inside', sdy.BooleanProp, False),
    ],
    sdy.MoveTo: [
        ('start_point', sdy.PointProperty, False),
    ],
    sdy.NplicatorContainer: [
        ('file', sdy.FileProp, False),
        ('replication', sdy.IntegerProp, False),
        ('visible', sdy.BooleanArrayProp, False),
        ('origin', sdy.PointArrayProp, False),
        ('rotate', sdy.AngleArrayProp, False),
        ('orientation', sdy.OrientationProp, False),
        ('scale', sdy.PointArrayProp, False),
        ('constant_parameters', sdy.InputParametersProp, False),
        ('input_parameters', sdy.InputParametersProp, False),
        ('output_parameters', sdy.OutputParametersProp, False),
    ],
    sdy.OutputParametersProp: [
        ('output_parameters', sdy.OutputParamProp, True),
    ],
    sdy.PanelContainer: [
        ('visible', sdy.BooleanProp, False),
        ('origin', sdy.PointProperty, False),
        ('width', sdy.RealProp, False),
        ('height', sdy.RealProp, False),
        ('priority', sdy.PriorityProp, False),
    ],
    sdy.Path: [
        ('visible', sdy.BooleanProp, False),
        ('line_width', sdy.IntegerProp, False),
        ('line_stipple', sdy.IntegerProp, False),
        ('line_cap', sdy.LineCapProp, False),
        ('haloing', sdy.BooleanProp, False),
        ('halo_color', sdy.IntegerProp, False),
        ('outline_color', sdy.IntegerProp, False),
        ('outline_opacity', sdy.IntegerProp, False),
        ('fill_color', sdy.IntegerProp, False),
        ('fill_opacity', sdy.IntegerProp, False),
        ('polygon_smooth', sdy.BooleanProp, False),
        ('texture', sdy.TextureProp, False),
        ('gradient', sdy.IntegerProp, False),
        ('modulate', sdy.BooleanProp, False),
        ('tessellate', sdy.BooleanProp, False),
    ],
    sdy.PointArrayProp: [
        ('x', sdy.RealArrayProp, False),
        ('y', sdy.RealArrayProp, False),
    ],
    sdy.PointTextureProp: [
        ('u', sdy.RealProp, False),
        ('v', sdy.RealProp, False),
    ],
    sdy.PointerEventListener: [
        ('enable', sdy.BooleanProp, False),
        ('event_id', sdy.IntegerProp, False),
        ('relative', sdy.BooleanProp, False),
    ],
    sdy.PointsProp: [
        ('point', sdy.PointProperty, True),
    ],
    sdy.QuadraticCurveTo: [
        ('control_point', sdy.PointProperty, False),
        ('end_point', sdy.PointProperty, False),
    ],
    sdy.Rectangle: [
        ('visible', sdy.BooleanProp, False),
        ('first_point', sdy.PointTextureProp, False),
        ('third_point', sdy.PointTextureProp, False),
        ('first_arc', sdy.ArcSegmentProp, False),
        ('second_arc', sdy.ArcSegmentProp, False),
        ('third_arc', sdy.ArcSegmentProp, False),
        ('fourth_arc', sdy.ArcSegmentProp, False),
        ('haloing', sdy.BooleanProp, False),
        ('line_width', sdy.IntegerProp, False),
        ('line_stipple', sdy.IntegerProp, False),
        ('outline_color', sdy.IntegerProp, False),
        ('halo_color', sdy.IntegerProp, False),
        ('fill_color', sdy.IntegerProp, False),
        ('outline_opacity', sdy.IntegerProp, False),
        ('fill_opacity', sdy.IntegerProp, False),
        ('line_cap', sdy.LineCapProp, False),
        ('polygon_smooth', sdy.BooleanProp, False),
        ('texture', sdy.TextureProp, False),
        ('texture_control', sdy.BooleanProp, False),
        ('modulate', sdy.BooleanProp, False),
        ('tessellate', sdy.BooleanProp, False),
        ('gradient', sdy.IntegerProp, False),
    ],
    sdy.RectangleArea: [
        ('enable', sdy.BooleanProp, False),
        ('pointer_id', sdy.IntegerProp, False),
        ('first_point', sdy.PointProperty, False),
        ('third_point', sdy.PointProperty, False),
    ],
    sdy.ReferenceContainer: [
        ('file', sdy.FileProp, False),
        ('visible', sdy.BooleanProp, False),
        ('origin', sdy.PointProperty, False),
        ('rotate', sdy.AngleProp, False),
        ('orientation', sdy.OrientationProp, False),
        ('scale', sdy.CoordinatePoint, False),
        ('constant_parameters', sdy.InputParametersProp, False),
        ('input_parameters', sdy.InputParametersProp, False),
        ('output_parameters', sdy.OutputParametersProp, False),
    ],
    sdy.RichText: [
        ('visible', sdy.BooleanProp, False),
        ('position', sdy.PointProperty, False),
        ('max_length', sdy.IntegerProp, False),
        ('text_value', sdy.TextProp, False),
        ('line_width', sdy.IntegerProp, False),
        ('font', sdy.IntegerProp, False),
        ('outline_color', sdy.IntegerProp, False),
        ('horiz_align', sdy.TextHorizAlignProp, False),
        ('vert_align', sdy.TextVertAlignProp, False),
    ],
    sdy.RotationContainer: [
        ('visible', sdy.BooleanProp, False),
        ('origin', sdy.PointProperty, False),
        ('ref_angle', sdy.AngleProp, False),
        ('orientation', sdy.OrientationProp, False),
        ('start_rotation_angle', sdy.AngleProp, False),
        ('end_rotation_angle', sdy.AngleProp, False),
        ('start_rotation_value', sdy.RealProp, False),
        ('end_rotation_value', sdy.RealProp, False),
        ('start_rotation_locked', sdy.BooleanProp, False),
        ('end_rotation_locked', sdy.BooleanProp, False),
        ('functional_rotation_value', sdy.RealProp, False),
        ('priority', sdy.PriorityProp, False),
    ],
    sdy.Shape: [
        ('visible', sdy.BooleanProp, False),
        ('haloing', sdy.BooleanProp, False),
        ('line_width', sdy.IntegerProp, False),
        ('line_stipple', sdy.IntegerProp, False),
        ('outline_color', sdy.IntegerProp, False),
        ('halo_color', sdy.IntegerProp, False),
        ('fill_color', sdy.IntegerProp, False),
        ('outline_opacity', sdy.IntegerProp, False),
        ('fill_opacity', sdy.IntegerProp, False),
        ('line_cap', sdy.LineCapProp, False),
        ('polygon_smooth', sdy.BooleanProp, False),
        ('texture_control', sdy.BooleanProp, False),
        ('texture', sdy.TextureProp, False),
        ('modulate', sdy.BooleanProp, False),
        ('tessellate', sdy.BooleanProp, False),
        ('gradient', sdy.IntegerProp, False),
    ],
    sdy.ShapeArea: [
        ('enable', sdy.BooleanProp, False),
        ('pointer_id', sdy.IntegerProp, False),
        ('points', sdy.PointsProp, False),
    ],
    sdy.SmoothCurveTo: [
        ('second_control_point', sdy.PointProperty, False),
        ('end_point', sdy.PointProperty, False),
    ],
    sdy.SmoothQuadraticCurveTo: [
        ('end_point', sdy.PointProperty, False),
    ],
    sdy.Stencil: [
        ('mask_activity', sdy.BooleanProp, False),
        ('tessellate', sdy.BooleanProp, False),
    ],
    sdy.Text: [
        ('visible', sdy.BooleanProp, False),
        ('position', sdy.PointProperty, False),
        ('max_length', sdy.IntegerProp, False),
        ('text_value', sdy.TextProp, False),
        ('haloing', sdy.BooleanProp, False),
        ('line_width', sdy.IntegerProp, False),
        ('font', sdy.IntegerProp, False),
        ('outline_color', sdy.IntegerProp, False),
        ('halo_color', sdy.IntegerProp, False),
        ('horiz_align', sdy.TextHorizAlignProp, False),
        ('vert_align', sdy.TextVertAlignProp, False),
    ],
    sdy.TextArea: [
        ('visible', sdy.BooleanProp, False),
        ('first_point', sdy.PointProperty, False),
        ('third_point', sdy.PointProperty, False),
        ('max_length', sdy.IntegerProp, False),
        ('text_value', sdy.TextProp, False),
        ('haloing', sdy.BooleanProp, False),
        ('line_width', sdy.IntegerProp, False),
        ('font', sdy.IntegerProp, False),
        ('outline_color', sdy.IntegerProp, False),
        ('halo_color', sdy.IntegerProp, False),
        ('horiz_align', sdy.TextHorizAlignProp, False),
        ('vert_align', sdy.TextVertAlignProp, False),
    ],
    sdy.TextureProp: [
        ('texture_id', sdy.IntegerProp, False),
    ],
    sdy.TranslationContainer: [
        ('visible', sdy.BooleanProp, False),
        ('priority', sdy.PriorityProp, False),
        ('origin', sdy.PointProperty, False),
        ('ref_point', sdy.PointProperty, False),
        ('start_translation_point', sdy.PointProperty, False),
        ('end_translation_point', sdy.PointProperty, False),
        ('start_translation_value', sdy.RealProp, False),
        ('end_translation_value', sdy.RealProp, False),
        ('start_translation_locked', sdy.BooleanProp, False),
        ('end_translation_locked', sdy.BooleanProp, False),
        ('functional_translation_value', sdy.RealProp, False),
    ],
    sdy.VerticalLineTo: [
        ('end_y', sdy.RealProp, False),
    ],
}
#}}sdy_access_ut
# fmt: on


def test_consistency():
    # ensure the consistency between SCADE Display API and generated accessors
    for cls, properties in classes.items():
        instance = cls()
        for name, type_, many in properties:
            attribute = getattr(instance, name)
            if many:
                for value in attribute:
                    assert isinstance(value, type_)
            else:
                assert attribute is None or isinstance(attribute, type_)
            assert getattr(instance, f'p_{name}') is not None
