# -*- coding: utf-8 -*-
"""ZSFY 系列雨淋报警阀组整体装配（04S206 第28、29页）。

所有零件几何全部内联在本文件中，不做任何跨文件 import，
满足 pyp3d 单文件单 Component 的约束。

==================== 一、图纸数据 ====================
部件表（17 个编号）：
  1 消防给水管 DN100/150/200   2 信号阀 ZSFD-16Z
  3 试验信号阀                 4 雨淋报警阀 ZSFY
  5 压力表 Y-100               6 水力警铃 ZSJL
  7 压力开关 ZSJF              8 电磁阀 DN20
  9 手动开启阀 DN20            10 止回阀 DN20
  11 控制管球阀 DN20           12 报警管球阀 DN20
  13 试警铃球阀 DN20           14 过滤器 DN20
  15 试验放水阀 DN40           16 管卡 ×2
  17 泄水阀 Q11f-16 DN50

安装尺寸表：
  型号      A   B   C   D   E   F   G   H    法兰连接
  ZSFY100  420 500 400 500 400 300 100 990  DN100 φ220 16×M16×160
  ZSFY150  480 580 400 500 400 370 100 960  DN150 φ280 16×M18×165
  ZSFY200  690 680 500 500 480 470 150 855  DN200 φ340 32×M20×180
  另有 500（主立管管卡中心标高）

==================== 二、坐标系与定位基准链 ====================
单位 mm；+Z 向上；-Y 指向正视图观察者（阀组正面），+Y 指向墙；
X 为正视图左右方向（左负右正）。
局部原点（定位点）= 主立管与地面接触面的圆心。

竖向链（Z，自地面起算，以 ZSFY100 为例）：
  0              室内地面（定位点）
  H=990          信号阀(2)下法兰底面
  H+蝶阀长=1145  雨淋报警阀(4)下法兰底面（与信号阀顶直接法兰对接）
  +A=1565        雨淋报警阀上法兰顶面
  +D=2065        顶部报警横管中心线 / 系统横管标高
  500            主立管管卡(16)中心标高

正视方向链（X，以主立管轴线为 0）：
  -E=-400        左侧 DN20 控制立管轴线
  -B=-500        顶部系统横管左端 / 压力开关(7)盒左缘
  +C=+400        水力警铃(6)铃体右缘

进深方向链（Y，以主立管轴线为 0，向墙为正）：
  墙面          Y=+F=+300
  报警回路平面  Y=+(F-G)=+200（报警立管/横管、警铃、压力开关）

==================== 三、装配拓扑 ====================
主水路   ：主立管(1) → 信号阀(2) → 雨淋报警阀(4) → 立管 → 试验信号阀(3)
           → 顶部弯头转 -X → 系统横管（-B 处截断，接系统）
报警回路 ：主立管取水点(z=H-90) → 报警立管(Y=+200) → 试警铃球阀(13)
           → 阀体报警口三通 → 报警管球阀(12) → 报警横管
           → 左接压力开关(7)、右接水力警铃(6)
控制回路 ：主立管取水点 → 过滤器(14) → 左控制立管(X=-E) → 控制管球阀(11)
           → 止回阀(10) → 阀体隔膜腔控制口；支管接压力表(5)；
           泄放支管：电磁阀(8) → 手动开启阀(9) → 自由排水
试验放水 ：系统侧立管 DN40 支路 → 试验放水阀(15) → 向下自由排水
泄水回路 ：阀底进水侧 DN50 支口 → 泄水阀(17) → 向下自由排水
支吊架   ：管卡(16)×2（主立管 z=500、顶部系统横管），背部支撑柱锚墙
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
    """用 FilletPipe 生成带真实圆弧弯头的折线管道（空心）。

    points        折线节点 [(x, y, z), ...]，至少两点，按介质走向顺序给出；
    bend_radius   弯曲半径，缺省取 1D（= 管外径）。

    两端节点倒角半径固定为 0；中间节点的倒角半径按相邻两段管长收敛到
    0.45×较短段，保证同一段管上的两个弯头不会重叠；同时不小于
    0.55×外径，避免弯曲半径小于管半径导致弯头自交。
    """
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


def _六角截面X(x_position, across_flats, center_y=0.0, center_z=0.0):
    circumradius = across_flats / math.sqrt(3.0)
    points = []
    for index in range(6):
        angle = math.pi / 6.0 + index * math.pi / 3.0
        points.append(Vec3(
            x_position,
            center_y + circumradius * math.cos(angle),
            center_z + circumradius * math.sin(angle)
        ))
    points.append(points[0])
    return Section(Line(*points))


def _六角柱X(x_start, x_end, across_flats, center_y=0.0, center_z=0.0):
    result = Loft(
        _六角截面X(x_start, across_flats, center_y, center_z),
        _六角截面X(x_end, across_flats, center_y, center_z)
    )
    result.smooth = False
    return result


def _六角截面Z(z_position, across_flats, center_x=0.0, center_y=0.0):
    circumradius = across_flats / math.sqrt(3.0)
    points = []
    for index in range(6):
        angle = math.pi / 6.0 + index * math.pi / 3.0
        points.append(Vec3(
            center_x + circumradius * math.cos(angle),
            center_y + circumradius * math.sin(angle),
            z_position
        ))
    points.append(points[0])
    return Section(Line(*points))


def _六角柱Z(z_start, z_end, across_flats, center_x=0.0, center_y=0.0):
    result = Loft(
        _六角截面Z(z_start, across_flats, center_x, center_y),
        _六角截面Z(z_end, across_flats, center_x, center_y)
    )
    result.smooth = False
    return result


def _圆截面X(x_position, radius):
    return translate(x_position, 0, 0) * \
           rotate(Vec3(0, 1, 0), math.pi / 2.0) * \
           Section(scale(radius) * Arc(2.0 * math.pi))


def _圆截面Z(z_position, radius):
    return translate(0, 0, z_position) * \
           Section(scale(radius) * Arc(2.0 * math.pi))


# 全局配色
_色_管道 = (0.66, 0.69, 0.72, 1.0)
_色_阀体红 = (0.82, 0.035, 0.025, 1.0)
_色_阀体红亮 = (0.90, 0.055, 0.040, 1.0)
_色_阀体红暗 = (0.64, 0.020, 0.015, 1.0)
_色_黄铜 = (0.78, 0.57, 0.16, 1.0)
_色_黄铜亮 = (0.90, 0.70, 0.28, 1.0)
_色_黄铜暗 = (0.48, 0.31, 0.07, 1.0)
_色_钢 = (0.72, 0.74, 0.76, 1.0)
_色_铸铁 = (0.34, 0.36, 0.38, 1.0)
_色_铸铁亮 = (0.43, 0.45, 0.47, 1.0)
_色_标牌黄 = (0.92, 0.69, 0.12, 1.0)


# ============================================================
# 编号2/3：信号蝶阀 ZSFD-16Z（内联）
# ============================================================
def _信号蝶阀(length=155.0, dn=100.0):
    """信号蝶阀 ZSFD-16Z。

    最终朝向：主管轴线沿 Z，手轮位于 +X 侧，轮面朝 -Y 正前方；
    局部原点位于阀体几何中心。几何随公称直径 dn 以 DN100 为基准等比缩放。
    """
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
# 编号4：雨淋报警阀 ZSFY（隔膜式，内联新建）
# ============================================================
def _雨淋报警阀(total_height=420.0, dn=100.0, main_od=114.0,
                flange_od=220.0, bolt_circle=180.0, bolt_count=16,
                bolt_hole_diameter=18.0):
    """ZSFY 隔膜式雨淋报警阀单体。

    坐标约定：
    - 主流道沿 +Z；检修盖位于 -Y 正前方；
    - 左侧(-X)：上方为隔膜腔控制口(DN20)、下方为进水侧泄水口(DN50)；
    - 背面(+Y)：报警信号口(DN20)；
    - 局部原点 = 下法兰底面中心（与信号阀顶的贴合面）；
    - 阀体总高 = total_height（安装尺寸 A）。

    阀体结构（自下而上）：下法兰 → 下颈 → 梨形下阀体 → 中部隔膜压兰
    （带贯通螺栓母）→ 上部隔膜腔穹盖 → 上颈 → 上法兰。
    控制/报警/泄水口随阀体标高按比例定位，管径不随型号变化（配件均为
    DN20/DN50）。
    """
    sf = dn / 100.0
    A = total_height
    flange_t = 24.0
    r_neck = 70.0 * sf
    r_body = 135.0 * sf
    r_mid = 150.0 * sf
    r_flange = flange_od / 2.0
    r_bore_pipe = main_od / 2.0
    r_bore = dn / 2.0

    # 关键标高（按总高 A 的比例定位）
    z1 = 0.143 * A      # 下颈顶
    z2 = 0.286 * A      # 下阀体中段
    z3 = 0.476 * A      # 阀体最大处（中法兰下缘）
    z4 = 0.533 * A      # 中法兰上缘
    z5 = 0.667 * A      # 上穹中段
    z6 = 0.786 * A
    z7 = 0.857 * A      # 上颈底
    z8 = 0.943 * A      # 上颈顶
    z_alarm = 0.595 * A   # 报警口标高（背面 +Y）
    z_ctrl = 0.845 * A    # 隔膜腔控制口标高（左侧 -X）
    z_drain = 0.131 * A   # 进水侧泄水口标高（左侧 -X）

    main_bore = Cone(
        Vec3(0, 0, -2.0), Vec3(0, 0, A + 2.0), r_bore, r_bore
    )

    # ---------- 1. 铸造阀体（多截面放样） ----------
    body_sections = [
        _圆截面Z(flange_t, r_neck),
        _圆截面Z(z1, r_neck),
        _圆截面Z(z2, (r_neck + r_body) / 2.0),
        _圆截面Z(z3, r_body),
        _圆截面Z(z4, r_body),
        _圆截面Z(z5, r_body * 0.889),
        _圆截面Z(z6, r_neck * 1.286),
        _圆截面Z(z7, r_neck),
        _圆截面Z(z8, r_neck),
    ]
    body_blank = Loft(*body_sections)
    body_blank.smooth = True
    body = body_blank - main_bore

    # ---------- 2. 中部隔膜压兰 + 贯通螺栓母 ----------
    mid_flange = Cone(
        Vec3(0, 0, z3), Vec3(0, 0, z4), r_mid, r_mid
    ) - main_bore
    mid_nuts = []
    for index in range(bolt_count):
        angle = 2.0 * math.pi * index / bolt_count
        nut_x = bolt_circle / 2.0 * math.cos(angle)
        nut_y = bolt_circle / 2.0 * math.sin(angle)
        mid_nuts.append(_六角柱Z(z4, z4 + 10.0 * sf, 24.0 * sf, nut_x, nut_y))
    mid_bolt_set = combine(*mid_nuts)

    # ---------- 3. 顶/底连接法兰 ----------
    def make_flange(z_low, z_high):
        flange = Cone(
            Vec3(0, 0, z_low), Vec3(0, 0, z_high), r_flange, r_flange
        )
        flange = flange - Cone(
            Vec3(0, 0, z_low - 1.0), Vec3(0, 0, z_high + 1.0),
            r_bore_pipe, r_bore_pipe
        )
        for index in range(bolt_count):
            angle = 2.0 * math.pi * index / bolt_count
            hole_x = bolt_circle / 2.0 * math.cos(angle)
            hole_y = bolt_circle / 2.0 * math.sin(angle)
            flange = flange - Cone(
                Vec3(hole_x, hole_y, z_low - 1.0),
                Vec3(hole_x, hole_y, z_high + 1.0),
                bolt_hole_diameter / 2.0, bolt_hole_diameter / 2.0
            )
        return flange

    bottom_flange = make_flange(0.0, flange_t)
    top_flange = make_flange(A - flange_t, A)

    # ---------- 4. 前部椭圆检修盖 + 螺栓 ----------
    z_cover = 0.333 * A
    r_section_low = (r_neck + r_body) / 2.0
    r_at_cover = r_section_low + (r_body - r_section_low) * \
                 (z_cover - z2) / (z3 - z2)
    cover_rx = 85.0 * sf
    cover_rz = 65.0 * sf
    cover_back_y = -r_at_cover + 4.0
    cover_front_y = cover_back_y - 14.0

    def ellipse_section_y(y_position):
        return translate(0, y_position, z_cover) * \
               rotate(Vec3(1, 0, 0), math.pi / 2.0) * \
               Section(scale(cover_rx, cover_rz) * Arc(2.0 * math.pi))

    cover_plate = Loft(
        ellipse_section_y(cover_back_y),
        ellipse_section_y(cover_front_y)
    )
    cover_plate.smooth = False

    cover_bolts = []
    for index in range(8):
        angle = 2.0 * math.pi * index / 8
        bolt_x = cover_rx * 0.80 * math.cos(angle)
        bolt_z = z_cover + cover_rz * 0.80 * math.sin(angle)
        cover_bolts.append(Cone(
            Vec3(bolt_x, cover_front_y, bolt_z),
            Vec3(bolt_x, cover_front_y - 6.0, bolt_z),
            5.0 * sf, 5.0 * sf
        ))
    cover_bolt_set = combine(*cover_bolts)

    # ---------- 5. 正面铭牌 ----------
    nameplate = translate(
        -26.0 * sf, cover_front_y - 1.2, z_cover - 12.0 * sf
    ) * scale(52.0 * sf, 1.2, 24.0 * sf) * Cube()

    # ---------- 6. 三个管口（控制口/报警口/泄水口） ----------
    def make_port(dir_x, dir_y, center_z, outside_d, inside_d,
                  length, body_radius_at_z):
        """自阀体壁面伸出的圆管口（带端部承口）。

        外管自体内 (body_radius_at_z-8) 起算、向外伸出 length，
        保证与阀体完全相贯、不悬空。
        """
        outer_r = outside_d / 2.0
        inner_r = inside_d / 2.0
        start_x = dir_x * (body_radius_at_z - 8.0)
        start_y = dir_y * (body_radius_at_z - 8.0)
        end_x = dir_x * (body_radius_at_z - 8.0 + length)
        end_y = dir_y * (body_radius_at_z - 8.0 + length)
        tube = Cone(
            Vec3(start_x, start_y, center_z),
            Vec3(end_x, end_y, center_z),
            outer_r, outer_r
        ) - Cone(
            Vec3(dir_x * (body_radius_at_z - 10.0),
                 dir_y * (body_radius_at_z - 10.0), center_z),
            Vec3(dir_x * (body_radius_at_z + length + 2.0),
                 dir_y * (body_radius_at_z + length + 2.0), center_z),
            inner_r, inner_r
        )
        collar = Cone(
            Vec3(dir_x * (body_radius_at_z + length - 22.0),
                 dir_y * (body_radius_at_z + length - 22.0), center_z),
            Vec3(end_x, end_y, center_z),
            outer_r * 1.24, outer_r * 1.24
        ) - Cone(
            Vec3(dir_x * (body_radius_at_z + length - 24.0),
                 dir_y * (body_radius_at_z + length - 24.0), center_z),
            Vec3(dir_x * (body_radius_at_z + length + 2.0),
                 dir_y * (body_radius_at_z + length + 2.0), center_z),
            inner_r, inner_r
        )
        return combine(tube, collar)

    # 各接口根部所在标高的阀体半径（与放样截面一致）
    r_at_ctrl = r_neck * 1.286 - (r_neck * 1.286 - r_neck) * \
                (z_ctrl - z6) / (z7 - z6)
    r_at_alarm = r_body - (r_body - r_body * 0.889) * \
                 (z_alarm - z4) / (z5 - z4)
    r_at_drain = r_neck

    # 隔膜腔控制口（-X，DN20）
    port_ctrl = make_port(-1.0, 0.0, z_ctrl, 28.0, 21.0, 65.0, r_at_ctrl)
    # 报警信号口（+Y，DN20）
    port_alarm = make_port(0.0, 1.0, z_alarm, 28.0, 21.0, 60.0, r_at_alarm)
    # 进水侧泄水口（-X，DN50）
    port_drain = make_port(-1.0, 0.0, z_drain, 60.0, 53.0, 70.0, r_at_drain)

    # ---------- 7. 配色与输出 ----------
    return combine(
        body.color(*_色_阀体红),
        combine(mid_flange, mid_bolt_set).color(*_色_阀体红暗),
        combine(bottom_flange, top_flange).color(*_色_阀体红),
        cover_plate.color(*_色_阀体红亮),
        cover_bolt_set.color(*_色_钢),
        combine(port_ctrl, port_alarm, port_drain).color(*_色_阀体红),
        nameplate.color(*_色_标牌黄)
    )


# ==== 雨淋报警阀的关键接口坐标（供装配计算，与上面几何保持一致） ====
def _雨淋阀接口(local_z_ratio, total_height, dn, reach):
    """计算某比例标高、向外 reach 长度管口的端面到阀轴线的距离。"""
    sf = dn / 100.0
    A = total_height
    z = local_z_ratio * A
    r_neck = 70.0 * sf
    r_body = 135.0 * sf
    z4 = 0.476 * A
    z5 = 0.667 * A
    z6 = 0.786 * A
    z7 = 0.857 * A
    if abs(local_z_ratio - 0.845) < 1e-6:
        r_at = r_neck * 1.286 - (r_neck * 1.286 - r_neck) * (z - z6) / (z7 - z6)
    elif abs(local_z_ratio - 0.595) < 1e-6:
        r_at = r_body - (r_body - r_body * 0.889) * (z - z4) / (z5 - z4)
    else:
        r_at = r_neck
    return r_at - 8.0 + reach


# ============================================================
# 编号10：止回阀 DN20（内联）
# ============================================================
def _止回阀(dn=20.0, total_length=92.0, body_length=50.0,
           body_diameter=50.0, hex_width=36.0,
           cover_diameter=38.0, cover_height=8.0,
           cover_hex_width=30.0, cover_hex_height=7.0,
           neck_height=10.0, interface_od=28.0):
    """DN20 黄铜内螺纹止回阀。

    主管流道沿 +X（进口在 -X、出口在 +X），阀盖位于 +Z，阀体中心为局部原点。
    """
    half_total = total_length / 2.0
    half_body = body_length / 2.0
    body_radius = body_diameter / 2.0
    connector_length = half_total - half_body

    end_radius = interface_od * 0.62
    body_sections = [
        _圆截面X(-half_body, end_radius),
        _圆截面X(-half_body * 0.58, body_radius * 0.91),
        _圆截面X(0.0, body_radius),
        _圆截面X(half_body * 0.58, body_radius * 0.91),
        _圆截面X(half_body, end_radius)
    ]
    body_outer = Loft(*body_sections)
    body_outer.smooth = True
    main_bore = Cone(
        Vec3(-half_total - 2.0, 0, 0), Vec3(half_total + 2.0, 0, 0),
        dn / 2.0, dn / 2.0
    )
    body = body_outer - main_bore

    left_hex = _六角柱X(-half_total, -half_body, hex_width) - main_bore
    right_hex = _六角柱X(half_body, half_total, hex_width) - main_bore
    left_boss = Cone(
        Vec3(-half_body - connector_length * 0.22, 0, 0),
        Vec3(-half_body + 5.0, 0, 0), interface_od * 0.62
    ) - main_bore
    right_boss = Cone(
        Vec3(half_body - 5.0, 0, 0),
        Vec3(half_body + connector_length * 0.22, 0, 0), interface_od * 0.62
    ) - main_bore
    connectors = combine(left_hex, right_hex, left_boss, right_boss)

    neck_bottom_z = body_radius * 0.48
    neck_top_z = body_radius + neck_height
    neck = Loft(
        _圆截面Z(neck_bottom_z, cover_diameter * 0.33),
        _圆截面Z(body_radius * 0.86, cover_diameter * 0.45),
        _圆截面Z(neck_top_z, cover_diameter * 0.42)
    )
    neck.smooth = True
    cover_collar = Cone(
        Vec3(0, 0, neck_top_z - cover_height), Vec3(0, 0, neck_top_z),
        cover_diameter / 2.0
    )
    cover_hex = _六角柱Z(
        neck_top_z, neck_top_z + cover_hex_height, cover_hex_width
    )
    cover_top = Cone(
        Vec3(0, 0, neck_top_z + cover_hex_height),
        Vec3(0, 0, neck_top_z + cover_hex_height + 3.0),
        cover_hex_width * 0.52
    )
    bonnet = combine(neck, cover_collar, cover_hex, cover_top)

    thread_rings = []
    ring_outer_radius = dn / 2.0 + 1.5
    ring_inner_radius = max(dn / 2.0 - 0.8, 1.0)
    thread_count = 4
    thread_pitch = min(3.0, connector_length / (thread_count + 1))
    for index in range(thread_count):
        offset = 4.0 + index * thread_pitch
        left_x = -half_total + offset
        right_x = half_total - offset
        left_ring = Cone(
            Vec3(left_x, 0, 0), Vec3(left_x + 1.1, 0, 0), ring_outer_radius
        ) - Cone(
            Vec3(left_x - 1.0, 0, 0), Vec3(left_x + 2.1, 0, 0), ring_inner_radius
        )
        right_ring = Cone(
            Vec3(right_x - 1.1, 0, 0), Vec3(right_x, 0, 0), ring_outer_radius
        ) - Cone(
            Vec3(right_x - 2.1, 0, 0), Vec3(right_x + 1.0, 0, 0), ring_inner_radius
        )
        thread_rings.extend([left_ring, right_ring])
    threads = combine(*thread_rings)

    return combine(
        body.color(*_色_黄铜),
        connectors.color(*_色_黄铜),
        bonnet.color(*_色_黄铜亮),
        threads.color(*_色_黄铜暗)
    )


# ============================================================
# 编号9/11/12/13：DN20 内螺纹球阀（内联）
# ============================================================
def _DN20球阀(dn=20.0, total_length=56.0, hex_width=31.0,
              connector_length=12.0, thread_depth=10.0,
              body_length=37.0, body_diameter=40.0, body_end_diameter=27.0,
              gland_diameter=22.0, gland_height=10.0,
              stem_diameter=7.0, stem_height=16.0,
              nut_width=13.0, nut_height=5.0,
              handle_length=91.0, handle_width=13.0, handle_thickness=3.2,
              handle_back=14.0, handle_angle_deg=0.0):
    """DN20 内螺纹球阀。主流道沿 +X，阀杆沿 +Z，阀体中心为局部原点。

    handle_angle_deg = 0 时手柄与流道平行（开启状态）。
    """
    half_total = total_length / 2.0
    connector_length = min(connector_length, half_total - 3.0)
    thread_depth = min(thread_depth, connector_length - 1.0)
    body_length = min(body_length, total_length - 2.0 * connector_length + 4.0)
    half_body = body_length / 2.0
    body_radius = body_diameter / 2.0
    body_end_radius = body_end_diameter / 2.0
    gland_radius = gland_diameter / 2.0
    stem_radius = stem_diameter / 2.0
    handle_back = min(handle_back, handle_length / 2.0)
    handle_angle = math.radians(handle_angle_deg)

    body_blank = Loft(
        _圆截面X(-half_body, body_end_radius),
        _圆截面X(-half_body * 0.55, body_radius * 0.92),
        _圆截面X(0.0, body_radius),
        _圆截面X(half_body * 0.55, body_radius * 0.92),
        _圆截面X(half_body, body_end_radius)
    )
    body_blank.smooth = True
    main_bore = Cone(
        Vec3(-half_total - 1.0, 0, 0), Vec3(half_total + 1.0, 0, 0),
        dn / 2.0, dn / 2.0
    )
    body = body_blank - main_bore

    left_connector = _六角柱X(-half_total, -half_body + 0.4, hex_width) - main_bore
    right_connector = _六角柱X(half_body - 0.4, half_total, hex_width) - main_bore
    connectors = combine(left_connector, right_connector)

    thread_parts = []
    thread_count = 4
    thread_pitch = max((thread_depth - 2.5) / thread_count, 1.0)
    for index in range(thread_count):
        offset = 1.6 + index * thread_pitch
        for direction in (-1.0, 1.0):
            x_position = direction * (half_total - offset)
            thread_parts.append(
                Cone(Vec3(x_position - 0.3, 0, 0), Vec3(x_position + 0.3, 0, 0),
                     dn / 2.0 + 0.45, dn / 2.0 + 0.45) -
                Cone(Vec3(x_position - 0.6, 0, 0), Vec3(x_position + 0.6, 0, 0),
                     dn / 2.0 - 0.35, dn / 2.0 - 0.35)
            )
    threads = combine(*thread_parts)

    gland = Loft(
        _圆截面Z(body_radius * 0.55, gland_radius * 0.65),
        _圆截面Z(body_radius, gland_radius),
        _圆截面Z(body_radius + gland_height, gland_radius * 0.82)
    )
    gland.smooth = True
    gland_end_z = body_radius + gland_height
    stem_end_z = gland_end_z + stem_height
    stem = Cone(
        Vec3(0, 0, gland_end_z - 0.5), Vec3(0, 0, stem_end_z),
        stem_radius, stem_radius
    )
    nut = _六角柱Z(stem_end_z - nut_height, stem_end_z, nut_width)

    handle_z = stem_end_z
    center_start = -handle_back + handle_width / 2.0
    center_end = handle_length - handle_back - handle_width / 2.0
    bar = translate(center_start, -handle_width / 2.0, handle_z) * \
          scale(center_end - center_start, handle_width, handle_thickness) * Cube()
    start_round = Cone(
        Vec3(center_start, 0, handle_z),
        Vec3(center_start, 0, handle_z + handle_thickness),
        handle_width / 2.0, handle_width / 2.0
    )
    end_round = Cone(
        Vec3(center_end, 0, handle_z),
        Vec3(center_end, 0, handle_z + handle_thickness),
        handle_width / 2.0, handle_width / 2.0
    )
    handle = rotate(Vec3(0, 0, 1), handle_angle) * \
             combine(bar, start_round, end_round)

    return combine(
        body.color(*_色_黄铜),
        connectors.color(*_色_黄铜),
        threads.color(*_色_黄铜暗),
        combine(gland, stem, nut).color(*_色_黄铜亮),
        handle.color(*_色_阀体红)
    )


# ============================================================
# 编号8：电磁阀 DN20（内联新建）
# ============================================================
def _电磁阀(dn=20.0, hex_width=27.0, hex_height=14.0,
            body_diameter=32.0, body_height=46.0,
            bonnet_diameter=20.0, coil_diameter=30.0, coil_height=42.0,
            cap_diameter=34.0, cap_height=6.0):
    """DN20 电磁阀（隔膜腔泄放用）。

    流道沿 +Z，局部原点位于底部接口端面中心；
    自下而上：六角接头 → 黄铜阀体 → 阀盖 → 电磁线圈 → 顶部端盖，
    线圈侧面带接线盒。
    """
    main_bore = Cone(
        Vec3(0, 0, -1.0), Vec3(0, 0, body_height + 1.0), dn / 2.0, dn / 2.0
    )
    lower_hex = _六角柱Z(0.0, hex_height, hex_width) - main_bore
    body = Cone(
        Vec3(0, 0, hex_height - 0.5), Vec3(0, 0, body_height),
        body_diameter / 2.0, body_diameter / 2.0
    ) - main_bore
    bonnet = Cone(
        Vec3(0, 0, body_height - 1.0), Vec3(0, 0, body_height + 4.0),
        bonnet_diameter / 2.0, bonnet_diameter / 2.0
    )
    coil_bottom = body_height + 3.0
    coil = Cone(
        Vec3(0, 0, coil_bottom), Vec3(0, 0, coil_bottom + coil_height),
        coil_diameter / 2.0, coil_diameter / 2.0
    )
    cap = Cone(
        Vec3(0, 0, coil_bottom + coil_height),
        Vec3(0, 0, coil_bottom + coil_height + cap_height),
        cap_diameter / 2.0, cap_diameter / 2.0
    )
    terminal = translate(
        coil_diameter / 2.0 - 2.0, -8.0, coil_bottom + coil_height * 0.40
    ) * scale(14.0, 16.0, 18.0) * Cube()

    return combine(
        combine(lower_hex, body).color(*_色_黄铜),
        bonnet.color(*_色_黄铜亮),
        combine(coil, terminal).color(0.16, 0.17, 0.20, 1.0),
        cap.color(*_色_钢)
    )


# ============================================================
# 编号5：弹簧管压力表 Y-100（内联）
# ============================================================
def _压力表(dial_diameter=100.0, rod_height=60.0, rod_diameter=14.0):
    """弹簧管压力表（编号5 Y-100）。

    连系杆底端位于局部原点，表盘位于 +Z 上方、盘面法线沿 Y 轴。
    表壳背板在 +Y 侧，开口面与指针在 -Y 侧——装配时不作任何旋转，
    读数面即朝向正前方。
    """
    D = dial_diameter
    R = D / 2.0
    H = rod_height
    RG = rod_diameter / 2.0

    HG = H * 0.3
    HT = H * 0.15
    HP = H * 0.05
    S = D * 0.05
    L = D * 0.85
    B = D * 0.15
    SY = rod_diameter * 1.2
    SQ = SY * 0.1
    RP = D * 0.2
    RT1 = RP * 0.7
    RT2 = RP * 0.6

    下杆 = Cone(Vec3(0, 0, 0), Vec3(0, 0, HG), RG, RG)
    下片 = Cone(Vec3(0, 0, HG), Vec3(0, 0, HG + HP), RP, RP)
    下圆台 = Cone(Vec3(0, 0, HG + HP), Vec3(0, 0, HG + HP + HT), RT2, RT1)
    上圆台 = Cone(Vec3(0, 0, HG + HP + HT), Vec3(0, 0, HG + HP + HT * 2), RT1, RT2)
    上片 = Cone(Vec3(0, 0, HG + HP + HT * 2),
                Vec3(0, 0, HG + HP + HT * 2 + HP), RP, RP)
    上杆 = Cone(Vec3(0, 0, HG + HP + HT * 2 + HP),
                Vec3(0, 0, HG + HP + HT * 2 + HP + HG + S), RG, RG)

    连系杆 = combine(下杆, 下片, 下圆台, 上圆台, 上片, 上杆)

    dial_z = HG + HP + HT * 2 + HP + HG + R
    y_back = SY / 2.0
    y_face = y_back - SQ

    表壳 = Cone(Vec3(0, -y_back, dial_z), Vec3(0, y_back, dial_z), R, R) - \
           Cone(Vec3(0, -y_back, dial_z), Vec3(0, y_face, dial_z), R - S, R - S)
    刻度盘 = Cone(
        Vec3(0, y_face - 0.8, dial_z), Vec3(0, y_face, dial_z), R - S, R - S
    )

    三角平面 = Section(Line(
        Vec3(-B / 2.0, y_face - 0.8, 0),
        Vec3(B / 2.0, y_face - 0.8, 0),
        Vec3(0, y_face - 0.8, L)
    ))
    扫掠体 = Sweep(三角平面, Line(Vec3(0, 0, 0), Vec3(0, -0.6 * y_face, 0)))
    指针 = translate(0, 0, dial_z) * roty(math.pi / 6.0) * \
           translate(0, 0, -L / 2.0) * 扫掠体

    return combine(
        连系杆.color(*_色_钢),
        表壳.color(0.20, 0.21, 0.24, 1.0),
        刻度盘.color(0.94, 0.94, 0.96, 1.0),
        指针.color(0.82, 0.05, 0.04, 1.0)
    )


# ============================================================
# 编号14：Y型过滤器 DN20（内联）
# ============================================================
def _过滤器几何():
    """ZSPL DN20 Y型过滤器，局部主管轴线沿X，滤筒朝向左下方倾斜。"""
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
# 编号15/17：内螺纹球阀 DN40/DN50（内联）
# ============================================================
def _手柄球阀(dn=50.0, total_length=106.0, hex_width=62.0,
              connector_length=22.0, thread_depth=19.0,
              body_length=68.0, body_diameter=76.0, body_end_diameter=62.0,
              gland_diameter=31.0, gland_height=14.0,
              stem_diameter=10.0, stem_height=22.0,
              nut_width=17.0, nut_height=7.0,
              handle_length=155.0, handle_width=18.0, handle_thickness=4.0,
              handle_back=20.0, handle_angle_deg=0.0):
    """内螺纹手柄球阀（编号15 DN40 / 编号17 DN50 共用）。

    主流道沿 +X，阀杆沿 +Z，阀体中心为局部原点。
    handle_angle_deg = 0 时手柄与流道平行（开启状态）。
    """
    half_total = total_length / 2.0
    connector_length = min(connector_length, half_total - 6.0)
    thread_depth = min(thread_depth, connector_length - 1.0)
    body_length = min(body_length, total_length - 2.0 * connector_length + 8.0)
    half_body = body_length / 2.0
    body_radius = body_diameter / 2.0
    body_end_radius = body_end_diameter / 2.0
    gland_radius = gland_diameter / 2.0
    stem_radius = stem_diameter / 2.0
    handle_back = min(handle_back, handle_length / 2.0)
    handle_angle = math.radians(handle_angle_deg)

    body_blank = Loft(
        _圆截面X(-half_body, body_end_radius),
        _圆截面X(-half_body * 0.62, body_radius * 0.92),
        _圆截面X(0.0, body_radius),
        _圆截面X(half_body * 0.62, body_radius * 0.92),
        _圆截面X(half_body, body_end_radius)
    )
    body_blank.smooth = True
    main_bore = Cone(
        Vec3(-half_total - 2.0, 0, 0), Vec3(half_total + 2.0, 0, 0),
        dn / 2.0, dn / 2.0
    )
    body = body_blank - main_bore

    left_hex = _六角柱X(-half_total, -half_body + 0.5, hex_width) - main_bore
    right_hex = _六角柱X(half_body - 0.5, half_total, hex_width) - main_bore
    left_transition = Cone(
        Vec3(-half_body - 2.0, 0, 0), Vec3(-half_body + 5.0, 0, 0),
        body_end_radius, body_end_radius
    ) - main_bore
    right_transition = Cone(
        Vec3(half_body - 5.0, 0, 0), Vec3(half_body + 2.0, 0, 0),
        body_end_radius, body_end_radius
    ) - main_bore
    connectors = combine(left_hex, right_hex, left_transition, right_transition)

    thread_rings = []
    thread_count = 5
    thread_pitch = max((thread_depth - 4.0) / thread_count, 1.2)
    for index in range(thread_count):
        offset = 2.5 + index * thread_pitch
        left_x0 = -half_total + offset
        thread_rings.append(
            Cone(Vec3(left_x0, 0, 0), Vec3(left_x0 + 0.7, 0, 0),
                 dn / 2.0 + 0.55, dn / 2.0 + 0.55) -
            Cone(Vec3(left_x0 - 0.3, 0, 0), Vec3(left_x0 + 1.0, 0, 0),
                 dn / 2.0 - 0.45, dn / 2.0 - 0.45)
        )
        right_x1 = half_total - offset
        thread_rings.append(
            Cone(Vec3(right_x1 - 0.7, 0, 0), Vec3(right_x1, 0, 0),
                 dn / 2.0 + 0.55, dn / 2.0 + 0.55) -
            Cone(Vec3(right_x1 - 1.0, 0, 0), Vec3(right_x1 + 0.3, 0, 0),
                 dn / 2.0 - 0.45, dn / 2.0 - 0.45)
        )
    internal_threads = combine(*thread_rings)

    body_top_z = body_radius
    gland_base = Loft(
        _圆截面Z(body_top_z * 0.58, gland_radius * 0.72),
        _圆截面Z(body_top_z + gland_height * 0.32, gland_radius),
        _圆截面Z(body_top_z + gland_height, gland_radius * 0.82)
    )
    gland_base.smooth = True
    stem_start_z = body_top_z + gland_height - 0.5
    stem_end_z = stem_start_z + stem_height
    stem = Cone(
        Vec3(0, 0, stem_start_z), Vec3(0, 0, stem_end_z),
        stem_radius, stem_radius
    )
    nut = _六角柱Z(
        stem_end_z - nut_height * 0.80, stem_end_z + nut_height * 0.20, nut_width
    )
    stem_set = combine(gland_base, stem, nut)

    handle_z = stem_end_z + nut_height * 0.20
    handle_x_start = -handle_back + handle_width / 2.0
    handle_x_end = handle_length - handle_back - handle_width / 2.0
    handle_bar = translate(
        handle_x_start, -handle_width / 2.0, handle_z
    ) * scale(
        handle_x_end - handle_x_start, handle_width, handle_thickness
    ) * Cube()
    handle_start_round = Cone(
        Vec3(handle_x_start, 0, handle_z),
        Vec3(handle_x_start, 0, handle_z + handle_thickness),
        handle_width / 2.0, handle_width / 2.0
    )
    handle_end_round = Cone(
        Vec3(handle_x_end, 0, handle_z),
        Vec3(handle_x_end, 0, handle_z + handle_thickness),
        handle_width / 2.0, handle_width / 2.0
    )
    handle = rotate(Vec3(0, 0, 1), handle_angle) * combine(
        handle_bar, handle_start_round, handle_end_round
    )
    stop_plate = translate(-13.0, -13.0, handle_z - 2.0) * \
                 scale(26.0, 26.0, 2.0) * Cube()
    top_washer = Cone(
        Vec3(0, 0, handle_z + handle_thickness),
        Vec3(0, 0, handle_z + handle_thickness + 2.0),
        nut_width * 0.58, nut_width * 0.58
    )

    return combine(
        body.color(*_色_黄铜),
        connectors.color(*_色_黄铜),
        internal_threads.color(*_色_黄铜暗),
        stem_set.color(*_色_黄铜亮),
        handle.color(*_色_阀体红),
        combine(stop_plate, top_washer).color(*_色_钢)
    )


# ============================================================
# 编号6：水力警铃 ZSJL（内联）
# ============================================================
def _水力警铃():
    """水力警铃 ZSJL，定位点为 DN20 进水口外端面，进水方向沿 -X。"""
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

    # 定位原点位于右侧 DN20 进水口，水轮壳体和钟罩位于 -X 侧。
    housing_x = -port_length - housing_radius
    housing_z = 0.0
    bell_x = housing_x
    bell_z = 0.0
    housing_back_y = -housing_depth / 2
    housing_front_y = housing_depth / 2
    bell_front_y = housing_back_y + 9.0
    bell_back_y = bell_front_y - bell_depth

    # 1. 封闭红色警铃罩。
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

    # 2. 水轮壳体和正面检修盖。
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

    # 3. DN20 进水口和 DN25 排水口。
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

    # 排水口沿局部 +Z；装配旋转后朝下。
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

    # 4. 击锤及支架。
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
# 编号7：压力开关 ZSJF（内联）
# ============================================================
def _压力开关(box_width=95.0, box_depth=62.0, box_height=70.0,
              cover_height=9.0):
    """压力开关 ZSJF。方形壳体，局部原点位于壳体底面中心。"""
    box = translate(-box_width / 2.0, -box_depth / 2.0, 0.0) * \
          scale(box_width, box_depth, box_height) * Cube()
    cover = translate(
        -box_width * 0.44, -box_depth * 0.45, box_height
    ) * scale(box_width * 0.88, box_depth * 0.90, cover_height) * Cube()
    cover_screws = []
    for sx in (-1.0, 1.0):
        for sy in (-1.0, 1.0):
            cover_screws.append(Cone(
                Vec3(sx * box_width * 0.38, sy * box_depth * 0.36, box_height),
                Vec3(sx * box_width * 0.38, sy * box_depth * 0.36,
                     box_height + cover_height + 2.0),
                3.0, 3.0
            ))
    return combine(
        box.color(0.24, 0.26, 0.30, 1.0),
        cover.color(0.34, 0.36, 0.40, 1.0),
        combine(*cover_screws).color(*_色_钢)
    )


# ============================================================
# 编号16：管卡（内联，参数化抱管直径）
# ============================================================
def _管卡(pipe_od=114.0, band_radial_thickness=14.0, band_height=20.0,
          ear_length=48.0, ear_width=26.0, bolt_diameter=12.0):
    """管卡（抱箍板 + 两侧螺栓耳）。

    局部原点位于被抱管的轴线上、管卡中心标高处；抱箍平面为 XY 平面，
    两侧螺栓耳沿 ±X 伸出，与正视图中的矩形带孔卡板一致。
    """
    pipe_radius = pipe_od / 2.0
    band_outer = pipe_radius + band_radial_thickness
    half_height = band_height / 2.0

    band = Cone(
        Vec3(0, 0, -half_height), Vec3(0, 0, half_height), band_outer, band_outer
    ) - Cone(
        Vec3(0, 0, -half_height - 1.0), Vec3(0, 0, half_height + 1.0),
        pipe_radius, pipe_radius
    )

    ears = []
    bolts = []
    for direction in (-1.0, 1.0):
        x_start = direction * (band_outer - 4.0)
        ear = translate(
            min(x_start, x_start + direction * ear_length),
            -ear_width / 2.0, -half_height
        ) * scale(ear_length, ear_width, band_height) * Cube()
        bolt_x = direction * (band_outer + ear_length * 0.55)
        ear = ear - Cone(
            Vec3(bolt_x, 0, -half_height - 1.0),
            Vec3(bolt_x, 0, half_height + 1.0),
            bolt_diameter / 2.0, bolt_diameter / 2.0
        )
        ears.append(ear)
        bolts.append(Cone(
            Vec3(bolt_x, 0, -half_height - 5.0),
            Vec3(bolt_x, 0, half_height + 5.0),
            bolt_diameter / 2.0, bolt_diameter / 2.0
        ))
        bolts.append(_六角柱Z(
            half_height + 5.0, half_height + 12.0,
            bolt_diameter * 1.6, bolt_x, 0.0
        ))

    return combine(
        band.color(*_色_铸铁亮),
        combine(*ears).color(*_色_铸铁亮),
        combine(*bolts).color(*_色_钢)
    )


# ============================================================
# ZSFY 系列雨淋报警阀组 —— 整体装配
# ============================================================
class ZSFY雨淋报警阀组(Component):
    """ZSFY100/150/200 雨淋报警阀组整体（编号 1~17 全部）。

    定位点 = 主立管与地面接触面的圆心。
    切换『型号』时先查 MODEL_DIMS 刷新全部驱动尺寸，再重建几何。
    """

    MODEL_DIMS = {
        'ZSFY100': {
            # ---- 04S206 安装尺寸表 ----
            '尺寸A': 420.0,          # 雨淋报警阀总高
            '尺寸B': 500.0,          # 轴线到系统横管左端（压力开关盒左缘）
            '尺寸C': 400.0,          # 轴线到水力警铃铃体右缘
            '尺寸D': 500.0,          # 雨淋阀上法兰顶面到报警横管中心线
            '尺寸E': 400.0,          # 主立管轴线到左侧控制立管轴线
            '尺寸F': 300.0,          # 墙面到主立管轴线（进深）
            '尺寸G': 100.0,          # 墙面到背面报警立管轴线
            '尺寸H': 990.0,          # 地面到信号阀下法兰底面
            '管卡中心标高': 500.0,
            # ---- 主通路 ----
            '信号蝶阀结构长度': 155.0,
            '主管公称直径': 100.0, '主管外径': 114.0, '主管壁厚': 7.0,
            '信号蝶阀公称直径': 100.0,
            '雨淋报警阀公称直径': 100.0,
            '消防给水管公称直径': 100.0,
            # ---- 法兰连接尺寸 ----
            '法兰外径值': 220.0, '螺栓孔中心圆值': 180.0,
            '螺栓数量值': 16, '螺栓孔直径值': 18.0,
            '法兰公称直径': 'DN100',
            '法兰外径': 'φ220 mm',
            '螺栓孔中心直径': 'φ180 mm',
            '法兰螺栓': '16×M16×160',
        },
        'ZSFY150': {
            '尺寸A': 480.0, '尺寸B': 580.0, '尺寸C': 400.0, '尺寸D': 500.0,
            '尺寸E': 400.0, '尺寸F': 370.0, '尺寸G': 100.0, '尺寸H': 960.0,
            '管卡中心标高': 500.0,
            '信号蝶阀结构长度': 175.0,
            '主管公称直径': 150.0, '主管外径': 168.0, '主管壁厚': 8.0,
            '信号蝶阀公称直径': 150.0,
            '雨淋报警阀公称直径': 150.0,
            '消防给水管公称直径': 150.0,
            '法兰外径值': 280.0, '螺栓孔中心圆值': 240.0,
            '螺栓数量值': 16, '螺栓孔直径值': 22.0,
            '法兰公称直径': 'DN150',
            '法兰外径': 'φ280 mm',
            '螺栓孔中心直径': 'φ240 mm',
            '法兰螺栓': '16×M18×165',
        },
        'ZSFY200': {
            '尺寸A': 690.0, '尺寸B': 680.0, '尺寸C': 500.0, '尺寸D': 500.0,
            '尺寸E': 480.0, '尺寸F': 470.0, '尺寸G': 150.0, '尺寸H': 855.0,
            '管卡中心标高': 500.0,
            '信号蝶阀结构长度': 210.0,
            '主管公称直径': 200.0, '主管外径': 219.0, '主管壁厚': 8.0,
            '信号蝶阀公称直径': 200.0,
            '雨淋报警阀公称直径': 200.0,
            '消防给水管公称直径': 200.0,
            '法兰外径值': 340.0, '螺栓孔中心圆值': 295.0,
            '螺栓数量值': 32, '螺栓孔直径值': 24.0,
            '法兰公称直径': 'DN200',
            '法兰外径': 'φ340 mm',
            '螺栓孔中心直径': 'φ295 mm',
            '法兰螺栓': '32×M20×180',
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
        self['信号蝶阀结构长度'] = Attr(155.0, obvious=True, readonly=True,
                                   group='安装尺寸')

        # ===== 主通路驱动属性 =====
        self['主管公称直径'] = Attr(100.0, obvious=False, group='主通路')
        self['主管外径'] = Attr(114.0, obvious=False, group='主通路')
        self['主管壁厚'] = Attr(7.0, obvious=False, group='主通路')
        self['信号蝶阀公称直径'] = Attr(
            100.0, obvious=True, readonly=True, group='信号蝶阀'
        )
        self['雨淋报警阀公称直径'] = Attr(
            100.0, obvious=True, readonly=True, group='雨淋报警阀'
        )

        # ===== 法兰连接驱动属性 =====
        self['法兰外径值'] = Attr(220.0, obvious=False, group='法兰')
        self['螺栓孔中心圆值'] = Attr(180.0, obvious=False, group='法兰')
        self['螺栓数量值'] = Attr(16, obvious=False, group='法兰')
        self['螺栓孔直径值'] = Attr(18.0, obvious=False, group='法兰')

        # ===== 标识 =====
        self['名称'] = Attr('ZSFY系列雨淋报警阀组', obvious=True,
                            readonly=True, group='标识')
        self['图集号'] = Attr('04S206', obvious=True, readonly=True, group='标识')

        # ===== 业务属性（部件型号，对应雨淋阀组部件表） =====
        self['信号阀型号'] = Attr(
            'ZSFD-16Z', obvious=True, readonly=True, group='业务属性'
        )
        self['试验信号阀型号'] = Attr(
            'ZSFD-16Z', obvious=True, readonly=True, group='业务属性'
        )
        self['雨淋报警阀型号'] = Attr(
            'ZSFY', obvious=True, readonly=True, group='业务属性'
        )
        self['压力表型号'] = Attr(
            'Y-100', obvious=True, readonly=True, group='业务属性'
        )
        self['水力警铃型号'] = Attr(
            'ZSJL', obvious=True, readonly=True, group='业务属性'
        )
        self['压力开关型号'] = Attr(
            'ZSJF', obvious=True, readonly=True, group='业务属性'
        )
        self['电磁阀型号'] = Attr(
            '图纸未注明', obvious=True, readonly=True, group='业务属性'
        )
        self['泄水阀型号'] = Attr(
            'Q11f-16', obvious=True, readonly=True, group='业务属性'
        )

        # ===== 图纸技术参数与安装要求 =====
        self['法兰公称直径'] = Attr(
            'DN100', obvious=True, readonly=True, group='技术参数'
        )
        self['法兰外径'] = Attr(
            'φ220 mm', obvious=True, readonly=True, group='技术参数'
        )
        self['螺栓孔中心直径'] = Attr(
            'φ180 mm', obvious=True, readonly=True, group='技术参数'
        )
        self['法兰螺栓'] = Attr(
            '16×M16×160', obvious=True, readonly=True, group='技术参数'
        )
        self['两侧最小检修距离'] = Attr(
            '距墙不小于 0.5 m', obvious=True, readonly=True, group='安装要求'
        )
        self['正面最小检修距离'] = Attr(
            '距墙不小于 1.2 m', obvious=True, readonly=True, group='安装要求'
        )

        # ===== 各部件公称直径 =====
        self['消防给水管公称直径'] = Attr(
            100.0, obvious=True, readonly=True, group='消防给水管'
        )
        self['电磁阀公称直径'] = Attr(
            20.0, obvious=True, readonly=True, group='电磁阀'
        )
        self['手动开启阀公称直径'] = Attr(
            20.0, obvious=True, readonly=True, group='手动开启阀'
        )
        self['止回阀公称直径'] = Attr(
            20.0, obvious=True, readonly=True, group='止回阀'
        )
        self['控制管球阀公称直径'] = Attr(
            20.0, obvious=True, readonly=True, group='控制管球阀'
        )
        self['报警管球阀公称直径'] = Attr(
            20.0, obvious=True, readonly=True, group='报警管球阀'
        )
        self['试警铃球阀公称直径'] = Attr(
            20.0, obvious=True, readonly=True, group='试警铃球阀'
        )
        self['过滤器公称直径'] = Attr(
            20.0, obvious=True, readonly=True, group='过滤器'
        )
        self['试验放水阀公称直径'] = Attr(
            40.0, obvious=True, readonly=True, group='试验放水阀'
        )
        self['泄水阀公称直径'] = Attr(
            50.0, obvious=True, readonly=True, group='泄水阀'
        )
        self['管卡数量'] = Attr(
            2, obvious=True, readonly=True, group='管卡'
        )

        # ===== 04S206 图纸部件表（数量及工作状态均按图纸） =====
        self['1_消防给水管'] = Attr(
            'DN100/150/200 / 供水 / 平时：充满水 / 失火时：充满水',
            obvious=True, readonly=True, group='图纸部件表'
        )
        self['2_信号阀'] = Attr(
            'DN100/150/200 / 供水控制阀，阀门关闭时有电信号输出 '
            '/ 平时：常开 / 失火时：开',
            obvious=True, readonly=True, group='图纸部件表'
        )
        self['3_试验信号阀'] = Attr(
            'DN100/150/200 / 平时常开，试验雨淋阀时关闭，关闭时有电信号输出 '
            '/ 平时：常闭 / 失火时：闭',
            obvious=True, readonly=True, group='图纸部件表'
        )
        self['4_雨淋报警阀'] = Attr(
            'ZSFY / 系统控制阀，开启时可输出报警水流信号 '
            '/ 平时：常闭 / 失火时：自动开启',
            obvious=True, readonly=True, group='图纸部件表'
        )
        self['5_压力表'] = Attr(
            'Y-100 / 显示水压',
            obvious=True, readonly=True, group='图纸部件表'
        )
        self['6_水力警铃'] = Attr(
            'ZSJL / 报警阀开启时，发出音响信号 / 平时：不动作 / 失火时：报警',
            obvious=True, readonly=True, group='图纸部件表'
        )
        self['7_压力开关'] = Attr(
            'ZSJF / 雨淋阀开启时，发出电信号 / 平时：不动作 / 失火时：输出电信号',
            obvious=True, readonly=True, group='图纸部件表'
        )
        self['8_电磁阀'] = Attr(
            'DN20 / 探测器报警后，联动开启雨淋报警阀 / 平时：常闭',
            obvious=True, readonly=True, group='图纸部件表'
        )
        self['9_手动开启阀'] = Attr(
            'DN20 / 火灾时，现场手动应急开启雨淋报警阀 / 平时：常闭 / 失火时：常闭',
            obvious=True, readonly=True, group='图纸部件表'
        )
        self['10_止回阀'] = Attr(
            'DN20 / 单向补水，防止控制腔水压不稳产生误动作 '
            '/ 平时：常开 / 失火时：常开',
            obvious=True, readonly=True, group='图纸部件表'
        )
        self['11_控制管球阀'] = Attr(
            'DN20 / 控制腔控制供水 / 平时：常开 / 失火时：常开',
            obvious=True, readonly=True, group='图纸部件表'
        )
        self['12_报警管球阀'] = Attr(
            'DN20 / 手动关闭后，可消除报警 / 平时：常开 / 失火时：常开',
            obvious=True, readonly=True, group='图纸部件表'
        )
        self['13_试警铃球阀'] = Attr(
            'DN20 / 手动打开后，可在主阀关闭状态下试验警铃 '
            '/ 平时：常闭 / 失火时：常闭',
            obvious=True, readonly=True, group='图纸部件表'
        )
        self['14_过滤器'] = Attr(
            'DN20 / 过滤水中杂质，防止管路堵塞 / 平时：通流 / 失火时：通流',
            obvious=True, readonly=True, group='图纸部件表'
        )
        self['15_试验放水阀'] = Attr(
            'DN40 / 系统调试或功能试验时打开放水 / 平时：常闭',
            obvious=True, readonly=True, group='图纸部件表'
        )
        self['16_管卡'] = Attr(
            '数量：2 / 固定管道',
            obvious=True, readonly=True, group='图纸部件表'
        )
        self['17_泄水阀'] = Attr(
            'Q11f-16 / DN50 / 系统检修时排空放水',
            obvious=True, readonly=True, group='图纸部件表'
        )

        # ===== 输出属性（只让整体默认显示，避免重复渲染） =====
        self['主立管'] = Attr(None)
        self['信号阀'] = Attr(None)
        self['雨淋报警阀'] = Attr(None)
        self['试验信号阀'] = Attr(None)
        self['顶部系统管'] = Attr(None)
        self['报警回路'] = Attr(None)
        self['水力警铃'] = Attr(None)
        self['压力开关'] = Attr(None)
        self['控制回路'] = Attr(None)
        self['压力表'] = Attr(None)
        self['电磁阀'] = Attr(None)
        self['试验放水支路'] = Attr(None)
        self['泄水回路'] = Attr(None)
        self['管卡'] = Attr(None)
        self['整体'] = Attr(None, show=True)

        # ===== 驱动特征点：本阀组与外部系统的对接接口 =====
        z_sig = '[定位点Z]+[尺寸H]'
        z_valve_bottom = z_sig + '+[信号蝶阀结构长度]'
        z_valve_top = z_valve_bottom + '+[尺寸A]'
        z_alarm_pipe = z_valve_top + '+[尺寸D]'

        self.setDrivenFeaturePoint('主立管底端中心', SnapMode.GeometricCenter,
            '[定位点X]', '[定位点Y]', '[定位点Z]')
        self.setDrivenFeaturePoint('信号阀下法兰底面', SnapMode.GeometricCenter,
            '[定位点X]', '[定位点Y]', z_sig)
        self.setDrivenFeaturePoint('雨淋报警阀下端', SnapMode.GeometricCenter,
            '[定位点X]', '[定位点Y]', z_valve_bottom)
        self.setDrivenFeaturePoint('雨淋报警阀上法兰顶面',
            SnapMode.GeometricCenter,
            '[定位点X]', '[定位点Y]', z_valve_top)
        self.setDrivenFeaturePoint('报警横管中心', SnapMode.GeometricCenter,
            '[定位点X]', '[定位点Y]+[尺寸F]-[尺寸G]', z_alarm_pipe)
        self.setDrivenFeaturePoint('系统侧横管出口', SnapMode.GeometricCenter,
            '[定位点X]-[尺寸B]', '[定位点Y]', z_alarm_pipe)
        self.setDrivenFeaturePoint('左控制立管轴线', SnapMode.GeometricCenter,
            '[定位点X]-[尺寸E]', '[定位点Y]', '[定位点Z]+[尺寸H]-90')

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
        main_dn = self['主管公称直径']
        main_od = self['主管外径']
        main_id = main_od - 2.0 * self['主管壁厚']
        flange_od = self['法兰外径值']
        bolt_circle = self['螺栓孔中心圆值']
        bolt_count = int(self['螺栓数量值'])
        bolt_hole_d = self['螺栓孔直径值']

        trim_od = 28.0          # DN20 配管外径
        trim_id = 21.0          # DN20 配管内径
        test_od = 48.0          # DN40 配管外径
        test_id = 40.0          # DN40 配管内径
        drain_od = 60.0         # DN50 配管外径
        drain_id = 53.0         # DN50 配管内径

        # ===== 2. 竖向基准链（自地面起算） =====
        z_sig_bottom = H                          # 信号阀下法兰底面
        z_sig_top = z_sig_bottom + bfv_length     # 信号阀顶 = 雨淋阀底
        z_valve_top = z_sig_top + A               # 雨淋阀上法兰顶面
        z_alarm_pipe = z_valve_top + D            # 报警横管/系统横管标高
        ya = F - G                                # 报警回路平面 Y
        z_source = H - 90.0                       # 控制/报警取水点标高
        z_alarm_port = z_sig_top + 0.595 * A      # 阀体报警口标高
        z_ctrl_port = z_sig_top + 0.845 * A       # 阀体隔膜腔控制口标高
        z_drain_port = z_sig_top + 0.131 * A      # 阀底泄水口标高

        # 雨淋阀三个管口端面到阀轴线的距离（与单体几何一致）
        ctrl_port_reach = _雨淋阀接口(0.845, A, main_dn, 65.0)
        alarm_port_reach = _雨淋阀接口(0.595, A, main_dn, 60.0)
        drain_port_reach = _雨淋阀接口(0.131, A, main_dn, 70.0)

        # ===== 3. 编号1：主立管（消防给水管） =====
        main_pipe = _空心管(
            Vec3(0, 0, 0), Vec3(0, 0, z_sig_bottom), main_od, main_id
        ).color(*_色_管道)

        # ===== 4. 编号2：信号阀 ZSFD-16Z =====
        butterfly = translate(0, 0, z_sig_bottom + bfv_length / 2.0) * \
                    _信号蝶阀(bfv_length, main_dn)

        # ===== 5. 编号4：雨淋报警阀 ZSFY（底部与信号阀顶直接对接） =====
        deluge_valve = translate(0, 0, z_sig_top) * _雨淋报警阀(
            total_height=A, dn=main_dn, main_od=main_od,
            flange_od=flange_od, bolt_circle=bolt_circle,
            bolt_count=bolt_count, bolt_hole_diameter=bolt_hole_d
        )

        # ===== 6. 编号3：试验信号阀 + 顶部系统横管 =====
        z_riser1_top = z_valve_top + 185.0
        upper_riser = _空心管(
            Vec3(0, 0, z_valve_top), Vec3(0, 0, z_riser1_top),
            main_od, main_id
        ).color(*_色_管道)
        test_butterfly = translate(
            0, 0, z_riser1_top + bfv_length / 2.0
        ) * _信号蝶阀(bfv_length, main_dn)
        z_valve3_top = z_riser1_top + bfv_length
        # 立管上行至报警横管标高后圆弧弯头转 -X，至 -B 截断（接系统）
        top_run = _折弯管([
            (0.0, 0.0, z_valve3_top),
            (0.0, 0.0, z_alarm_pipe),
            (-B, 0.0, z_alarm_pipe)
        ], main_od, main_id).color(*_色_管道)
        system_run = combine(upper_riser, test_butterfly, top_run)

        # ===== 7. 报警回路（背面 Y=+ya 平面） =====
        # 7.1 取水立管：主立管后壁取水 → 后移 → 上行 → 顶部转 +X 至警铃进水口
        gong_inlet_x = C - 160.0                  # 警铃进水口（铃体右缘对齐 +C）
        alarm_riser = _折弯管([
            (0.0, main_od / 2.0 - 17.0, z_source),
            (0.0, ya, z_source),
            (0.0, ya, z_alarm_pipe),
            (gong_inlet_x, ya, z_alarm_pipe)
        ], trim_od, trim_id).color(*_色_管道)

        # 7.2 编号13 试警铃球阀：立管下段（报警口三通之下），常闭
        test_gong_valve = translate(
            0, ya, (z_source + z_alarm_port) / 2.0
        ) * rotate(Vec3(0, 1, 0), -math.pi / 2.0) * \
            _DN20球阀(handle_angle_deg=90.0)

        # 7.3 阀体报警口连接管（阀体背面 → 报警立管三通）
        alarm_port_pipe = _空心管(
            Vec3(0, alarm_port_reach - 2.0, z_alarm_port),
            Vec3(0, ya, z_alarm_port), trim_od, trim_id
        ).color(*_色_管道)

        # 7.4 编号12 报警管球阀：立管上段，常开
        alarm_pipe_valve = translate(
            0, ya, z_valve_top + 185.0
        ) * rotate(Vec3(0, 1, 0), -math.pi / 2.0) * _DN20球阀()

        # 7.5 报警横管左段：立管顶 → 压力开关
        switch_x = -B + 47.5                      # 压力开关盒中心（左缘对齐 -B）
        alarm_left_pipe = _空心管(
            Vec3(0, ya, z_alarm_pipe), Vec3(switch_x, ya, z_alarm_pipe),
            trim_od, trim_id
        ).color(*_色_管道)

        # 7.6 编号7 压力开关（盒底经短立管坐于报警横管上）
        switch_stub = _空心管(
            Vec3(switch_x, ya, z_alarm_pipe),
            Vec3(switch_x, ya, z_alarm_pipe + 30.0), trim_od, trim_id
        ).color(*_色_管道)
        pressure_switch = translate(
            switch_x, ya, z_alarm_pipe + 30.0
        ) * _压力开关()

        # 7.7 编号6 水力警铃：进水口接横管右端，铃面朝 -Y 正前方
        water_gong = translate(gong_inlet_x, ya, z_alarm_pipe) * \
                     rotate(Vec3(0, 0, 1), math.pi) * \
                     rotate(Vec3(1, 0, 0), math.pi) * _水力警铃()

        alarm_circuit = combine(
            alarm_riser, test_gong_valve, alarm_port_pipe,
            alarm_pipe_valve, alarm_left_pipe, switch_stub,
            pressure_switch, water_gong
        )

        # ===== 8. 控制回路（左侧 X=-E 立管，Y=0 平面） =====
        # 8.1 取水管 → 过滤器 → 左控制立管 → 阀体隔膜腔控制口（一根折弯管）
        ctrl_feed = _折弯管([
            (-main_od / 2.0 + 17.0, 0.0, z_source),
            (-E, 0.0, z_source),
            (-E, 0.0, z_ctrl_port),
            (-ctrl_port_reach + 2.0, 0.0, z_ctrl_port)
        ], trim_od, trim_id).color(*_色_管道)

        # 8.2 编号14 过滤器（水平取水段上）
        filter_geometry = translate(-E / 2.0, 0, z_source) * _过滤器几何()

        # 8.3 编号11 控制管球阀（左立管下段，常开）
        ctrl_ball_valve = translate(
            -E, 0, z_source + 100.0
        ) * rotate(Vec3(0, 1, 0), -math.pi / 2.0) * _DN20球阀()

        # 8.4 编号10 止回阀（左立管中段，单向向上补水）
        check_valve = translate(
            -E, 0, z_source + 350.0
        ) * rotate(Vec3(0, 1, 0), -math.pi / 2.0) * _止回阀()

        # 8.5 编号5 压力表（控制顶横管上立杆，表盘朝 -Y）
        gauge_stub = _空心管(
            Vec3(-E + 120.0, 0, z_ctrl_port),
            Vec3(-E + 120.0, 0, z_ctrl_port + 60.0), 22.0, 16.0
        ).color(*_色_管道)
        pressure_gauge = translate(
            -E + 120.0, 0, z_ctrl_port + 60.0
        ) * _压力表(dial_diameter=100.0, rod_height=60.0, rod_diameter=14.0)

        # 8.6 泄放支管：控制顶横管三通向下 → 电磁阀(8) → 手动开启阀(9) → 自由排水
        release_pipe = _空心管(
            Vec3(-E + 40.0, 0, z_ctrl_port - 2.0),
            Vec3(-E + 40.0, 0, z_ctrl_port - 350.0), trim_od, trim_id
        ).color(*_色_管道)
        solenoid_valve = translate(
            -E + 40.0, 0, z_ctrl_port - 145.0
        ) * _电磁阀()
        # 手动开启阀(9) 再绕 Z 转 180°，使阀杆朝 +X，避开左侧控制立管
        manual_valve = translate(
            -E + 40.0, 0, z_ctrl_port - 220.0
        ) * rotate(Vec3(0, 0, 1), math.pi) * \
            rotate(Vec3(0, 1, 0), -math.pi / 2.0) * \
            _DN20球阀(handle_angle_deg=90.0)

        control_circuit = combine(
            ctrl_feed, filter_geometry, ctrl_ball_valve, check_valve,
            gauge_stub, pressure_gauge,
            release_pipe, solenoid_valve, manual_valve
        )

        # ===== 9. 编号15 试验放水支路（系统侧 DN40，向右引出后向下） =====
        z_test_tap = z_valve_top + 85.0
        test_drain_pipe = _折弯管([
            (0.0, 0.0, z_test_tap),
            (250.0, 0.0, z_test_tap),
            (250.0, 0.0, z_sig_top + 55.0)
        ], test_od, test_id).color(*_色_管道)
        test_drain_valve = translate(150.0, 0, z_test_tap) * _手柄球阀(
            dn=40.0, total_length=96.0, hex_width=54.0,
            connector_length=20.0, thread_depth=17.0,
            body_length=60.0, body_diameter=66.0, body_end_diameter=54.0,
            gland_diameter=27.0, gland_height=12.0,
            handle_length=130.0, handle_angle_deg=90.0
        )
        test_drain = combine(test_drain_pipe, test_drain_valve)

        # ===== 10. 编号17 泄水回路（阀底进水侧 DN50 支口 → 泄水阀 → 向下） =====
        drain_valve_center_x = -drain_port_reach - 58.0
        drain_elbow_x = -drain_port_reach - 168.0
        drain_pipe = _折弯管([
            (-drain_port_reach + 2.0, 0.0, z_drain_port),
            (drain_elbow_x, 0.0, z_drain_port),
            (drain_elbow_x, 0.0, z_sig_top - 145.0)
        ], drain_od, drain_id).color(*_色_管道)
        drain_valve = translate(
            drain_valve_center_x, 0, z_drain_port
        ) * _手柄球阀(handle_angle_deg=-90.0)
        drain_circuit = combine(drain_pipe, drain_valve)

        # ===== 11. 编号16 管卡 ×2（背部支撑柱锚墙） =====
        band_radial = 14.0
        band_height = 20.0
        strut_width = 40.0
        strut_thickness = 20.0

        def make_clamp_with_strut(center_x, pipe_diameter, horizontal=False):
            """抱管管卡 + 背部支撑柱（支撑柱嵌进抱箍、锚到墙面 Y=F）。"""
            if horizontal:
                clamp = translate(center_x, 0.0, z_alarm_pipe) * \
                        rotate(Vec3(0, 1, 0), math.pi / 2.0) * _管卡(
                            pipe_od=pipe_diameter,
                            band_radial_thickness=band_radial,
                            band_height=band_height
                        )
                clamp_z = z_alarm_pipe
            else:
                clamp = translate(center_x, 0.0, z_clamp) * _管卡(
                    pipe_od=pipe_diameter,
                    band_radial_thickness=band_radial,
                    band_height=band_height
                )
                clamp_z = z_clamp
            band_outer = pipe_diameter / 2.0 + band_radial
            allowed_depth = band_radial * 0.70
            max_half_width = math.sqrt(max(
                band_outer ** 2 - (band_outer - allowed_depth) ** 2, 1.0
            ))
            half_width = min(strut_width / 2.0, max_half_width)
            chord_y = math.sqrt(max(band_outer ** 2 - half_width ** 2, 0.0))
            embed_depth = min(band_outer - chord_y + 1.5, allowed_depth)
            strut_start_y = band_outer - embed_depth
            strut_length = max(F - strut_start_y, 1.0)
            strut = translate(
                center_x - half_width, strut_start_y,
                clamp_z - strut_thickness / 2.0
            ) * scale(half_width * 2.0, strut_length, strut_thickness) * Cube()
            return combine(clamp, strut.color(*_色_铸铁))

        clamps = combine(
            make_clamp_with_strut(0.0, main_od, horizontal=False),
            make_clamp_with_strut(-B + 20.0, main_od, horizontal=True)
        )

        # ===== 12. 整体组合与输出 =====
        overall = combine(
            main_pipe, butterfly, deluge_valve, system_run,
            alarm_circuit, control_circuit, test_drain, drain_circuit,
            clamps
        )

        self['主立管'] = main_pipe
        self['信号阀'] = butterfly
        self['雨淋报警阀'] = deluge_valve
        self['试验信号阀'] = test_butterfly
        self['顶部系统管'] = top_run
        self['报警回路'] = alarm_circuit
        self['水力警铃'] = water_gong
        self['压力开关'] = pressure_switch
        self['控制回路'] = control_circuit
        self['压力表'] = pressure_gauge
        self['电磁阀'] = solenoid_valve
        self['试验放水支路'] = test_drain
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
