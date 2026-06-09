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

* for each class having properties
  * create instance with values different from default
  * for each property
    * assess read access
    * assess write access
"""

from typing import List, Tuple

import pytest

import ansys.scade.apitools.prop.sdyaccess as sdy


def test_circle():
    circle = sdy.Circle(center=(1.0, 2.0), radius=3.0, haloing=True)
    assert circle.modulate is None

    # read
    assert circle.p_visible
    assert circle.p_center == (1.0, 2.0)
    assert circle.p_radius == 3.0
    assert circle.p_haloing
    # some properties are not created in constructor
    assert circle.gradient is None
    # they remain accessible without error
    assert circle.p_gradient == 0  # default value
    # read access does not modify the model
    assert circle.gradient is None

    # write
    # should update properties
    circle.p_visible = False
    circle.p_center = 4.0, 5.0
    circle.p_radius = 6.0
    circle.p_haloing = False
    # should create and set properties
    circle.p_gradient = 7

    # traditional access
    assert not circle.visible.init
    assert circle.center.x.init == 4.0
    assert circle.center.y.init == 5.0
    assert circle.radius.init == 6.0
    assert not circle.haloing.init
    # the property has been created
    assert circle.gradient.init == 7


@pytest.mark.parametrize(
    'class_, names',
    [
        (sdy.Arc, [('start_angle', 'start_angle'), ('end_angle', 'end_angle')]),
        (sdy.ArcEllipse, [('start_angle', 'start_angle'), ('end_angle', 'end_angle')]),
        (sdy.ClipPlane, [('clip_angle', 'angle')]),
        (sdy.Crown, [('start_angle', 'start_angle'), ('end_angle', 'end_angle')]),
        (sdy.CondContainer, [('rotate', 'angle')]),
        (sdy.Container, [('rotate', 'angle')]),
        (
            sdy.FilterRotationContainer,
            [('start_rotation_angle', 'start_angle'), ('end_rotation_angle', 'end_angle')],
        ),
        (sdy.MaskContainer, [('rotate', 'angle')]),
        (sdy.ReferenceContainer, [('rotate', 'angle')]),
        (
            sdy.RotationContainer,
            [
                ('ref_angle', 'ref_angle'),
                ('start_rotation_angle', 'start_angle'),
                ('end_rotation_angle', 'end_angle'),
            ],
        ),
    ],
)
def test_angle_property(class_: type, names: List[Tuple[str, str]]):
    d = {default: float(index + 1) for index, (_, default) in enumerate(names)}
    c = class_(**d)
    for name, _ in names:
        prop_name = f'p_{name}'
        value = getattr(c, name).angle.init
        assert getattr(c, prop_name) == value
        value *= 2.0
        setattr(c, prop_name, value)
        assert getattr(c, name).angle.init == value


@pytest.mark.parametrize(
    'class_, names',
    [
        (sdy.Rectangle, ['first_arc', 'second_arc', 'third_arc', 'fourth_arc']),
        (sdy.IndexTexturePoint, ['arc_segment']),
        (sdy.IndexedPoint, ['arc_segment']),
    ],
)
def test_arc_segment_prop(class_: type, names: List[str]):
    c = class_()
    flag = False
    for index, name in enumerate(names):
        prop_name = f'p_{name}'
        value = getattr(c, name)
        assert value is None
        assert getattr(c, prop_name) == (False, 0.0)
        angle = 1.0 + index
        flag = not flag
        value = (flag, angle)
        setattr(c, prop_name, value)
        assert getattr(c, prop_name) == value
        assert getattr(c, name).orientation.clockwise == flag
        assert getattr(c, name).angle.angle.init == angle


# AssignmentOutputProp: N/A


@pytest.mark.parametrize(
    'class_, names',
    [
        (sdy.MaskContainer, ['scale']),
        (sdy.ReferenceContainer, ['scale']),
    ],
)
def test_coordinate_point(class_: type, names: List[str]):
    d = {name: (1.0 + index, 2.0 + index) for index, name in enumerate(names)}
    c = class_(**d)
    for name in names:
        prop_name = f'p_{name}'
        x = getattr(c, name).x.init
        y = getattr(c, name).y.init
        assert getattr(c, prop_name) == (x, y)
        x *= 2.0
        y *= 3.0
        setattr(c, prop_name, (x, y))
        assert getattr(c, name).x.init == x
        assert getattr(c, name).y.init == y


@pytest.mark.parametrize(
    'class_, names',
    [
        (sdy.Behavior, ['file']),
        (sdy.NplicatorContainer, ['file']),
        (sdy.ReferenceContainer, ['file']),
    ],
)
def test_file_prop(class_: type, names: List[str]):
    d = {name: str(index + 1) for index, name in enumerate(names)}
    c = class_(**d)
    for name in names:
        prop_name = f'p_{name}'
        value = getattr(c, name).file
        assert getattr(c, prop_name) == value
        value = f'{value}ex'
        setattr(c, prop_name, value)
        assert getattr(c, name).file == value


@pytest.mark.parametrize(
    'class_, names',
    [
        (sdy.BiFont, ['format']),
    ],
)
def test_format_prop(class_: type, names: List[str]):
    c = class_()
    for name in names:
        prop_name = f'p_{name}'
        ip = getattr(c, name).integral_part.init
        fp = getattr(c, name).fractional_part.init
        s = getattr(c, name).separator
        sfp = getattr(c, name).second_font_pos.init
        lz = getattr(c, name).leading_zeros.init
        ds = getattr(c, name).display_sign.init
        assert getattr(c, prop_name) == (s, ip, fp, sfp, lz, ds)
        ip = getattr(c, name).integral_part.init
        fp = getattr(c, name).fractional_part.init
        s = getattr(c, name).separator
        sfp = getattr(c, name).second_font_pos.init
        lz = getattr(c, name).leading_zeros.init
        ds = getattr(c, name).display_sign.init
        setattr(c, prop_name, (s, ip, fp, sfp, lz, ds))
        assert getattr(c, name).integral_part.init == ip
        assert getattr(c, name).fractional_part.init == fp
        assert getattr(c, name).separator == s
        assert getattr(c, name).second_font_pos.init == sfp
        assert getattr(c, name).leading_zeros.init == lz
        assert getattr(c, name).display_sign.init == ds


@pytest.mark.parametrize(
    'class_, names',
    [
        (sdy.Imported, ['function']),
    ],
)
def test_function_prop(class_: type, names: List[str]):
    d = {name: str(index + 1) for index, name in enumerate(names)}
    c = class_(**d)
    for name in names:
        prop_name = f'p_{name}'
        value = getattr(c, name).name
        assert getattr(c, prop_name) == value
        value = f'{value}ex'
        setattr(c, prop_name, value)
        assert getattr(c, name).name == value


@pytest.mark.parametrize(
    'class_, names',
    [
        (sdy.Line, ['points']),
        (sdy.Stencil, ['points']),
    ],
)
def test_indexed_points_prop(class_: type, names: List[str]):
    points = [(1.0, 2.0), (3.0, 4.0), (5.0, 6.0)]
    c = class_(points=points)
    for name in names:
        for index, point in enumerate(points):
            prop = getattr(c, name).points[index]
            assert getattr(prop, 'p_point') == point
            assert getattr(prop, 'p_arc_segment') == (False, 0.0)


@pytest.mark.parametrize(
    'class_, names',
    [
        (sdy.CondContainer, ['indexes']),
    ],
)
def test_indexes_prop(class_: type, names: List[str]):
    c = class_()
    for name in names:
        prop_name = f'p_{name}'
        dis = getattr(c, name).default_is_other
        assert getattr(c, prop_name) == dis
        dis = not dis
        setattr(c, prop_name, dis)
        assert getattr(c, name).default_is_other == dis


@pytest.mark.parametrize(
    'class_, names, opts',
    [
        (sdy.Behavior, [('input_parameters', 'inputs')], []),
        (sdy.Imported, [('input_parameters', 'inputs')], []),
        (sdy.NplicatorContainer, [('input_parameters', 'inputs')], ['constant_parameters']),
        (sdy.ReferenceContainer, [('input_parameters', 'inputs')], ['constant_parameters']),
    ],
)
def test_input_parameters_prop(class_: type, names: List[Tuple[str, str]], opts: List[str]):
    bool_type = sdy.PredefType(sdy.SimpleType.BOOL)
    d = {default: [(f'I{index}', bool_type)] for index, (_, default) in enumerate(names)}
    c = class_(**d)
    for name, _ in names:
        prop_name = f'p_{name}'
        prop = getattr(c, name)
        values = [(_.name, _.representation) for _ in prop.parameters]
        assert getattr(c, prop_name) == values
        inputs = [('color', sdy.Representation.COLOR), ('font', sdy.Representation.FONT)]
        setattr(c, prop_name, inputs)
        assert getattr(c, name).parameters[0].name == inputs[0][0]
        assert getattr(c, name).parameters[0].representation == inputs[0][1]
        assert getattr(c, name).parameters[1].name == inputs[1][0]
        assert getattr(c, name).parameters[1].representation == inputs[1][1]

    for index, name in enumerate(opts):
        prop_name = f'p_{name}'
        value = getattr(c, name)
        assert value is None
        assert getattr(c, prop_name) == []  # ('', sdy.Representation.NONE)
        param = f'C{index}'
        representation = sdy.Representation.GRADIENT
        value = [(param, representation)]
        setattr(c, prop_name, value)
        assert getattr(c, prop_name) == value
        assert len(getattr(c, name).parameters) == 1
        assert getattr(c, name).parameters[0].name == param
        assert getattr(c, name).parameters[0].representation == representation


@pytest.mark.parametrize(
    'class_, names',
    [
        (sdy.Behavior, ['function']),
    ],
)
def test_node_function_prop(class_: type, names: List[str]):
    d = {name: f'F{index}' for index, name in enumerate(names)}
    c = class_(**d)
    for name in names:
        prop_name = f'p_{name}'
        is_node = getattr(c, name).is_node
        function = getattr(c, name).name
        assert getattr(c, prop_name) == (is_node, function)
        is_node = not is_node
        function = f'{function}ex'
        value = (is_node, function)
        setattr(c, prop_name, value)
        assert getattr(c, prop_name) == value
        assert getattr(c, name).is_node == is_node
        assert getattr(c, name).name == function


@pytest.mark.parametrize(
    'class_, names',
    [
        (sdy.Arc, [('orientation', 'clockwise')]),
        (sdy.ArcEllipse, [('orientation', 'clockwise')]),
        (sdy.ClipPlane, [('orientation', 'clockwise')]),
        (sdy.Crown, [('orientation', 'clockwise')]),
        (sdy.CondContainer, [('orientation', 'clockwise')]),
        (sdy.Container, [('orientation', 'clockwise')]),
        (sdy.FilterRotationContainer, [('orientation', 'clockwise')]),
        (sdy.MaskContainer, [('orientation', 'clockwise')]),
        (sdy.NplicatorContainer, [('orientation', 'clockwise')]),
        (sdy.ReferenceContainer, [('orientation', 'clockwise')]),
        (sdy.RotationContainer, [('orientation', 'clockwise')]),
        (sdy.ArcSegmentProp, [('orientation', 'clockwise')]),
    ],
)
def test_orientation_property(class_: type, names: List[Tuple[str, str]]):
    d = {default: index % 2 == 0 for index, (_, default) in enumerate(names)}
    c = class_(**d)
    for name, _ in names:
        prop_name = f'p_{name}'
        value = getattr(c, name).clockwise
        assert getattr(c, prop_name) == value
        value = not value
        setattr(c, prop_name, value)
        assert getattr(c, name).clockwise == value


@pytest.mark.parametrize(
    'class_, names',
    [
        (sdy.Behavior, [('output_parameters', 'outputs')]),
        (sdy.Imported, [('output_parameters', 'outputs')]),
        (sdy.NplicatorContainer, [('output_parameters', 'outputs')]),
        (sdy.ReferenceContainer, [('output_parameters', 'outputs')]),
    ],
)
def test_output_parameters_prop(class_: type, names: List[Tuple[str, str]]):
    bool_type = sdy.PredefType(sdy.SimpleType.BOOL)
    d = {default: [(f'I{index}', bool_type)] for index, (_, default) in enumerate(names)}
    c = class_(**d)
    for name, _ in names:
        prop_name = f'p_{name}'
        prop = getattr(c, name)
        values = [(_.name, _.representation) for _ in prop.output_parameters]
        assert getattr(c, prop_name) == values
        outputs = [('color', sdy.Representation.COLOR), ('font', sdy.Representation.FONT)]
        setattr(c, prop_name, outputs)
        assert getattr(c, name).output_parameters[0].name == outputs[0][0]
        assert getattr(c, name).output_parameters[0].representation == outputs[0][1]
        assert getattr(c, name).output_parameters[1].name == outputs[1][0]
        assert getattr(c, name).output_parameters[1].representation == outputs[1][1]


# OutputPointProp: N/A
# PluggableProperty: N/A


@pytest.mark.parametrize(
    'class_, names',
    [
        (sdy.NplicatorContainer, ['origin', 'scale']),
    ],
)
def test_point_array_prop(class_: type, names: List[str]):
    values = ((1.0, 2.0), (3.0, 4.0))
    c = class_()
    for name in names:
        prop_name = f'p_{name}'
        setattr(c, prop_name, values)
        assert getattr(c, prop_name) == values
        assert getattr(c, name).x.init[0] == values[0][0]
        assert getattr(c, name).x.init[1] == values[0][1]
        assert getattr(c, name).y.init[0] == values[1][0]
        assert getattr(c, name).y.init[1] == values[1][1]


@pytest.mark.parametrize(
    'class_, names',
    [
        (sdy.ShapeArea, ['points']),
    ],
)
def test_points_prop(class_: type, names: List[str]):
    points = [(1.0, 2.0), (3.0, 4.0)]
    d = {name: points for name in names}
    c = class_(**d)
    for name in names:
        prop_name = f'p_{name}'
        assert getattr(c, prop_name) == points
        points = [(5.0, 6.0)]
        setattr(c, prop_name, points)
        assert getattr(c, prop_name) == points
        assert len(getattr(c, name).point) == 1
        assert getattr(c, name).point[0].x.init == points[0][0]
        assert getattr(c, name).point[0].y.init == points[0][1]


@pytest.mark.parametrize(
    'class_, names',
    [
        (sdy.Container, ['static']),
    ],
)
def test_static_container_prop(class_: type, names: List[str]):
    c = class_()
    for name in names:
        prop_name = f'p_{name}'
        assert getattr(c, name) is None
        assert getattr(c, prop_name) == (False, 0.0, 0.0, 0.0, 0.0, False)
        init = False
        min_x = 4.0
        max_x = 3.0
        min_y = 2.0
        max_y = 1.0
        gss = True
        values = (init, min_x, max_x, min_y, max_y, gss)
        setattr(c, prop_name, values)
        assert getattr(c, prop_name) == values
        assert getattr(c, name).init == init
        assert getattr(c, name).min_x == min_x
        assert getattr(c, name).max_x == max_x
        assert getattr(c, name).min_y == min_y
        assert getattr(c, name).max_y == max_y
        assert getattr(c, name).generate_static_sequence == gss


@pytest.mark.parametrize(
    'class_, names',
    [
        (sdy.Arc, ['texture']),
        (sdy.ArcEllipse, ['texture']),
        (sdy.Circle, ['texture']),
        (sdy.Crown, ['texture']),
        (sdy.Ellipse, ['texture']),
        (sdy.Path, ['texture']),
        (sdy.Rectangle, ['texture']),
        (sdy.Shape, ['texture']),
    ],
)
def test_texture_prop(class_: type, names: List[str]):
    c = class_()
    for name in names:
        prop_name = f'p_{name}'
        assert getattr(c, name) is None
        assert getattr(c, prop_name) == (
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
        values = (ha, va, hp, vp, id)
        setattr(c, prop_name, values)
        assert getattr(c, prop_name) == values
        assert getattr(c, name).horiz_align == ha
        assert getattr(c, name).vert_align == va
        assert getattr(c, name).horiz_pattern == hp
        assert getattr(c, name).vert_pattern == vp
        assert getattr(c, name).texture_id.init == id


@pytest.mark.parametrize(
    'class_, names',
    [
        (sdy.NplicatorContainer, ['rotate']),
    ],
)
def test_angle_array_prop_prop(class_: type, names: List[str]):
    c = class_()
    for name in names:
        prop_name = f'p_{name}'
        values = [1.0, 2.0]
        setattr(c, prop_name, values)
        assert getattr(c, prop_name) == values
        assert getattr(c, name).init == values


@pytest.mark.parametrize(
    'class_, names',
    [
        (sdy.NplicatorContainer, ['visible']),
    ],
)
def test_boolean_array_prop(class_: type, names: List[str]):
    c = class_()
    for name in names:
        prop_name = f'p_{name}'
        values = [True, False]
        setattr(c, prop_name, values)
        assert getattr(c, prop_name) == values
        assert getattr(c, name).init == values


@pytest.mark.parametrize(
    'class_, names',
    [
        (sdy.Circle, ['visible']),
        # TODO JH: find and add all occurrences
    ],
)
def test_boolean_prop(class_: type, names: List[str]):
    c = class_()
    for name in names:
        prop_name = f'p_{name}'
        value = getattr(c, name).init
        assert getattr(c, prop_name) == value
        value = not value
        setattr(c, prop_name, value)
        assert getattr(c, name).init == value


@pytest.mark.parametrize(
    'class_, names',
    [
        (sdy.CondContainer, ['index']),
    ],
)
def test_conditionnal_index_prop(class_: type, names: List[str]):
    c = class_()
    for name in names:
        prop_name = f'p_{name}'
        index = getattr(c, name).index_prop_enum
        all_visible = getattr(c, name).all_visible
        assert getattr(c, prop_name) == (index, all_visible)
        value = (sdy.IndexPropEnum.OTHER, not all_visible)
        setattr(c, prop_name, value)
        assert getattr(c, name).index_prop_enum == value[0]
        assert getattr(c, name).all_visible == value[1]


# InputProp: N/A


@pytest.mark.parametrize(
    'class_, names',
    [
        (sdy.KeyboardEventListener, ['event_id']),
        # TODO JH: find and add all occurrences
    ],
)
def test_integer_prop(class_: type, names: List[str]):
    c = class_()
    for name in names:
        prop_name = f'p_{name}'
        value = getattr(c, name).init
        assert getattr(c, prop_name) == value
        value = value + 1
        setattr(c, prop_name, value)
        assert getattr(c, name).init == value


@pytest.mark.parametrize(
    'class_, names',
    [
        (sdy.Arc, ['line_cap']),
        (sdy.ArcEllipse, ['line_cap']),
        (sdy.Circle, ['line_cap']),
        (sdy.Crown, ['line_cap']),
        (sdy.Ellipse, ['line_cap']),
        (sdy.Line, ['line_cap']),
        (sdy.Path, ['line_cap']),
        (sdy.Rectangle, ['line_cap']),
        (sdy.Shape, ['line_cap']),
    ],
)
def test_line_cap_prop(class_: type, names: List[str]):
    c = class_()
    for name in names:
        prop_name = f'p_{name}'
        assert getattr(c, name) is None
        assert getattr(c, prop_name) in sdy.LineCapEnum
        value = sdy.LineCapEnum.ROUND
        setattr(c, prop_name, value)
        assert getattr(c, name).init == value


# ParamProp: N/A


@pytest.mark.parametrize(
    'class_, names',
    [
        (sdy.CondContainer, ['priority']),
        (sdy.Container, ['priority']),
        (sdy.FilterRotationContainer, ['priority']),
        (sdy.FilterTranslationContainer, ['priority']),
        (sdy.PanelContainer, ['priority']),
        (sdy.RotationContainer, ['priority']),
        (sdy.TranslationContainer, ['priority']),
    ],
)
def test_priority_prop(class_: type, names: List[str]):
    c = class_()
    for name in names:
        prop_name = f'p_{name}'
        assert getattr(c, name) is None
        assert getattr(c, prop_name) == 0
        value = 31
        setattr(c, prop_name, value)
        assert getattr(c, name).init == value


@pytest.mark.parametrize(
    'class_, names',
    [
        (sdy.PointArrayProp, ['x', 'y']),
    ],
)
def test_real_array_prop(class_: type, names: List[str]):
    c = class_()
    for name in names:
        prop_name = f'p_{name}'
        values = [-2.0, 3.14]
        setattr(c, prop_name, values)
        assert getattr(c, prop_name) == values
        assert getattr(c, name).init == values


@pytest.mark.parametrize(
    'class_, names',
    [
        (sdy.FilterRotationContainer, ['start_rotation_value']),
        # TODO JH: find and add all occurrences
    ],
)
def test_real_prop(class_: type, names: List[str]):
    c = class_()
    for name in names:
        prop_name = f'p_{name}'
        value = 3.14
        setattr(c, prop_name, value)
        assert getattr(c, name).init == value
        assert getattr(c, prop_name) == value


@pytest.mark.parametrize(
    'class_, names',
    [
        (sdy.BiFont, ['horiz_align']),
        (sdy.RichText, ['horiz_align']),
        (sdy.Text, ['horiz_align']),
        (sdy.TextArea, ['horiz_align']),
    ],
)
def test_text_horiz_align_prop(class_: type, names: List[str]):
    c = class_()
    for name in names:
        prop_name = f'p_{name}'
        for value in sdy.HorizAlignEnum:
            setattr(c, prop_name, value)
            assert getattr(c, prop_name) == value
            assert getattr(c, name).init == value


@pytest.mark.parametrize(
    'class_, names',
    [
        (sdy.BiFont, ['vert_align']),
        (sdy.RichText, ['vert_align']),
        (sdy.Text, ['vert_align']),
        (sdy.TextArea, ['vert_align']),
    ],
)
def test_text_vert_align_prop(class_: type, names: List[str]):
    c = class_()
    for name in names:
        prop_name = f'p_{name}'
        for value in sdy.VertAlignEnum:
            setattr(c, prop_name, value)
            assert getattr(c, prop_name) == value
            assert getattr(c, name).init == value


@pytest.mark.parametrize(
    'class_, names',
    [
        (sdy.RichText, ['text_value']),
        (sdy.Text, ['text_value']),
        (sdy.TextArea, ['text_value']),
    ],
)
def test_text_prop(class_: type, names: List[str]):
    c = class_()
    for name in names:
        prop_name = f'p_{name}'
        type_ = sdy.TextTypeEnum.INT
        init = [9, 31]
        value = (type_, init)
        setattr(c, prop_name, value)
        assert getattr(c, prop_name) == value
        assert getattr(c, name).type == type_
        assert getattr(c, name).init == init


@pytest.mark.parametrize(
    'class_, names',
    [
        (sdy.Rectangle, [('first_point', 'first_point'), ('third_point', 'third_point')]),
        (sdy.IndexTexturePoint, [('point', 'val')]),
    ],
)
def test_point_texture_prop(class_: type, names: List[str]):
    d = {default: (1.0 + index, 2.0 + index) for index, (_, default) in enumerate(names)}
    c = class_(**d)
    for name, _ in names:
        prop_name = f'p_{name}'
        x = getattr(c, name).x.init
        y = getattr(c, name).y.init
        assert getattr(c, name).u is None
        assert getattr(c, name).v is None
        assert getattr(c, prop_name) == (x, y, 0.0, 0.0)
        x *= 2.0
        y *= 3.0
        u = -x
        v = -y
        setattr(c, prop_name, (x, y, u, v))
        assert getattr(c, name).x.init == x
        assert getattr(c, name).y.init == y
        assert getattr(c, name).u.init == u
        assert getattr(c, name).v.init == v
