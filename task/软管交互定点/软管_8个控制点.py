# -*- coding: utf-8 -*-
import pyp3d as p3d
from pyp3d import *
import math


EPSILON = 1e-7


def _add(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def _sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def _mul(a, value):
    return (a[0] * value, a[1] * value, a[2] * value)


def _dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _cross(a, b):
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0]
    )


def _length(vector):
    return math.sqrt(max(_dot(vector, vector), 0.0))


def _unit(vector, fallback=(1.0, 0.0, 0.0)):
    vector_length = _length(vector)
    if vector_length < EPSILON:
        return fallback
    return _mul(vector, 1.0 / vector_length)


def _distance(a, b):
    return _length(_sub(a, b))


def _clamp(value, lower, upper):
    return max(lower, min(value, upper))


def _rotate_vector(vector, axis, angle):
    cosine = math.cos(angle)
    sine = math.sin(angle)
    return _add(
        _add(_mul(vector, cosine), _mul(_cross(axis, vector), sine)),
        _mul(axis, _dot(axis, vector) * (1.0 - cosine))
    )


def _remove_consecutive_duplicates(points):
    result = []
    for point in points:
        if not result or _distance(point, result[-1]) >= EPSILON:
            result.append(point)
    return result


def _stable_perpendicular(direction):
    reference = (0.0, 0.0, 1.0)
    if abs(_dot(direction, reference)) > 0.85:
        reference = (0.0, 1.0, 0.0)
    return _unit(_cross(direction, reference), (0.0, 1.0, 0.0))


def _expand_reversing_corners(points, detour_distance):
    """Add a planar U-route when a guide path makes an excessively tight turn."""
    if len(points) < 3:
        return points

    expanded = [points[0]]
    for index in range(1, len(points) - 1):
        previous_point = points[index - 1]
        corner_point = points[index]
        next_point = points[index + 1]
        expanded.append(corner_point)

        incoming = _unit(_sub(corner_point, previous_point))
        outgoing = _unit(_sub(next_point, corner_point))
        if _dot(incoming, outgoing) < -0.85:
            bend_plane_normal = _cross(incoming, outgoing)
            if _length(bend_plane_normal) >= EPSILON:
                side_direction = _unit(_cross(bend_plane_normal, incoming))
            else:
                side_direction = _stable_perpendicular(incoming)
            side_offset = _mul(side_direction, detour_distance)
            expanded.append(_add(corner_point, side_offset))
            expanded.append(_add(next_point, side_offset))

    expanded.append(points[-1])
    return _remove_consecutive_duplicates(expanded)


def _relax_points_for_safe_bends(points, requested_radius, minimum_radius):
    """Move only unsafe guide corners toward their neighbours."""
    if len(points) < 3:
        return points

    relaxed = list(points)
    relaxation_ratio = 0.10
    for unused_iteration in range(30):
        unsafe_indices = set()
        for index in range(1, len(relaxed) - 1):
            corner = _make_corner(
                relaxed[index - 1],
                relaxed[index],
                relaxed[index + 1],
                requested_radius
            )
            if corner is not None and corner['radius'] < minimum_radius:
                unsafe_indices.add(index)
                if index > 1:
                    unsafe_indices.add(index - 1)
                if index < len(relaxed) - 2:
                    unsafe_indices.add(index + 1)

        if not unsafe_indices:
            break

        next_points = [relaxed[0]]
        maximum_move = 0.0
        for index in range(1, len(relaxed) - 1):
            point = relaxed[index]
            if index in unsafe_indices:
                neighbour_midpoint = _mul(
                    _add(relaxed[index - 1], relaxed[index + 1]), 0.5
                )
                adjusted = _add(
                    _mul(point, 1.0 - relaxation_ratio),
                    _mul(neighbour_midpoint, relaxation_ratio)
                )
                maximum_move = max(maximum_move, _distance(point, adjusted))
                next_points.append(adjusted)
            else:
                next_points.append(point)
        next_points.append(relaxed[-1])
        relaxed = next_points

        if maximum_move < EPSILON:
            break

    while len(relaxed) > 2:
        worst_index = None
        worst_radius = minimum_radius
        for index in range(1, len(relaxed) - 1):
            incoming = _unit(_sub(relaxed[index], relaxed[index - 1]))
            outgoing = _unit(_sub(relaxed[index + 1], relaxed[index]))
            if _dot(incoming, outgoing) < -0.85:
                worst_index = index
                worst_radius = 0.0
                break

            corner = _make_corner(
                relaxed[index - 1],
                relaxed[index],
                relaxed[index + 1],
                requested_radius
            )
            if corner is not None and corner['radius'] < worst_radius:
                worst_index = index
                worst_radius = corner['radius']

        if worst_index is None:
            break
        del relaxed[worst_index]

    return _remove_consecutive_duplicates(relaxed)


def _make_corner(previous_point, corner_point, next_point, requested_radius):
    incoming_vector = _sub(corner_point, previous_point)
    outgoing_vector = _sub(next_point, corner_point)
    incoming_length = _length(incoming_vector)
    outgoing_length = _length(outgoing_vector)
    if incoming_length < EPSILON or outgoing_length < EPSILON:
        return None

    incoming = _mul(incoming_vector, 1.0 / incoming_length)
    outgoing = _mul(outgoing_vector, 1.0 / outgoing_length)
    turn_angle = math.acos(_clamp(_dot(incoming, outgoing), -1.0, 1.0))

    if turn_angle < 1e-4 or turn_angle > math.pi - 1e-4:
        return None

    tangent_factor = math.tan(turn_angle * 0.5)
    if tangent_factor < EPSILON:
        return None

    maximum_trim = min(incoming_length, outgoing_length) * 0.44
    trim = min(requested_radius * tangent_factor, maximum_trim)
    if trim < EPSILON:
        return None

    actual_radius = trim / tangent_factor
    entry = _sub(corner_point, _mul(incoming, trim))
    exit_point = _add(corner_point, _mul(outgoing, trim))

    previous_ray = _mul(incoming, -1.0)
    bisector = _unit(_add(previous_ray, outgoing))
    half_inner_angle = (math.pi - turn_angle) * 0.5
    sine_half_inner = math.sin(half_inner_angle)
    if sine_half_inner < EPSILON:
        return None

    center_distance = actual_radius / sine_half_inner
    center = _add(corner_point, _mul(bisector, center_distance))
    radial_start = _sub(entry, center)
    radial_end = _sub(exit_point, center)
    axis = _unit(_cross(radial_start, radial_end))

    return {
        'incoming': incoming,
        'outgoing': outgoing,
        'angle': turn_angle,
        'trim': trim,
        'radius': actual_radius,
        'entry': entry,
        'exit': exit_point,
        'center': center,
        'radial_start': radial_start,
        'axis': axis
    }


def _build_rounded_path(points, requested_radius):
    corners = [None] * len(points)
    for index in range(1, len(points) - 1):
        corners[index] = _make_corner(
            points[index - 1], points[index], points[index + 1], requested_radius
        )

    center_points = []
    tangent_points = []

    def append_sample(point, tangent):
        tangent = _unit(tangent)
        if center_points and _distance(center_points[-1], point) < EPSILON:
            tangent_points[-1] = tangent
            return
        center_points.append(point)
        tangent_points.append(tangent)

    first_tangent = _unit(_sub(points[1], points[0]))
    append_sample(points[0], first_tangent)

    for index in range(1, len(points) - 1):
        corner = corners[index]
        if corner is None:
            outgoing = _unit(_sub(points[index + 1], points[index]), tangent_points[-1])
            append_sample(points[index], outgoing)
            continue

        append_sample(corner['entry'], corner['incoming'])
        arc_segments = int(math.ceil(corner['angle'] / (math.pi / 24.0)))
        arc_segments = max(4, min(arc_segments, 48))
        for segment_index in range(1, arc_segments + 1):
            ratio = float(segment_index) / arc_segments
            radial = _rotate_vector(
                corner['radial_start'],
                corner['axis'],
                corner['angle'] * ratio
            )
            arc_point = _add(corner['center'], radial)
            arc_tangent = _unit(_cross(corner['axis'], radial), corner['outgoing'])
            append_sample(arc_point, arc_tangent)

    last_tangent = _unit(_sub(points[-1], points[-2]), tangent_points[-1])
    append_sample(points[-1], last_tangent)

    straight_length = 0.0
    for index in range(len(points) - 1):
        segment_length = _distance(points[index], points[index + 1])
        start_trim = corners[index]['trim'] if corners[index] is not None else 0.0
        end_trim = corners[index + 1]['trim'] if corners[index + 1] is not None else 0.0
        straight_length += max(segment_length - start_trim - end_trim, 0.0)

    arc_length = 0.0
    radii = []
    for corner in corners:
        if corner is not None:
            arc_length += corner['radius'] * corner['angle']
            radii.append(corner['radius'])

    return center_points, tangent_points, straight_length + arc_length, radii


def _hash_points(points):
    """生成 Vec3 列表的稳定字符串哈希，用于检测关键点是否变化"""
    parts = []
    for p in points:
        parts.append(f"{round(p.x, 6):.6f},{round(p.y, 6):.6f},{round(p.z, 6):.6f}")
    return "|".join(parts)


def wsl(data):
    """软管建模函数 — 从 data['关键点'] 读取光标点选的控制点，生成带圆角过渡的空心软管"""
    diameter = max(float(data['公称直径']), 2.0)
    outer_radius = diameter * 0.5
    wall_thickness = _clamp(
        float(data['壁厚']), 0.1, outer_radius * 0.9
    )
    inner_radius = outer_radius - wall_thickness

    requested_radius = max(
        float(data['期望圆角半径']), outer_radius * 1.05
    )

    # === 坐标同步逻辑 ===
    # 从光标点选的关键点列表读取控制点
    KeyPoint = data['关键点']
    current_hash = _hash_points(KeyPoint)

    # 关键点hash变化时（用户通过MultiPointPlace修改了控制点），同步到独立XYZ参数
    if current_hash != data['_关键点哈希'] and len(KeyPoint) == 10:
        data['起点X'] = round(KeyPoint[0].x, 6)
        data['起点Y'] = round(KeyPoint[0].y, 6)
        data['起点Z'] = round(KeyPoint[0].z, 6)
        for i in range(1, 9):
            data[f'中间点{i}X'] = round(KeyPoint[i].x, 6)
            data[f'中间点{i}Y'] = round(KeyPoint[i].y, 6)
            data[f'中间点{i}Z'] = round(KeyPoint[i].z, 6)
        data['终点X'] = round(KeyPoint[9].x, 6)
        data['终点Y'] = round(KeyPoint[9].y, 6)
        data['终点Z'] = round(KeyPoint[9].z, 6)
        data['_关键点哈希'] = current_hash

    # 从独立XYZ参数读取控制点（始终作为几何计算的真实数据源）
    raw_points = [
        (float(data['起点X']), float(data['起点Y']), float(data['起点Z'])),
        (float(data['中间点1X']), float(data['中间点1Y']), float(data['中间点1Z'])),
        (float(data['中间点2X']), float(data['中间点2Y']), float(data['中间点2Z'])),
        (float(data['中间点3X']), float(data['中间点3Y']), float(data['中间点3Z'])),
        (float(data['中间点4X']), float(data['中间点4Y']), float(data['中间点4Z'])),
        (float(data['中间点5X']), float(data['中间点5Y']), float(data['中间点5Z'])),
        (float(data['中间点6X']), float(data['中间点6Y']), float(data['中间点6Z'])),
        (float(data['中间点7X']), float(data['中间点7Y']), float(data['中间点7Z'])),
        (float(data['中间点8X']), float(data['中间点8Y']), float(data['中间点8Z'])),
        (float(data['终点X']), float(data['终点Y']), float(data['终点Z'])),
    ]

    points = _remove_consecutive_duplicates(raw_points)
    if len(points) == 1:
        points.append(_add(points[0], (diameter * 2.0, 0.0, 0.0)))

    detour_distance = max(requested_radius, diameter * 1.5)
    points = _expand_reversing_corners(points, detour_distance)
    points = _relax_points_for_safe_bends(
        points,
        requested_radius,
        outer_radius * 1.05
    )
    center_points, tangent_points, pipe_length, actual_radii = _build_rounded_path(
        points, requested_radius
    )

    data['管道长度'] = round(pipe_length, 2)
    data['实际最小圆角半径'] = (
        round(min(actual_radii), 2) if actual_radii else 0.0
    )

    circle_segments = 24
    frames = []
    outer_contours = []

    first_tangent = _unit(tangent_points[0])
    normal = _stable_perpendicular(first_tangent)

    def make_contour(center, section_normal, section_binormal, radius):
        contour = []
        for index in range(circle_segments + 1):
            angle = 2.0 * math.pi * index / circle_segments
            offset = _add(
                _mul(section_normal, radius * math.cos(angle)),
                _mul(section_binormal, radius * math.sin(angle))
            )
            point = _add(center, offset)
            contour.append(Vec3(point[0], point[1], point[2]))
        return contour

    for center, tangent in zip(center_points, tangent_points):
        tangent = _unit(tangent, first_tangent)
        projected_normal = _sub(normal, _mul(tangent, _dot(normal, tangent)))
        if _length(projected_normal) < EPSILON:
            projected_normal = _stable_perpendicular(tangent)

        normal = _unit(projected_normal, _stable_perpendicular(tangent))
        binormal = _unit(_cross(tangent, normal))
        frames.append((center, tangent, normal, binormal))
        outer_contours.append(make_contour(center, normal, binormal, outer_radius))

    passage_extension = max(wall_thickness, diameter * 0.02)
    first_center, first_tangent, first_normal, first_binormal = frames[0]
    last_center, last_tangent, last_normal, last_binormal = frames[-1]
    inner_contours = [
        make_contour(
            _sub(first_center, _mul(first_tangent, passage_extension)),
            first_normal,
            first_binormal,
            inner_radius
        )
    ]
    for center, tangent, section_normal, section_binormal in frames:
        inner_contours.append(
            make_contour(center, section_normal, section_binormal, inner_radius)
        )
    inner_contours.append(
        make_contour(
            _add(last_center, _mul(last_tangent, passage_extension)),
            last_normal,
            last_binormal,
            inner_radius
        )
    )

    outer_pipe = RuledSweepPlus(outer_contours)
    inner_passage = RuledSweepPlus(inner_contours)
    data['软管'] = (outer_pipe - inner_passage).color(0.08, 0.47, 0.68, 1.0)


if __name__ == '__main__':
    data = P3DData({
        '公称直径': 160.0,
        '壁厚': 8.0,
        '期望圆角半径': 200.0,
        '管道长度': 0.0,
        '实际最小圆角半径': 0.0,
        '软管': None,
        '构件名称': '软管-10点布置',
        '关键点': [
            Vec3(0, 0, 0),
            Vec3(1300, 0, 500),
            Vec3(2200, -1000, 1000),
            Vec3(3000, 1000, 1500),
            Vec3(3500, -1000, 2000),
            Vec3(4000, 1000, 2500),
            Vec3(4800, -500, 3000),
            Vec3(5200, 800, 3200),
            Vec3(5600, -300, 3400),
            Vec3(6000, 0, 3600),
        ],
        '_关键点哈希': _hash_points([
            Vec3(0, 0, 0), Vec3(1300, 0, 500), Vec3(2200, -1000, 1000),
            Vec3(3000, 1000, 1500), Vec3(3500, -1000, 2000), Vec3(4000, 1000, 2500),
            Vec3(4800, -500, 3000), Vec3(5200, 800, 3200), Vec3(5600, -300, 3400),
            Vec3(6000, 0, 3600),
        ]),
        '起点X': 0.0, '起点Y': 0.0, '起点Z': 0.0,
        '中间点1X': 1300.0, '中间点1Y': 0.0, '中间点1Z': 500.0,
        '中间点2X': 2200.0, '中间点2Y': -1000.0, '中间点2Z': 1000.0,
        '中间点3X': 3000.0, '中间点3Y': 1000.0, '中间点3Z': 1500.0,
        '中间点4X': 3500.0, '中间点4Y': -1000.0, '中间点4Z': 2000.0,
        '中间点5X': 4000.0, '中间点5Y': 1000.0, '中间点5Z': 2500.0,
        '中间点6X': 4800.0, '中间点6Y': -500.0, '中间点6Z': 3000.0,
        '中间点7X': 5200.0, '中间点7Y': 800.0, '中间点7Z': 3200.0,
        '中间点8X': 5600.0, '中间点8Y': -300.0, '中间点8Z': 3400.0,
        '终点X': 6000.0, '终点Y': 0.0, '终点Z': 3600.0,
    })

    data.setup('公称直径', obvious=True)
    data.setup('壁厚', obvious=True)
    data.setup('期望圆角半径', obvious=True)
    data.setup('管道长度', obvious=True, readonly=True)
    data.setup('实际最小圆角半径', obvious=True, readonly=True)
    data.setup('软管', show=True)
    data.setup('构件名称', obvious=True)

    data.setup('_关键点哈希', obvious=False)

    data.setup('起点X', obvious=True, group='起点坐标')
    data.setup('起点Y', obvious=True, group='起点坐标')
    data.setup('起点Z', obvious=True, group='起点坐标')

    for i in range(1, 9):
        data.setup(f'中间点{i}X', obvious=True, group=f'中间点{i}坐标')
        data.setup(f'中间点{i}Y', obvious=True, group=f'中间点{i}坐标')
        data.setup(f'中间点{i}Z', obvious=True, group=f'中间点{i}坐标')

    data.setup('终点X', obvious=True, group='终点坐标')
    data.setup('终点Y', obvious=True, group='终点坐标')
    data.setup('终点Z', obvious=True, group='终点坐标')

    data['replace'] = wsl
    p3d.MultiPointPlace.MultiPointFunction(data, '关键点')
    wsl(data)
    p3d.launchData(data)