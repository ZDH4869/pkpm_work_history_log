# -*- coding: utf-8 -*-
"""ZSFY 雨淋报警阀组整体装配（04S206 第28、29页）。

所有零件几何内联，单文件单 Component。
部件表（17 个编号）：1消防给水管 2信号阀 3试验信号阀 4雨淋报警阀ZSFY
  5压力表Y-100×2 6水力警铃ZSJL 7压力开关ZSJY 8电磁阀DN20 9手动开启阀DN20
  10止回阀DN20 11控制管球阀DN20 12报警管球阀DN20 13试验管球阀DN20
  14过滤器DN20 15试验放水阀DN40 16管卡 17泄水阀Q11f-16 DN50

安装尺寸表（mm）：
  型号      A    B    C    D    E    F    G    H
  ZSFY100  420  500  400  500  400  300  100  990
  ZSFY150  480  580  400  500  400  370  100  960
  ZSFY200  690  680  500  500  480  470  150  855
法兰：DN100 φ220/中心圆φ180/8×φ18；DN150 φ280/φ240/8×φ23；DN200 φ340/φ295/12×φ23

坐标系：+Z 向上；-Y 朝正视观察者，+Y 朝墙；定位点=主立管与地面接触面圆心。
竖向链：0地面 → 500主立管管卡 → H信号阀下法兰底 → +蝶阀长+50 报警阀底
        → +A 报警阀顶 → +D 警铃顶（铃中心=顶-80）。
X 链：-B 左缘（压力开关侧）、+C 右缘（警铃侧）、+E 泄水阀排水竖管轴线。
Y 链：墙面 Y=+F；顶部主水路横管 Y=F-G；报警回路平面 Y=60（横管前方）。

装配拓扑：
主通路  ：主立管(1)→信号阀(2)→连接短管→雨淋报警阀(4)→顶部出水管(后移)
          →顶部横管→试验信号阀(3)→系统侧出口
控制回路：报警阀左下供水腔接口→过滤器(14)→控制管球阀(11)(竖管)→止回阀(10)
          →控制腔接口；控制腔顶部→泄放立管/横管→电磁阀(8)+手动开启阀(9)→泄放口
报警回路：报警阀右侧报警口→报警管球阀(12)→后移上升→左接压力开关(7)、右接水力警铃(6)
试验回路：连接短管右侧(供水侧)→试验管球阀(13)→向上接入报警管路(12下游)
试验放水：报警阀系统腔右侧接口→试验放水阀(15)→管口朝+X
泄水回路：主立管右侧接口→泄水阀(17)→X=+E 竖管向下放空
支吊架  ：Z=500 主立管管卡 + 顶部横管管卡，支撑柱锚墙
"""

from pyp3d import *
import math


# ============================================================
# 通用工具
# ============================================================
def _空心管(start, end, outside_diameter, inside_diameter):
    """由起点、终点、外径、内径生成一段空心直管。"""
    return Cone(start, end, outside_diameter / 2.0) - \
           Cone(start, end, inside_diameter / 2.0)


def _折弯管(points, outside_diameter, inside_diameter, bend_radius=None):
    """FilletPipe 空心折弯管；倒角半径按相邻段长自动收敛，不小于 0.55×外径。"""
    if bend_radius is None:
        bend_radius = outside_diameter
    min_radius = outside_diameter * 0.55

    def seg_len(a, b):
        return math.sqrt(
            (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2
        )

    radii = []
    last = len(points) - 1
    for index in range(len(points)):
        if index == 0 or index == last:
            radii.append(0.0)
            continue
        limit = min(
            seg_len(points[index - 1], points[index]),
            seg_len(points[index], points[index + 1])
        )
        radius = min(bend_radius, limit * 0.45)
        if radius < min_radius:
            radius = min(min_radius, limit * 0.95)
        radii.append(radius)

    outer = FilletPipe(
        [Vec3(p[0], p[1], p[2]) for p in points],
        list(radii), outside_diameter / 2.0
    )
    inner = FilletPipe(
        [Vec3(p[0], p[1], p[2]) for p in points],
        list(radii), inside_diameter / 2.0
    )
    return outer - inner


def _圆截面Z(z_position, radius):
    return translate(0, 0, z_position) * \
           Section(scale(radius) * Arc(2.0 * math.pi))


def _椭圆截面Z(z_position, radius_x, radius_y):
    return translate(0, 0, z_position) * \
           Section(scale(radius_x, radius_y, 1.0) * Arc(2.0 * math.pi))


def _六角截面X(x_position, across_flats, center_z=0.0):
    circumradius = across_flats / math.sqrt(3.0)
    points = []
    for index in range(6):
        angle = math.pi / 6.0 + index * math.pi / 3.0
        points.append(Vec3(
            x_position,
            circumradius * math.cos(angle),
            center_z + circumradius * math.sin(angle)
        ))
    points.append(points[0])
    return Section(Line(*points))


def _六角柱X(x_start, x_end, across_flats, center_z=0.0):
    result = Loft(
        _六角截面X(x_start, across_flats, center_z),
        _六角截面X(x_end, across_flats, center_z)
    )
    result.smooth = False
    return result


# 全局配色
_色_管道 = (0.66, 0.69, 0.72, 1.0)
_色_阀体红 = (0.82, 0.035, 0.025, 1.0)
_色_阀体红亮 = (0.90, 0.055, 0.040, 1.0)
_色_阀体红暗 = (0.64, 0.020, 0.015, 1.0)
_色_黄铜 = (0.78, 0.57, 0.16, 1.0)
_色_黄铜亮 = (0.90, 0.70, 0.28, 1.0)
_色_钢 = (0.72, 0.74, 0.76, 1.0)
_色_铸铁 = (0.34, 0.36, 0.38, 1.0)
_色_深色 = (0.22, 0.25, 0.29, 1.0)


# ============================================================
# 编号2：信号阀（内联自 信号蝶阀，随 dn 等比缩放）
# ============================================================
def _信号蝶阀(length=155.0, dn=100.0):
    """信号蝶阀 ZSFD-16Z：主轴沿 Z，手轮位于 +X 侧，轮面朝 -Y 正前方。
    局部原点位于阀体几何中心。几何随 dn 以 DN100 为基准等比缩放。"""
    scale_factor = dn / 100.0

    L = length
    D_flange = 150.0 * scale_factor
    D_inner = 100.0 * scale_factor
    B = 20.0 * scale_factor
    R_flange = D_flange / 2
    R_inner = D_inner / 2
    R_body_inner = R_flange - B

    D_butterfly = D_inner
    T_butterfly = 15.0 * scale_factor
    R_butterfly = D_butterfly / 2

    H_packing = 25.0 * scale_factor
    H_bracket = 60.0 * scale_factor
    W_bracket = 80.0 * scale_factor

    Hcr = 160.0 * scale_factor
    Hsr = 0.11 * Hcr
    Zr = 1.2 * Hsr
    Zh = Hsr
    Zl = 60.0 * scale_factor
    Lr = 0.7 * Hsr

    body_outer = Cone(Vec3(-L / 2, 0, 0), Vec3(L / 2, 0, 0), R_flange, R_flange)
    body_inner = Cone(
        Vec3(-L / 2 - 1, 0, 0), Vec3(L / 2 + 1, 0, 0), R_body_inner, R_body_inner
    )
    valve_body = body_outer - body_inner

    seat_outer = Cone(
        Vec3(-L / 2 - 1, 0, 0), Vec3(L / 2 + 1, 0, 0), R_body_inner, R_body_inner
    )
    seat_inner = Cone(
        Vec3(-L / 2 - 2, 0, 0), Vec3(L / 2 + 2, 0, 0), R_inner, R_inner
    )
    valve_seat = seat_outer - seat_inner

    butterfly = Cone(
        Vec3(0, -T_butterfly / 2, 0),
        Vec3(0, T_butterfly / 2, 0),
        R_butterfly, R_butterfly
    )

    z_body_top = R_flange
    z_support_bottom = -R_flange - 10
    support_height = H_packing + H_bracket + 30 + (z_body_top - z_support_bottom)
    z_support_top = z_support_bottom + support_height
    z_support_center = (z_support_bottom + z_support_top) / 2
    R_support = W_bracket / 2
    support = translate(0, 0, z_support_center) * \
              Cone(Vec3(0, 0, -support_height / 2),
                   Vec3(0, 0, support_height / 2),
                   R_support, R_support)
    support = support - body_outer

    z_shaft_bottom = z_support_top - 20
    shaft = Cone(Vec3(0, 0, 0), Vec3(0, 0, Zl), Zr / 2)
    shaft_top = Cone(Vec3(0, 0, Zl), Vec3(0, 0, Zl + Zh), Zr / 2)
    rod = Cone(Vec3(0, 0, 0), Vec3(0, 0, Hcr / 2), Lr / 2)
    rod1 = translate(0, 0, Zl) * rotate(pi / 4) * rotate(Vec3(0, 1, 0), pi / 2) * rod
    rod2 = rotate(pi / 2) * rod1
    rod3 = rotate(pi / 2) * rod2
    rod4 = rotate(pi / 2) * rod3
    rods = rod1 + rod2 + rod3 + rod4
    ring_path = translate(0, 0, Zl) * Line(scale(Hcr / 2) * Arc(pi * 2))
    ring_section_curve = translate(Hcr / 2, 0, Zl) * \
                         rotate(Vec3(1, 0, 0), pi / 2) * \
                         scale(Hsr / 2) * Arc(pi * 2)
    ring_section = Section(ring_section_curve)
    ring = Sweep(ring_section, ring_path)
    wheel = shaft + shaft_top + rods + ring
    wheel_assembly = translate(0, 0, z_shaft_bottom) * \
                     rotate(Vec3(0, 0, 1), pi / 2) * \
                     rotate(Vec3(0, 1, 0), pi / 2) * wheel

    all_parts = combine(
        valve_body.color(0.60, 0.60, 0.60, 1.0),
        valve_seat.color(0.40, 0.40, 0.45, 1.0),
        butterfly.color(0.45, 0.45, 0.50, 1.0),
        support.color(0.55, 0.55, 0.55, 1.0),
        wheel_assembly.color(0.20, 0.30, 0.80, 1.0)
    )

    return rotate(Vec3(1, 0, 0), math.pi) * \
           rotate(Vec3(0, 1, 0), math.pi / 2) * all_parts


# ============================================================
# 编号3：试验信号阀（闸阀样式，主轴沿 X、阀杆 +Z、手轮面水平）
# ============================================================
def _试验信号阀(length=155.0, dn=100.0):
    """试验信号阀：主轴沿 X，手轮在 +Z 顶部（轮面水平）。
    局部原点 = 阀体几何中心。手轮顶压低至阀体顶上方约 50mm，
    避免超过水力警铃顶面。几何随 dn 等比缩放。"""
    sf = dn / 100.0
    L = length
    R_flange = 75.0 * sf
    R_inner = 50.0 * sf
    B = 20.0 * sf
    R_body_inner = R_flange - B

    body = Cone(Vec3(-L / 2, 0, 0), Vec3(L / 2, 0, 0), R_flange, R_flange) - \
           Cone(Vec3(-L / 2 - 1, 0, 0), Vec3(L / 2 + 1, 0, 0),
                R_body_inner, R_body_inner)
    seat = Cone(Vec3(-L / 2 - 1, 0, 0), Vec3(L / 2 + 1, 0, 0),
                R_body_inner, R_body_inner) - \
           Cone(Vec3(-L / 2 - 2, 0, 0), Vec3(L / 2 + 2, 0, 0), R_inner, R_inner)
    # 闸板（关闭位，YOZ 面薄板）
    gate = translate(-4.0 * sf, -R_inner, -R_inner) * \
           scale(8.0 * sf, 2.0 * R_inner, 2.0 * R_inner) * Cube()
    # 阀杆 + 阀杆螺母
    stem = Cone(Vec3(0, 0, R_flange - 5.0), Vec3(0, 0, R_flange + 30.0 * sf), 7.0 * sf)
    nut = Cone(Vec3(0, 0, R_flange + 30.0 * sf),
               Vec3(0, 0, R_flange + 40.0 * sf), 12.0 * sf)
    # 手轮（轮面水平，绕 Z）
    wheel_z0 = R_flange + 40.0 * sf
    wheel_ring = Cone(Vec3(0, 0, wheel_z0), Vec3(0, 0, wheel_z0 + 8.0 * sf),
                      40.0 * sf, 40.0 * sf) - \
                 Cone(Vec3(0, 0, wheel_z0 - 1.0), Vec3(0, 0, wheel_z0 + 9.0 * sf),
                      30.0 * sf, 30.0 * sf)
    spoke_x = Cone(Vec3(-38.0 * sf, 0, wheel_z0 + 4.0 * sf),
                   Vec3(38.0 * sf, 0, wheel_z0 + 4.0 * sf), 3.0 * sf)
    spoke_y = Cone(Vec3(0, -38.0 * sf, wheel_z0 + 4.0 * sf),
                   Vec3(0, 38.0 * sf, wheel_z0 + 4.0 * sf), 3.0 * sf)
    hub = Cone(Vec3(0, 0, wheel_z0 - 1.0), Vec3(0, 0, wheel_z0 + 9.0 * sf),
               10.0 * sf, 10.0 * sf)
    return combine(
        body.color(0.60, 0.60, 0.60, 1.0),
        seat.color(0.40, 0.40, 0.45, 1.0),
        gate.color(0.45, 0.45, 0.50, 1.0),
        combine(stem, nut).color(0.55, 0.55, 0.55, 1.0),
        combine(wheel_ring, spoke_x, spoke_y, hub).color(0.20, 0.30, 0.80, 1.0)
    )


# ============================================================
# 编号9/11/12/13：DN20 小球阀（内联自湿式参考，主管沿 Z）
# ============================================================
def _小球阀():
    """DN20 小球阀：主管轴线沿 Z，底部连接点为原点；
    控制轴从 -Y 侧伸出，圆形手轮在轴端。"""
    ball_diameter = 28.0
    ball_center_z = 20.0
    ball = translate(0, 0, ball_center_z) * \
           scale(ball_diameter / 2, ball_diameter / 2, ball_diameter / 2) * Sphere()
    valve_port = Cone(Vec3(0, 0, 0), Vec3(0, 0, 38), 10.5)

    ball_radius = ball_diameter / 2
    shaft_start_y = -ball_radius + 2
    shaft_end_y = -ball_radius - 18
    control_shaft = Cone(
        Vec3(0, shaft_start_y, ball_center_z),
        Vec3(0, shaft_end_y, ball_center_z),
        3.2
    )
    wheel_y0 = shaft_end_y - 2.5
    wheel_y1 = shaft_end_y + 2.5
    wheel_outer = Cone(
        Vec3(0, wheel_y0, ball_center_z),
        Vec3(0, wheel_y1, ball_center_z),
        13.0
    )
    wheel_inner = Cone(
        Vec3(0, wheel_y0 - 1, ball_center_z),
        Vec3(0, wheel_y1 + 1, ball_center_z),
        8.5
    )
    wheel_ring = wheel_outer - wheel_inner
    wheel_spoke_x = Cone(
        Vec3(-12, shaft_end_y, ball_center_z),
        Vec3(12, shaft_end_y, ball_center_z),
        1.6
    )
    wheel_spoke_z = Cone(
        Vec3(0, shaft_end_y, ball_center_z - 12),
        Vec3(0, shaft_end_y, ball_center_z + 12),
        1.6
    )
    wheel_hub = Cone(
        Vec3(0, wheel_y0 - 1, ball_center_z),
        Vec3(0, wheel_y1 + 1, ball_center_z),
        4.5
    )
    handwheel = combine(wheel_ring, wheel_spoke_x, wheel_spoke_z, wheel_hub)
    return combine(ball, valve_port, control_shaft, handwheel).color(*_色_黄铜)


# ============================================================
# 编号15：DN40 球阀（试验放水阀，主管沿 Z）
# ============================================================
def _DN40球阀():
    """DN40 黄铜球阀：主管轴线沿 Z，底部连接点为原点，手轮朝 -Y。"""
    ball_diameter = 40.0
    ball_center_z = 28.0
    ball = translate(0, 0, ball_center_z) * scale(20.0, 20.0, 20.0) * Sphere()
    valve_port = Cone(Vec3(0, 0, 0), Vec3(0, 0, 54), 15.0)

    ball_radius = ball_diameter / 2
    shaft_start_y = -ball_radius + 2
    shaft_end_y = -ball_radius - 26
    control_shaft = Cone(
        Vec3(0, shaft_start_y, ball_center_z),
        Vec3(0, shaft_end_y, ball_center_z),
        4.5
    )
    wheel_y0 = shaft_end_y - 3.0
    wheel_y1 = shaft_end_y + 3.0
    wheel_outer = Cone(
        Vec3(0, wheel_y0, ball_center_z),
        Vec3(0, wheel_y1, ball_center_z),
        19.0
    )
    wheel_inner = Cone(
        Vec3(0, wheel_y0 - 1, ball_center_z),
        Vec3(0, wheel_y1 + 1, ball_center_z),
        12.0
    )
    wheel_ring = wheel_outer - wheel_inner
    wheel_spoke_x = Cone(
        Vec3(-17, shaft_end_y, ball_center_z),
        Vec3(17, shaft_end_y, ball_center_z),
        2.2
    )
    wheel_spoke_z = Cone(
        Vec3(0, shaft_end_y, ball_center_z - 17),
        Vec3(0, shaft_end_y, ball_center_z + 17),
        2.2
    )
    wheel_hub = Cone(
        Vec3(0, wheel_y0 - 1, ball_center_z),
        Vec3(0, wheel_y1 + 1, ball_center_z),
        6.5
    )
    handwheel = combine(wheel_ring, wheel_spoke_x, wheel_spoke_z, wheel_hub)
    return combine(ball, valve_port, control_shaft, handwheel).color(*_色_黄铜)


# ============================================================
# 编号17：DN50 球阀（泄水阀，主管沿 Z，装配时旋转至沿 X）
# ============================================================
def _DN50球阀():
    """DN50 黄铜球阀：主管轴线沿 Z，控制轴朝 -Y，圆形手轮在轴端。"""
    ball_diameter = 58.0
    ball_center_z = 0.0
    ball_radius = ball_diameter / 2
    total_height = 82.0

    ball = scale(ball_radius, ball_radius, ball_radius) * Sphere()
    valve_port = Cone(
        Vec3(0, 0, -total_height / 2),
        Vec3(0, 0, total_height / 2),
        30
    )
    bore = Cone(
        Vec3(0, 0, -total_height / 2 - 1),
        Vec3(0, 0, total_height / 2 + 1),
        25
    )
    valve_body = combine(ball, valve_port) - bore

    shaft_start_y = -ball_radius + 2
    shaft_end_y = -ball_radius - 37
    control_shaft = Cone(
        Vec3(0, shaft_start_y, ball_center_z),
        Vec3(0, shaft_end_y, ball_center_z),
        6.5
    )
    wheel_y0 = shaft_end_y - 5
    wheel_y1 = shaft_end_y + 5
    wheel_outer = Cone(
        Vec3(0, wheel_y0, ball_center_z),
        Vec3(0, wheel_y1, ball_center_z),
        26.0
    )
    wheel_inner = Cone(
        Vec3(0, wheel_y0 - 1, ball_center_z),
        Vec3(0, wheel_y1 + 1, ball_center_z),
        17.0
    )
    wheel_ring = wheel_outer - wheel_inner
    wheel_spoke_x = Cone(
        Vec3(-24, shaft_end_y, ball_center_z),
        Vec3(24, shaft_end_y, ball_center_z),
        3.2
    )
    wheel_spoke_z = Cone(
        Vec3(0, shaft_end_y, ball_center_z - 24),
        Vec3(0, shaft_end_y, ball_center_z + 24),
        3.2
    )
    wheel_hub = Cone(
        Vec3(0, wheel_y0 - 1, ball_center_z),
        Vec3(0, wheel_y1 + 1, ball_center_z),
        9.0
    )
    handwheel = combine(wheel_ring, wheel_spoke_x, wheel_spoke_z, wheel_hub)
    result = combine(valve_body, control_shaft, handwheel)
    return result.color(*_色_黄铜)


# ============================================================
# 编号10：DN20 止回阀（内联自湿式参考，轴线沿 X）
# ============================================================
def _止回阀DN20():
    """DN20 止回阀：轴线沿 X，几何中心在原点。"""
    length = 92.0
    body_length = 50.0
    half_length = length / 2
    half_body = body_length / 2
    bore = Cone(Vec3(-half_length - 1, 0, 0),
                Vec3(half_length + 1, 0, 0), 10)
    body_sections = [
        translate(-half_body, 0, 0) * rotate(Vec3(0, 1, 0), math.pi / 2) *
        Section(scale(17.5) * Arc(2 * math.pi)),
        translate(-14, 0, 0) * rotate(Vec3(0, 1, 0), math.pi / 2) *
        Section(scale(23.0) * Arc(2 * math.pi)),
        translate(0, 0, 0) * rotate(Vec3(0, 1, 0), math.pi / 2) *
        Section(scale(25.0) * Arc(2 * math.pi)),
        translate(14, 0, 0) * rotate(Vec3(0, 1, 0), math.pi / 2) *
        Section(scale(23.0) * Arc(2 * math.pi)),
        translate(half_body, 0, 0) * rotate(Vec3(0, 1, 0), math.pi / 2) *
        Section(scale(17.5) * Arc(2 * math.pi))
    ]
    body = Loft(*body_sections)
    body.smooth = True
    body = body - bore
    connectors = combine(
        _六角柱X(-half_length, -half_body, 36) - bore,
        _六角柱X(half_body, half_length, 36) - bore
    )
    neck = Loft(
        translate(0, 0, 12) * Section(scale(12.5) * Arc(2 * math.pi)),
        translate(0, 0, 22) * Section(scale(17.0) * Arc(2 * math.pi)),
        translate(0, 0, 35) * Section(scale(16.0) * Arc(2 * math.pi))
    )
    neck.smooth = True
    collar = Cone(Vec3(0, 0, 27), Vec3(0, 0, 35), 19)
    cap = translate(-15, -15, 35) * scale(30, 30, 10) * Cube()
    return combine(
        combine(body, connectors).color(*_色_黄铜),
        combine(neck, collar, cap).color(*_色_黄铜亮)
    )


# ============================================================
# 编号14：DN20 Y 型过滤器（内联自湿式参考，主管轴线沿 X）
# ============================================================
def _过滤器几何():
    """DN20 Y型过滤器：主管轴线沿 X，滤嘴朝向左下方。"""
    body_d = 40.0
    body = Cone(Vec3(-45, 0, 0), Vec3(45, 0, 0), body_d / 2)
    angle = math.pi / 3
    barrel_len = 50.0
    end = Vec3(-barrel_len * math.cos(angle), 0, -barrel_len * math.sin(angle))
    barrel = Cone(Vec3(0, 0, 0), end, 18)
    cap_axis = Vec3(-math.cos(angle), 0, -math.sin(angle))
    cap = Cone(end, end + cap_axis * 4, 20)
    return combine(body, barrel, cap).color(*_色_黄铜)


# ============================================================
# 编号5：压力表 Y-100（表盘朝 -Y 正前方）
# ============================================================
def _压力表(dial_diameter=90.0, rod_height=40.0, rod_diameter=12.0):
    """压力表：连系杆从原点向上，表盘竖直、读数面朝 -Y。"""
    rod = Cone(Vec3(0, 0, 0), Vec3(0, 0, rod_height), rod_diameter / 2)
    center_z = rod_height + dial_diameter / 2
    shell = Cone(Vec3(0, -8, center_z), Vec3(0, 8, center_z), dial_diameter / 2)
    face = Cone(Vec3(0, -10, center_z), Vec3(0, -8, center_z),
                dial_diameter * 0.43)
    pointer = Cone(Vec3(0, -11, center_z),
                   Vec3(dial_diameter * 0.25, -11,
                        center_z + dial_diameter * 0.10), 1.2)
    return combine(
        combine(rod, shell).color(0.70, 0.73, 0.77, 1.0),
        face.color(0.94, 0.94, 0.92, 1.0),
        pointer.color(0.10, 0.10, 0.10, 1.0)
    )


# ============================================================
# 编号7：压力开关 ZSJY（底部接口为原点，深色方盒）
# ============================================================
def _压力开关(box_width=70.0, box_depth=55.0, box_height=65.0):
    """压力开关：底部短管接口 + 深色方盒 + 顶部接线盒。"""
    stub = Cone(Vec3(0, 0, 0), Vec3(0, 0, 12), 6)
    base = Cone(Vec3(0, 0, 12), Vec3(0, 0, 20), 12)
    box = translate(-box_width / 2, -box_depth / 2, 20) * \
          scale(box_width, box_depth, box_height) * Cube()
    cable = translate(-10, -10, 20 + box_height) * scale(20, 20, 18) * Cube()
    return combine(
        combine(stub, base).color(*_色_黄铜),
        combine(box, cable).color(*_色_深色)
    )


# ============================================================
# 编号8：电磁阀 DN20（黄铜阀座 + 顶部黑色方盒线圈）
# ============================================================
def _电磁阀():
    """电磁阀：底部 DN20 接口为原点，黄铜阀座，顶部黑色线圈盒。"""
    inlet = Cone(Vec3(0, 0, 0), Vec3(0, 0, 25), 11)
    chamber = translate(0, 0, 32) * scale(17, 17, 14) * Sphere()
    neck = Cone(Vec3(0, 0, 40), Vec3(0, 0, 50), 7)
    coil = translate(-14, -11, 50) * scale(28, 22, 34) * Cube()
    coil_top = translate(-8, -6, 84) * scale(16, 12, 10) * Cube()
    return combine(
        combine(inlet, chamber, neck).color(*_色_黄铜),
        combine(coil, coil_top).color(*_色_深色)
    )


# ============================================================
# 编号6：水力警铃 ZSJL（内联自湿式参考）
# ============================================================
def _水力警铃几何():
    """水力警铃：定位点为 DN20 进水口外端面，进水方向沿 -X（铃体在 -X 侧）。"""
    bell_diameter = 160.0
    bell_depth = 42.0
    bell_sections = 16
    rim_thickness = 4.0
    housing_diameter = 84.0
    housing_depth = 50.0
    cover_diameter = 88.0
    cover_thickness = 5.0
    bolt_count = 8
    bolt_diameter = 8.0
    bolt_height = 5.0
    inlet_dn = 20.0
    outlet_dn = 25.0
    inlet_od = 30.0
    outlet_od = 36.0
    port_length = 38.0
    shaft_diameter = 12.0
    center_bolt_d = 12.0
    center_bolt_h = 8.0

    bell_radius = bell_diameter / 2
    housing_radius = housing_diameter / 2

    housing_x = -port_length - housing_radius
    housing_z = 0.0
    bell_x = housing_x
    bell_z = 0.0
    housing_back_y = -housing_depth / 2
    housing_front_y = housing_depth / 2
    bell_front_y = housing_back_y + 9.0
    bell_back_y = bell_front_y - bell_depth

    bell_profiles = []
    for index in range(bell_sections + 1):
        t = index / bell_sections
        y_position = bell_back_y + bell_depth * t
        radius_factor = 0.72 + 0.28 * math.sin(math.pi * t / 2)
        current_radius = bell_radius * radius_factor
        profile = translate(bell_x, y_position, bell_z) * \
                  rotate(Vec3(1, 0, 0), math.pi / 2) * \
                  Section(scale(current_radius) * Arc(2 * math.pi))
        bell_profiles.append(profile)

    bell_cover = Loft(*bell_profiles)
    bell_cover.smooth = True
    rim_outer = Cone(
        Vec3(bell_x, bell_front_y - rim_thickness, bell_z),
        Vec3(bell_x, bell_front_y + rim_thickness, bell_z),
        bell_radius
    )
    rim_inner = Cone(
        Vec3(bell_x, bell_front_y - rim_thickness - 1, bell_z),
        Vec3(bell_x, bell_front_y + rim_thickness + 1, bell_z),
        bell_radius - rim_thickness
    )
    bell_rim = rim_outer - rim_inner
    center_shaft = Cone(
        Vec3(bell_x, bell_front_y - 5, bell_z),
        Vec3(bell_x, housing_front_y + cover_thickness, bell_z),
        shaft_diameter / 2
    )
    center_bolt = Cone(
        Vec3(bell_x, bell_back_y - center_bolt_h, bell_z),
        Vec3(bell_x, bell_back_y, bell_z),
        center_bolt_d / 2
    )
    bell_set = combine(bell_cover, bell_rim, center_bolt)

    housing = Cone(
        Vec3(housing_x, housing_back_y, housing_z),
        Vec3(housing_x, housing_front_y, housing_z),
        housing_radius
    )
    housing_boss = Cone(
        Vec3(housing_x, housing_back_y - 6, housing_z),
        Vec3(housing_x, housing_back_y + 8, housing_z),
        housing_radius * 0.72
    )
    housing_set = combine(housing, housing_boss, center_shaft)

    cover_start_y = housing_front_y
    cover_end_y = cover_start_y + cover_thickness
    cover_plate = Cone(
        Vec3(housing_x, cover_start_y, housing_z),
        Vec3(housing_x, cover_end_y, housing_z),
        cover_diameter / 2
    )
    cover_bolts = []
    bolt_circle_radius = cover_diameter * 0.37
    for index in range(bolt_count):
        angle = 2 * math.pi * index / bolt_count
        bolt_x = housing_x + bolt_circle_radius * math.cos(angle)
        bolt_z = housing_z + bolt_circle_radius * math.sin(angle)
        cover_bolts.append(Cone(
            Vec3(bolt_x, cover_end_y, bolt_z),
            Vec3(bolt_x, cover_end_y + bolt_height, bolt_z),
            bolt_diameter / 2
        ))
    cover_set = combine(cover_plate, *cover_bolts)

    inlet_connection_x = housing_x + housing_radius
    inlet_outer = Cone(
        Vec3(0, 0, 0), Vec3(inlet_connection_x - 4, 0, 0), inlet_od / 2
    )
    inlet_inner = Cone(
        Vec3(1, 0, 0), Vec3(inlet_connection_x - 5, 0, 0), inlet_dn / 2
    )
    inlet = inlet_outer - inlet_inner
    inlet_collar = Cone(
        Vec3(-8, 0, 0), Vec3(0, 0, 0), inlet_od * 0.62
    ) - Cone(
        Vec3(-9, 0, 0), Vec3(1, 0, 0), inlet_dn / 2
    )

    outlet_start_z = housing_radius
    outlet_end_z = outlet_start_z + 100
    outlet_outer = Cone(
        Vec3(housing_x, 0, outlet_start_z - 4),
        Vec3(housing_x, 0, outlet_end_z),
        outlet_od / 2
    )
    outlet_inner = Cone(
        Vec3(housing_x, 0, outlet_start_z - 5),
        Vec3(housing_x, 0, outlet_end_z + 1),
        outlet_dn / 2
    )
    outlet = outlet_outer - outlet_inner
    outlet_collar = Cone(
        Vec3(housing_x, 0, outlet_end_z),
        Vec3(housing_x, 0, outlet_end_z + 8),
        outlet_od * 0.62
    ) - Cone(
        Vec3(housing_x, 0, outlet_end_z - 1),
        Vec3(housing_x, 0, outlet_end_z + 9),
        outlet_dn / 2
    )
    ports = combine(inlet, inlet_collar, outlet, outlet_collar)

    bracket_y = housing_back_y - 2
    bracket_z = housing_z + housing_radius * 0.72
    bracket_base = translate(
        housing_x - 20, bracket_y - 4, bracket_z - 8
    ) * scale(40, 8, 16) * Cube()
    bracket_arm = translate(
        housing_x + 10, bracket_y - 4, bracket_z - 8
    ) * rotate(Vec3(0, 1, 0), -math.pi / 6) * scale(12, 8, 48) * Cube()
    hammer_stem = Cone(
        Vec3(housing_x + 12, bracket_y, bracket_z + 12),
        Vec3(bell_x + bell_radius * 0.25, bell_front_y + 2,
             bell_z - bell_radius * 0.08),
        3.5
    )
    hammer_head = translate(
        bell_x + bell_radius * 0.25, bell_front_y + 2,
        bell_z - bell_radius * 0.08
    ) * scale(16, 12, 16) * Sphere()
    hammer_set = combine(bracket_base, bracket_arm, hammer_stem, hammer_head)

    return combine(
        bell_set.color(0.82, 0.035, 0.025, 1.0),
        housing_set.color(0.29, 0.31, 0.33, 1.0),
        cover_set.color(0.72, 0.74, 0.76, 1.0),
        ports.color(0.48, 0.50, 0.52, 1.0),
        hammer_set.color(0.40, 0.42, 0.44, 1.0)
    )


# ============================================================
# 编号16：管卡（内联自湿式参考，定位点为管道轴线中心）
# ============================================================
def _管卡(pipe_od=114.0, strap_width=30.0, strap_thickness=5.0, bolt_dia=10.0):
    """条带式 U 型管卡：定位点为管道轴线中心（管道沿 Z），
    水平条带抱住管道，前侧有 U 型螺栓头。"""
    R_inner = pipe_od / 2
    R_outer = R_inner + strap_thickness
    half_h = strap_width / 2
    R_mid = (R_inner + R_outer) / 2

    section = Section(
        Vec2(-strap_thickness / 2, -half_h),
        Vec2(strap_thickness / 2, -half_h),
        Vec2(strap_thickness / 2, half_h),
        Vec2(-strap_thickness / 2, half_h)
    )

    N = 64
    pieces = []
    for i in range(N):
        angle = 2 * math.pi * (i + 0.5) / N
        seg_length = 2 * math.pi * R_mid / N
        oriented = rotate(Vec3(0, 0, 1), angle) * \
                   rotate(Vec3(1, 0, 0), math.pi / 2) * section
        half_seg = seg_length / 2
        line = Line(
            Vec3(-math.sin(angle) * half_seg, math.cos(angle) * half_seg, 0),
            Vec3(math.sin(angle) * half_seg, -math.cos(angle) * half_seg, 0)
        )
        seg = Sweep(oriented, line)
        seg = translate(R_mid * math.cos(angle),
                        R_mid * math.sin(angle), 0) * seg
        pieces.append(seg)

    band = combine(*pieces)

    bolt = Cone(
        Vec3(0, -R_outer - 2, 0),
        Vec3(0, R_outer + 3, 0),
        bolt_dia / 2
    )
    bolt_upper = translate(0, 0, -half_h * 0.5) * bolt
    bolt_lower = translate(0, 0, half_h * 0.5) * bolt

    nut = Cone(
        Vec3(0, R_outer, 0),
        Vec3(0, R_outer + 4, 0),
        bolt_dia * 0.7
    )
    nut_upper = translate(0, 0, -half_h * 0.5) * nut
    nut_lower = translate(0, 0, half_h * 0.5) * nut

    return band + bolt_upper + bolt_lower + nut_upper + nut_lower


# ============================================================
# 编号4：雨淋报警阀 ZSFY（隔膜式，红色阀体）
# ============================================================
def _雨淋报警阀(total_height=420.0, dn=100.0,
                flange_od=220.0, bolt_circle=180.0,
                bolt_dia=18.0, bolt_count=8):
    """ZSFY 隔膜式雨淋报警阀单体。

    局部原点 = 下法兰底面中心，主流道沿 +Z。
    左侧(-X)：下=供水腔控制接口(DN20, z=60)、上=控制腔接口(DN20, z=300)；
    右侧(+X)：中=报警口(DN20, z=250)、上=试验放水口(DN40, z=340)；
    前部(-Y)：中部椭圆检修盖 + 6 螺栓。
    阀体细节以 DN100 为基准按 dn 等比缩放，接口高度按 total_height/420 缩放。
    """
    sf = dn / 100.0
    zs = total_height / 420.0

    flange_radius = flange_od / 2.0
    flange_thickness = 24.0 * sf
    bore_radius = dn / 2.0
    neck_radius = dn / 2.0 + 12.0 * sf
    body_rx = 140.0 * sf
    body_ry = 100.0 * sf

    body_bottom = flange_thickness
    body_top = total_height - flange_thickness
    body_mid = (body_bottom + body_top) / 2.0

    main_bore = Cone(
        Vec3(0, 0, -2.0), Vec3(0, 0, total_height + 2.0),
        bore_radius, bore_radius
    )

    # ---------- 1. 铸造阀体（椭圆截面 Loft，下窄→中宽→上窄） ----------
    body_sections = [
        _椭圆截面Z(body_bottom, neck_radius * 1.15, neck_radius * 1.15),
        _椭圆截面Z(body_bottom + 46.0 * zs, body_rx * 0.86, body_ry * 0.86),
        _椭圆截面Z(body_mid, body_rx, body_ry),
        _椭圆截面Z(body_top - 46.0 * zs, body_rx * 0.86, body_ry * 0.86),
        _椭圆截面Z(body_top, neck_radius * 1.15, neck_radius * 1.15)
    ]
    body_blank = Loft(*body_sections)
    body_blank.smooth = True
    body = body_blank - main_bore

    # ---------- 2. 上下法兰（带螺栓孔） ----------
    def make_flange(z_low, z_high):
        flange = Cone(
            Vec3(0, 0, z_low), Vec3(0, 0, z_high),
            flange_radius, flange_radius
        )
        flange = flange - Cone(
            Vec3(0, 0, z_low - 1.0), Vec3(0, 0, z_high + 1.0),
            bore_radius, bore_radius
        )
        for index in range(bolt_count):
            angle = 2.0 * math.pi * index / bolt_count
            x_position = bolt_circle / 2.0 * math.cos(angle)
            y_position = bolt_circle / 2.0 * math.sin(angle)
            flange = flange - Cone(
                Vec3(x_position, y_position, z_low - 1.0),
                Vec3(x_position, y_position, z_high + 1.0),
                bolt_dia / 2.0, bolt_dia / 2.0
            )
        return flange

    lower_flange = make_flange(0.0, flange_thickness)
    upper_flange = make_flange(body_top, total_height)

    # ---------- 3. 侧向接口（穿入阀体保证相贯，端部带承口） ----------
    port_start = 90.0 * sf          # 穿入阀体内
    port_end = 185.0 * sf           # 接口端面（全局布局对接点）

    def make_port(side, center_z, outside_d, inside_d):
        tube = Cone(
            Vec3(side * port_start, 0, center_z),
            Vec3(side * port_end, 0, center_z),
            outside_d / 2.0, outside_d / 2.0
        ) - Cone(
            Vec3(side * (port_start - 10.0), 0, center_z),
            Vec3(side * (port_end + 1.0), 0, center_z),
            inside_d / 2.0, inside_d / 2.0
        )
        collar = Cone(
            Vec3(side * (port_end - 14.0), 0, center_z),
            Vec3(side * port_end, 0, center_z),
            outside_d * 0.62, outside_d * 0.62
        ) - Cone(
            Vec3(side * (port_end - 15.0), 0, center_z),
            Vec3(side * (port_end + 1.0), 0, center_z),
            inside_d / 2.0, inside_d / 2.0
        )
        return combine(tube, collar)

    port_fill = make_port(-1, 60.0 * zs, 28.0, 21.0)     # 左下：供水腔控制接口
    port_ctrl = make_port(-1, 300.0 * zs, 28.0, 21.0)    # 左上：控制腔接口
    port_alarm = make_port(1, 250.0 * zs, 28.0, 21.0)    # 右中：报警口
    port_test = make_port(1, 340.0 * zs, 48.0, 41.0)     # 右上：试验放水口

    # ---------- 4. 前部椭圆检修盖（-Y，6 螺栓） ----------
    cover_width = 200.0 * sf
    cover_height = 220.0 * sf
    cover_thickness = 15.0
    cover_center_z = 210.0 * zs

    def cover_section(y_position, rx, rz):
        return translate(0, y_position, cover_center_z) * \
               rotate(Vec3(1, 0, 0), -math.pi / 2) * \
               Section(scale(rx, rz) * Arc(2.0 * math.pi))

    cover = Loft(
        cover_section(-body_ry + 3.0, cover_width / 2, cover_height / 2),
        cover_section(-body_ry - cover_thickness,
                      cover_width / 2, cover_height / 2)
    )
    cover.smooth = False
    cover_bolts = []
    for index in range(6):
        angle = 2.0 * math.pi * index / 6
        bolt_x = (cover_width / 2 - 15.0) * math.cos(angle)
        bolt_z = cover_center_z + (cover_height / 2 - 15.0) * math.sin(angle)
        cover_bolts.append(Cone(
            Vec3(bolt_x, -body_ry - cover_thickness - 6.0, bolt_z),
            Vec3(bolt_x, -body_ry - cover_thickness + 2.0, bolt_z),
            5.0
        ))
    cover_bolt_set = combine(*cover_bolts)

    return combine(
        combine(body, lower_flange, upper_flange).color(*_色_阀体红),
        combine(port_fill, port_ctrl, port_alarm, port_test).color(*_色_阀体红亮),
        cover.color(*_色_阀体红暗),
        cover_bolt_set.color(*_色_钢)
    )


# ============================================================
# ZSFY 雨淋报警阀组整体装配
# ============================================================
class ZSFY雨淋报警阀组(Component):
    """ZSFY 雨淋报警阀组整体（编号 1~17 全部）。

    定位点 = 主立管与地面接触面的圆心。
    切换『型号』时先查 MODEL_DIMS 刷新全部驱动尺寸，再重建几何。
    布局参数（控制/报警竖管位置等）由 dn、B、C 自动推算，三型号自适应。
    """

    MODEL_DIMS = {
        'ZSFY100': {
            '尺寸A': 420.0, '尺寸B': 500.0, '尺寸C': 400.0, '尺寸D': 500.0,
            '尺寸E': 400.0, '尺寸F': 300.0, '尺寸G': 100.0, '尺寸H': 990.0,
            '信号蝶阀结构长度': 155.0,
            '主管公称直径': 100.0, '主管外径': 114.0, '主管壁厚': 7.0,
            '信号阀公称直径': 100.0, '雨淋报警阀公称直径': 100.0,
            '法兰外径': 220.0, '法兰孔中心圆': 180.0,
            '法兰孔径': 18.0, '法兰孔数': 8,
        },
        # TODO: ZSFY150/200 的信号蝶阀结构长度为估算值，
        # 可用对应信号阀样本实测结构长度替换。
        'ZSFY150': {
            '尺寸A': 480.0, '尺寸B': 580.0, '尺寸C': 400.0, '尺寸D': 500.0,
            '尺寸E': 400.0, '尺寸F': 370.0, '尺寸G': 100.0, '尺寸H': 960.0,
            '信号蝶阀结构长度': 175.0,
            '主管公称直径': 150.0, '主管外径': 168.0, '主管壁厚': 8.0,
            '信号阀公称直径': 150.0, '雨淋报警阀公称直径': 150.0,
            '法兰外径': 280.0, '法兰孔中心圆': 240.0,
            '法兰孔径': 23.0, '法兰孔数': 8,
        },
        'ZSFY200': {
            '尺寸A': 690.0, '尺寸B': 680.0, '尺寸C': 500.0, '尺寸D': 500.0,
            '尺寸E': 480.0, '尺寸F': 470.0, '尺寸G': 150.0, '尺寸H': 855.0,
            '信号蝶阀结构长度': 200.0,
            '主管公称直径': 200.0, '主管外径': 219.0, '主管壁厚': 8.0,
            '信号阀公称直径': 200.0, '雨淋报警阀公称直径': 200.0,
            '法兰外径': 340.0, '法兰孔中心圆': 295.0,
            '法兰孔径': 23.0, '法兰孔数': 12,
        },
    }

    def __init__(self):
        Component.__init__(self)

        # ===== 型号选择 =====
        self['型号'] = Attr('ZSFY100', obvious=True, group='型号选择',
                            combo=['ZSFY100', 'ZSFY150', 'ZSFY200'])

        # ===== 04S206 安装尺寸（切型号自动刷新，只读） =====
        self['尺寸A'] = Attr(420.0, obvious=True, readonly=True, group='安装尺寸')
        self['尺寸B'] = Attr(500.0, obvious=True, readonly=True, group='安装尺寸')
        self['尺寸C'] = Attr(400.0, obvious=True, readonly=True, group='安装尺寸')
        self['尺寸D'] = Attr(500.0, obvious=True, readonly=True, group='安装尺寸')
        self['尺寸E'] = Attr(400.0, obvious=True, readonly=True, group='安装尺寸')
        self['尺寸F'] = Attr(300.0, obvious=True, readonly=True, group='安装尺寸')
        self['尺寸G'] = Attr(100.0, obvious=True, readonly=True, group='安装尺寸')
        self['尺寸H'] = Attr(990.0, obvious=True, readonly=True, group='安装尺寸')
        self['管卡中心标高'] = Attr(500.0, obvious=True, readonly=True,
                                 group='安装尺寸')

        # ===== 主通路驱动属性（被驱动点引用的必须 obvious=True） =====
        self['信号蝶阀结构长度'] = Attr(155.0, obvious=True, readonly=True,
                                    group='主通路')
        self['信号阀到报警阀短管长度'] = Attr(50.0, obvious=True, readonly=True,
                                        group='主通路')
        self['主管公称直径'] = Attr(100.0, obvious=True, readonly=True,
                                 group='主通路')
        self['主管外径'] = Attr(114.0, obvious=False, group='主通路')
        self['主管壁厚'] = Attr(7.0, obvious=False, group='主通路')
        self['信号阀公称直径'] = Attr(100.0, obvious=True, readonly=True,
                                  group='信号阀')
        self['雨淋报警阀公称直径'] = Attr(100.0, obvious=True, readonly=True,
                                    group='雨淋报警阀')

        # ===== 法兰参数 =====
        self['法兰外径'] = Attr(220.0, obvious=False, group='雨淋报警阀')
        self['法兰孔中心圆'] = Attr(180.0, obvious=False, group='雨淋报警阀')
        self['法兰孔径'] = Attr(18.0, obvious=False, group='雨淋报警阀')
        self['法兰孔数'] = Attr(8, obvious=False, group='雨淋报警阀')

        # ===== 小回路驱动属性 =====
        self['水力警铃外径'] = Attr(160.0, obvious=True, readonly=True,
                                 group='报警回路')
        self['报警管外径'] = Attr(28.0, obvious=False, group='报警回路')
        self['报警管壁厚'] = Attr(3.5, obvious=False, group='报警回路')
        self['试验放水管外径'] = Attr(48.0, obvious=False, group='试验放水')
        self['试验放水管内径'] = Attr(41.0, obvious=False, group='试验放水')
        self['泄水管外径'] = Attr(60.0, obvious=False, group='泄水回路')
        self['泄水管壁厚'] = Attr(3.5, obvious=False, group='泄水回路')
        self['泄水阀接口标高'] = Attr(700.0, obvious=False, group='泄水回路')
        self['泄水管出口标高'] = Attr(150.0, obvious=True, readonly=True,
                                   group='泄水回路')

        # ===== 标识 =====
        self['名称'] = Attr('ZSFY系列雨淋报警阀组', obvious=True,
                            readonly=True, group='标识')
        self['图集号'] = Attr('04S206', obvious=True, readonly=True, group='标识')

        # ===== 业务属性（部件型号，对应 ZSFY 部件表） =====
        self['信号阀型号'] = Attr('ZSFD-16Z', obvious=True, readonly=True,
                              group='业务属性')
        self['试验信号阀型号'] = Attr('ZSFD-16Z', obvious=True, readonly=True,
                                group='业务属性')
        self['雨淋报警阀型号'] = Attr('ZSFY', obvious=True, readonly=True,
                                 group='业务属性')
        self['压力表型号'] = Attr('Y-100', obvious=True, readonly=True,
                              group='业务属性')
        self['水力警铃型号'] = Attr('ZSJL', obvious=True, readonly=True,
                               group='业务属性')
        self['压力开关型号'] = Attr('ZSJY', obvious=True, readonly=True,
                               group='业务属性')
        self['泄水阀型号'] = Attr('Q11f-16', obvious=True, readonly=True,
                              group='业务属性')

        # ===== 技术参数 =====
        self['工作压力'] = Attr('1.6MPa', obvious=True, readonly=True,
                             group='技术参数')
        self['推荐安装位置'] = Attr('安全且便于操作的明显位置', obvious=True,
                               readonly=True, group='安装要求')
        self['两侧最小检修距离'] = Attr('距墙不小于 0.5 m', obvious=True,
                                  readonly=True, group='安装要求')
        self['正面最小检修距离'] = Attr('距墙不小于 1.2 m', obvious=True,
                                  readonly=True, group='安装要求')

        # ===== 图纸部件表（按 04S206 第29页） =====
        self['1_消防给水管'] = Attr(
            'DN100/150/200 / 供水 / 平时：充满水 / 失火时：充满水',
            obvious=True, readonly=True, group='图纸部件表')
        self['2_信号阀'] = Attr(
            'DN100/150/200 / 供水控制阀，阀门关闭时有电信号输出 '
            '/ 平时：常开 / 失火时：开',
            obvious=True, readonly=True, group='图纸部件表')
        self['3_试验信号阀'] = Attr(
            'DN100/150/200 / 平时常开，试验雨淋阀时关闭，关闭时有电信号输出 '
            '/ 平时：开 / 失火时：闭',
            obvious=True, readonly=True, group='图纸部件表')
        self['4_雨淋报警阀'] = Attr(
            'ZSFY / 系统控制阀，开启时可输出报警水流信号 '
            '/ 平时：常闭 / 失火时：自动开启',
            obvious=True, readonly=True, group='图纸部件表')
        self['5_压力表'] = Attr(
            'Y-100 / 数量：2 / 显示水压',
            obvious=True, readonly=True, group='图纸部件表')
        self['6_水力警铃'] = Attr(
            'ZSJL / 报警阀开启时发出音响信号 / 平时：不动作 / 失火时：报警',
            obvious=True, readonly=True, group='图纸部件表')
        self['7_压力开关'] = Attr(
            'ZSJY / 雨淋阀开启时输出电信号 / 平时：不动作 / 失火时：输出电信号',
            obvious=True, readonly=True, group='图纸部件表')
        self['8_电磁阀'] = Attr(
            'DN20 / 探测器报警后联动开启雨淋报警阀 / 平时：常闭',
            obvious=True, readonly=True, group='图纸部件表')
        self['9_手动开启阀'] = Attr(
            'DN20 / 火灾时现场手动应急开启雨淋报警阀 / 平时：常闭',
            obvious=True, readonly=True, group='图纸部件表')
        self['10_止回阀'] = Attr(
            'DN20 / 单向补水，防止控制腔水压不稳产生误动作 / 平时：常开',
            obvious=True, readonly=True, group='图纸部件表')
        self['11_控制管球阀'] = Attr(
            'DN20 / 控制控制腔供水 / 平时：常开',
            obvious=True, readonly=True, group='图纸部件表')
        self['12_报警管球阀'] = Attr(
            'DN20 / 手动关闭后可消除报警 / 平时：常开',
            obvious=True, readonly=True, group='图纸部件表')
        self['13_试验管球阀'] = Attr(
            'DN20 / 手动打开后可在主阀关闭状态下试验警铃 / 平时：常闭',
            obvious=True, readonly=True, group='图纸部件表')
        self['14_过滤器'] = Attr(
            'DN20 / 过滤水中杂质，防止管路堵塞 / 通流',
            obvious=True, readonly=True, group='图纸部件表')
        self['15_试验放水阀'] = Attr(
            'DN40 / 系统调试或功能试验时打开放水 / 平时：常闭',
            obvious=True, readonly=True, group='图纸部件表')
        self['16_管卡'] = Attr(
            '数量：2 / 固定管道',
            obvious=True, readonly=True, group='图纸部件表')
        self['17_泄水阀'] = Attr(
            'Q11f-16 / DN50 / 系统检修时排空放水',
            obvious=True, readonly=True, group='图纸部件表')

        # ===== 输出属性（只让整体默认显示，避免重复渲染） =====
        self['主立管'] = Attr(None)
        self['信号阀'] = Attr(None)
        self['雨淋报警阀'] = Attr(None)
        self['顶部管路'] = Attr(None)
        self['试验信号阀'] = Attr(None)
        self['水力警铃'] = Attr(None)
        self['压力开关'] = Attr(None)
        self['报警回路'] = Attr(None)
        self['控制回路'] = Attr(None)
        self['电磁阀'] = Attr(None)
        self['手动开启阀'] = Attr(None)
        self['试验回路'] = Attr(None)
        self['试验放水阀'] = Attr(None)
        self['泄水回路'] = Attr(None)
        self['管卡'] = Attr(None)
        self['整体'] = Attr(None, show=True)

        # ===== 驱动特征点（与同系列一致，管口中心用 EndPoint） =====
        z_ab = ('[定位点Z]+[尺寸H]+[信号蝶阀结构长度]'
                '+[信号阀到报警阀短管长度]')
        self.setDrivenFeaturePoint('主立管底端中心', SnapMode.EndPoint,
            '[定位点X]', '[定位点Y]', '[定位点Z]')
        self.setDrivenFeaturePoint('信号阀下法兰底面', SnapMode.EndPoint,
            '[定位点X]', '[定位点Y]', '[定位点Z]+[尺寸H]')
        self.setDrivenFeaturePoint('雨淋报警阀下端', SnapMode.EndPoint,
            '[定位点X]', '[定位点Y]', z_ab)
        self.setDrivenFeaturePoint('雨淋报警阀上法兰顶面', SnapMode.EndPoint,
            '[定位点X]', '[定位点Y]', z_ab + '+[尺寸A]')
        self.setDrivenFeaturePoint('系统侧出口', SnapMode.EndPoint,
            '[定位点X]+[尺寸C]-150',
            '[定位点Y]+[尺寸F]-[尺寸G]',
            z_ab + '+[尺寸A]+[尺寸D]-[水力警铃外径]/2')
        self.setDrivenFeaturePoint('泄水阀排水口', SnapMode.EndPoint,
            '[定位点X]+[尺寸E]', '[定位点Y]',
            '[定位点Z]+[泄水管出口标高]')
        self.setDrivenFeaturePoint('控制腔泄放口', SnapMode.EndPoint,
            '[定位点X]-185*[主管公称直径]/100-180',
            '[定位点Y]',
            z_ab + '+300*[尺寸A]/420+115')

        self.replace()

    @export
    def replace(self):
        # ===== 0. 防止属性自更新触发递归 =====
        if not getattr(self, '_refreshing_dims', False):
            dims = self.MODEL_DIMS.get(self['型号'], self.MODEL_DIMS['ZSFY100'])
            self._refreshing_dims = True
            try:
                for key, value in dims.items():
                    self[key] = value
            finally:
                self._refreshing_dims = False

        # ===== 1. 读取参数 =====
        A = self['尺寸A']
        B = self['尺寸B']
        C = self['尺寸C']
        D = self['尺寸D']
        E = self['尺寸E']
        F = self['尺寸F']
        G = self['尺寸G']
        H = self['尺寸H']
        z_clamp = self['管卡中心标高']
        bfv_length = self['信号蝶阀结构长度']
        connect_len = self['信号阀到报警阀短管长度']
        main_dn = self['主管公称直径']
        main_od = self['主管外径']
        main_id = main_od - 2.0 * self['主管壁厚']
        bell_od = self['水力警铃外径']
        sf = main_dn / 100.0

        dn20_od = self['报警管外径']
        dn20_id = dn20_od - 2.0 * self['报警管壁厚']
        dn40_od = self['试验放水管外径']
        dn40_id = self['试验放水管内径']
        dn50_od = self['泄水管外径']
        dn50_id = dn50_od - 2.0 * self['泄水管壁厚']
        z_drain = self['泄水阀接口标高']
        drain_out_z = self['泄水管出口标高']

        # ===== 2. 竖向基准链（自地面起算） =====
        z_signal_bottom = H
        z_signal_top = H + bfv_length
        z_alarm_bottom = z_signal_top + connect_len
        z_alarm_top = z_alarm_bottom + A
        z_bell_top = z_alarm_top + D
        z_top_pipe = z_bell_top - bell_od / 2.0

        # ===== 3. 进深与水平布局（三型号自适应推算） =====
        y_back = F - G                  # 顶部主水路横管平面
        y_alarm = 60.0                  # 报警回路平面（横管前方，避免碰撞）

        zs = A / 420.0                  # 阀体接口高度缩放因子
        z_fill = z_alarm_bottom + 60.0 * zs      # 供水腔控制接口
        z_alarm_port = z_alarm_bottom + 250.0 * zs
        z_ctrl = z_alarm_bottom + 300.0 * zs     # 控制腔接口
        z_test_out = z_alarm_bottom + 340.0 * zs
        z_test_in = z_signal_top + connect_len / 2.0

        x_port = 185.0 * sf             # 报警阀接口端面
        x_ctrl = -(x_port + 130.0)      # 控制回路竖管
        x_bell_in = C - 30.0            # 警铃进水口（铃右缘=C-30）
        x_alm = x_bell_in - 40.0        # 报警回路竖管
        x_test_riser = x_alm - 40.0     # 试验管竖管
        x_out = C - 150.0               # 系统侧出口
        x_left = -(C - 20.0)            # 顶部横管左端头
        x_switch = -(B - 100.0)         # 压力开关
        x_vent = x_ctrl + 40.0          # 控制腔泄放立管
        z_vent = z_ctrl + 115.0
        x_mid = (x_ctrl - x_port) / 2.0

        # ===== 4. 编号1：主立管 =====
        main_pipe = _空心管(
            Vec3(0, 0, 0), Vec3(0, 0, z_signal_bottom), main_od, main_id
        ).color(*_色_管道)

        # 供水压力表①：连接短管左侧短管 + 压力表（表盘朝 -Y）
        gauge1_pipe = _空心管(
            Vec3(-40, 0, z_test_in), Vec3(-110, 0, z_test_in),
            dn20_od, dn20_id
        ).color(*_色_管道)
        gauge1 = translate(-110, 0, z_test_in) * _压力表(90.0, 40.0, 12.0)

        # ===== 5. 编号2：信号阀 =====
        signal_valve = translate(0, 0, z_signal_bottom + bfv_length / 2.0) * \
                       _信号蝶阀(bfv_length, self['信号阀公称直径'])

        # ===== 6. 连接短管 =====
        connect_pipe = _空心管(
            Vec3(0, 0, z_signal_top), Vec3(0, 0, z_alarm_bottom),
            main_od, main_id
        ).color(*_色_管道)

        # ===== 7. 编号4：雨淋报警阀 =====
        alarm_valve = translate(0, 0, z_alarm_bottom) * _雨淋报警阀(
            total_height=A,
            dn=self['雨淋报警阀公称直径'],
            flange_od=self['法兰外径'],
            bolt_circle=self['法兰孔中心圆'],
            bolt_dia=self['法兰孔径'],
            bolt_count=self['法兰孔数']
        )

        # ===== 8. 顶部出水管（后移至 Y=F-G 平面）+ 顶部横管 =====
        top_riser = _折弯管([
            (0, 0, z_alarm_top),
            (0, 0, z_alarm_top + 100.0),
            (0, y_back, z_alarm_top + 100.0),
            (0, y_back, z_top_pipe)
        ], main_od, main_id).color(*_色_管道)
        top_header = _空心管(
            Vec3(x_left, y_back, z_top_pipe),
            Vec3(x_out, y_back, z_top_pipe),
            main_od, main_id
        ).color(*_色_管道)

        # ===== 9. 编号3：试验信号阀（顶部横管上，手轮 +Z） =====
        test_signal_valve = translate(100.0, y_back, z_top_pipe) * \
                            _试验信号阀(bfv_length, self['信号阀公称直径'])

        # ===== 10. 编号6：水力警铃（报警横管右端，铃体 -X、铃面 -Y） =====
        bell = translate(x_bell_in, y_alarm, z_top_pipe) * \
               rotate(Vec3(1, 0, 0), math.pi) * _水力警铃几何()

        # ===== 11. 报警回路：报警口 → 12 → 后移上升 → 顶部横管 =====
        alarm_feed = _空心管(
            Vec3(x_port, 0, z_alarm_port), Vec3(x_alm, 0, z_alarm_port),
            dn20_od, dn20_id
        ).color(*_色_管道)
        valve12 = translate(x_port + 15.0, 0, z_alarm_port) * \
                  rotate(Vec3(0, 1, 0), math.pi / 2.0) * _小球阀()
        alarm_riser = _折弯管([
            (x_alm, 0, z_alarm_port),
            (x_alm, y_alarm, z_alarm_port),
            (x_alm, y_alarm, z_top_pipe)
        ], dn20_od, dn20_id).color(*_色_管道)
        alarm_left = _空心管(
            Vec3(x_alm, y_alarm, z_top_pipe),
            Vec3(x_switch, y_alarm, z_top_pipe),
            dn20_od, dn20_id
        ).color(*_色_管道)
        alarm_right = _空心管(
            Vec3(x_alm, y_alarm, z_top_pipe),
            Vec3(x_bell_in, y_alarm, z_top_pipe),
            dn20_od, dn20_id
        ).color(*_色_管道)
        # 编号7：压力开关（报警横管左端，坐于管顶）
        pressure_switch = translate(
            x_switch, y_alarm, z_top_pipe + dn20_od / 2.0 - 2.0
        ) * _压力开关()

        # ===== 12. 试验回路：供水侧 → 13 → 接入报警管路（12 下游） =====
        test_run = _折弯管([
            (40, 0, z_test_in),
            (x_test_riser, 0, z_test_in),
            (x_test_riser, 0, z_alarm_port)
        ], dn20_od, dn20_id).color(*_色_管道)
        valve13 = translate(
            x_test_riser, 0, (z_test_in + z_alarm_port) / 2.0 - 19.0
        ) * _小球阀()

        # ===== 13. 控制回路：供水腔接口 → 14 → 11(竖管) → 10 → 控制腔 =====
        ctrl_lower = _空心管(
            Vec3(-x_port, 0, z_fill), Vec3(x_ctrl, 0, z_fill),
            dn20_od, dn20_id
        ).color(*_色_管道)
        filter14 = translate(x_mid, 0, z_fill) * _过滤器几何()
        valve11 = translate(x_ctrl, 0, z_fill) * _小球阀()
        ctrl_riser = _空心管(
            Vec3(x_ctrl, 0, z_fill), Vec3(x_ctrl, 0, z_ctrl),
            dn20_od, dn20_id
        ).color(*_色_管道)
        ctrl_upper = _空心管(
            Vec3(x_ctrl, 0, z_ctrl), Vec3(-x_port, 0, z_ctrl),
            dn20_od, dn20_id
        ).color(*_色_管道)
        check10 = translate(x_mid, 0, z_ctrl) * _止回阀DN20()

        # ===== 14. 控制腔泄放：立管 → 横管 → 8(电磁阀) / 9(手动开启阀) =====
        vent_riser = _空心管(
            Vec3(x_vent, 0, z_ctrl), Vec3(x_vent, 0, z_vent),
            dn20_od, dn20_id
        ).color(*_色_管道)
        vent_header = _空心管(
            Vec3(x_vent - 90.0, 0, z_vent), Vec3(x_vent + 88.0, 0, z_vent),
            dn20_od, dn20_id
        ).color(*_色_管道)
        solenoid_branch = _空心管(
            Vec3(x_vent - 60.0, 0, z_vent),
            Vec3(x_vent - 60.0, 0, z_vent + 14.0),
            dn20_od, dn20_id
        ).color(*_色_管道)
        solenoid8 = translate(x_vent - 60.0, 0, z_vent + 14.0) * _电磁阀()
        valve9 = translate(x_vent + 50.0, 0, z_vent) * \
                 rotate(Vec3(0, 1, 0), math.pi / 2.0) * _小球阀()
        # 控制腔压力表②：泄放横管上引
        gauge2_pipe = _空心管(
            Vec3(x_vent + 20.0, 0, z_vent),
            Vec3(x_vent + 20.0, 0, z_vent + 14.0),
            dn20_od, dn20_id
        ).color(*_色_管道)
        gauge2 = translate(x_vent + 20.0, 0, z_vent + 14.0) * \
                 _压力表(90.0, 40.0, 12.0)

        # ===== 15. 编号15：试验放水阀 DN40（系统腔右侧 → +X） =====
        test_out_pipe = _空心管(
            Vec3(x_port, 0, z_test_out), Vec3(x_alm - 20.0, 0, z_test_out),
            dn40_od, dn40_id
        ).color(*_色_管道)
        valve15 = translate(
            (x_port + x_alm - 20.0) / 2.0 - 27.0, 0, z_test_out
        ) * rotate(Vec3(0, 1, 0), math.pi / 2.0) * _DN40球阀()

        # ===== 16. 编号17：泄水回路 DN50（主立管右侧 → +X → X=+E 向下） =====
        drain_run = _折弯管([
            (40, 0, z_drain),
            (E, 0, z_drain),
            (E, 0, drain_out_z)
        ], dn50_od, dn50_id).color(*_色_管道)
        valve17 = translate(E / 2.0, 0, z_drain) * \
                  rotate(Vec3(0, 1, 0), math.pi / 2.0) * _DN50球阀()

        # ===== 17. 编号16：管卡 ×2 + 锚墙支撑柱 =====
        clamp_outer = main_od / 2.0 + 5.0
        main_clamp = translate(0, 0, z_clamp) * _管卡(pipe_od=main_od)
        main_clamp = main_clamp.color(*_色_铸铁)
        main_strut = translate(-1.0, clamp_outer, z_clamp - 15.0) * \
                     scale(2.0, F - clamp_outer, 30.0) * Cube()
        main_strut = main_strut.color(*_色_铸铁)

        header_clamp = translate(-200.0, y_back, z_top_pipe) * \
                       rotate(Vec3(0, 1, 0), math.pi / 2.0) * \
                       _管卡(pipe_od=main_od)
        header_clamp = header_clamp.color(*_色_铸铁)
        header_strut_length = max(F - (y_back + clamp_outer), 1.0)
        header_strut = translate(
            -201.0, y_back + clamp_outer, z_top_pipe - 15.0
        ) * scale(2.0, header_strut_length, 30.0) * Cube()
        header_strut = header_strut.color(*_色_铸铁)

        # ===== 18. 分组组合与整体输出 =====
        alarm_circuit = combine(
            alarm_feed, valve12, alarm_riser, alarm_left, alarm_right
        )
        control_circuit = combine(
            ctrl_lower, filter14, valve11, ctrl_riser, ctrl_upper, check10,
            vent_riser, vent_header, gauge2_pipe, gauge2
        )
        test_circuit = combine(test_run, valve13)
        test_drain = combine(test_out_pipe, valve15)
        drain_circuit = combine(drain_run, valve17)
        clamps = combine(main_clamp, main_strut, header_clamp, header_strut)
        main_riser_group = combine(main_pipe, gauge1_pipe, gauge1)
        top_pipes = combine(top_riser, top_header)

        overall = combine(
            main_riser_group, signal_valve, connect_pipe, alarm_valve,
            top_pipes, test_signal_valve, bell, pressure_switch,
            alarm_circuit, control_circuit,
            combine(solenoid_branch, solenoid8), valve9,
            test_circuit, test_drain, drain_circuit, clamps
        )

        self['主立管'] = main_riser_group
        self['信号阀'] = signal_valve
        self['雨淋报警阀'] = alarm_valve
        self['顶部管路'] = top_pipes
        self['试验信号阀'] = test_signal_valve
        self['水力警铃'] = bell
        self['压力开关'] = pressure_switch
        self['报警回路'] = alarm_circuit
        self['控制回路'] = control_circuit
        self['电磁阀'] = combine(solenoid_branch, solenoid8)
        self['手动开启阀'] = valve9
        self['试验回路'] = test_circuit
        self['试验放水阀'] = test_drain
        self['泄水回路'] = drain_circuit
        self['管卡'] = clamps
        self['整体'] = overall


def create_ZSFY雨淋报警阀组(**parameters):
    """创建 ZSFY 雨淋报警阀组，并用关键字覆盖默认参数。"""
    component = ZSFY雨淋报警阀组()
    for name, value in parameters.items():
        component[name] = value
    component.replace()
    return component


if __name__ == '__main__':
    FinalGeometry = ZSFY雨淋报警阀组()
    place(FinalGeometry)


