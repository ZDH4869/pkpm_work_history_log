# -*- coding: utf-8 -*-
"""ZSFC100 干式报警阀组整体装配（04S206 第17、18页）。

本文件按修改后的建模过程编写，所有零件几何全部内联在本文件中，
不做任何跨文件 import，满足 pyp3d 单文件单 Component 的约束。

==================== 一、图纸数据 ====================
部件表（16 个编号）：
  1 消防给水管 DN100          2 信号蝶阀 ZSFD-16Z DN100
  3 自动滴水阀 ZSFC100.2      4 干式报警阀 ZSFC DN100
  5 主排水阀 50Q11f-16 DN50   6 气压表
  7 气路止回阀 20H11T-16 DN20 8 安全阀 15A27H-10K DN15
  9 供气截止阀 20J11W-16 DN20 10 水力警铃 ZSJL
  11 水压表                   12 压力开关 YL1.2
  13 管卡 ×2                  14 冷凝水排水阀 20Q11f-16 DN20
  15 注水口管堵 DN20          16 排水管 DN50

安装尺寸表 ZSFC100：
  A=445 B=245 C=423 D=173 E=335 F=260 G=200 H=360 I=215
  DN100 法兰：外径 φ215、螺栓孔中心圆 φ180、8×φ18
  另有 978（地面至信号蝶阀下法兰底面）、500（主流道上管卡距地高度）

==================== 二、坐标系与定位基准链 ====================
单位 mm；+Z 向上（主流道方向）；-Y 指向正视图观察者（阀组正面），
+Y 指向墙；X 为正视图左右方向，供气回路沿 -X 展开。
局部原点（定位点）= 主流道管道与地面接触面的圆心。

竖向链（Z，自地面起算）：
  0                       室内地面（定位点）
  978                     信号蝶阀下法兰底面
  978 + 信号蝶阀阀体长度   干式报警阀下端（底部主流道管段起点）
  978 + A + 信号蝶阀阀体长度  干式报警阀上法兰顶面
  978 + A + B             组件顶（水力警铃顶面 = 顶部出口短管顶）
  500                     管卡(13)中心标高

正视方向链（X，以主立管/报警阀轴线为 0）：
  -C = -423   左侧最外缘（水力警铃侧）
  +D = +173   右侧最外缘（报警阀阀体外轮廓）
  -E = -335   排水管(16)轴线

进深方向链（Y，以墙面为 0、向外为负；模型内以主立管轴线为 Y=0）：
  墙面      Y = +(G+H) = +560
  靠墙立管  Y = +H     = +360   （冷凝水排水阀/注水口支管）
  报警回路平面 Y = +F  = +260   （水力警铃/压力开关）
  报警阀正面最前端 Y = -I = -215
  排水管(16)  Y = 0（与主立管同一竖直平面，见 `排水管进深偏移`）

==================== 三、装配拓扑 ====================
主通路   ：主立管(1) → 信号蝶阀(2) → 干式报警阀(4) → 顶部出口短管
供气回路 ：报警阀左上 DN20 接口 → 止回阀(7) → 安全阀(8) → 供气截止阀(9)
           → 接供气管路；中途向下引气压表(6)，向前引"接加速器"接口
报警回路 ：报警阀左侧 DN15 报警接口 → 水平向左延伸 → 水平后移(+Y)
	       → 圆弧向下转弯(-Z) → 接入下部水平排水管
	         警铃水平管左接水力警铃(10)、右接压力开关(12)
冷凝水/注水：报警接口后移水平段设置两个独立安装点
           → 靠阀体侧单独上引注水口管堵(15)，靠弯头侧串接冷凝水排水阀(14)
水压表回路：干式报警阀排水口与主排水阀之间的 DN50 管段上设三通
	       → DN20 支管直接与 DN50 主管相贯，水平后移(+Y) 至警铃平面
	         → 水压表(11)安装在后移水平段上，其立柱后方串接一只排水阀
	         → 排水阀把手朝 +Z，管道随后圆弧上弯接入警铃水平管
           → 立管下端经 X/Y 转折汇入排水管(16)
           → 立管下端与横管为相贯三通，反向水平支管转向上接自动滴水阀(3)
排水回路 ：报警阀底部红色主流道颈段 DN50 接口 → 短管 → 主排水阀(5)
           → 沿 -X 水平延伸至 X=-E → 圆弧弯头直接竖直向下 → 排水管(16)
           → 出口高于地面自由排放（与主立管同一竖直平面，不作进深转折）
后侧水平支管：底部管段向 +Y 水平引出
           → 末端侧接自动滴水阀（删除原靠墙立管、管堵和冷凝水排水阀）
支吊架   ：Z=500 处 2 个管卡(13)，分别抱主立管与排水管，背部支架锚固于墙
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
    外径管减内径管得到空心管道，端面为环形。
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


def _三通X向Z(center, main_od, main_id, branch_od, branch_id, branch_length):
    """主管沿 X、支管沿 +Z 的三通。

    center        三通中心（位于主管轴线上）
    branch_length 支管自主管轴线起的伸出长度

    构造：主管上的加厚鞍座 + 向上支管 + 端部承口，最后减去主管流道与
    支管流道，使支管内腔与主管内腔连通。
    """
    cx, cy, cz = center
    saddle_half = branch_od * 0.85
    saddle = Cone(
        Vec3(cx - saddle_half, cy, cz), Vec3(cx + saddle_half, cy, cz),
        main_od * 0.70, main_od * 0.70
    )
    branch = Cone(
        Vec3(cx, cy, cz), Vec3(cx, cy, cz + branch_length),
        branch_od / 2.0, branch_od / 2.0
    )
    collar = Cone(
        Vec3(cx, cy, cz + branch_length - 12.0),
        Vec3(cx, cy, cz + branch_length),
        branch_od * 0.70, branch_od * 0.70
    )
    body = combine(saddle, branch, collar)
    body = body - Cone(
        Vec3(cx - saddle_half - 2.0, cy, cz),
        Vec3(cx + saddle_half + 2.0, cy, cz),
        main_id / 2.0, main_id / 2.0
    )
    body = body - Cone(
        Vec3(cx, cy, cz), Vec3(cx, cy, cz + branch_length + 1.0),
        branch_id / 2.0, branch_id / 2.0
    )
    return body


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
# 编号2：信号蝶阀 ZSFD-16Z（内联）
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
# 编号4：干式报警阀 ZSFC DN100（内联，底部按正视图改造）
# ============================================================
def _干式报警阀(total_height=445.0, dn=100.0, flange_bore_diameter=114.0,
              bottom_pipe_height=70.0, bottom_pipe_od=114.0,
              fill_port_z=50.0, fill_port_dn=20.0,
              fill_port_od=25.0, fill_port_length=45.0,
              gas_port_z=295.0, gas_port_dn=20.0,
              gas_port_od=34.0, gas_port_length=42.0,
              alarm_port_z=230.0, alarm_port_dn=15.0,
              alarm_port_od=30.0, alarm_port_length=36.0,
              drain_port_z=40.0, drain_port_dn=53.0,
              drain_port_od=60.0, drain_port_length=60.0):
    """ZSFC 系列干式报警阀单体。

    坐标约定：
    - 主流道沿 +Z；检修盖位于 -Y 正前方；左侧控制接口沿 -X；
    - 局部原点 = 底部主流道管段的底面中心（即与信号蝶阀上法兰的贴合面）；
    - 阀体总高 = total_height（安装尺寸 A）。

    与图纸正视图一致的底部构造：
    顶面为 04S206 标准 DN100 法兰；底部不是简单法兰，而是一段 DN100
    主流道管段（高 bottom_pipe_height），由该管段沿 +Y 引出 DN20
    注水/冷凝水管口（接靠墙立管）。

    左侧自上而下三个控制接口（腔室不同，不可合并）：
      - gas_port    DN20 供气接口（阀瓣以上气室）
      - alarm_port  DN15 报警信号接口（阀瓣中腔）
      - drain_port  DN50 主排水接口（供水侧腔室，接主排水阀）
    """
    # 总体尺寸
    body_rx = 264.0 / 2.0       # 阀体最大宽度 / 2
    body_ry = 196.0 / 2.0       # 阀体最大深度 / 2
    neck_radius = 124.0 / 2.0   # 上颈外径 / 2

    # DN100 法兰（04S206）
    flange_outer_radius = 215.0 / 2.0
    flange_thickness = 24.0
    bolt_circle_radius = 180.0 / 2.0
    bolt_hole_radius = 18.0 / 2.0
    flange_bolt_count = 8
    flange_bore_radius = flange_bore_diameter / 2.0
    # 顶部短管外径与法兰中心孔共用 flange_bore_diameter。
    # 密封面只在管外露出 2 mm，避免原 φ158 环面造成管径明显偏小的视觉错觉。
    seal_outer_radius = flange_bore_radius + 2.0
    seal_height = 2.0

    # 前部梨形检修盖
    cover_width = 270.0
    cover_height = 190.0
    cover_thickness = 18.0
    cover_center_z = bottom_pipe_height + 90.0
    cover_bolt_count = 6
    cover_bolt_width = 15.0

    # 标牌
    nameplate_width = 52.0
    nameplate_height = 24.0

    # 关键高度：铸造阀体自底部管段顶面起算
    body_bottom = bottom_pipe_height
    upper_flange_bottom = total_height - flange_thickness
    upper_flange_top = total_height
    neck_bottom = upper_flange_bottom - 42.0
    bottom_pipe_radius = bottom_pipe_od / 2.0

    def ellipse_section_z(z_position, radius_x, radius_y):
        return translate(0, 0, z_position) * \
               Section(scale(radius_x, radius_y, 1.0) * Arc(2.0 * math.pi))

    def circle_section_z(z_position, radius):
        return ellipse_section_z(z_position, radius, radius)

    def hex_section_y(y_position, center_x, center_z, across_flats):
        circumradius = across_flats / math.sqrt(3.0)
        points = []
        for index in range(6):
            angle = math.pi / 6.0 + index * math.pi / 3.0
            points.append(Vec3(
                center_x + circumradius * math.cos(angle),
                y_position,
                center_z + circumradius * math.sin(angle)
            ))
        points.append(points[0])
        return Section(Line(*points))

    def hex_prism_y(y_start, y_end, center_x, center_z, across_flats):
        result = Loft(
            hex_section_y(y_start, center_x, center_z, across_flats),
            hex_section_y(y_end, center_x, center_z, across_flats)
        )
        result.smooth = False
        return result

    def pear_section_y(y_position, width, height, center_z):
        """正视图中上窄下宽、周边圆顺的梨形盖板截面。"""
        z_bottom = center_z - height / 2.0
        levels = [
            (0.00, 0.28), (0.03, 0.35), (0.08, 0.41),
            (0.17, 0.46), (0.30, 0.49), (0.46, 0.50),
            (0.62, 0.47), (0.77, 0.42), (0.90, 0.34),
            (0.97, 0.29), (1.00, 0.27)
        ]
        left_points = [
            Vec3(-width * half_ratio, y_position,
                 z_bottom + height * height_ratio)
            for height_ratio, half_ratio in levels
        ]
        right_points = [
            Vec3(width * half_ratio, y_position,
                 z_bottom + height * height_ratio)
            for height_ratio, half_ratio in reversed(levels)
        ]
        points = left_points + right_points
        points.append(points[0])
        return Section(Line(*points))

    def pear_plate_y(width, height, y_start, y_end, center_z):
        result = Loft(
            pear_section_y(y_start, width, height, center_z),
            pear_section_y(y_end, width, height, center_z)
        )
        result.smooth = False
        return result

    # ---------- 1. 顶部 DN100 法兰（04S206 标准） ----------
    def make_top_flange():
        z_low = upper_flange_bottom
        z_high = upper_flange_top
        flange = Cone(
            Vec3(0, 0, z_low), Vec3(0, 0, z_high),
            flange_outer_radius, flange_outer_radius
        )
        center_bore = Cone(
            Vec3(0, 0, z_low - 1.0), Vec3(0, 0, z_high + 1.0),
            flange_bore_radius, flange_bore_radius
        )
        flange = flange - center_bore
        for index in range(flange_bolt_count):
            angle = 2.0 * math.pi * index / flange_bolt_count
            x_position = bolt_circle_radius * math.cos(angle)
            y_position = bolt_circle_radius * math.sin(angle)
            flange = flange - Cone(
                Vec3(x_position, y_position, z_low - 1.0),
                Vec3(x_position, y_position, z_high + 1.0),
                bolt_hole_radius, bolt_hole_radius
            )
        seal = Cone(
            Vec3(0, 0, z_high), Vec3(0, 0, z_high + seal_height),
            seal_outer_radius, seal_outer_radius
        ) - Cone(
            Vec3(0, 0, z_high - 1.0), Vec3(0, 0, z_high + seal_height + 1.0),
            flange_bore_radius, flange_bore_radius
        )
        return combine(flange, seal)

    upper_flange = make_top_flange()

    # ---------- 2. 底部主流道管段（替代下法兰） ----------
    main_bore = Cone(
        Vec3(0, 0, -2.0), Vec3(0, 0, upper_flange_top + 2.0),
        dn / 2.0, dn / 2.0
    )
    bottom_pipe = Cone(
        Vec3(0, 0, 0.0), Vec3(0, 0, body_bottom + 6.0),
        bottom_pipe_radius, bottom_pipe_radius
    ) - main_bore
    # 底部管段与铸造阀体之间的过渡圆台
    bottom_collar = Cone(
        Vec3(0, 0, body_bottom - 10.0), Vec3(0, 0, body_bottom + 8.0),
        bottom_pipe_radius * 1.16, bottom_pipe_radius * 1.16
    ) - main_bore

    # ---------- 3. 底部三个管口 ----------
    def make_bottom_port(direction, center_z, nominal, outside, length):
        """direction: Vec3 单位方向（-X / -Y / +Y）。"""
        outer_radius = outside / 2.0
        inner_radius = nominal / 2.0
        start = Vec3(
            direction.x * (bottom_pipe_radius - 6.0),
            direction.y * (bottom_pipe_radius - 6.0),
            center_z
        )
        end = Vec3(
            direction.x * (bottom_pipe_radius + length),
            direction.y * (bottom_pipe_radius + length),
            center_z
        )
        tube = Cone(start, end, outer_radius, outer_radius) - \
               Cone(
                   Vec3(direction.x * (bottom_pipe_radius - 8.0),
                        direction.y * (bottom_pipe_radius - 8.0), center_z),
                   Vec3(direction.x * (bottom_pipe_radius + length + 1.0),
                        direction.y * (bottom_pipe_radius + length + 1.0),
                        center_z),
                   inner_radius, inner_radius
               )
        collar_start = Vec3(
            direction.x * (bottom_pipe_radius + length - 14.0),
            direction.y * (bottom_pipe_radius + length - 14.0),
            center_z
        )
        collar = Cone(collar_start, end, outer_radius * 1.24, outer_radius * 1.24) - \
                 Cone(
                     Vec3(direction.x * (bottom_pipe_radius + length - 16.0),
                          direction.y * (bottom_pipe_radius + length - 16.0),
                          center_z),
                     Vec3(direction.x * (bottom_pipe_radius + length + 1.0),
                          direction.y * (bottom_pipe_radius + length + 1.0),
                          center_z),
                     inner_radius, inner_radius
                 )
        return combine(tube, collar)

    bottom_ports = make_bottom_port(
        Vec3(0, 1, 0), fill_port_z,
        fill_port_dn, fill_port_od, fill_port_length
    )

    # ---------- 4. 上窄下宽的铸造阀体 ----------
    body_sections = [
        ellipse_section_z(body_bottom - 0.5, body_rx * 0.74, body_ry * 0.72),
        ellipse_section_z(body_bottom + 42.0, body_rx * 0.94, body_ry * 0.96),
        ellipse_section_z(body_bottom + 118.0, body_rx, body_ry),
        ellipse_section_z(body_bottom + 220.0, body_rx * 0.83, body_ry * 0.86),
        ellipse_section_z(neck_bottom - 42.0, body_rx * 0.60, body_ry * 0.64),
        circle_section_z(neck_bottom + 0.5, neck_radius)
    ]
    body_blank = Loft(*body_sections)
    body_blank.smooth = True
    body = body_blank - main_bore

    upper_neck = Cone(
        Vec3(0, 0, neck_bottom - 0.5),
        Vec3(0, 0, upper_flange_bottom + 0.5),
        neck_radius, neck_radius
    ) - main_bore

    # ---------- 5. 前部梨形检修盖 ----------
    cover_back_y = -body_ry + 5.0
    cover_front_y = cover_back_y - cover_thickness

    cover_seat = pear_plate_y(
        cover_width + 10.0, cover_height + 10.0,
        cover_back_y + 2.0, cover_front_y + 4.0, cover_center_z
    )
    cover_plate = pear_plate_y(
        cover_width, cover_height,
        cover_front_y + 3.0, cover_front_y, cover_center_z
    )

    cover_bolts = []
    washer_radius = cover_bolt_width * 0.60
    bolt_positions = [
        (-cover_width * 0.24, cover_center_z + cover_height * 0.27),
        (cover_width * 0.24, cover_center_z + cover_height * 0.27),
        (-cover_width * 0.43, cover_center_z - cover_height * 0.02),
        (cover_width * 0.43, cover_center_z - cover_height * 0.02),
        (-cover_width * 0.27, cover_center_z - cover_height * 0.34),
        (cover_width * 0.27, cover_center_z - cover_height * 0.34)
    ][:cover_bolt_count]
    for bolt_x, bolt_z in bolt_positions:
        washer = Cone(
            Vec3(bolt_x, cover_front_y, bolt_z),
            Vec3(bolt_x, cover_front_y - 2.2, bolt_z),
            washer_radius, washer_radius
        )
        head = hex_prism_y(
            cover_front_y - 2.0, cover_front_y - 8.0,
            bolt_x, bolt_z, cover_bolt_width
        )
        cover_bolts.extend([washer, head])
    bolt_set = combine(*cover_bolts)

    # ---------- 6. 左侧三个控制接口凸台 ----------
    def make_left_port(center_z, nominal_diameter,
                       outside_diameter, length, body_x):
        """左侧控制接口凸台。

        外管从主流道壁面起算、穿过铸造阀体壁后再伸出 length，因此无论阀体
        在该标高的实际半宽是多少，管口都与阀体完全相连、不会脱空；
        伸入主流道的部分由主流道圆柱切除，不侵占过流断面。
        """
        outer_radius = outside_diameter / 2.0
        inside_radius = nominal_diameter / 2.0
        x_outer = body_x - length
        tube = Cone(
            Vec3(0, 0, center_z), Vec3(x_outer, 0, center_z),
            outer_radius, outer_radius
        ) - main_bore
        tube = tube - Cone(
            Vec3(0, 0, center_z), Vec3(x_outer - 1.0, 0, center_z),
            inside_radius, inside_radius
        )
        collar = Cone(
            Vec3(x_outer + 9.0, 0, center_z), Vec3(x_outer - 3.0, 0, center_z),
            outer_radius * 1.30, outer_radius * 1.30
        ) - Cone(
            Vec3(x_outer + 10.0, 0, center_z), Vec3(x_outer - 4.0, 0, center_z),
            inside_radius, inside_radius
        )
        return combine(tube, collar)

    gas_port = make_left_port(
        gas_port_z, gas_port_dn, gas_port_od,
        gas_port_length, -body_rx * _报警阀_供气口系数
    )
    alarm_port = make_left_port(
        alarm_port_z, alarm_port_dn, alarm_port_od,
        alarm_port_length, -body_rx * _报警阀_报警口系数
    )
    # 主排水口下移到底部红色主流道颈段时，根部应以该颈管外圆为基准，
    # 不能继续使用上方铸造阀体的最大半宽，否则接口凸台会与颈管脱开。
    drain_root_x = (
        -bottom_pipe_radius
        if drain_port_z <= body_bottom
        else -body_rx * _报警阀_排水口系数
    )
    drain_port = make_left_port(
        drain_port_z, drain_port_dn, drain_port_od,
        drain_port_length, drain_root_x
    )
    side_ports = combine(gas_port, alarm_port, drain_port)

    # ---------- 7. 正面铭牌 ----------
    front_nameplate = translate(
        -nameplate_width / 2.0, cover_front_y - 1.4,
        cover_center_z - nameplate_height / 2.0
    ) * scale(nameplate_width, 1.4, nameplate_height) * Cube()

    # ---------- 8. 配色与输出 ----------
    colored_body = combine(body, upper_neck).color(*_色_阀体红)
    colored_bottom = combine(bottom_pipe, bottom_collar).color(*_色_阀体红)
    colored_ports_bottom = bottom_ports.color(*_色_阀体红)
    colored_upper_flange = upper_flange.color(*_色_阀体红)
    colored_cover_seat = cover_seat.color(*_色_阀体红暗)
    colored_cover = cover_plate.color(*_色_阀体红亮)
    colored_bolts = bolt_set.color(*_色_钢)
    colored_ports = side_ports.color(*_色_阀体红)
    colored_labels = front_nameplate.color(*_色_标牌黄)

    return combine(
        colored_body,
        colored_bottom,
        colored_ports_bottom,
        colored_upper_flange,
        colored_cover_seat,
        colored_cover,
        colored_bolts,
        colored_ports,
        colored_labels
    )


# ==== 干式报警阀的关键接口坐标（供装配计算，与上面几何保持一致） ====
# 三个系数是各接口根部所在的阀体名义半宽比例，越靠下阀体越宽、系数越大。
_报警阀_供气口系数 = 0.82
_报警阀_报警口系数 = 0.93
_报警阀_排水口系数 = 0.99

_报警阀_阀体最大宽度 = 264.0
_报警阀_底部管外径 = 114.0
_报警阀_半宽 = _报警阀_阀体最大宽度 / 2.0

# 供气接口（DN20，接供气回路）
_报警阀_供气口Z = 295.0
_报警阀_供气口端X = -(_报警阀_半宽 * _报警阀_供气口系数) - 42.0     # -150.24
# 报警信号接口（DN15，接水力警铃/压力开关）
_报警阀_报警口Z = 230.0
_报警阀_报警口端X = -(_报警阀_半宽 * _报警阀_报警口系数) - 36.0     # -158.76
# 主排水接口（DN50，由底部红色主流道颈段引出）
_报警阀_排水口Z = 40.0
_报警阀_排水口端X = -(_报警阀_底部管外径 / 2.0) - 60.0              # -117.0


# ============================================================
# 编号7：气路止回阀 20H11T-16 DN20（内联）
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

    # ---------- 1. 鼓形黄铜阀体 ----------
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

    # ---------- 2. 两端六角内螺纹接头 ----------
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

    # ---------- 3. 顶部阀盖 ----------
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

    # ---------- 4. 端口内螺纹可视化 ----------
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
# 编号8：安全阀 15A27H-10K DN15（内联）
# ============================================================
def _安全阀(dn=15.0, total_height=135.0,
           lower_body_diameter=43.0, outlet_diameter=25.0,
           outlet_z=28.0, outlet_length=40.0,
           frame_width=30.0, frame_start_z=39.0, frame_height=66.0,
           frame_post_diameter=4.5, bridge_height=7.0,
           adjust_width=19.0, adjust_height=8.0,
           top_stem_diameter=8.0, top_stem_height=22.0,
           top_cap_diameter=11.0, top_cap_height=5.0,
           top_bar_length=42.0, top_bar_diameter=4.5):
    """DN15 弹簧微启式安全阀。

    左右贯通流道沿 X，顶部中心阀杆沿 +Z，局部原点位于阀体底部平面，
    出口中心位于 +Z = outlet_z 高度。
    """
    lower_body_radius = lower_body_diameter / 2.0
    outlet_radius = outlet_diameter / 2.0
    frame_post_radius = frame_post_diameter / 2.0
    top_stem_radius = top_stem_diameter / 2.0
    top_cap_radius = top_cap_diameter / 2.0
    top_bar_radius = top_bar_diameter / 2.0
    frame_top_z = frame_start_z + frame_height

    # ---------- 1. 左右贯通式横向阀体 ----------
    barrel_radius = lower_body_radius * 0.80
    barrel_half_length = lower_body_radius * 0.98
    barrel_blank = Cone(
        Vec3(-barrel_half_length, 0, outlet_z),
        Vec3(barrel_half_length, 0, outlet_z),
        barrel_radius, barrel_radius
    )
    horizontal_flow = Cone(
        Vec3(-outlet_length - 1.0, 0, outlet_z),
        Vec3(outlet_length + 1.0, 0, outlet_z),
        dn / 2.0, dn / 2.0
    )
    barrel = barrel_blank - horizontal_flow
    upper_neck = Cone(
        Vec3(0, 0, outlet_z + barrel_radius * 0.35),
        Vec3(0, 0, frame_start_z + 2.0),
        lower_body_radius * 0.62, lower_body_radius * 0.62
    )
    lower_body = combine(barrel, upper_neck)

    # ---------- 2. 左右贯通接口（光面圆管口，不带六角） ----------
    def make_side_port(direction):
        body_edge_x = direction * barrel_half_length
        side_bore = Cone(
            Vec3(direction * (barrel_half_length - 3.0), 0, outlet_z),
            Vec3(direction * (outlet_length + 1.0), 0, outlet_z),
            dn / 2.0, dn / 2.0
        )
        round_port = Cone(
            Vec3(direction * (barrel_half_length - 2.0), 0, outlet_z),
            Vec3(direction * outlet_length, 0, outlet_z),
            outlet_radius, outlet_radius
        ) - side_bore
        root = Cone(
            Vec3(body_edge_x - direction * 4.0, 0, outlet_z),
            Vec3(body_edge_x + direction * 5.0, 0, outlet_z),
            outlet_radius * 1.22, outlet_radius * 1.05
        ) - side_bore
        return combine(root, round_port)

    outlet_set = combine(make_side_port(-1.0), make_side_port(1.0))

    # ---------- 3. 顶部双立柱支架 ----------
    frame_base = Cone(
        Vec3(0, 0, frame_start_z - 2.0), Vec3(0, 0, frame_start_z + 6.0),
        frame_width * 0.52, frame_width * 0.52
    )
    post_offset_x = frame_width / 2.0 - frame_post_radius
    post_bottom_z = frame_start_z + 4.0
    post_top_z = frame_top_z - bridge_height + 1.0
    left_post = Cone(
        Vec3(-post_offset_x, 0, post_bottom_z),
        Vec3(-post_offset_x, 0, post_top_z),
        frame_post_radius, frame_post_radius
    )
    right_post = Cone(
        Vec3(post_offset_x, 0, post_bottom_z),
        Vec3(post_offset_x, 0, post_top_z),
        frame_post_radius, frame_post_radius
    )
    top_bridge = translate(
        -frame_width / 2.0, -frame_post_radius, frame_top_z - bridge_height
    ) * scale(frame_width, frame_post_radius * 2.0, bridge_height) * Cube()
    top_frame = combine(frame_base, left_post, right_post, top_bridge)

    # ---------- 4. 顶部调整帽、中心阀杆与 T 形横杆 ----------
    adjust_start_z = frame_top_z - 1.0
    adjust_end_z = adjust_start_z + adjust_height
    adjust_nut = _六角柱Z(adjust_start_z, adjust_end_z, adjust_width)
    stem_end_z = min(
        adjust_end_z + top_stem_height, total_height - top_cap_height + 0.5
    )
    center_stem = Cone(
        Vec3(0, 0, adjust_end_z - 0.5), Vec3(0, 0, stem_end_z),
        top_stem_radius, top_stem_radius
    )
    stem_collar = Cone(
        Vec3(0, 0, adjust_end_z - 1.0), Vec3(0, 0, adjust_end_z + 3.0),
        top_stem_radius * 1.45, top_stem_radius * 1.45
    )
    top_cap = Cone(
        Vec3(0, 0, total_height - top_cap_height), Vec3(0, 0, total_height),
        top_cap_radius, top_cap_radius
    )
    top_bar_z = total_height - top_bar_radius
    top_bar = Cone(
        Vec3(-top_bar_length / 2.0, 0, top_bar_z),
        Vec3(top_bar_length / 2.0, 0, top_bar_z),
        top_bar_radius, top_bar_radius
    )
    top_stem_set = combine(center_stem, stem_collar, top_cap, top_bar)

    return combine(
        lower_body.color(*_色_铸铁),
        outlet_set.color(*_色_铸铁),
        top_frame.color(*_色_铸铁亮),
        adjust_nut.color(*_色_钢),
        top_stem_set.color(*_色_钢)
    )


# ============================================================
# 编号9：供气截止阀 20J11W-16 DN20（内联）
# ============================================================
def _供气截止阀(dn=20.0, total_length=56.0,
              hex_width=30.0, connector_length=12.0,
              thread_depth=10.0, body_length=38.0,
              body_diameter=38.0, body_end_diameter=27.0,
              bonnet_diameter=29.0, bonnet_start_z=8.0,
              bonnet_height=27.0, gland_width=19.0,
              gland_height=7.0, stem_diameter=6.0,
              wheel_center_z=47.0, wheel_diameter=53.0,
              wheel_rim_width=4.5, wheel_thickness=4.0,
              wheel_spoke_width=3.5, wheel_hub_diameter=12.0):
    """DN20 内螺纹供气截止阀。主流道沿 X，阀杆与手轮轴线沿 +Z。"""
    half_total = total_length / 2.0
    connector_length = min(connector_length, half_total - 3.0)
    thread_depth = min(thread_depth, connector_length - 1.0)
    body_length = min(body_length, total_length - 2.0 * connector_length + 4.0)
    half_body = body_length / 2.0
    body_radius = body_diameter / 2.0
    body_end_radius = body_end_diameter / 2.0
    bonnet_radius = bonnet_diameter / 2.0
    bonnet_top_z = bonnet_start_z + bonnet_height
    stem_radius = stem_diameter / 2.0
    wheel_radius = wheel_diameter / 2.0
    wheel_hub_radius = wheel_hub_diameter / 2.0

    # ---------- 1. 鼓形截止阀阀体 ----------
    body_blank = Loft(
        _圆截面X(-half_body, body_end_radius),
        _圆截面X(-half_body * 0.62, body_radius * 0.91),
        _圆截面X(0.0, body_radius),
        _圆截面X(half_body * 0.62, body_radius * 0.91),
        _圆截面X(half_body, body_end_radius)
    )
    body_blank.smooth = True
    main_bore = Cone(
        Vec3(-half_total - 1.0, 0, 0), Vec3(half_total + 1.0, 0, 0),
        dn / 2.0, dn / 2.0
    )
    body = body_blank - main_bore
    lower_chamber = translate(0, 0, -body_radius * 0.38) * scale(
        body_radius * 0.72, body_radius * 0.72, body_radius * 0.62
    ) * Sphere()

    # ---------- 2. 两端内螺纹六角接口 ----------
    left_hex = _六角柱X(-half_total, -half_body + 0.4, hex_width) - main_bore
    right_hex = _六角柱X(half_body - 0.4, half_total, hex_width) - main_bore
    connectors = combine(left_hex, right_hex)

    thread_parts = []
    thread_count = 4
    thread_pitch = max((thread_depth - 2.5) / thread_count, 1.0)
    for index in range(thread_count):
        offset = 1.6 + index * thread_pitch
        for direction in (-1.0, 1.0):
            x_position = direction * (half_total - offset)
            outer = Cone(
                Vec3(x_position - 0.3, 0, 0), Vec3(x_position + 0.3, 0, 0),
                dn / 2.0 + 0.45, dn / 2.0 + 0.45
            )
            inner = Cone(
                Vec3(x_position - 0.6, 0, 0), Vec3(x_position + 0.6, 0, 0),
                dn / 2.0 - 0.35, dn / 2.0 - 0.35
            )
            thread_parts.append(outer - inner)
    internal_threads = combine(*thread_parts)

    # ---------- 3. 阀盖和填料压盖 ----------
    bonnet = Loft(
        _圆截面Z(bonnet_start_z, bonnet_radius * 0.65),
        _圆截面Z(bonnet_start_z + 8.0, bonnet_radius),
        _圆截面Z(bonnet_top_z - 6.0, bonnet_radius * 0.76),
        _圆截面Z(bonnet_top_z, bonnet_radius * 0.62)
    )
    bonnet.smooth = True
    gland = _六角柱Z(bonnet_top_z - 1.0, bonnet_top_z + gland_height, gland_width)

    # ---------- 4. 中央升降阀杆 ----------
    stem = Cone(
        Vec3(0, 0, bonnet_top_z + gland_height - 0.5),
        Vec3(0, 0, wheel_center_z + wheel_thickness / 2.0 + 1.5),
        stem_radius, stem_radius
    )
    stem_nut = _六角柱Z(
        wheel_center_z + wheel_thickness / 2.0,
        wheel_center_z + wheel_thickness / 2.0 + 4.0, 11.0
    )
    stem_set = combine(stem, stem_nut)

    # ---------- 5. 顶部圆形手轮 ----------
    wheel_z0 = wheel_center_z - wheel_thickness / 2.0
    wheel_z1 = wheel_center_z + wheel_thickness / 2.0
    wheel_ring = Cone(
        Vec3(0, 0, wheel_z0), Vec3(0, 0, wheel_z1), wheel_radius, wheel_radius
    ) - Cone(
        Vec3(0, 0, wheel_z0 - 0.5), Vec3(0, 0, wheel_z1 + 0.5),
        wheel_radius - wheel_rim_width, wheel_radius - wheel_rim_width
    )
    spoke_x = translate(
        -wheel_radius + wheel_rim_width, -wheel_spoke_width / 2.0, wheel_z0
    ) * scale(
        2.0 * (wheel_radius - wheel_rim_width), wheel_spoke_width, wheel_thickness
    ) * Cube()
    spoke_y = translate(
        -wheel_spoke_width / 2.0, -wheel_radius + wheel_rim_width, wheel_z0
    ) * scale(
        wheel_spoke_width, 2.0 * (wheel_radius - wheel_rim_width), wheel_thickness
    ) * Cube()
    wheel_hub = Cone(
        Vec3(0, 0, wheel_z0 - 0.5), Vec3(0, 0, wheel_z1 + 0.5),
        wheel_hub_radius, wheel_hub_radius
    )
    handwheel = combine(wheel_ring, spoke_x, spoke_y, wheel_hub)

    return combine(
        combine(body, lower_chamber).color(*_色_黄铜),
        connectors.color(*_色_黄铜),
        internal_threads.color(*_色_黄铜暗),
        combine(bonnet, gland).color(*_色_黄铜亮),
        stem_set.color(*_色_钢),
        handwheel.color(0.72, 0.025, 0.018, 1.0)
    )


# ============================================================
# 编号6/11：弹簧管压力表
# ============================================================
def _压力表(dial_diameter=105.0, rod_height=90.0, rod_diameter=15.0):
    """弹簧管压力表（编号6 气压表 / 编号11 水压表共用）。

    连系杆底端位于局部原点，表盘位于 +Z 上方、盘面法线沿 Y 轴。
    表壳背板在 +Y 侧，开口面与指针在 -Y 侧——装配时不作任何旋转，
    读数面即朝向正前方。不含小手轮。
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

    # 表壳：背板在 +Y（朝墙），开口面朝 -Y（朝正前方）
    dial_z = HG + HP + HT * 2 + HP + HG + R
    y_back = SY / 2.0          # 表壳背面
    y_face = y_back - SQ       # 背板内表面，即刻度盘所在平面

    表壳 = Cone(Vec3(0, -y_back, dial_z), Vec3(0, y_back, dial_z), R, R) - \
           Cone(Vec3(0, -y_back, dial_z), Vec3(0, y_face, dial_z), R - S, R - S)
    刻度盘 = Cone(
        Vec3(0, y_face - 0.8, dial_z), Vec3(0, y_face, dial_z), R - S, R - S
    )

    # 指针贴在刻度盘前方、朝 -Y 扫出厚度，从开口面可见
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
# 编号5：主排水阀 50Q11f-16 DN50（内联）
# ============================================================
def _主排水阀(dn=50.0, total_length=106.0, hex_width=62.0,
            connector_length=22.0, thread_depth=19.0,
            body_length=68.0, body_diameter=76.0, body_end_diameter=62.0,
            gland_diameter=31.0, gland_height=14.0,
            stem_diameter=10.0, stem_height=22.0,
            nut_width=17.0, nut_height=7.0,
            handle_length=155.0, handle_width=18.0, handle_thickness=4.0,
            handle_back=20.0, handle_angle_deg=0.0):
    """DN50 内螺纹主排水球阀。主流道沿 +X，阀杆沿 +Z，阀体中心为局部原点。

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

    # ---------- 1. 鼓形黄铜阀体 ----------
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

    # ---------- 2. 两端六角内螺纹接头 ----------
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

    # ---------- 3. 顶部压盖、阀杆和螺母 ----------
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

    # ---------- 4. 红色平直手柄 ----------
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
# 编号3：自动滴水阀 ZSFC100.2（内联）
# ============================================================
def _自动滴水阀(bore_diameter=11.5, socket_depth=17.0,
              hex_width=32.0, hex_height=25.0,
              shoulder_height=3, body_diameter=28.0,
              body_height=30.0, top_thickness=1.2,
              hole_diameter=7.0, hole_center_z=43.0, hole_depth=9.0,
              stem_diameter=6.5, stem_height=5.5, stem_base_diameter=8.5,
              pin_diameter=1.0, pin_left=17.0, pin_right=19.0,
              pin_split_rise=4.5, lock_cap_diameter=4.5,
              show_hole_shadow=True):
    """自动滴水阀 ZSFC100.2。

    底部接口中心为局部原点，阀体轴线沿 +Z，侧面滴水孔朝 +X。
    """
    bore_radius = max(bore_diameter / 2.0, 1.0)
    socket_depth = min(socket_depth, hex_height - 1.0)
    body_radius = body_diameter / 2.0
    hole_radius = hole_diameter / 2.0
    hole_depth = min(max(hole_depth, 1.0), body_radius + 0.5)
    stem_radius = stem_diameter / 2.0
    stem_base_radius = stem_base_diameter / 2.0
    pin_radius = pin_diameter / 2.0
    lock_cap_radius = lock_cap_diameter / 2.0

    z_hex_top = hex_height
    z_shoulder_top = z_hex_top + shoulder_height
    z_body_top = z_shoulder_top + body_height
    z_top = z_body_top + top_thickness
    z_stem_top = z_top + stem_height
    hole_z = max(
        z_shoulder_top + hole_radius + 1.0,
        min(hole_center_z, z_body_top - hole_radius - 1.0)
    )

    # ---------- 1. 下部六角本体 ----------
    lower_hex = _六角柱Z(0.0, z_hex_top + 0.25, hex_width) - Cone(
        Vec3(0, 0, -0.5), Vec3(0, 0, socket_depth), bore_radius
    )

    # ---------- 2. 六角到圆柱的短斜肩 ----------
    shoulder = Loft(
        _六角截面Z(z_hex_top - 0.25, hex_width * 0.995),
        _圆截面Z(z_shoulder_top + 0.20, body_radius)
    )
    shoulder.smooth = False

    # ---------- 3. 上部圆柱阀体与侧面滴水孔 ----------
    upper_body = Cone(
        Vec3(0, 0, z_shoulder_top - 0.25), Vec3(0, 0, z_body_top + 0.15),
        body_radius
    ) - Cone(
        Vec3(body_radius + 0.8, 0, hole_z),
        Vec3(body_radius - hole_depth, 0, hole_z), hole_radius
    )
    hole_shadow = Cone(
        Vec3(body_radius - 0.75, 0, hole_z), Vec3(body_radius - 0.15, 0, hole_z),
        max(hole_radius - 0.55, 0.6)
    )
    top_face = Cone(
        Vec3(0, 0, z_body_top - 0.30), Vec3(0, 0, z_top), body_radius
    )

    # ---------- 4. 顶部短阀杆与开口销 ----------
    stem_base = Cone(
        Vec3(0, 0, z_body_top - 0.10), Vec3(0, 0, z_top + 1.2), stem_base_radius
    )
    stem = Cone(Vec3(0, 0, z_top + 0.65), Vec3(0, 0, z_stem_top), stem_radius)
    pin_z = z_top + stem_height * 0.58
    split_pin = combine(
        Cone(Vec3(-pin_left, 0, pin_z), Vec3(1.0, 0, pin_z), pin_radius),
        Cone(Vec3(0.0, 0, pin_z),
             Vec3(pin_right, 1.6, pin_z + pin_split_rise), pin_radius),
        Cone(Vec3(0.0, 0, pin_z - 0.15),
             Vec3(pin_right * 0.92, -1.8, pin_z + pin_split_rise * 0.25),
             pin_radius)
    )
    lock_cap_x = stem_base_radius + lock_cap_radius * 0.80
    lock_cap = Cone(
        Vec3(lock_cap_x, 0, z_top - 0.05), Vec3(lock_cap_x, 0, z_top + 0.85),
        lock_cap_radius
    )

    valve_parts = [
        lower_hex.color(0.80, 0.60, 0.22, 1.0),
        shoulder.color(0.80, 0.60, 0.22, 1.0),
        upper_body.color(0.80, 0.60, 0.22, 1.0),
        top_face.color(0.92, 0.73, 0.34, 1.0),
        combine(stem_base, stem).color(0.92, 0.73, 0.34, 1.0),
        split_pin.color(*_色_钢),
        lock_cap.color(*_色_钢)
    ]
    if show_hole_shadow:
        valve_parts.insert(
            4, hole_shadow.color(0.08, 0.055, 0.020, 1.0)
        )
    return combine(*valve_parts)


# ============================================================
# 编号14：冷凝水排水阀 20Q11f-16 DN20（内联）
# ============================================================
def _冷凝水排水阀(dn=20.0, total_length=56.0, hex_width=31.0,
               connector_length=12.0, thread_depth=10.0,
               body_length=37.0, body_diameter=40.0, body_end_diameter=27.0,
               gland_diameter=22.0, gland_height=10.0,
               stem_diameter=7.0, stem_height=16.0,
               nut_width=13.0, nut_height=5.0,
               handle_length=91.0, handle_width=13.0, handle_thickness=3.2,
               handle_back=14.0, handle_angle_deg=0.0):
    """DN20 冷凝水排水球阀。主流道沿 +X，阀杆沿 +Z，阀体中心为局部原点。"""
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
# 编号15：注水口管堵 DN20（内联）
# ============================================================
def _注水口管堵(thread_major_diameter=26.4, thread_core_diameter=23.5,
             thread_length=16.0, thread_count=7,
             hex_width=30.0, hex_length=11.0, shoulder_length=3.0,
             washer_diameter=30.0, washer_thickness=1.5):
    """DN20 / G3/4 实心六角管堵。螺纹轴线沿 +X，旋入端面为局部原点。"""
    thread_major_radius = thread_major_diameter / 2.0
    thread_core_radius = min(thread_core_diameter / 2.0, thread_major_radius - 0.2)
    thread_count = max(int(thread_count), 3)
    washer_radius = washer_diameter / 2.0

    thread_core = Cone(
        Vec3(0, 0, 0), Vec3(thread_length, 0, 0),
        thread_core_radius, thread_core_radius
    )
    closed_tip = Cone(
        Vec3(0, 0, 0), Vec3(1.2, 0, 0),
        thread_major_radius * 0.94, thread_core_radius
    )
    thread_teeth = []
    pitch = thread_length / (thread_count + 0.6)
    tooth_width = min(1.0, pitch * 0.48)
    for index in range(thread_count):
        x0 = 1.2 + index * pitch
        x1 = min(x0 + tooth_width, thread_length - 0.3)
        thread_teeth.append(Cone(
            Vec3(x0, 0, 0), Vec3(x1, 0, 0),
            thread_major_radius, thread_major_radius
        ))
    thread_set = combine(thread_core, closed_tip, *thread_teeth)

    shoulder_end = thread_length + shoulder_length
    shoulder = Cone(
        Vec3(thread_length - 0.3, 0, 0), Vec3(shoulder_end, 0, 0),
        thread_major_radius * 1.06, hex_width * 0.50
    )
    washer = Cone(
        Vec3(shoulder_end - washer_thickness, 0, 0), Vec3(shoulder_end, 0, 0),
        washer_radius, washer_radius
    )
    hex_head = _六角柱X(shoulder_end, shoulder_end + hex_length, hex_width)

    return combine(
        thread_set.color(0.43, 0.46, 0.49, 1.0),
        combine(shoulder, hex_head).color(0.67, 0.70, 0.73, 1.0),
        washer.color(0.30, 0.24, 0.15, 1.0)
    )


# ============================================================
# 编号10：水力警铃 ZSJL（新建）
# ============================================================
def _水力警铃():
    """内联自湿式报警阀组的水力警铃，定位点为 DN20 进水口外端面。"""
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

    # 局部排水口沿 +Z；装配时关于 XY 平面翻转，使其在干式阀组中朝下。
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
# 编号12：压力开关 YL1.2（新建）
# ============================================================
def _压力开关(box_width=95.0, box_depth=62.0, box_height=70.0,
            cover_height=9.0):
    """压力开关 YL1.2。

    方形壳体，局部原点位于壳体底面中心。
    按当前装配图取消右侧小圆柱出线口和底部的独立竖直接管。
    """
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
# 编号13：管卡（新建，参数化抱管直径）
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
# ZSFC 系列干式报警阀组 —— 整体装配
# ============================================================
class ZSFC干式报警阀组(Component):
    """ZSFC100 干式报警阀组整体（编号 1~16 全部）。

    定位点 = 主流道管道与地面接触面的圆心。
    切换『型号』时先查 MODEL_DIMS 刷新全部驱动尺寸，再重建几何。
    """

    MODEL_DIMS = {
        'ZSFC100': {
            # ---- 04S206 安装尺寸表 ----
            '尺寸A': 445.0,          # 干式报警阀总高
            '尺寸B': 245.0,          # 报警阀上法兰顶面以上的仪表段高度
            '尺寸C': 423.0,          # 轴线到左侧最外缘（水力警铃侧）
            '尺寸D': 173.0,          # 轴线到右侧最外缘（报警阀阀体）
            '尺寸E': 335.0,          # 排水管轴线到主立管轴线（正视方向）
            '尺寸F': 260.0,          # 主立管轴线到报警回路平面（侧视方向）
            '尺寸G': 200.0,          # 墙面到靠墙立管轴线
            '尺寸H': 360.0,          # 靠墙立管轴线到主立管轴线
            '尺寸I': 215.0,          # 主立管轴线到报警阀正面最前端
            '地面至蝶阀底高度': 978.0,  # 图中 978
            '管卡中心标高': 500.0,      # 图中 500
            # ---- 主通路 ----
            '信号蝶阀结构长度': 155.0,
            '主管公称直径': 100.0, '主管外径': 114.0, '主管壁厚': 7.0,
            '信号蝶阀公称直径': 100.0,
            '干式报警阀公称直径': 100.0,
            '报警阀底部管段高度': 70.0,
            # ---- 供气回路（沿 -X：报警阀 → 接加速器三通 → 气压表
            #      → 止回阀 → 安全阀 → 截止阀 → 接供气管路）----
            '端口到加速器三通管长': 90.0,
            '加速器三通到气压表管长': 90.0,
            '气压表到止回阀管长': 90.0,
            '止回阀到安全阀管长': 60.0,
            '安全阀到截止阀管长': 60.0,
            '气源端短管长度': 40.0,
            '气压表支管长度': 30.0,
            '气压表表盘直径': 90.0,
            '气压表连系杆高度': 70.0,
            '加速器接口长度': 55.0,
            '供气主管外径': 28.0, '供气主管壁厚': 3.5,
            # ---- 报警信号回路 ----
            '报警立管外伸长度': 80.0,
            '报警管外径': 28.0, '报警管壁厚': 3.5,
            '水力警铃外径': 160.0,
            '水压表表盘直径': 60.0,
            '水压表连系杆高度': 40.0,
            '水压表距取压点水平距离': 90.0,
            '压力开关X坐标': -100.0,
            '压力开关立管高度': 41.0,
            # ---- 排水回路（自报警阀左侧 DN50 主排水接口引出）----
            '主排水接口标高': 40.0,
            '主排水接口伸出长度': 60.0,
            '接口到主排水阀管长': 80.0,  # 左移主排水阀，为编号11三通留位
            '水压表取压三通距排水口': 55.0,
            '排水管外径': 60.0, '排水管壁厚': 3.5,
            '排水管出口标高': 150.0,
            '排水管进深偏移': 0.0,
            # ---- 警铃立管与编号16排水管的直接连接回路 ----
            '警铃排水支管汇入标高': 778.0,
            '警铃排水弯曲半径': 20.0,
            # ---- 自动滴水阀支路（底部三通 → 水平管 → 上弯）----
            '滴水支管水平外伸': 125.0,
            '滴水阀立管高度': 220.0,
            '滴水支管弯曲半径': 20.0,
            '滴水阀主接口短管长度': 35.0,
            '滴水孔接管插入深度': 10.0,
            # ---- 冷凝水/注水支管 ----
            '注水管口标高': 50.0,
            '注水管口伸出长度': 45.0,
            '注水口相对标高': 240.0,
            '冷凝水阀相对标高': -120.0,
            '靠墙支管外径': 25.0, '靠墙支管壁厚': 2.5,
            # ---- 管卡与支撑柱 ----
            '管卡厚度': 20.0,
            '管卡箍径向厚度': 14.0,
            '支撑柱宽度': 40.0,
            '支撑柱厚度': 20.0,
        },
    }

    def __init__(self):
        Component.__init__(self)

        # ===== 型号选择 =====
        self['型号'] = Attr('ZSFC100', obvious=True, group='型号选择',
                            combo=['ZSFC100'])

        # ===== 04S206 安装尺寸（切型号自动刷新，只读） =====
        self['尺寸A'] = Attr(445.0, obvious=True, readonly=True, group='安装尺寸')
        self['尺寸B'] = Attr(245.0, obvious=True, readonly=True, group='安装尺寸')
        self['尺寸C'] = Attr(423.0, obvious=True, readonly=True, group='安装尺寸')
        self['尺寸D'] = Attr(173.0, obvious=True, readonly=True, group='安装尺寸')
        self['尺寸E'] = Attr(335.0, obvious=True, readonly=True, group='安装尺寸')
        self['尺寸F'] = Attr(260.0, obvious=True, readonly=True, group='安装尺寸')
        self['尺寸G'] = Attr(200.0, obvious=True, readonly=True, group='安装尺寸')
        self['尺寸H'] = Attr(360.0, obvious=True, readonly=True, group='安装尺寸')
        self['尺寸I'] = Attr(215.0, obvious=True, readonly=True, group='安装尺寸')
        self['地面至蝶阀底高度'] = Attr(978.0, obvious=True, readonly=True,
                                     group='安装尺寸')
        self['管卡中心标高'] = Attr(500.0, obvious=True, readonly=True,
                                 group='安装尺寸')

        # ===== 主通路驱动属性 =====
        self['信号蝶阀结构长度'] = Attr(155.0, obvious=False, group='主通路')
        self['主管公称直径'] = Attr(100.0, obvious=False, group='主通路')
        self['主管外径'] = Attr(114.0, obvious=False, group='主通路')
        self['主管壁厚'] = Attr(7.0, obvious=False, group='主通路')
        self['报警阀底部管段高度'] = Attr(70.0, obvious=False, group='主通路')
        self['信号蝶阀公称直径'] = Attr(
            100.0, obvious=True, readonly=True, group='信号蝶阀'
        )
        self['干式报警阀公称直径'] = Attr(
            100.0, obvious=True, readonly=True, group='干式报警阀'
        )

        # ===== 供气回路驱动属性 =====
        self['端口到加速器三通管长'] = Attr(90.0, obvious=False, group='供气回路')
        self['加速器三通到气压表管长'] = Attr(90.0, obvious=False, group='供气回路')
        self['气压表到止回阀管长'] = Attr(90.0, obvious=False, group='供气回路')
        self['止回阀到安全阀管长'] = Attr(60.0, obvious=False, group='供气回路')
        self['安全阀到截止阀管长'] = Attr(60.0, obvious=False, group='供气回路')
        self['气源端短管长度'] = Attr(40.0, obvious=False, group='供气回路')
        self['气压表支管长度'] = Attr(30.0, obvious=False, group='供气回路')
        self['气压表表盘直径'] = Attr(90.0, obvious=False, group='供气回路')
        self['气压表连系杆高度'] = Attr(70.0, obvious=False, group='供气回路')
        self['加速器接口长度'] = Attr(55.0, obvious=False, group='供气回路')
        self['供气主管外径'] = Attr(28.0, obvious=False, group='供气回路')
        self['供气主管壁厚'] = Attr(3.5, obvious=False, group='供气回路')

        # ===== 报警信号回路驱动属性 =====
        self['报警立管外伸长度'] = Attr(80.0, obvious=False, group='报警回路')
        self['报警管外径'] = Attr(28.0, obvious=False, group='报警回路')
        self['报警管壁厚'] = Attr(3.5, obvious=False, group='报警回路')
        self['水力警铃外径'] = Attr(160.0, obvious=False, group='报警回路')
        self['水压表表盘直径'] = Attr(60.0, obvious=False, group='报警回路')
        self['水压表连系杆高度'] = Attr(40.0, obvious=False, group='报警回路')
        self['水压表距取压点水平距离'] = Attr(90.0, obvious=False, group='报警回路')
        self['压力开关X坐标'] = Attr(-100.0, obvious=False, group='报警回路')
        self['压力开关立管高度'] = Attr(41.0, obvious=False, group='报警回路')

        # ===== 排水回路驱动属性 =====
        self['主排水接口标高'] = Attr(40.0, obvious=False, group='排水回路')
        self['主排水接口伸出长度'] = Attr(60.0, obvious=False, group='排水回路')
        self['接口到主排水阀管长'] = Attr(80.0, obvious=False, group='排水回路')
        self['水压表取压三通距排水口'] = Attr(
            55.0, obvious=False, group='排水回路'
        )
        self['排水管外径'] = Attr(60.0, obvious=False, group='排水回路')
        self['排水管壁厚'] = Attr(3.5, obvious=False, group='排水回路')
        self['排水管出口标高'] = Attr(150.0, obvious=False, group='排水回路')
        # 排水管与主立管同处 Y=0 竖直平面，只作水平左伸 + 竖直下弯
        self['排水管进深偏移'] = Attr(0.0, obvious=False, group='排水回路')

        # ===== 警铃立管与排水管连接回路 =====
        self['警铃排水支管汇入标高'] = Attr(778.0, obvious=False, group='报警回路')
        self['警铃排水弯曲半径'] = Attr(20.0, obvious=False, group='报警回路')

        # ===== 自动滴水阀侧支路 =====
        self['滴水支管水平外伸'] = Attr(125.0, obvious=False, group='滴水支管')
        self['滴水阀立管高度'] = Attr(220.0, obvious=False, group='滴水支管')
        self['滴水支管弯曲半径'] = Attr(20.0, obvious=False, group='滴水支管')
        self['滴水阀主接口短管长度'] = Attr(35.0, obvious=False, group='滴水支管')
        self['滴水孔接管插入深度'] = Attr(10.0, obvious=False, group='滴水支管')

        # ===== 冷凝水/注水支管驱动属性 =====
        self['注水管口标高'] = Attr(50.0, obvious=False, group='靠墙支管')
        self['注水管口伸出长度'] = Attr(45.0, obvious=False, group='靠墙支管')
        self['注水口相对标高'] = Attr(240.0, obvious=False, group='靠墙支管')
        self['冷凝水阀相对标高'] = Attr(-120.0, obvious=False, group='靠墙支管')
        self['靠墙支管外径'] = Attr(25.0, obvious=False, group='靠墙支管')
        self['靠墙支管壁厚'] = Attr(2.5, obvious=False, group='靠墙支管')

        # ===== 管卡与支撑柱驱动属性 =====
        self['管卡厚度'] = Attr(20.0, obvious=False, group='管卡')
        self['管卡箍径向厚度'] = Attr(14.0, obvious=False, group='管卡')
        self['支撑柱宽度'] = Attr(40.0, obvious=False, group='管卡')
        self['支撑柱厚度'] = Attr(20.0, obvious=False, group='管卡')

        # ===== 标识 =====
        self['名称'] = Attr('ZSFC系列干式报警阀组', obvious=True,
                            readonly=True, group='标识')
        self['图集号'] = Attr('04S206', obvious=True, readonly=True, group='标识')

        # ===== 业务属性（参照湿式报警阀组的分组方式） =====
        self['信号蝶阀型号'] = Attr(
            'ZSFD-16Z', obvious=True, readonly=True, group='业务属性'
        )
        self['自动滴水阀型号'] = Attr(
            'ZSFC100.2', obvious=True, readonly=True, group='业务属性'
        )
        self['干式报警阀型号'] = Attr(
            'ZSFC', obvious=True, readonly=True, group='业务属性'
        )
        self['主排水阀型号'] = Attr(
            '50Q11f-16', obvious=True, readonly=True, group='业务属性'
        )
        self['气压表型号'] = Attr(
            '图纸未注明', obvious=True, readonly=True, group='业务属性'
        )
        self['气路止回阀型号'] = Attr(
            '20H11T-16', obvious=True, readonly=True, group='业务属性'
        )
        self['安全阀型号'] = Attr(
            '15A27H-10K', obvious=True, readonly=True, group='业务属性'
        )
        self['供气截止阀型号'] = Attr(
            '20J11W-16', obvious=True, readonly=True, group='业务属性'
        )
        self['水力警铃型号'] = Attr(
            'ZSJL', obvious=True, readonly=True, group='业务属性'
        )
        self['水压表型号'] = Attr(
            '图纸未注明', obvious=True, readonly=True, group='业务属性'
        )
        self['压力开关型号'] = Attr(
            'YL1.2', obvious=True, readonly=True, group='业务属性'
        )
        self['冷凝水排水阀型号'] = Attr(
            '20Q11f-16', obvious=True, readonly=True, group='业务属性'
        )
        self['注水口管堵型号'] = Attr(
            '图纸未注明', obvious=True, readonly=True, group='业务属性'
        )

        # ===== 图纸技术参数与安装要求 =====
        self['法兰公称直径'] = Attr(
            'DN100', obvious=True, readonly=True, group='技术参数'
        )
        self['法兰外径'] = Attr(
            'φ215 mm', obvious=True, readonly=True, group='技术参数'
        )
        self['法兰螺栓孔中心直径'] = Attr(
            'φ180 mm', obvious=True, readonly=True, group='技术参数'
        )
        self['法兰螺栓孔'] = Attr(
            '8×φ18 mm', obvious=True, readonly=True, group='技术参数'
        )
        self['推荐安装高度'] = Attr(
            '距室内地面宜为 1.2 m', obvious=True, readonly=True,
            group='安装要求'
        )
        self['两侧最小检修距离'] = Attr(
            '距墙不小于 0.5 m', obvious=True, readonly=True,
            group='安装要求'
        )
        self['正面最小检修距离'] = Attr(
            '距墙不小于 1.2 m', obvious=True, readonly=True,
            group='安装要求'
        )

        # ===== 各部件公称直径与数量 =====
        self['消防给水管公称直径'] = Attr(
            100.0, obvious=True, readonly=True, group='消防给水管'
        )
        self['主排水阀公称直径'] = Attr(
            50.0, obvious=True, readonly=True, group='主排水阀'
        )
        self['气路止回阀公称直径'] = Attr(
            20.0, obvious=True, readonly=True, group='气路止回阀'
        )
        self['安全阀公称直径'] = Attr(
            15.0, obvious=True, readonly=True, group='安全阀'
        )
        self['供气截止阀公称直径'] = Attr(
            20.0, obvious=True, readonly=True, group='供气截止阀'
        )
        self['冷凝水排水阀公称直径'] = Attr(
            20.0, obvious=True, readonly=True, group='冷凝水排水阀'
        )
        self['注水口管堵公称直径'] = Attr(
            20.0, obvious=True, readonly=True, group='注水口管堵'
        )
        self['排水管公称直径'] = Attr(
            50.0, obvious=True, readonly=True, group='排水管'
        )
        self['管卡数量'] = Attr(
            2, obvious=True, readonly=True, group='管卡'
        )

        # ===== 04S206 图纸部件表（数量及工作状态均按图纸） =====
        self['1_消防给水管'] = Attr(
            'DN100 / 供水 / 平时：充满水 / 失火时：充满水',
            obvious=True, readonly=True, group='图纸部件表'
        )
        self['2_信号蝶阀'] = Attr(
            'ZSFD-16Z / DN100 / 数量：1 / 系统检修用 / 平时：常开 / 失火时：开',
            obvious=True, readonly=True, group='图纸部件表'
        )
        self['3_自动滴水阀'] = Attr(
            'ZSFC100.2 / 数量：1 / 排出系统微渗的水，接通大气密封干式阀阀瓣 '
            '/ 平时：常开 / 失火时：自动关闭',
            obvious=True, readonly=True, group='图纸部件表'
        )
        self['4_干式报警阀'] = Attr(
            'ZSFC / DN100 / 数量：1 / 系统控制阀，开启时输出报警水流信号 '
            '/ 平时：常闭 / 失火时：自动开启',
            obvious=True, readonly=True, group='图纸部件表'
        )
        self['5_主排水阀'] = Attr(
            '50Q11f-16 / DN50 / 数量：1 / 测试供水管路，系统复位时排出系统管网余水 '
            '/ 平时：常开 / 失火时：常开',
            obvious=True, readonly=True, group='图纸部件表'
        )
        self['6_气压表'] = Attr(
            '数量：1 / 指示系统管网侧气压 / 平时：显示 / 失火时：显示',
            obvious=True, readonly=True, group='图纸部件表'
        )
        self['7_气路止回阀'] = Attr(
            '20H11T-16 / DN20 / 数量：1 / 允许压力气体单向流入系统，防止因气压变化引起误动作 '
            '/ 平时：单向开 / 失火时：单向关',
            obvious=True, readonly=True, group='图纸部件表'
        )
        self['8_安全阀'] = Attr(
            '15A27H-10K / DN15 / 数量：1 / 防止供气压力过大 '
            '/ 平时：不动作 / 失火时：不动作',
            obvious=True, readonly=True, group='图纸部件表'
        )
        self['9_供气截止阀'] = Attr(
            '20J11W-16 / DN20 / 数量：1 / 可截止供气，维修供气系统用 '
            '/ 平时：常开 / 失火时：常开',
            obvious=True, readonly=True, group='图纸部件表'
        )
        self['10_水力警铃'] = Attr(
            'ZSJL / 数量：1 / 报警阀开启时发出音响信号 '
            '/ 平时：不动作 / 失火时：报警',
            obvious=True, readonly=True, group='图纸部件表'
        )
        self['11_水压表'] = Attr(
            '数量：1 / 指示供水侧水压 / 平时：显示 / 失火时：显示',
            obvious=True, readonly=True, group='图纸部件表'
        )
        self['12_压力开关'] = Attr(
            'YL1.2 / 数量：1 / 报警阀开启时输出报警电信号 '
            '/ 平时：不动作 / 失火时：输出信号',
            obvious=True, readonly=True, group='图纸部件表'
        )
        self['13_管卡'] = Attr(
            '数量：2 / 固定管道',
            obvious=True, readonly=True, group='图纸部件表'
        )
        self['14_冷凝水排水阀'] = Attr(
            '20Q11f-16 / DN20 / 数量：1 / 保持预注水位高度，排出冷凝水（注水、排水时用） '
            '/ 平时：常闭 / 失火时：常闭',
            obvious=True, readonly=True, group='图纸部件表'
        )
        self['15_注水口管堵'] = Attr(
            'DN20 / 数量：1 / 系统复位时，向干式阀内腔注水用 '
            '/ 平时：封闭 / 失火时：封闭',
            obvious=True, readonly=True, group='图纸部件表'
        )
        self['16_排水管'] = Attr(
            'DN50 / 排水', obvious=True, readonly=True, group='图纸部件表'
        )

        # ===== 输出属性（只让整体默认显示，避免重复渲染） =====
        self['主立管'] = Attr(None)
        self['信号蝶阀'] = Attr(None)
        self['干式报警阀'] = Attr(None)
        self['顶部出口短管'] = Attr(None)
        self['供气回路'] = Attr(None)
        self['报警信号回路'] = Attr(None)
        self['编号11水压表回路'] = Attr(None)
        self['编号11水压表'] = Attr(None)
        self['水压表后排水阀'] = Attr(None)
        self['排水回路'] = Attr(None)
        self['水力警铃排水连接回路'] = Attr(None)
        self['自动滴水阀支路'] = Attr(None)
        self['冷凝水注水支管'] = Attr(None)
        self['后侧水平支管'] = Attr(None)
        self['管卡'] = Attr(None)
        self['整体'] = Attr(None, show=True)

        # ===== 驱动特征点：本阀组与外部系统的对接接口 =====
        z_bfv = '[定位点Z]+[地面至蝶阀底高度]'
        z_alarm_bottom = z_bfv + '+[信号蝶阀结构长度]'
        z_alarm_top = z_alarm_bottom + '+[尺寸A]'
        z_group_top = ('[定位点Z]+[地面至蝶阀底高度]+[尺寸A]+[尺寸B]')
        z_gas = z_alarm_bottom + '+295'

        self.setDrivenFeaturePoint('主立管底端中心', SnapMode.EndPoint,
            '[定位点X]', '[定位点Y]', '[定位点Z]')
        self.setDrivenFeaturePoint('信号蝶阀下法兰底面', SnapMode.EndPoint,
            '[定位点X]', '[定位点Y]', z_bfv)
        self.setDrivenFeaturePoint('干式报警阀下端', SnapMode.EndPoint,
            '[定位点X]', '[定位点Y]', z_alarm_bottom)
        self.setDrivenFeaturePoint('干式报警阀上法兰顶面中心', SnapMode.EndPoint,
            '[定位点X]', '[定位点Y]', z_alarm_top)
        self.setDrivenFeaturePoint('系统侧出口中心', SnapMode.EndPoint,
            '[定位点X]', '[定位点Y]', z_group_top)
        self.setDrivenFeaturePoint('供气回路端头', SnapMode.EndPoint,
            ('[定位点X]-150.24-[端口到加速器三通管长]'
             '-[加速器三通到气压表管长]-[气压表到止回阀管长]-92'
             '-[止回阀到安全阀管长]-40-[安全阀到截止阀管长]-56'
             '-[气源端短管长度]'),
            '[定位点Y]', z_gas)
        # 接加速器三通支管朝 +Z，接口在支管顶端
        self.setDrivenFeaturePoint('加速器接口', SnapMode.EndPoint,
            '[定位点X]-150.24-[端口到加速器三通管长]',
            '[定位点Y]', z_gas + '+[加速器接口长度]')
        self.setDrivenFeaturePoint('排水管出口', SnapMode.EndPoint,
            '[定位点X]-[尺寸E]', '[定位点Y]+[排水管进深偏移]',
            '[定位点Z]+[排水管出口标高]')
        self.setDrivenFeaturePoint('注水口', SnapMode.EndPoint,
            '[定位点X]', '[定位点Y]+[尺寸H]',
            z_alarm_bottom + '+[注水口相对标高]')

        self.replace()

    @export
    def replace(self):
        # ===== 0. 防止属性自更新触发递归 =====
        if not getattr(self, '_refreshing_dims', False):
            dims = self.MODEL_DIMS.get(self['型号'], self.MODEL_DIMS['ZSFC100'])
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
        E = self['尺寸E']
        F = self['尺寸F']
        H = self['尺寸H']
        Z978 = self['地面至蝶阀底高度']
        z_clamp = self['管卡中心标高']

        bfv_length = self['信号蝶阀结构长度']
        main_dn = self['主管公称直径']
        main_od = self['主管外径']
        main_id = main_od - 2.0 * self['主管壁厚']
        # 顶部法兰孔和出口短管必须始终使用同一组管径，防止参数调整后失配。
        top_connection_od = main_od
        top_connection_id = main_id
        bottom_pipe_height = self['报警阀底部管段高度']

        gas_od = self['供气主管外径']
        gas_id = gas_od - 2.0 * self['供气主管壁厚']
        alarm_od = self['报警管外径']
        alarm_id = alarm_od - 2.0 * self['报警管壁厚']
        drain_od = self['排水管外径']
        drain_id = drain_od - 2.0 * self['排水管壁厚']
        wall_od = self['靠墙支管外径']
        wall_id = wall_od - 2.0 * self['靠墙支管壁厚']

        # ===== 2. 竖向基准链（自地面起算） =====
        z_bfv_bottom = Z978                       # 信号蝶阀下法兰底面
        z_alarm_bottom = z_bfv_bottom + bfv_length  # 干式报警阀下端
        z_alarm_top = z_alarm_bottom + A          # 报警阀上法兰顶面 = 978+A+蝶阀长
        z_group_top = Z978 + A + B                # 组件顶 = 978+A+B

        # ===== 3. 编号1：DN100 主立管（消防给水管） =====
        main_pipe = _空心管(
            Vec3(0, 0, 0), Vec3(0, 0, z_bfv_bottom), main_od, main_id
        ).color(*_色_管道)

        # ===== 4. 编号2：信号蝶阀 ZSFD-16Z DN100 =====
        butterfly = translate(0, 0, z_bfv_bottom + bfv_length / 2.0) * \
                    _信号蝶阀(bfv_length, main_dn)

        # ===== 5. 编号4：干式报警阀 ZSFC DN100 =====
        alarm_valve = translate(0, 0, z_alarm_bottom) * _干式报警阀(
            total_height=A,
            dn=main_dn,
            flange_bore_diameter=top_connection_od,
            bottom_pipe_height=bottom_pipe_height,
            bottom_pipe_od=main_od,
            fill_port_z=self['注水管口标高'],
            fill_port_length=self['注水管口伸出长度'],
            fill_port_dn=wall_id,
            fill_port_od=wall_od,
            gas_port_z=_报警阀_供气口Z,
            alarm_port_z=_报警阀_报警口Z,
            alarm_port_dn=alarm_id,
            alarm_port_od=alarm_od,
            drain_port_z=self['主排水接口标高'],
            drain_port_length=self['主排水接口伸出长度'],
            drain_port_dn=drain_id,
            drain_port_od=drain_od
        )

        # ===== 6. 顶部出口短管：报警阀上法兰顶面 → 组件顶（接系统配水干管） =====
        # 向法兰孔内嵌入 5 mm，外径与法兰孔径一致，顶部仍保持在组件总高处。
        top_stub_insert_depth = 5.0
        top_stub_start_z = z_alarm_top - top_stub_insert_depth
        top_stub = _空心管(
            Vec3(0, 0, top_stub_start_z), Vec3(0, 0, z_group_top),
            top_connection_od, top_connection_id
        ).color(*_色_管道)

        # ===== 7. 供气回路：报警阀左上 DN20 接口沿 -X 水平引出 =====
        gas_z = z_alarm_bottom + _报警阀_供气口Z
        port_x = _报警阀_供气口端X

        # 沿 -X 的接管顺序（与图纸一致）：
        #   报警阀左上接口 → 接加速器三通 → 气压表(6) → 气路止回阀(7)
        #   → 安全阀(8) → 供气截止阀(9) → 接供气管路
        accel_x = port_x - self['端口到加速器三通管长']
        gauge_x = accel_x - self['加速器三通到气压表管长']
        check_outlet_x = gauge_x - self['气压表到止回阀管长']
        check_center_x = check_outlet_x - 46.0
        check_inlet_x = check_center_x - 46.0
        safety_outlet_x = check_inlet_x - self['止回阀到安全阀管长']
        safety_center_x = safety_outlet_x - 20.0
        safety_inlet_x = safety_center_x - 20.0
        shutoff_outlet_x = safety_inlet_x - self['安全阀到截止阀管长']
        shutoff_center_x = shutoff_outlet_x - 28.0
        shutoff_inlet_x = shutoff_center_x - 28.0
        gas_end_x = shutoff_inlet_x - self['气源端短管长度']

        # 供气水平管：自报警阀引出管口一直贯通到止回阀入口，
        # 该段较长，中部依次设接加速器三通与气压表支管
        pipe_port_to_check = _空心管(
            Vec3(port_x, 0, gas_z), Vec3(check_outlet_x, 0, gas_z),
            gas_od, gas_id
        ).color(*_色_管道)
        check_valve = translate(check_center_x, 0, gas_z) * _止回阀()
        pipe_check_to_safety = _空心管(
            Vec3(check_inlet_x, 0, gas_z), Vec3(safety_outlet_x, 0, gas_z),
            gas_od, gas_id
        ).color(*_色_管道)
        safety_valve = translate(safety_center_x, 0, gas_z - 28.0) * _安全阀()
        pipe_safety_to_shutoff = _空心管(
            Vec3(safety_inlet_x, 0, gas_z), Vec3(shutoff_outlet_x, 0, gas_z),
            gas_od, gas_id
        ).color(*_色_管道)
        shutoff_valve = translate(shutoff_center_x, 0, gas_z) * _供气截止阀()
        pipe_to_source = _空心管(
            Vec3(shutoff_inlet_x, 0, gas_z), Vec3(gas_end_x, 0, gas_z),
            gas_od, gas_id
        ).color(*_色_管道)

        # 编号6 气压表：位于报警阀与止回阀之间，自水平管顶部向上引支管，
        # 表盘竖直、读数面朝 -Y 正前方（_压力表 本身即朝 -Y，无需旋转）
        gauge_branch_bottom = gas_z + gas_od / 2.0
        gauge_branch_top = gauge_branch_bottom + self['气压表支管长度']
        gauge_branch = _空心管(
            Vec3(gauge_x, 0, gauge_branch_bottom),
            Vec3(gauge_x, 0, gauge_branch_top), 22.0, 16.0
        ).color(*_色_管道)
        gas_gauge = translate(gauge_x, 0, gauge_branch_top) * _压力表(
            dial_diameter=self['气压表表盘直径'],
            rod_height=self['气压表连系杆高度'],
            rod_diameter=16.0
        )

        # "接加速器"接口：引出管口与止回阀之间的水平管上设三通，支管朝 +Z
        accel_tee = _三通X向Z(
            (accel_x, 0.0, gas_z), gas_od, gas_id,
            gas_od, gas_id, self['加速器接口长度']
        ).color(*_色_管道)

        gas_circuit = combine(
            pipe_port_to_check, accel_tee, gauge_branch, gas_gauge,
            check_valve, pipe_check_to_safety,
            safety_valve, pipe_safety_to_shutoff, shutoff_valve,
            pipe_to_source
        )

        # ===== 8. 报警信号回路：报警阀左下 DN15 接口 → 警铃/压力开关 =====
        alarm_y = F                                  # 侧视距主流通道轴线 F，向墙侧为 +Y
        bell_diameter = self['水力警铃外径']
        bell_inlet_x = -C + bell_diameter             # 湿式警铃左缘对齐 -C
        bell_z = z_group_top - bell_diameter / 2.0    # 铃壳顶对齐组件顶
        alarm_h_z = bell_z                            # 湿式警铃进水口与铃壳中心同高
        switch_x = self['压力开关X坐标']

        port_x_alarm = _报警阀_报警口端X
        port_z_alarm = z_alarm_bottom + _报警阀_报警口Z
        riser_x = port_x_alarm - self['报警立管外伸长度']
        alarm_drain_merge_z = self['警铃排水支管汇入标高']
        alarm_drain_bend_r = self['警铃排水弯曲半径']
        drain_riser_x = -E
        drain_riser_y = self['排水管进深偏移']
        drip_valve_x = riser_x + self['滴水支管水平外伸']
        drip_valve_z = alarm_drain_merge_z + self['滴水阀立管高度']
        drip_bend_r = self['滴水支管弯曲半径']
        drip_insert_depth = self['滴水孔接管插入深度']

        # 8.1 报警接口来管：先沿 -X 向左延伸，再沿 +Y 水平后移，
        #     到达报警回路平面后圆弧转向 -Z，竖直向下接入下方水平管。
        feed_bend_radius = max(
            alarm_od * 0.55,
            min(alarm_od, self['报警立管外伸长度'] * 0.45)
        )
        # 8.1.1 编号14/15：在蓝色箭头所示的 +Y 水平直管上分开布置。
        # 从侧视图看，靠阀体侧（较小 Y）为编号15注水口管堵，靠弯头侧
        # （较大 Y）为编号14冷凝水排水阀，两者不再共用同一个立管。
        trim_x = riser_x
        trim_z = port_z_alarm
        fill_plug_y = alarm_y * 0.32
        condensate_valve_y = alarm_y * 0.70
        condensate_valve_half_length = 56.0 / 2.0
        connection_insert = 4.0

        # 编号14串接在水平主管中，因此把原 FilletPipe 在阀门处断开。
        upstream_end_y = (
            condensate_valve_y
            - condensate_valve_half_length
            + connection_insert
        )
        downstream_start_y = (
            condensate_valve_y
            + condensate_valve_half_length
            - connection_insert
        )
        alarm_feed_upstream_points = [
            Vec3(port_x_alarm, 0.0, port_z_alarm),
            Vec3(riser_x, 0.0, port_z_alarm),
            Vec3(riser_x, upstream_end_y, port_z_alarm)
        ]
        alarm_feed_upstream_radii = [0.0, feed_bend_radius, 0.0]
        alarm_feed_upstream = (
            FilletPipe(
                alarm_feed_upstream_points,
                alarm_feed_upstream_radii,
                alarm_od / 2.0
            ) - FilletPipe(
                alarm_feed_upstream_points,
                alarm_feed_upstream_radii,
                alarm_id / 2.0
            )
        ).color(*_色_管道)

        # 删除竖管上的两只排水阀，恢复从上部弯头到下部汇合点的连续管段。
        alarm_feed_downstream_points = [
            Vec3(riser_x, downstream_start_y, port_z_alarm),
            Vec3(riser_x, alarm_y, port_z_alarm),
            Vec3(riser_x, alarm_y, alarm_drain_merge_z)
        ]
        alarm_feed_downstream_radii = [0.0, feed_bend_radius, 0.0]
        alarm_feed_downstream = (
            FilletPipe(
                alarm_feed_downstream_points,
                alarm_feed_downstream_radii,
                alarm_od / 2.0
            ) - FilletPipe(
                alarm_feed_downstream_points,
                alarm_feed_downstream_radii,
                alarm_id / 2.0
            )
        ).color(*_色_管道)
        alarm_feed_run = combine(
            alarm_feed_upstream,
            alarm_feed_downstream
        )

        # 编号14默认流道沿 +X；绕 Z 轴 +90° 后与 +Y 水平主管同轴。
        condensate_valve = translate(
            trim_x, condensate_valve_y, trim_z
        ) * rotate(Vec3(0, 0, 1), math.pi / 2.0) * _冷凝水排水阀()

        # 编号15单独设置短竖向支口；管堵轴线由 +X 转为 +Z。
        fill_branch_height = 28.0
        fill_branch = _空心管(
            Vec3(trim_x, fill_plug_y, trim_z),
            Vec3(trim_x, fill_plug_y, trim_z + fill_branch_height),
            wall_od, wall_id
        ).color(*_色_管道)
        fill_port_plug = translate(
            trim_x,
            fill_plug_y,
            trim_z + fill_branch_height - connection_insert
        ) * rotate(Vec3(0, 1, 0), -math.pi / 2.0) * _注水口管堵()

        condensate_fill_trim = combine(
            condensate_valve,
            fill_branch,
            fill_port_plug
        )

        # 下部管路恢复为连续的 FilletPipe，不再串接冷凝水排水阀。
        alarm_lower_points = [
            Vec3(drip_valve_x, alarm_y, drip_valve_z + drip_insert_depth),
            Vec3(drip_valve_x, alarm_y, alarm_drain_merge_z),
            Vec3(drain_riser_x, alarm_y, alarm_drain_merge_z),
        ]
        alarm_lower_radii = [0.0, drip_bend_r]
        if abs(alarm_y - drain_riser_y) > 1e-6:
            alarm_lower_points.append(
                Vec3(drain_riser_x, drain_riser_y, alarm_drain_merge_z)
            )
            alarm_lower_radii.append(alarm_drain_bend_r)
        alarm_lower_radii.append(0.0)
        alarm_lower_run = (
            FilletPipe(alarm_lower_points, alarm_lower_radii, alarm_od / 2.0)
            - FilletPipe(alarm_lower_points, alarm_lower_radii, alarm_id / 2.0)
        ).color(*_色_管道)
        alarm_riser = alarm_lower_run

        # 8.2 编号10 水力警铃：采用湿式报警阀组同款几何。
        # 湿式警铃局部钟罩沿 -X 展开；沿 Z 镜像后，其排水口在干式装配中朝下。
        bell = translate(bell_inlet_x, alarm_y, bell_z) * \
               scale(1.0, 1.0, -1.0) * _水力警铃()

        # 8.3 警铃—压力开关主管：水平管在压力开关下方以圆弧弯头
        #     转向 +Z，再用一小段竖管接到箱体底面，形状与参考图一致。
        #     压力开关本体的右侧小圆柱仍保持删除。
        switch_riser_h = self['压力开关立管高度']
        switch_bend_radius = max(
            alarm_od * 0.55,
            min(alarm_od, switch_riser_h * 0.45)
        )
        alarm_top_points = [
            Vec3(bell_inlet_x, alarm_y, alarm_h_z),
            Vec3(switch_x, alarm_y, alarm_h_z),
            Vec3(switch_x, alarm_y, alarm_h_z + switch_riser_h)
        ]
        alarm_top_radii = [0.0, switch_bend_radius, 0.0]
        alarm_top_run = (
            FilletPipe(alarm_top_points, alarm_top_radii, alarm_od / 2.0)
            - FilletPipe(alarm_top_points, alarm_top_radii, alarm_id / 2.0)
        ).color(*_色_管道)
        pressure_switch = translate(
            switch_x, alarm_y, alarm_h_z + switch_riser_h
        ) * _压力开关()

        alarm_circuit = combine(
            alarm_feed_run, condensate_fill_trim,
            alarm_riser, alarm_top_run,
            bell, pressure_switch
        )

        # ===== 9. 排水回路：DN50 主排水接口 → 主排水阀(5) → 排水管(16) =====
        # 主排水接口从图示底部红色主流道颈段水平向左引出，串主排水阀(5)，
        # 再经一个圆弧弯头直接竖直向下，即为排水管(16)。
        drain_z = z_alarm_bottom + self['主排水接口标高']
        drain_port_end_x = -(main_od / 2.0) - self['主排水接口伸出长度']
        drain_valve_outlet_x = drain_port_end_x - self['接口到主排水阀管长']
        drain_valve_center_x = drain_valve_outlet_x - 53.0
        drain_valve_inlet_x = drain_valve_center_x - 53.0
        drain_outlet_z = self['排水管出口标高']

        # 9.1 接口 → 主排水阀 的水平短管
        pipe_port_to_drain_valve = _空心管(
            Vec3(drain_port_end_x, 0, drain_z),
            Vec3(drain_valve_outlet_x, 0, drain_z), drain_od, drain_id
        ).color(*_色_管道)
        # 9.2 编号5 主排水阀（手柄转 -90°朝正前方，避开报警阀阀体）
        main_drain_valve = translate(drain_valve_center_x, 0, drain_z) * \
                           _主排水阀(handle_angle_deg=-90.0)
        # 9.3 主排水阀 → 沿 -X 水平延伸至 X=-E → 一个圆弧弯头直接转向下 →
        #     编号16 排水管竖直落到出口。全程位于 Y=drain_riser_y 竖直平面内，
        #     与主立管共面，不作进深方向转折。
        drain_points = [
            (drain_valve_inlet_x, 0.0, drain_z),
            (drain_riser_x, 0.0, drain_z)
        ]
        if abs(drain_riser_y) > 1e-6:
            # 仅当显式给了进深偏移时才插入一段进深转折
            drain_points.append((drain_riser_x, drain_riser_y, drain_z))
        drain_points.append(
            (drain_riser_x, drain_riser_y, drain_outlet_z)
        )
        drain_run = _折弯管(
            drain_points, drain_od, drain_id
        ).color(*_色_管道)

        # 9.4 编号11水压表回路：支管在干式报警阀排水口与主排水阀
        #     之间的 DN50 水平管段上直接相贯，不再叠加实体三通鞍座和管口突起。
        #     DN20 支管沿 +Y 后移，再圆弧上弯并接入警铃水平主管。
        drain_link_length = self['接口到主排水阀管长']
        pressure_takeoff_offset = min(
            max(self['水压表取压三通距排水口'], alarm_od),
            max(drain_link_length - alarm_od * 0.55, alarm_od)
        )
        water_pressure_x = drain_port_end_x - pressure_takeoff_offset

        # 水压表不再安装在警铃旁的上部交点，而是放在取压点之后的
        # +Y 水平管段上。表下增加一根 DN20 竖直支管，支管底端与
        # 水平管中心线相贯，顶端高度按“表盘中心 = 警铃水平管中心”反算。
        water_pressure_gauge_y = min(
            max(self['水压表距取压点水平距离'], alarm_od),
            max(alarm_y - alarm_od * 2.0, alarm_od)
        )

        # 水压表立柱后方 75 mm 串接排水阀。阀体总长 56 mm，管段分别
        # 向两端接口内插 4 mm；阀门主流道沿 +Y，阀杆/把手组件保持 +Z 向上。
        water_pressure_valve_offset = 75.0
        water_pressure_valve_half_length = 56.0 / 2.0
        water_pressure_valve_insert = 4.0
        water_pressure_valve_y = min(
            water_pressure_gauge_y + water_pressure_valve_offset,
            alarm_y - feed_bend_radius - water_pressure_valve_half_length
        )
        water_pressure_pipe_before_valve = _空心管(
            Vec3(water_pressure_x, 0.0, drain_z),
            Vec3(
                water_pressure_x,
                water_pressure_valve_y
                - water_pressure_valve_half_length
                + water_pressure_valve_insert,
                drain_z
            ),
            alarm_od,
            alarm_id
        ).color(*_色_管道)
        water_pressure_pipe_after_valve = _折弯管([
            (
                water_pressure_x,
                water_pressure_valve_y
                + water_pressure_valve_half_length
                - water_pressure_valve_insert,
                drain_z
            ),
            (water_pressure_x, alarm_y, drain_z),
            (water_pressure_x, alarm_y, alarm_h_z)
        ], alarm_od, alarm_id).color(*_色_管道)
        water_pressure_pipe = combine(
            water_pressure_pipe_before_valve,
            water_pressure_pipe_after_valve
        )
        water_pressure_drain_valve = translate(
            water_pressure_x,
            water_pressure_valve_y,
            drain_z
        ) * rotate(Vec3(0, 0, 1), math.pi / 2.0) * _冷凝水排水阀()

        gauge_dial_center_offset = (
            self['水压表连系杆高度']
            + self['水压表表盘直径'] / 2.0
        )
        water_pressure_gauge_base_z = alarm_h_z - gauge_dial_center_offset
        water_pressure_gauge_riser = _空心管(
            Vec3(water_pressure_x, water_pressure_gauge_y, drain_z),
            Vec3(water_pressure_x, water_pressure_gauge_y,
                 water_pressure_gauge_base_z),
            alarm_od, alarm_id
        ).color(*_色_管道)
        water_pressure_gauge = translate(
            water_pressure_x,
            water_pressure_gauge_y,
            water_pressure_gauge_base_z
        ) * _压力表(
            dial_diameter=self['水压表表盘直径'],
            rod_height=self['水压表连系杆高度'],
            rod_diameter=12.0
        )
        water_pressure_circuit = combine(
            water_pressure_pipe,
            water_pressure_drain_valve,
            water_pressure_gauge_riser,
            water_pressure_gauge
        )

        drain_circuit = combine(
            pipe_port_to_drain_valve, main_drain_valve, drain_run
        )
        alarm_circuit = combine(
            alarm_circuit,
            water_pressure_pipe,
            water_pressure_drain_valve,
            water_pressure_gauge_riser,
            water_pressure_gauge
        )

        # ===== 10. 编号3 自动滴水阀支路：底部三通 → 反向水平支管 → 上弯 → 滴水阀 =====
        # 支管从警铃立管下端的三通中心沿 +X 引出（图中红箭头向左），
        # 水平末端再用 alarm_riser 转向 +Z，上升管向滴水孔内插入
        # drip_insert_depth，与阀体产生实体重叠，避免两个切平面仅相切留缝。

        # 按图纸局部表达：滴水阀水平布置，主接口朝 +X，侧面滴水孔朝 -Z。
        # _自动滴水阀默认侧孔中心为局部 (14, 0, 43)。经下列旋转后，
        # 该点相对局部原点变为 (-43, 0, -14)，因此将原点平移到
        # (drip_valve_x+43, alarm_y, drip_valve_z+14)，使侧孔精确落在上升管轴线顶端。
        drip_valve_origin_x = drip_valve_x + 43.0
        drip_valve_origin_z = drip_valve_z + 14.0
        drip_valve = translate(
            drip_valve_origin_x, alarm_y, drip_valve_origin_z
        ) * rotate(Vec3(0, 0, 1), math.pi) * \
            rotate(Vec3(0, 1, 0), math.pi / 2.0) * _自动滴水阀(
                bore_diameter=alarm_id,
                hole_diameter=alarm_id,
                hole_depth=14.5,
                show_hole_shadow=False
            )

        # 主接口朝 +X，从阀体接口原点继续接一段与报警支管同规格的空心短管。
        drip_main_stub_length = self['滴水阀主接口短管长度']
        drip_main_stub = _空心管(
            Vec3(drip_valve_origin_x, alarm_y, drip_valve_origin_z),
            Vec3(drip_valve_origin_x + drip_main_stub_length,
                 alarm_y, drip_valve_origin_z),
            alarm_od, alarm_id
        ).color(*_色_管道)

        # 管路本体已经作为 alarm_riser 并入报警回路，这里只再合并阀体和主接口短管，
        # 避免同一根管道在整体模型中重复渲染。
        drip_branch = combine(drip_valve, drip_main_stub)

        # ===== 11. 后侧水平支管：仅保留 DN20 横管，末端侧接图示自动滴水阀 =====
        wall_terminal_y = H                    # 水平管末端（距墙 G）
        wall_branch_z = z_alarm_bottom + self['注水管口标高']
        wall_port_end_y = (main_od / 2.0) + self['注水管口伸出长度']

        # _自动滴水阀的侧孔默认位于局部 (+X, 0, 43)，阀体半径为 14。
        # 绕 Z 轴转 -90° 后侧孔朝 -Y，正对从报警阀向 +Y 延伸的水平管。
        # 横管再向阀体内插入一小段，避免两个切平面仅相切而出现可见缝隙。
        rear_drip_body_radius = 14.0
        rear_drip_hole_z = 43.0
        rear_drip_insert_depth = self['滴水孔接管插入深度']
        wall_run_y = _空心管(
            Vec3(0, wall_port_end_y, wall_branch_z),
            Vec3(0, wall_terminal_y + rear_drip_insert_depth, wall_branch_z),
            wall_od, wall_id
        ).color(*_色_管道)
        rear_drip_valve = translate(
            0.0,
            wall_terminal_y + rear_drip_body_radius,
            wall_branch_z - rear_drip_hole_z
        ) * rotate(Vec3(0, 0, 1), -math.pi / 2.0) * _自动滴水阀(
            bore_diameter=wall_id,
            hole_diameter=wall_id,
            hole_depth=rear_drip_body_radius + rear_drip_insert_depth,
            show_hole_shadow=False
        )
        wall_branch = combine(wall_run_y, rear_drip_valve)

        # ===== 12. 编号13 管卡 ×2（Z=500，抱主立管与排水管，支撑柱锚墙） =====
        wall_y = self['尺寸G'] + H              # 墙面 Y 坐标
        band_radial = self['管卡箍径向厚度']
        band_height = self['管卡厚度']
        strut_width = self['支撑柱宽度']
        # 支撑柱竖向厚度不得超过管卡厚度
        strut_thickness = min(self['支撑柱厚度'], band_height)

        def make_clamp_with_strut(center_x, center_y, pipe_od,
                                  ear_length, ear_width, bolt_diameter):
            clamp = translate(center_x, center_y, z_clamp) * _管卡(
                pipe_od=pipe_od,
                band_radial_thickness=band_radial,
                band_height=band_height,
                ear_length=ear_length,
                ear_width=ear_width,
                bolt_diameter=bolt_diameter
            )
            # 支撑柱连接管卡与墙面，只生根在管卡上，不接触被抱的管道。
            # 抱箍外缘是圆柱面而支撑柱端面是平面，若端面正好落在外缘切平面上
            # 就只有中间一条线相切；因此把端面沿 -Y 退到对应的弦位置再多埋
            # 一点，使整个端面都嵌进抱箍。埋深受限于抱箍径向厚度，不会碰到管道。
            band_outer = pipe_od / 2.0 + band_radial
            allowed_depth = band_radial * 0.70
            # 端面半宽过大时先收窄，保证弦的矢高不超过允许埋深
            max_half_width = math.sqrt(max(
                band_outer ** 2 - (band_outer - allowed_depth) ** 2, 1.0
            ))
            half_width = min(strut_width / 2.0, max_half_width)
            chord_y = math.sqrt(max(band_outer ** 2 - half_width ** 2, 0.0))
            embed_depth = min(band_outer - chord_y + 1.5, allowed_depth)

            strut_start_y = center_y + band_outer - embed_depth
            strut_length = max(wall_y - strut_start_y, 1.0)
            strut = translate(
                center_x - half_width,
                strut_start_y,
                z_clamp - strut_thickness / 2.0
            ) * scale(
                half_width * 2.0, strut_length, strut_thickness
            ) * Cube()
            return combine(clamp, strut.color(*_色_铸铁))

        clamps = combine(
            make_clamp_with_strut(0.0, 0.0, main_od, 48.0, 26.0, 12.0),
            make_clamp_with_strut(drain_riser_x, drain_riser_y, drain_od,
                                  34.0, 20.0, 10.0)
        )

        # ===== 13. 整体组合与输出 =====
        overall = combine(
            main_pipe, butterfly, alarm_valve, top_stub,
            gas_circuit, alarm_circuit, drain_circuit,
            drip_branch, wall_branch, clamps
        )

        self['主立管'] = main_pipe
        self['信号蝶阀'] = butterfly
        self['干式报警阀'] = alarm_valve
        self['顶部出口短管'] = top_stub
        self['供气回路'] = gas_circuit
        self['报警信号回路'] = alarm_circuit
        self['编号11水压表回路'] = water_pressure_circuit
        self['编号11水压表'] = water_pressure_gauge
        self['水压表后排水阀'] = water_pressure_drain_valve
        self['排水回路'] = drain_circuit
        self['水力警铃排水连接回路'] = alarm_riser
        self['自动滴水阀支路'] = drip_branch
        self['冷凝水注水支管'] = condensate_fill_trim
        self['后侧水平支管'] = wall_branch
        self['管卡'] = clamps
        self['整体'] = overall


def create_ZSFC干式报警阀组(**parameters):
    """创建 ZSFC100 干式报警阀组，并用关键字覆盖默认参数。"""
    component = ZSFC干式报警阀组()
    for name, value in parameters.items():
        component[name] = value
    component.replace()
    return component


if __name__ == '__main__':
    FinalGeometry = ZSFC干式报警阀组()
    place(FinalGeometry)
