from pickle import FALSE

from pyp3d import *
import math


def _空心管(start, end, outside_diameter, inside_diameter):
    return Cone(start, end, outside_diameter / 2) - \
           Cone(start, end, inside_diameter / 2)


def _L型弯管(长度, 高度, 直径=28, 倒角半径=15):
    """L型弯管：水平段沿 +X，竖直段沿 +Z，弯角位于 (长度, 0, 0)。
    参考 零件库_Py/弯管L型.py：FilletPipe 三点轨迹，弯折半径需大于管半径。
    """
    r = 直径 / 2
    return FilletPipe(
        [Vec3(0, 0, 0), Vec3(长度, 0, 0), Vec3(长度, 0, 高度)],
        [0, 倒角半径, 0],
        r
    )


def _圆截面X(x, radius, center_z=0):
    return translate(x, 0, center_z) * rotate(Vec3(0, 1, 0), math.pi / 2) * \
           Section(scale(radius) * Arc(2 * math.pi))


def _圆截面Z(z, radius):
    return translate(0, 0, z) * Section(scale(radius) * Arc(2 * math.pi))


def _六角截面X(x, across_flats, center_z=0):
    radius = across_flats / math.sqrt(3.0)
    points = []
    for index in range(6):
        angle = math.pi / 6 + index * math.pi / 3
        points.append(Vec3(
            x,
            radius * math.cos(angle),
            center_z + radius * math.sin(angle)
        ))
    points.append(points[0])
    return Section(Line(*points))


def _六角柱X(x0, x1, across_flats, center_z=0):
    body = Loft(
        _六角截面X(x0, across_flats, center_z),
        _六角截面X(x1, across_flats, center_z)
    )
    body.smooth = False
    return body


def _信号蝶阀(length=155.0, dn=100.0):
    """内联自 信号蝶阀.py。

    原始建模逻辑中阀体主轴沿 X、手轮在 +Z、轮面 +Y；
    本函数在尾部叠加两次旋转：
      1) rotate(Vec3(0,1,0), pi/2)  将主轴 +X 映射为 -Z、手轮 +Z 映射为 +X、轮面 +Y 保持 +Y；
      2) rotate(Vec3(1,0,0), pi)    将主轴 -Z 翻转为 +Z、轮面 +Y 翻转为 -Y（朝 -Y 正前方）；
    最终朝向：主管轴线沿 Z，手轮位于 +X 侧，轮面朝 -Y 正前方（与图中所示一致）。

    【几何随公称直径 dn 等比缩放】
    以 DN100 为基准（scale_factor = 1.0），所有硬编码尺寸 = 基准值 * (dn / 100.0)。
    DN150 时 scale_factor = 1.5：外径 150→225（大于主管 168），内径 100→150，壁厚、蝶板、
    支架、手轮同步放大，保持视觉比例与原版完全一致。
    （注：缩放因子命名为 scale_factor，避免与 pyp3d 的 scale() 函数同名冲突）
    """
    scale_factor = dn / 100.0  # DN100→1.0（不变），DN150→1.5

    # 主管路参数
    L = length
    D_flange = 150.0 * scale_factor   # 法兰外径（阀体可见外径），必须 > 主管外径
    D_inner = 100.0 * scale_factor    # 通径，等于公称直径
    B = 20.0 * scale_factor           # 阀体壁厚
    R_flange = D_flange / 2
    R_inner = D_inner / 2
    R_body_inner = R_flange - B

    # 蝶板参数（关闭状态：平面在 XZ 面内，旋转轴沿 Y）
    D_butterfly = D_inner
    T_butterfly = 15.0 * scale_factor
    R_butterfly = D_butterfly / 2

    # 填料压盖 + 支架
    H_packing = 25.0 * scale_factor
    H_bracket = 60.0 * scale_factor
    W_bracket = 80.0 * scale_factor

    # 手轮（沿用零件库 手轮.py 派生关系）
    Hcr = 160.0 * scale_factor
    Hsr = 0.11 * Hcr
    Zr = 1.2 * Hsr
    Zh = Hsr
    Zl = 60.0 * scale_factor
    Lr = 0.7 * Hsr

    # 1) 阀体（空心短管：外径 R_flange，壁厚 B，长 L）
    body_outer = Cone(Vec3(-L / 2, 0, 0), Vec3(L / 2, 0, 0), R_flange, R_flange)
    body_inner = Cone(
        Vec3(-L / 2 - 1, 0, 0), Vec3(L / 2 + 1, 0, 0), R_body_inner, R_body_inner
    )
    valve_body = body_outer - body_inner

    # 2) 阀座 / 密封圈
    seat_outer = Cone(
        Vec3(-L / 2 - 1, 0, 0), Vec3(L / 2 + 1, 0, 0), R_body_inner, R_body_inner
    )
    seat_inner = Cone(
        Vec3(-L / 2 - 2, 0, 0), Vec3(L / 2 + 2, 0, 0), R_inner, R_inner
    )
    valve_seat = seat_outer - seat_inner

    # 3) 蝶板
    butterfly = Cone(
        Vec3(0, -T_butterfly / 2, 0),
        Vec3(0, T_butterfly / 2, 0),
        R_butterfly, R_butterfly
    )

    # 4) 填料压盖 + 支架（圆柱体三通式连接，底部穿透阀体形成相贯）
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

    # 5) 手轮（手轮轴坐落于支架顶部再下移 20mm）
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
    # 本地坐标下：手轮面 +Y，轴 +Z
    wheel_assembly = translate(0, 0, z_shaft_bottom) * \
                     rotate(Vec3(0, 0, 1), pi / 2) * \
                     rotate(Vec3(0, 1, 0), pi / 2) * wheel

    # 整体组合 + 着色
    all_parts = combine(
        valve_body.color(0.6, 0.6, 0.6, 1.0),
        valve_seat.color(0.4, 0.4, 0.45, 1.0),
        butterfly.color(0.45, 0.45, 0.5, 1.0),
        support.color(0.55, 0.55, 0.55, 1.0),
        wheel_assembly.color(0.2, 0.3, 0.8, 1.0)
    )

    # 旋转换向：主轴沿 Z，手轮位于 +X 侧，轮面朝 -Y 正前方
    return rotate(Vec3(1, 0, 0), math.pi) * \
           rotate(Vec3(0, 1, 0), math.pi / 2) * all_parts


def _湿式报警阀(total_height=247.0, dn=100.0):
    """DN100湿式报警阀：左侧DN50出口、右侧两个DN20出口。"""
    flange_thickness = 24.0
    body_height = total_height - 2 * flange_thickness
    body_radius = 115.0
    neck_radius = dn / 2 + 12.0
    body_bottom = -body_height / 2
    body_top = body_height / 2

    body_outer = Loft(
        _圆截面Z(body_bottom, neck_radius),
        _圆截面Z(body_bottom + 43, body_radius),
        _圆截面Z(body_top - 43, body_radius),
        _圆截面Z(body_top, neck_radius)
    )
    body_outer.smooth = True
    main_bore = Cone(
        Vec3(0, 0, -total_height / 2 - 2),
        Vec3(0, 0, total_height / 2 + 2),
        dn / 2
    )
    body = body_outer - main_bore

    def flange(z0, z1):
        flange_body = Cone(Vec3(0, 0, z0), Vec3(0, 0, z1), 107.5) - \
                      Cone(Vec3(0, 0, min(z0, z1) - 1),
                           Vec3(0, 0, max(z0, z1) + 1), neck_radius)
        for index in range(8):
            angle = 2 * math.pi * index / 8
            hole_x = 90 * math.cos(angle)
            hole_y = 90 * math.sin(angle)
            hole = Cone(
                Vec3(hole_x, hole_y, min(z0, z1) - 1),
                Vec3(hole_x, hole_y, max(z0, z1) + 1),
                9
            )
            flange_body = flange_body - hole
        return flange_body

    lower_flange = flange(body_bottom - flange_thickness, body_bottom)
    upper_flange = flange(body_top, body_top + flange_thickness)

    # 与局部回路和L形排水管对接的三个出口。
    right_upper = Cone(Vec3(90, 0, 55), Vec3(138, 0, 55), 14)
    right_lower = Cone(Vec3(90, 0, -55), Vec3(138, 0, -55), 14)
    left_drain = Cone(Vec3(-90, 0, -18), Vec3(-142, 0, -18), 30)

    return combine(
        combine(body, lower_flange, upper_flange).color(0.43, 0.48, 0.56, 1.0),
        combine(right_upper, right_lower, left_drain).color(0.68, 0.71, 0.75, 1.0)
    )


def _DN50球阀竖直():
    """L形排水管上的DN50球阀，主管轴线沿Z。
    参照 _小球阀压力表 中的球阀：球体+端口+侧向控制轴+圆形手轮。
    控制轴从球阀前侧（-Y方向）表面连续伸出，圆形手轮安装在轴端。
    """
    ball_diameter = 58.0
    ball_center_z = 0.0
    ball_radius = ball_diameter / 2
    total_height = 82.0

    # 球阀主体：球体 + 端口 + 内孔
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

    # 控制轴从球阀前侧（-Y 方向）表面连续伸出
    shaft_start_y = -ball_radius + 2
    shaft_end_y = -ball_radius - 37
    control_shaft = Cone(
        Vec3(0, shaft_start_y, ball_center_z),
        Vec3(0, shaft_end_y, ball_center_z),
        6.5
    )

    # 圆形手轮（环面 + 轮辐 + 轮毂），轮面位于 XZ 平面（轴线沿 Y 方向）
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
    # 轮辐在 XZ 平面内（沿 X 和 Z 方向）
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
    return combine(valve_body, control_shaft, handwheel).color(0.76, 0.55, 0.16, 1.0)


def _止回阀DN20():
    """编号11，轴线沿X。"""
    length = 92.0
    body_length = 50.0
    half_length = length / 2
    half_body = body_length / 2
    bore = Cone(Vec3(-half_length - 1, 0, 0),
                Vec3(half_length + 1, 0, 0), 10)
    body_sections = [
        _圆截面X(-half_body, 17.5),
        _圆截面X(-14, 23),
        _圆截面X(0, 25),
        _圆截面X(14, 23),
        _圆截面X(half_body, 17.5)
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
        translate(0, 0, 22) * Section(scale(17) * Arc(2 * math.pi)),
        translate(0, 0, 35) * Section(scale(16) * Arc(2 * math.pi))
    )
    neck.smooth = True
    collar = Cone(Vec3(0, 0, 27), Vec3(0, 0, 35), 19)
    cap = translate(-15, -15, 35) * scale(30, 30, 10) * Cube()
    return combine(
        combine(body, connectors).color(0.78, 0.57, 0.16, 1.0),
        combine(neck, collar, cap).color(0.88, 0.70, 0.28, 1.0)
    )

 
def _小球阀():
    """编号10/12共用的小球阀，主管轴线沿Z，底部连接点为原点。
    仅包含阀体（球+端口+侧向控制轴+圆形手轮），不含压力表。
    """
    ball_diameter = 28.0
    ball_center_z = 20.0
    ball = translate(0, 0, ball_center_z) * \
           scale(ball_diameter / 2, ball_diameter / 2, ball_diameter / 2) * Sphere()
    valve_port = Cone(Vec3(0, 0, 0), Vec3(0, 0, 38), 10.5)

    # 控制轴从球阀前侧（-Y 方向）表面连续伸出，圆形手轮安装在轴端，不再悬空。
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
    # 手轮环面位于 XZ 平面（轴线沿 Y 方向）
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
    # 轮辐在 XZ 平面内（沿 X 和 Z 方向）
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
    return combine(ball, valve_port, control_shaft, handwheel).color(0.76, 0.55, 0.16, 1.0)


def _小球阀压力表(diameter=82.0):
    """编号10/12，小球阀位于压力表下方，底部连接点为原点。"""
    valve = _小球阀()

    # 仪表底部细长圆柱起点与球阀上部平台（z=38，半径10.5）顶部相接。
    gauge_base_z = 38.0
    stem_height = 32.0
    gauge_stem = Cone(Vec3(0, 0, gauge_base_z),
                      Vec3(0, 0, gauge_base_z + stem_height), 4.5)
    gauge_center_z = gauge_base_z + stem_height + diameter / 2
    shell = Cone(Vec3(0, -8, gauge_center_z),
                 Vec3(0, 8, gauge_center_z), diameter / 2)
    face = Cone(Vec3(0, -10, gauge_center_z),
                Vec3(0, -8, gauge_center_z), diameter * 0.43)
    pointer = Cone(Vec3(0, -11, gauge_center_z),
                   Vec3(diameter * 0.27, -11,
                        gauge_center_z + diameter * 0.12), 1.4)
    gauge = combine(
        combine(gauge_stem, shell).color(0.70, 0.73, 0.77, 1.0),
        face.color(0.94, 0.94, 0.92, 1.0),
        pointer.color(0.10, 0.10, 0.10, 1.0)
    )
    return combine(valve, gauge)


def _管卡(pipe_od=114.0, strap_width=30.0, strap_thickness=5.0, bolt_dia=10.0):
    """条带式U型管卡：定位点为管道轴线中心，水平条带抱住管道，前侧有U型螺栓头。
    形如参考图：圆环条带（沿 Z 轴向）+ 前侧两个螺栓头。
    由于 pyp3d 不支持 Lathe，用 N 个矩形截面沿圆周切线方向 Sweep 组成环形条带。
    """
    R_inner = pipe_od / 2
    R_outer = R_inner + strap_thickness
    half_h = strap_width / 2
    R_mid = (R_inner + R_outer) / 2

    # 矩形截面：X 径向（厚度），Y 轴向（宽度）
    section = Section(
        Vec2(-strap_thickness / 2, -half_h),
        Vec2(strap_thickness / 2, -half_h),
        Vec2(strap_thickness / 2, half_h),
        Vec2(-strap_thickness / 2, half_h)
    )

    # 沿圆周切线方向分 N 段，每段用矩形截面 Sweep 形成小方块
    N = 64
    pieces = []
    for i in range(N):
        angle = 2 * math.pi * (i + 0.5) / N
        seg_length = 2 * math.pi * R_mid / N

        # 截面定向：rotx(π/2) 让 Y 变 Z（轴向），再 rotz(angle) 转到对应角度
        oriented = rotate(Vec3(0, 0, 1), angle) * \
                   rotate(Vec3(1, 0, 0), math.pi / 2) * section

        # 切线方向线段（中心在原点）
        half_seg = seg_length / 2
        line = Line(
            Vec3(-math.sin(angle) * half_seg, math.cos(angle) * half_seg, 0),
            Vec3(math.sin(angle) * half_seg, -math.cos(angle) * half_seg, 0)
        )
        seg = Sweep(oriented, line)
        # 平移到该段中心位置
        seg = translate(R_mid * math.cos(angle),
                        R_mid * math.sin(angle), 0) * seg
        pieces.append(seg)

    band = combine(*pieces)

    # U 型螺栓：从前侧（+Y 方向）穿出，贯穿管道到背侧
    bolt = Cone(
        Vec3(0, -R_outer - 2, 0),
        Vec3(0, R_outer + 3, 0),
        bolt_dia / 2
    )
    bolt_upper = translate(0, 0, -half_h * 0.5) * bolt
    bolt_lower = translate(0, 0, half_h * 0.5) * bolt

    # 螺母：前侧（+Y 方向）两个小圆盘
    nut = Cone(
        Vec3(0, R_outer, 0),
        Vec3(0, R_outer + 4, 0),
        bolt_dia * 0.7
    )
    nut_upper = translate(0, 0, -half_h * 0.5) * nut
    nut_lower = translate(0, 0, half_h * 0.5) * nut

    return band + bolt_upper + bolt_lower + nut_upper + nut_lower


def _右侧仪表回路(spacing=110.0, run_length=230.0):
    """编号10、11、12组成的DN20回路，左端两接口中心在X=0。
    上右拐角和末端拐角（接12号）使用L型弯管，
    下右拐角用直管直角连接（参考 零件库_Py/弯管L型.py）。
    """
    dn = 20.0
    od = 28.0
    top_z = spacing / 2
    bottom_z = -spacing / 2
    gauge10_x = 48.0
    check_x = 125.0
    # 下水平管向右分支延长段长度
    extension = 60.0
    gauge12_x = run_length + extension
    # 12号支路L弯竖直段高度
    l_up_height = 55.0

    # 上右拐角L型弯管尺寸
    # 水平段长度由 run_length 推得（保证拐角X=run_length、且水平段>倒角半径>管半径）
    upper_H, upper_D = 50, 15
    # 上右拐角起点 = check_x + 46（止回阀右端）；拐角X = run_length
    upper_L = run_length - (check_x + 46)
    if upper_L <= upper_D:
        upper_L = upper_D + 1.0  # 保护：保证水平段长度 > 倒角半径
    # 末端拐角L型弯管尺寸
    # 水平35，竖直55 → 倒角16
    end_L, end_H, end_D = 35, 55, 16

    # 上右拐角L型弯管：水平段从左侧入，竖直段往下走（绕X轴转180°使+Z翻为-Z）
    # 拐角X = run_length，与中间竖直管X对齐（保证接上）
    upper_corner = translate(run_length - upper_L, 0, top_z) * \
                   rotate(Vec3(1, 0, 0), math.pi) * \
                   _L型弯管(upper_L, upper_H, od, upper_D)
    # 末端拐角L型弯管：水平段从左侧入，竖直段往上接12号
    end_corner = translate(gauge12_x - end_L, 0, bottom_z) * \
                 _L型弯管(end_L, end_H, od, end_D)

    # 直管段（下右拐角用直管直角连接，无圆角）
    pipes = combine(
        # 上水平管左段（0 到止回阀11左端）
        _空心管(Vec3(0, 0, top_z), Vec3(check_x - 46, 0, top_z), od, dn),
        # 上水平管右段（止回阀11右端到上右L弯起点）
        _空心管(Vec3(check_x + 46, 0, top_z),
                Vec3(run_length - upper_L, 0, top_z), od, dn),
        # 中间竖直管（上右L弯竖直段末端到下水平管）
        _空心管(Vec3(run_length, 0, top_z - upper_H),
                Vec3(run_length, 0, bottom_z), od, dn),
        # 下水平管左段（贯穿到下右拐角）
        _空心管(Vec3(0, 0, bottom_z),
                Vec3(run_length, 0, bottom_z), od, dn),
        # 下水平管中段（下右拐角到末端L弯起点）
        _空心管(Vec3(run_length, 0, bottom_z),
                Vec3(gauge12_x - end_L, 0, bottom_z), od, dn),
        # 两个L型弯管（上右和末端）
        upper_corner, end_corner
    ).color(0.66, 0.69, 0.72, 1.0)

    check = translate(check_x, 0, top_z) * _止回阀DN20()
    gauge10 = translate(gauge10_x, 0, top_z) * _小球阀压力表()
    # 编号12 接在末端L型弯管竖直段顶端
    gauge12 = translate(gauge12_x, 0, bottom_z + l_up_height) * _小球阀压力表()
    return combine(pipes, check, gauge10, gauge12)


def _延迟器几何(diameter=150.0, height=290.0):
    """内联ZSPY延迟器：直筒、平滑封头、环焊缝和上下接口。"""
    top_h = 48.0
    bottom_h = 45.0
    neck_r = 14.0
    straight_bottom = -height / 2 + bottom_h
    straight_top = height / 2 - top_h
    cylinder = Cone(Vec3(0, 0, straight_bottom), Vec3(0, 0, straight_top), diameter / 2)

    def head(start_z, direction, head_height):
        sections = []
        for index in range(25):
            t = index / 24
            radius = neck_r + (diameter / 2 - neck_r) * math.cos(math.pi * t / 2)
            sections.append(_圆截面Z(start_z + direction * head_height * t, radius))
        result = Loft(*sections)
        result.smooth = True
        return result

    top = head(straight_top, 1, top_h)
    bottom = head(straight_bottom, -1, bottom_h)
    weld = Cone(Vec3(0, 0, -2), Vec3(0, 0, 2), diameter / 2 + 2)
    top_port = _空心管(Vec3(0, 0, height / 2 - 4), Vec3(0, 0, height / 2 + 22), 28, 20)
    bottom_port = _空心管(Vec3(0, 0, -height / 2 - 20), Vec3(0, 0, -height / 2 + 4), 28, 20)
    top_collar = _空心管(Vec3(0, 0, height / 2 + 14), Vec3(0, 0, height / 2 + 22), 40, 20)
    bottom_collar = _空心管(Vec3(0, 0, -height / 2 - 20), Vec3(0, 0, -height / 2 - 12), 40, 20)
    red = (0.78, 0.05, 0.035, 1.0)
    return combine(
        combine(cylinder, top, bottom, top_port, bottom_port, top_collar, bottom_collar).color(*red),
        weld.color(0.58, 0.025, 0.02, 1.0)
    )


def _过滤器几何():
    """内联ZSPL DN20 Y型过滤器，局部主管轴线沿X。"""
    body_d = 40.0
    # 加长粗圆柱主体：原 x=-30~+30 改为 -45~+45，长度 60→90。
    body = Cone(Vec3(-45, 0, 0), Vec3(45, 0, 0), body_d / 2)
    angle = math.pi / 3
    barrel_len = 50.0  # 缩短滤筒长度（原76），避免与旁边管道碰撞
    # 滤嘴朝向左下方倾斜：夹角加大 45°→60° 后 end.x 从 -35 自然右移到 -25
    end = Vec3(-barrel_len * math.cos(angle), 0, -barrel_len * math.sin(angle))
    barrel = Cone(Vec3(0, 0, 0), end, 18)
    # 排污端盖改为扁圆盖（沿轴向 4mm 厚、半径 20），不再是一根 11.3mm 长的"粗管"
    cap_axis = Vec3(-math.cos(angle), 0, -math.sin(angle))
    cap = Cone(end, end + cap_axis * 4, 20)
    return combine(body, barrel, cap).color(0.76, 0.55, 0.16, 1.0)


def _三通(pipe_od=28.0, dn=20.0, branch_length=25.0):
    """三通（T型接头）：主管竖直方向，分支向左（-X）。以三通中心为原点。"""
    outer_r = pipe_od / 2
    inner_r = dn / 2
    wall = (pipe_od - dn) / 2

    # 主管竖直段：z 范围 -30 ~ +30，总长 60
    main_outer = Cone(Vec3(0, 0, -30), Vec3(0, 0, 30), outer_r)
    main_inner = Cone(Vec3(0, 0, -31), Vec3(0, 0, 31), inner_r)
    main = main_outer - main_inner

    # 水平分支：沿 -X 方向延伸
    branch_outer = Cone(Vec3(0, 0, 0), Vec3(-branch_length, 0, 0), outer_r)
    branch_inner = Cone(Vec3(1, 0, 0), Vec3(-branch_length - 1, 0, 0), inner_r)
    branch = branch_outer - branch_inner

    # 主管与分支的圆角过渡：用小半径的球面修整内角
    tee = combine(main, branch)
    return tee.color(0.66, 0.69, 0.72, 1.0)


def _压力开关(switch_size=38.0):
    """简化为正方体的压力开关，几何中心在原点。
    pyp3d 的 Cube() 单位立方体角点在 (0,0,0)，平移 -size/2 使其居中。
    """
    return translate(-switch_size / 2, -switch_size / 2, -switch_size / 2) * \
           scale(switch_size, switch_size, switch_size) * Cube()


def _水力警铃几何():
    """内联自水力警铃.py：定位点为DN20进水口外端面，进水方向沿-X。"""
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

    # 定位原点位于右侧DN20进水口，水轮壳体和钟罩位于-X侧。
    housing_x = -port_length - housing_radius
    housing_z = 0.0
    bell_x = housing_x
    # 圆铃面位于警铃底座正中间：装配旋转 (x, y, z) -> (-x, y, -z) 把局部 +Z 翻为装配图 -Z，
    # 因此把 bell_z 设为 0，铃面在装配图中正好位于 housing 中心 (z = 0)。
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

    # 3. DN20进水口和DN25排水口。
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

    # 排水口：在水力警铃下方引一根水管（如图2所示）。
    # 装配旋转为 (x, y, z) -> (-x, y, -z)，局部 +Z 方向经旋转后变为装配图 -Z 方向（向下）。
    # 因此在局部 +Z 方向从水轮壳体顶部（z=+housing_radius）引管，
    # 装配后即从警铃壳体底部向下延伸，与图2一致。
    # 排水管长度从原 port_length=38 延长到 100，给下方留更长的可视段。
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


def _新增左侧回路(A=247.0, E=235.0, F=200.0, H=840.0, D=375.0, B=300.0):
    """正视图左侧回路：延迟器、压力开关、水力警铃及过滤器球阀支路。

    走向：在左侧L型弯管球阀下方E处（z=H）向后水平一段，再竖直向上至报警阀上侧
    法兰上方D处（z = z_alarm_top + D），竖管上安装延迟器；延迟器上方的压力开关管路
    向右转弯后接水力警铃，延迟器右侧另引一条带过滤器和球阀的L型支路。
    """
    dn = 20.0
    od = 28.0
    pipe_color = (0.66, 0.69, 0.72, 1.0)
    dark = (0.22, 0.25, 0.29, 1.0)

    y_back = 200.0          # 向后（+Y方向，远离正前方）水平段长度
    gong_inlet_x = 100.0    # 水力警铃DN20进水口位置
    filter_drop_x = 25.0    # 过滤器支路向下转弯及球阀的X位置
    # B: 压力开关左边界到主立管管轴线的水平距离（来自图集尺寸B）
    switch_size = 38.0      # 压力开关正方体边长
    switch_stub = 15.0      # 压力开关前的短管长度
    # 由 B 反推三通向左分支长度，保证压力开关左边界在 X = -B
    tee_branch_len = B - switch_stub - switch_size - F
    tee_extension = 60.0    # 延迟器顶部到三通中心的竖直距离

    z_alarm_top = H + E + A
    z_delayer_top = z_alarm_top + D                 # 延迟器顶部管口高度
    z_delayer_center = z_delayer_top - 167          # 延迟器中心高度
    z_delayer_bottom = z_delayer_center - 165       # 延迟器底部管口高度
    z_tee = z_delayer_top + tee_extension            # 三通中心高度
    z_ball_valve = z_alarm_top - 30                 # 球阀底部连接点高度

    # ===== 1. U型弯管第一段L（向后 + 向上），拐角圆滑过渡 =====
    # 路径：(-F, 0, H) → (-F, y_back, H) → (-F, y_back, z_delayer_bottom)
    fillet_r = 15.0  # 增大圆角半径(原15)，使弯管视觉上更圆润
    l_shape_1 = FilletPipe(
        [Vec3(-F, 0, H),
         Vec3(-F, y_back, H),
         Vec3(-F, y_back, z_delayer_bottom)],
        [0, fillet_r, 0],
        od / 2
    ).color(*pipe_color)

    # ===== 2. 延迟器上端延伸短管（从 z_delayer_top 到 z_tee）=====
    top_extension = _空心管(
        Vec3(-F, y_back, z_delayer_top),
        Vec3(-F, y_back, z_tee),
        od, dn
    ).color(*pipe_color)

    # ===== 3. 压力开关处向右拐弯，并水平接至水力警铃 =====
    # 从三通内部起管，竖直向上后圆滑转向右侧；末端伸入警铃进水口2mm。
    # 竖直段加高到 50mm，确保拐弯圆角（20mm）能流畅过渡。
    z_tee_top = z_tee + 50
    tee_joint_overlap = 2.0
    tee_corner_radius = 20.0  # 大于管半径14，50mm竖直段可容纳该弯头
    gong_supply_pipe = FilletPipe(
        [Vec3(-F, y_back, z_tee - tee_joint_overlap),
         Vec3(-F, y_back, z_tee_top),
         Vec3(gong_inlet_x + tee_joint_overlap, y_back, z_tee_top)],
        [0, tee_corner_radius, 0],
        od / 2
    ).color(*pipe_color)

    # 使用上方内联的水力警铃几何。原模型从进水口向-X展开，绕Z轴旋转180°后
    # 改为从管道末端向+X展开，与正视图中"管在左、警铃在右"的方向一致。
    # 再绕X轴旋转180°，使圆形警铃面朝正前方（-Y方向）。
    water_gong = translate(gong_inlet_x, y_back, z_tee_top) * \
                 rotate(Vec3(0, 0, 1), math.pi) * \
                 rotate(Vec3(1, 0, 0), math.pi) * \
                 _水力警铃几何()

    # ===== 4. 三通（编号8的底座），放在竖直延伸段上 =====
    tee = translate(-F, y_back, z_tee) * _三通(od, dn, tee_branch_len)

    # ===== 5. 三通向左引出的短管 + 压力开关 =====
    # 短管从三通分支端（-F - tee_branch_len）继续向左至压力开关
    switch_pipe_start_x = -F - tee_branch_len
    switch_pipe_end_x = switch_pipe_start_x - switch_stub
    switch_pipe = _空心管(
        Vec3(switch_pipe_start_x, y_back, z_tee),
        Vec3(switch_pipe_end_x, y_back, z_tee),
        od, dn
    ).color(*pipe_color)

    # 压力开关（正方体），放在短管末端
    pressure_switch = translate(switch_pipe_end_x - switch_size / 2,
                                y_back,
                                z_tee) * \
                      _压力开关(switch_size)
    pressure_switch = pressure_switch.color(*dark)

    # ===== 6. 延迟器（编号6），放在竖直段上 =====
    delayer = translate(-F, y_back, z_delayer_center) * _延迟器几何()

    # ===== 7. 从延迟器右侧引出带过滤器的L型支路 =====
    # 起点伸入延迟器筒体15mm，确保侧向接口不悬空；随后水平向右并圆滑向下。
    delayer_side_z = z_delayer_center + 35.0
    delayer_side_start_x = -F + 60.0
    ball_valve_top_z = z_ball_valve + 38.0
    filter_ball_pipe = FilletPipe(
        [Vec3(delayer_side_start_x, y_back, delayer_side_z),
         Vec3(filter_drop_x, y_back, delayer_side_z),
         Vec3(filter_drop_x, y_back, ball_valve_top_z - tee_joint_overlap)],
        [0, tee_corner_radius, 0],
        od / 2
    ).color(*pipe_color)

    filter_x = (delayer_side_start_x + filter_drop_x) / 2
    filter_geometry = translate(filter_x, y_back, delayer_side_z) * _过滤器几何()

    # ===== 8. DN20球阀（编号4），接在过滤器支路竖直段末端 =====
    ball_valve = translate(filter_drop_x, y_back, z_ball_valve) * _小球阀()

    all_pipes = combine(l_shape_1, top_extension, gong_supply_pipe,
                        filter_ball_pipe, switch_pipe, tee)

    return combine(
        all_pipes,
        delayer,
        pressure_switch,
        filter_geometry,
        ball_valve,
        water_gong
    ), delayer, pressure_switch, filter_geometry, ball_valve, water_gong, all_pipes


class ZSFZ100基础阀组(Component):
    """按用户给出的6步顺序建立的ZSFZ100基础阀组。

    【型号驱动的尺寸切换】
    类顶部 MODEL_DIMS 字典集中保存每种型号的安装尺寸、信号蝶阀结构长度和主管参数。
    在 BIM 软件属性面板中切换『型号』下拉框时，replace() 会先查表把所有驱动属性
    (obvious=False) 同步成该型号的值，然后用这套新尺寸重新搭建整个阀组几何，
    整体几何按新尺寸变换，属性面板中的安装尺寸也随之变化。

    ZSFZ100 的尺寸按用户图纸录入；
    ZSFZ150 的尺寸为占位估算值（带 TODO 注释），用户在 BIM 切换到 ZSFZ150 后
    把这里替换为图纸中 ZSFZ150 那一行的实测值即可。
    """

    MODEL_DIMS = {
        'ZSFZ100': {
            '尺寸A': 247.0, '尺寸B': 300.0, '尺寸C': 400.0, '尺寸D': 375.0,
            '尺寸E': 235.0, '尺寸F': 200.0, '尺寸G': 300.0, '尺寸H': 840.0,
            '信号蝶阀结构长度': 155.0,
            '主管公称直径': 100.0, '主管外径': 114.0, '主管壁厚': 7.0,
            '信号蝶阀公称直径': 100.0,
            '湿式报警阀公称直径': 100.0,
        },
        # TODO: 用图纸中 ZSFZ150 那一行的实测安装尺寸替换下面的占位值。
        # 估算规则：150 比 100 各尺寸大致 +20%~+25%，主管壁厚 +1mm。
        'ZSFZ150': {
            '尺寸A': 280.0, '尺寸B': 380.0, '尺寸C': 400.0, '尺寸D': 400.0,
            '尺寸E': 260.0, '尺寸F': 240.0, '尺寸G': 310.0, '尺寸H': 800.0,
            '信号蝶阀结构长度': 175.0,
            '主管公称直径': 150.0, '主管外径': 168.0, '主管壁厚': 8.0,
            '信号蝶阀公称直径': 150.0,
            '湿式报警阀公称直径': 150.0,
        },
    }

    def __init__(self):
        Component.__init__(self)
        # ===== 型号选择（驱动源：切换型号时，pyp3d 自动调用 replace 重算尺寸和几何）=====
        self['型号'] = Attr('ZSFZ100', obvious=True, group='型号选择',
                            combo=['ZSFZ100', 'ZSFZ150'])
        # ===== 安装尺寸（obvious=True 在面板显示，readonly=True 禁止手动覆盖，
        # 切『型号』时由 MODEL_DIMS 自动刷新）=====
        self['尺寸A'] = Attr(247.0, obvious=True, readonly=True, group='安装尺寸')
        self['尺寸B'] = Attr(300.0, obvious=True, readonly=True, group='安装尺寸')
        self['尺寸C'] = Attr(400.0, obvious=True, readonly=True, group='安装尺寸')
        self['尺寸D'] = Attr(375.0, obvious=True, readonly=True, group='安装尺寸')
        self['尺寸E'] = Attr(235.0, obvious=True, readonly=True, group='安装尺寸')
        self['尺寸F'] = Attr(200.0, obvious=True, readonly=True, group='安装尺寸')
        self['尺寸G'] = Attr(300.0, obvious=True, readonly=True, group='安装尺寸')
        self['尺寸H'] = Attr(840.0, obvious=True, readonly=True, group='安装尺寸')
        self['信号蝶阀结构长度'] = Attr(155.0, obvious=False, group='信号蝶阀')
        self['主管公称直径'] = Attr(100.0, obvious=False, group='主管')
        self['主管外径'] = Attr(114.0, obvious=False, group='主管')
        self['主管壁厚'] = Attr(7.0, obvious=False, group='主管')
        # ===== 随型号联动的公称直径（obvious=True 在面板显示，readonly=True 禁止手动覆盖，
        # 切『型号』时由 MODEL_DIMS 自动刷新）=====
        self['信号蝶阀公称直径'] = Attr(100.0, obvious=True, readonly=True, group='信号蝶阀')
        self['湿式报警阀公称直径'] = Attr(100.0, obvious=True, readonly=True, group='湿式报警阀')
        self['名称'] = Attr('ZSFZ系列湿式报警阀组', obvious=True, readonly=True, group='标识')

        # ===== 业务属性（部件型号，对应 ZSFZ 系列自动喷水湿式报警阀组部件表） =====
        self['信号蝶阀型号'] = Attr('ZSFD-16Z', obvious=True, group='业务属性')
        self['湿式报警阀型号'] = Attr('ZSFZ', obvious=True, group='业务属性')
        self['球阀型号'] = Attr('Q11f-16', obvious=True, group='业务属性')
        self['过滤器型号'] = Attr('ZSPL', obvious=True, group='业务属性')
        self['延迟器型号'] = Attr('ZSPY', obvious=True, group='业务属性')
        self['水力警铃型号'] = Attr('ZSJL', obvious=True, group='业务属性')
        self['压力开关型号'] = Attr('YL1.2', obvious=True, group='业务属性')
        self['出水口压力表型号'] = Attr('Y-100', obvious=True, group='业务属性')
        self['进水口压力表型号'] = Attr('Y-100', obvious=True, group='业务属性')

        # ===== 技术参数（ZSFZ 系列湿式报警阀技术参数） =====
        self['工作压力'] = Attr('1.6MPa', obvious=True, group='技术参数')
        self['最低使用环境温度'] = Attr('4°C', obvious=True, group='技术参数')
        self['最高使用环境温度'] = Attr('70°C', obvious=True, group='技术参数')
        self['水头损失'] = Attr('<0.02MPa', obvious=True, group='技术参数')
        self['流量范围'] = Attr('15-60 L/min', obvious=True, group='技术参数')

        # ===== 公称直径（按部件分组，对应 ZSFZ 系列自动喷水湿式报警阀组部件表中的公称直径列） =====
        # 注：信号蝶阀公称直径、湿式报警阀公称直径已在上面『安装尺寸』区注册为
        # obvious=True, readonly=True，由 MODEL_DIMS 随型号自动刷新（不再重复定义）。
        self['DN20球阀公称直径'] = Attr(20.0, obvious=True, group='DN20球阀')
        self['DN50球阀公称直径'] = Attr(50.0, obvious=True, group='DN50球阀')
        self['过滤器公称直径'] = Attr(20.0, obvious=True, group='过滤器')
        self['止回阀公称直径'] = Attr(20.0, obvious=True, group='止回阀')
        self['排水管公称直径'] = Attr(50.0, obvious=True, group='排水管')

        self['主立管'] = Attr(None, show=True)
        self['信号蝶阀'] = Attr(None, show=True)
        self['湿式报警阀'] = Attr(None, show=True)
        self['左侧L型排水管'] = Attr(None, show=True)
        self['DN50球阀'] = Attr(None, show=True)
        self['右侧仪表回路'] = Attr(None, show=True)
        self['新增左侧回路'] = Attr(None, show=True)
        self['延迟器'] = Attr(None, show=True)
        self['压力开关'] = Attr(None, show=True)
        self['水力警铃'] = Attr(None, show=True)
        self['过滤器'] = Attr(None, show=True)
        self['DN20球阀'] = Attr(None, show=True)
        self['整体'] = Attr(None, show=True)

        self.setDrivenFeaturePoint('主立管底端', SnapMode.EndPoint,
            '[定位点X]', '[定位点Y]', '[定位点Z]')
        self.setDrivenFeaturePoint('信号蝶阀底部法兰', SnapMode.EndPoint,
            '[定位点X]', '[定位点Y]', '[定位点Z]+[尺寸H]')
        self.setDrivenFeaturePoint('湿式报警阀底部法兰', SnapMode.EndPoint,
            '[定位点X]', '[定位点Y]', '[定位点Z]+[尺寸H]+[尺寸E]')
        self.setDrivenFeaturePoint('左侧排水管轴线', SnapMode.EndPoint,
            '[定位点X]-[尺寸F]', '[定位点Y]', '[定位点Z]')
        self.replace()

    @export
    def replace(self):
        # ===== 0. 防止属性自更新触发递归调用 =====
        if getattr(self, '_refreshing_dims', False):
            # 已在本轮刷新中，直接按当前属性值走完几何重建逻辑
            pass
        else:
            # ===== 1. 根据当前『型号』查表，刷新所有驱动尺寸/主管参数 =====
            # 把每个驱动属性（obvious=False，面板上隐藏）的值同步为当前型号的实测值。
            # 之后下面的 A/B/.../H/butterfly_length/main_od 都从 self[...] 读到新值，
            # 整个阀组几何就按新尺寸重新搭建；面板里的『安装尺寸』分组也会自动更新。
            model = self['型号']
            dims = self.MODEL_DIMS.get(model, self.MODEL_DIMS['ZSFZ100'])
            self._refreshing_dims = True
            try:
                for key, value in dims.items():
                    self[key] = value
            finally:
                self._refreshing_dims = False

        A = self['尺寸A']
        B = self['尺寸B']
        C = self['尺寸C']
        D = self['尺寸D']
        E = self['尺寸E']
        F = self['尺寸F']
        G = self['尺寸G']
        H = self['尺寸H']
        butterfly_length = self['信号蝶阀结构长度']
        main_od = self['主管外径']
        main_inside = main_od - 2 * self['主管壁厚']
        main_dn = self['主管公称直径']

        # 1. DN100主立管，顶部正好连接信号蝶阀底部法兰。
        main_pipe = _空心管(
            Vec3(0, 0, 0), Vec3(0, 0, H), main_od, main_inside
        ).color(0.66, 0.69, 0.72, 1.0)

        # 2. 信号蝶阀底端位于Z=H；使用内联自 信号蝶阀.py 的建模逻辑，
        #    旋转换向后主轴沿Z、手轮在+X、轮面朝-Y（与图中所示方向一致）。
        butterfly_center_z = H + butterfly_length / 2
        butterfly = translate(0, 0, butterfly_center_z) * \
                    _信号蝶阀(butterfly_length, main_dn)

        # 3. 湿式报警阀底部法兰距蝶阀底部法兰E。
        alarm_bottom_z = H + E
        alarm_center_z = alarm_bottom_z + A / 2
        alarm = translate(0, 0, alarm_center_z) * _湿式报警阀(A, main_dn)

        # 蝶阀顶端到报警阀底端之间的DN100连接短管。
        butterfly_top_z = H + butterfly_length
        connecting_pipe = None
        if alarm_bottom_z > butterfly_top_z:
            connecting_pipe = _空心管(
                Vec3(0, 0, butterfly_top_z),
                Vec3(0, 0, alarm_bottom_z),
                main_od, main_inside
            ).color(0.66, 0.69, 0.72, 1.0)

        # 4. 左侧DN50 L形管：先向左到X=-F，再竖直向下。
        left_port_z = alarm_center_z - 18.0
        left_port_x = -142.0
        drain_end_z = 0.0
        l_pipe = FilletPipe(
            [
                Vec3(left_port_x, 0, left_port_z),
                Vec3(-F, 0, left_port_z),
                Vec3(-F, 0, drain_end_z)
            ],
            [0, 35, 0],
            30
        ).color(0.66, 0.69, 0.72, 1.0)

        # 5. DN50球阀中心与湿式报警阀底部法兰齐平。
        drain_ball = translate(-F, 0, alarm_bottom_z) * _DN50球阀竖直()

        # 6. 右侧两个出口安装10/11/12组件。
        #    右侧回路局部下水平管长 = run_length，12号压力表X = run_length + extension
        #    由 C 反推 run_length，保证12号压力表（最右侧）X = C
        right_port_x = 138.0
        right_extension = 60.0
        right_run_length = C - right_port_x - right_extension
        right_loop = translate(right_port_x, 0, alarm_center_z) * \
                     _右侧仪表回路(110.0, right_run_length)

        # 7. 主立管上的管卡（距主立管底部500mm处）。
        main_clamp = translate(0, 0, 500) * _管卡(pipe_od=main_od)
        main_clamp = main_clamp.color(0.55, 0.55, 0.58, 1.0)

        # 7b. 主立管管卡后方的延伸支撑柱：从主立管管卡后表面（R_outer）向 +Y 方向延伸到墙面，
        #     柱体总长 = G - R_outer。柱体截面 X×Z = 30×30（Z 与管卡宽度 strap_width 一致）。
        R_outer = main_od / 2 + 5  # strap_thickness = 5（与 _管卡 默认值一致）
        pillar_width = 2.0
        pillar_height = 30.0  # 与管卡宽度 strap_width = 30 一致
        pillar_y_length = G - R_outer
        support_pillar = translate(-pillar_width / 2, R_outer, 500 - pillar_height / 2) * \
                         scale(pillar_width, pillar_y_length, pillar_height) * Cube()
        support_pillar = support_pillar.color(0.55, 0.55, 0.58, 1.0)

        # 8. 左侧L型排水管竖直段上的管卡（同一高度z=500）。
        #    DN50排水管外径60（FilletPipe半径30）。
        drain_clamp = translate(-F, 0, 500) * _管卡(pipe_od=60.0)
        drain_clamp = drain_clamp.color(0.55, 0.55, 0.58, 1.0)

        # 8b. 排水管管卡后方的延伸支撑柱：与主立管支撑柱一摸一样。
        #     截面 2×30，柱体从管卡后表面延伸到墙面。
        drain_R_outer = 60.0 / 2 + 5  # 35
        drain_pillar_width = 2.0
        drain_pillar_height = 30.0
        drain_pillar_y_length = G - drain_R_outer
        drain_support_pillar = translate(-F - drain_pillar_width / 2,
                                         drain_R_outer,
                                         500 - drain_pillar_height / 2) * \
                              scale(drain_pillar_width, drain_pillar_y_length, drain_pillar_height) * Cube()
        drain_support_pillar = drain_support_pillar.color(0.55, 0.55, 0.58, 1.0)

        # 9. 新增左侧回路：延迟器右侧为过滤器+球阀支路；压力开关上方管路
        #    向右接水力警铃。函数返回 (整体, 延迟器, 压力开关,
        #    过滤器, 球阀, 水力警铃, 全部管段)。
        (new_loop, delayer, pressure_switch,
         filter_geometry, ball_valve, water_gong,
         new_pipes) = _新增左侧回路(A, E, F, H, D, B)

        # 9b. 新增左侧回路的竖直管上添加管卡 + 支撑柱（与主立管一摸一样）。
        #     竖直管位于 (-F, y_back=200, H) → (-F, y_back=200, z_delayer_bottom)。
        #     z_delayer_bottom = H + E + A + D - 332（与 _新增左侧回路 内一致）。
        new_loop_y_back = 200.0
        new_loop_z_bottom = H + E + A + D - 332
        new_loop_clamp_z = (H + new_loop_z_bottom) / 2  # 竖直管中点
        new_loop_clamp_od = 28.0  # DN20 管道外径
        new_loop_clamp = translate(-F, new_loop_y_back, new_loop_clamp_z) * \
                         _管卡(pipe_od=new_loop_clamp_od)
        new_loop_clamp = new_loop_clamp.color(0.55, 0.55, 0.58, 1.0)

        # 支撑柱：从管卡后表面延伸到墙面（与主立管支撑柱尺寸一摸一样）。
        # 由于该竖管本身已位于 y_back=200，剩余空间比主立管短。
        new_loop_R_outer = new_loop_clamp_od / 2 + 5  # 19
        new_loop_pillar_width = 2.0
        new_loop_pillar_height = 30.0
        new_loop_pillar_y_length = G - (new_loop_y_back + new_loop_R_outer)
        new_loop_pillar = translate(
            -F - new_loop_pillar_width / 2,
            new_loop_y_back + new_loop_R_outer,
            new_loop_clamp_z - new_loop_pillar_height / 2
        ) * scale(new_loop_pillar_width, new_loop_pillar_y_length, new_loop_pillar_height) * Cube()
        new_loop_pillar = new_loop_pillar.color(0.55, 0.55, 0.58, 1.0)

        # 9c. 水力警铃旁的水平管道（gong_supply_pipe 弯后段）加管卡 + 支撑柱。
        #     水平段位于 (X, y_back=200, z_tee_top)，从 -F+20 到 gong_inlet_x+2。
        #     警铃主体在 gong_inlet_x=100 右侧；管卡放在警铃进水口左侧。
        #     因为是水平管（X 方向），需要把管卡旋转 90°：
        #     绕 Y 轴把管卡的 Z 轴对齐到 X（管道方向），
        #     这样两根螺栓落在 +X/-X 位置（两边的洞口方向沿 X 管道方向），
        #     螺栓本身沿 Y 轴水平穿过管卡（与主立管管卡螺栓方向一致），
        #     螺母在 +Y 侧（朝向墙面），与主立管管卡的方位完全相同。
        gong_supply_z = H + E + A + D + 110  # z_tee_top
        gong_supply_x = 60  # 警铃进水口左侧约 40mm
        gong_supply_y = 200  # y_back
        gong_supply_clamp_od = 28.0  # DN20 管道外径
        gong_supply_clamp = translate(gong_supply_x, gong_supply_y, gong_supply_z) * \
                            rotate(Vec3(0, 1, 0), math.pi / 2) * \
                            _管卡(pipe_od=gong_supply_clamp_od)
        gong_supply_clamp = gong_supply_clamp.color(0.55, 0.55, 0.58, 1.0)

        # 支撑柱：从管卡后表面延伸到墙面（与主立管支撑柱尺寸一摸一样）。
        # 该水平管位于 y_back=200，剩余空间比主立管短。
        gong_supply_R_outer = gong_supply_clamp_od / 2 + 5  # 19
        gong_supply_pillar_width = 2.0
        gong_supply_pillar_height = 30.0
        gong_supply_pillar_y_length = G - (gong_supply_y + gong_supply_R_outer)  # 81
        gong_supply_pillar = translate(
            gong_supply_x - gong_supply_pillar_width / 2,
            gong_supply_y + gong_supply_R_outer,
            gong_supply_z - gong_supply_pillar_height / 2
        ) * scale(gong_supply_pillar_width, gong_supply_pillar_y_length, gong_supply_pillar_height) * Cube()
        gong_supply_pillar = gong_supply_pillar.color(0.55, 0.55, 0.58, 1.0)

        pieces = [main_pipe, butterfly, alarm, l_pipe, drain_ball, right_loop,
                  main_clamp, support_pillar, drain_clamp, drain_support_pillar,
                  new_loop, new_loop_clamp, new_loop_pillar,
                  gong_supply_clamp, gong_supply_pillar]
        if connecting_pipe is not None:
            pieces.append(connecting_pipe)
        overall = combine(*pieces)

        self['主立管'] = combine(main_pipe, connecting_pipe) if connecting_pipe is not None else main_pipe
        self['信号蝶阀'] = butterfly
        self['湿式报警阀'] = alarm
        self['左侧L型排水管'] = l_pipe
        self['DN50球阀'] = drain_ball
        self['右侧仪表回路'] = right_loop
        self['主立管管卡'] = main_clamp
        self['主立管支撑柱'] = support_pillar
        self['排水管管卡'] = drain_clamp
        self['排水管支撑柱'] = drain_support_pillar
        self['新增左侧回路'] = new_loop
        self['新增左侧回路管段'] = new_pipes
        self['新增左侧回路管卡'] = new_loop_clamp
        self['新增左侧回路支撑柱'] = new_loop_pillar
        self['水力警铃旁管卡'] = gong_supply_clamp
        self['水力警铃旁支撑柱'] = gong_supply_pillar
        self['延迟器'] = delayer
        self['压力开关'] = pressure_switch
        self['水力警铃'] = water_gong
        self['过滤器'] = filter_geometry
        self['DN20球阀'] = ball_valve
        self['整体'] = overall


def create_ZSFZ100基础阀组(**parameters):
    component = ZSFZ100基础阀组()
    for name, value in parameters.items():
        component[name] = value
    component.replace()
    return component


if __name__ == '__main__':
    FinalGeometry = ZSFZ100基础阀组()
    place(FinalGeometry)
