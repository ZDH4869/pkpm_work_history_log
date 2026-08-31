# -*- coding: utf-8 -*-
"""ZSFY 系列雨淋报警阀组整体装配（国标图集 04S206 第 28、29 页）。

所有零件几何全部内联在本文件中，不做任何跨文件 import，
满足 pyp3d「单文件、单 Component 子类」的约束。

==================== 一、图纸数据 ====================
雨淋阀组部件表（17 个编号）：
   1 消防给水管 100/150/200      2 信号阀 100/150/200
   3 试验信号阀 100/150/200      4 雨淋报警阀 ZSFY
   5 压力表 Y-100 (x3)           6 水力警铃 ZSJL
   7 压力开关 ZSJF               8 电磁阀 DN20
   9 手动开启阀 DN20            10 止回阀 DN20
  11 控制管球阀 DN20            12 报警球阀 DN20
  13 控制腔进水阀 DN40          14 过滤器 DN20
  15 试验放水阀 DN40            16 管卡 (x2)
  17 泄水阀 Q11f-16 DN50

雨淋阀组安装尺寸表：
  型号      A    B    C    D    E    F    G    H   公称直径 法兰外径 螺栓孔 螺栓
  ZSFY100  420  500  400  500  400  300  100  990  DN100   φ220   φ18  16xM16x160
  ZSFY150  480  580  400  500  400  370  100  960  DN150   φ280   φ23  16xM18x165
  ZSFY200  690  680  500  500  480  470  150  855  DN200   φ340   φ23  32xM20x180

图上另有直标尺寸：管卡(16)中心标高 500（地面至主立管管卡中心）。

【图纸表格勘误与取值口径】安装尺寸表「法兰连接尺寸」栏第三列标题为
「螺栓孔中心直径」，但其值 φ18 / φ23 / φ23 与法兰外径 φ220 / φ280 / φ340
明显不成比例——若真按 φ18 作分布圆，16 个 φ18 的通孔会互相重叠、并穿透
φ114 的主管，几何上不成立。故该列按其真实语义「螺栓通孔孔径」使用：
属性面板照表显示该列的名称与数值，建模也用同一数值作通孔孔径，两者统一。
螺栓在法兰上的分布圆直径表中未给出，按 GB/T 9119 PN16 取
φ180 / φ240 / φ295，作为隐藏参数『螺栓分布圆直径』。

==================== 二、坐标系与定位基准链 ====================
单位 mm；角度弧度制；右手坐标系。
  +Z 向上（主立管方向）；
  正视图为沿 +Y 方向观察，即观察者位于 -Y 侧，正视图屏幕右方 = +X；
  墙面位于 Y = +F，报警回路（水力警铃/报警球阀/试警铃球阀）贴墙布置。
局部原点（定位点）= 主立管与室内地面接触面的圆心。

竖向链（Z，自地面起算）：
  0                     室内地面（定位点）
  H                     信号阀(2)下法兰底面
  H + 信号阀结构长度     信号阀上法兰顶面 = 雨淋报警阀(4)底面
  H + A                 雨淋报警阀(4)上法兰顶面
  H + A + D             顶部水力警铃水平管轴线（阀组顶）
  500                   管卡(16)中心标高

正视方向链（X，以主立管轴线为 0）：
  -B  = -500  左侧最外缘（最左压力表外缘）
  +C  = +400  右侧最外缘（水力警铃外圆最右点）→ 警铃轴线 X = C - 警铃半径
  +E  = +400  泄水阀(17)排水立管轴线
  右侧另有一根试验放水阀(15)排水立管，图上未标注尺寸，按图面比例取 X = +610。

进深方向链（Y，主立管轴线为 0，墙面为 +F）：
  墙面        Y = +F
  报警回路面  Y = +(F - G)   水力警铃(6)/报警球阀(12)/试警铃球阀(13)
  雨淋阀检修盖 朝 -Y（正视图正前方）

==================== 三、装配拓扑 ====================
主通路   ：主立管(1) → 信号阀(2) → 雨淋报警阀(4) → 上部短管
           → 试验信号阀(3) → 主立管继续向上
法兰     ：全模型自下而上只有 3 个法兰，均由「下圆环 + 上圆环 + 贯穿螺栓
           + 上下六角螺帽」构成，不使用通用函数，重复件一律平移复制：
             法兰1 信号阀(2)   —— 对夹式，上下圆环净距 = 阀体结构长度
             法兰2 中部        —— 上下圆环仅隔一层垫片，位于雨淋阀上法兰
             法兰3 试验信号阀(3) —— 与法兰1 完全相同，由法兰1 整体平移复制
           雨淋阀的下法兰即法兰1 的上圆环，两者共用，故只有 3 个法兰。
报警回路 ：雨淋阀报警口(-X) → 后移至贴墙面 Y=+(F-G) → 报警立管向上
           （途中只串一只报警球阀(12)）→ 顶部转 +X 水平管 → 水力警铃(6)；
           水平管设管卡(16)，管卡另出一块锚固水平支撑板生根于墙
           压力开关(7) 挂在【报警立管】的 -X 侧（不在顶部水平管上）：
           立管引出水平支管 → 末端向上短竖管 → 接开关盒底面
控制回路 ：主立管供水侧(信号阀下方) → 控制管球阀(11) → 最左立管 / 控制立管
           控制立管自下而上：过滤器(14) → 止回阀(10) → 电磁阀(8) → 压力表(5)
           止回阀【竖直】安装，其阀体中心标高即控制腔进水管的轴线标高，
           DN40 控制腔进水管自阀体腰部水平引出接入雨淋阀控制腔，两者同高；
           该进水管上串一只控制腔进水阀(13)，在止回阀阀体外缘与控制腔接口
           之间居中布置（编号13 原为报警立管上的试警铃球阀，已移至此处，
           通径随管由 DN20 改为 DN40）；
           最左立管自下而上：手动开启阀(9) → 压力表(5)
试验放水 ：雨淋阀出口侧(试验信号阀下方) → +X 水平管 → 试验放水阀(15)
           → 弯头向下 → 排水立管；水平管上方接出水口压力表(5)
泄水回路 ：雨淋阀底部右侧 → 泄水阀(17) → +X 水平管 → 弯头向下
           → 排水立管（X = +E）
支吊架   ：管卡(16) 共 2 处，均带锚固水平支撑板生根于墙——
           Z=500 处抱主立管，顶部报警水平管处抱 DN20 报警管；
           支撑板端面按弦位嵌入抱箍，埋深受抱箍径向厚度限制，不触及被抱管道

==================== 三A、管路拐角的处理 ====================
凡是管路发生方向变化的地方，一律用 _折弯管（FilletPipe）一次生成连续的
「直管 + 圆弧弯头」，不允许两根直管在拐角处直角对接——那样两个管端截面
会裸露在外。本组件中的拐角包括：底部控制水平管 → 最左立管（编号11 球阀
之后的那个拐角）、报警口引出与后移段、报警立管顶部转水平、压力开关支管、
试验放水立管、泄水排水立管。

==================== 三B、驱动特征点（只设在管口） ====================
特征点只设在【水管的进口与出口】，共 5 个；法兰面、阀体中心、设备外形中心
等非管口位置一律不设。全部采用 SnapMode.GeometricCenter（管口圆截面的圆心）。
  进水 1 个：主立管进水口     （定位点本身，Z=0）
  出水 4 个：主立管出水口     （Z = H+A+D+主立管顶部延伸）
             泄水排水管出口   （X = E，Z = 排水管出口标高）
             试验放水立管出口 （X = 试验放水立管X，Z = H+A-试验放水立管下伸长度）
             水力警铃排水口   （随『水力警铃罩直径』联动）
公式中引用的参数必须 obvious=True，否则表达式引擎解析不到、特征点会退化到
世界原点；为此『主立管顶部延伸』『试验放水立管X』『试验放水立管下伸长度』
三项从隐藏参数提升为面板可见（置灰），归入「其他安装尺寸」组。

==================== 四、未标注尺寸的取值来源 ====================
图纸水平方向不按统一比例（B 段 0.72 px/mm、C 段 0.88 px/mm），
竖直方向经 A 段(0.95)、D 段(1.03) 验证约为 1.0 px/mm。
因此：竖向未标注位置按图面像素反推；水平向未标注位置按管件工程尺寸
与 B/C/E 的分配关系推定。所有推定值均注册为隐藏参数，可在面板外调整，
并在下方 MODEL_DIMS 中逐条注释来源。
"""

from pyp3d import *
import math


# ============================================================
# 全局配色
# ============================================================
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
# 通用工具
# ============================================================
def _空心管(start, end, outside_diameter, inside_diameter):
    """由起点、终点、外径、内径生成一段空心直管。"""
    return Cone(start, end, outside_diameter / 2.0, outside_diameter / 2.0) - \
           Cone(start, end, inside_diameter / 2.0, inside_diameter / 2.0)


def _折弯管(points, outside_diameter, inside_diameter, bend_radius=None):
    """用 FilletPipe 生成带真实圆弧弯头的折线管道（空心）。

    points        折线【拐点】序列 [(x, y, z), ...]，按介质走向顺序给出。
                  必须传两直线段的交点，不能传圆弧切点，否则弯头位置错误。
    bend_radius   弯曲半径，缺省取 1D（= 管外径）。

    首尾节点倒角半径固定为 0；中间节点的倒角半径按相邻两段管长收敛到
    0.45x较短段，保证同一段管上的两个弯头切点不会重叠；同时不小于
    0.55x外径，避免弯曲半径小于管半径导致弯头内侧自交。
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


def _圆截面X(x_position, radius, center_y=0.0, center_z=0.0):
    """法线沿 X 轴的圆截面（供 Loft 使用）。"""
    return translate(x_position, center_y, center_z) * \
           rotate(Vec3(0, 1, 0), math.pi / 2.0) * \
           Section(scale(radius) * Arc(2.0 * math.pi))


def _圆截面Y(y_position, radius, center_x=0.0, center_z=0.0):
    """法线沿 Y 轴的圆截面（供 Loft 使用）。"""
    return translate(center_x, y_position, center_z) * \
           rotate(Vec3(1, 0, 0), math.pi / 2.0) * \
           Section(scale(radius) * Arc(2.0 * math.pi))


def _圆截面Z(z_position, radius, center_x=0.0, center_y=0.0):
    """法线沿 Z 轴的圆截面（供 Loft 使用）。"""
    return translate(center_x, center_y, z_position) * \
           Section(scale(radius) * Arc(2.0 * math.pi))


def _椭圆截面Z(z_position, radius_x, radius_y):
    """法线沿 Z 轴的椭圆截面（铸造阀体轮廓用）。"""
    return translate(0, 0, z_position) * \
           Section(scale(radius_x, radius_y, 1.0) * Arc(2.0 * math.pi))


def _六角截面X(x_position, across_flats, center_y=0.0, center_z=0.0):
    """法线沿 X 的正六边形截面，across_flats 为对边距。"""
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


def _六角截面Y(y_position, across_flats, center_x=0.0, center_z=0.0):
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


def _六角柱Y(y_start, y_end, across_flats, center_x=0.0, center_z=0.0):
    result = Loft(
        _六角截面Y(y_start, across_flats, center_x, center_z),
        _六角截面Y(y_end, across_flats, center_x, center_z)
    )
    result.smooth = False
    return result


def _手轮(center_z, wheel_diameter, rim_width, thickness,
        spoke_count=3, spoke_width=None, hub_diameter=None):
    """轮面平行 XY 平面、轴线沿 Z 的手轮（轮缘 + 辐条 + 轮毂）。

    正视图中信号阀(2)/试验信号阀(3)/试验放水阀(15)/泄水阀(17) 的手轮均为
    辐条圆盘式；装配时再整体旋转到各自的轴线方向与轮面朝向。
    """
    wheel_radius = wheel_diameter / 2.0
    if spoke_width is None:
        spoke_width = max(wheel_diameter * 0.055, 3.0)
    if hub_diameter is None:
        hub_diameter = wheel_diameter * 0.20
    z0 = center_z - thickness / 2.0
    z1 = center_z + thickness / 2.0

    rim = Cone(Vec3(0, 0, z0), Vec3(0, 0, z1), wheel_radius, wheel_radius) - \
          Cone(Vec3(0, 0, z0 - 1.0), Vec3(0, 0, z1 + 1.0),
               wheel_radius - rim_width, wheel_radius - rim_width)

    spoke_length = wheel_radius - rim_width * 0.5
    spokes = []
    for index in range(spoke_count):
        angle = 2.0 * math.pi * index / spoke_count
        spokes.append(
            rotate(Vec3(0, 0, 1), angle) *
            translate(0, -spoke_width / 2.0, z0) *
            scale(spoke_length, spoke_width, thickness) * Cube()
        )

    hub = Cone(Vec3(0, 0, z0 - thickness * 0.35),
               Vec3(0, 0, z1 + thickness * 0.35),
               hub_diameter / 2.0, hub_diameter / 2.0)
    return combine(rim, hub, *spokes)



# ============================================================
# 编号2 / 编号3：信号阀 与 试验信号阀（蝶阀式，带手轮与信号装置）
# ============================================================
def _信号阀(structure_length=155.0, dn=100.0, body_outer_diameter=150.0,
          wheel_diameter=140.0, wheel_on_minus_x=True):
    """信号阀（编号2）/ 试验信号阀（编号3）共用体（对夹式蝶阀）。

    局部原点位于阀体几何中心，主流道轴线沿 Z（与主立管同轴）。
    传动：阀杆自阀体沿 ±X 伸出接入蜗轮箱，手轮装在蜗轮箱前方（-Y 侧），
    **轮面落在 XOZ 平面、轮轴沿 Y**，与阀组内其他星形手轮朝向一致；
    正视图中因此看到一个偏在主管左侧、正对观察者的完整圆形手轮。
    阀体上方带信号输出装置（微动开关盒），对应部件表「关闭时有电信号输出」。

    structure_length 为阀体两端连接面之间的结构长度（对夹式，不含法兰圆环）。
    """
    L = structure_length
    half_length = L / 2.0
    body_radius = body_outer_diameter / 2.0
    bore_radius = dn / 2.0
    wall = max(body_outer_diameter * 0.13, 8.0)
    body_inner_radius = body_radius - wall

    # ---------- 1. 阀体（两端为连接颈，中部鼓出的蝶阀体） ----------
    body_blank = Loft(
        _圆截面Z(-half_length, body_radius * 0.86),
        _圆截面Z(-half_length * 0.55, body_radius),
        _圆截面Z(half_length * 0.55, body_radius),
        _圆截面Z(half_length, body_radius * 0.86)
    )
    body_blank.smooth = True
    main_bore = Cone(
        Vec3(0, 0, -half_length - 2.0), Vec3(0, 0, half_length + 2.0),
        bore_radius, bore_radius
    )
    valve_body = body_blank - main_bore

    # 阀座衬圈（介于阀体内壁与通径之间）
    valve_seat = Cone(
        Vec3(0, 0, -half_length * 0.62), Vec3(0, 0, half_length * 0.62),
        body_inner_radius, body_inner_radius
    ) - main_bore

    # ---------- 2. 蝶板（阀轴沿 Y，蝶板法线沿 Z，图示为开启态） ----------
    disc_thickness = max(dn * 0.15, 12.0)
    butterfly = Cone(
        Vec3(0, -disc_thickness / 2.0, 0), Vec3(0, disc_thickness / 2.0, 0),
        bore_radius, bore_radius
    )
    butterfly = rotate(Vec3(0, 1, 0), math.pi / 2.0) * butterfly
    # 阀轴垂直于蝶板法线、垂直于流向，故沿 X 布置，一端接入蜗轮箱
    stem = Cone(
        Vec3(-body_radius, 0, 0), Vec3(body_radius, 0, 0),
        dn * 0.075, dn * 0.075
    )

    # ---------- 3. 阀杆支架、蜗轮箱与手轮（手轮轮面在 XOZ） ----------
    # sign_x 决定传动机构装在阀体的哪一侧；手轮始终朝 -Y（正视图观察者）
    sign_x = -1.0 if wheel_on_minus_x else 1.0
    bracket_length = body_radius * 0.95
    bracket_radius = body_outer_diameter * 0.26
    bracket = Cone(
        Vec3(sign_x * body_radius * 0.72, 0, 0),
        Vec3(sign_x * (body_radius + bracket_length), 0, 0),
        bracket_radius, bracket_radius * 0.82
    )

    gearbox_width = wheel_diameter * 0.50
    gearbox_depth = wheel_diameter * 0.42
    gearbox_height = wheel_diameter * 0.46
    gearbox_center_x = sign_x * (
        body_radius + bracket_length + gearbox_width / 2.0
    )
    gearbox = translate(
        gearbox_center_x - gearbox_width / 2.0,
        -gearbox_depth / 2.0, -gearbox_height / 2.0
    ) * scale(gearbox_width, gearbox_depth, gearbox_height) * Cube()

    # 手轮轴自蜗轮箱沿 -Y 伸出
    shaft_length = wheel_diameter * 0.20
    wheel_center_y = -(gearbox_depth / 2.0 + shaft_length)
    wheel_shaft = Cone(
        Vec3(gearbox_center_x, -gearbox_depth / 2.0 + 3.0, 0),
        Vec3(gearbox_center_x, wheel_center_y - wheel_diameter * 0.05, 0),
        dn * 0.055, dn * 0.055
    )

    # _手轮 生成的轮面在 XOY、轮轴沿 +Z；绕 X 轴 +90° 后 +Z 转到 -Y，
    # 轮面随之落到 XOZ 平面，正视图中即为一个完整的正圆
    wheel = translate(gearbox_center_x, wheel_center_y, 0) * \
        rotate(Vec3(1, 0, 0), math.pi / 2.0) * _手轮(
            0.0, wheel_diameter, wheel_diameter * 0.075,
            wheel_diameter * 0.055, spoke_count=3
        )
    wheel_nut = translate(
        gearbox_center_x, wheel_center_y - wheel_diameter * 0.05, 0
    ) * rotate(Vec3(1, 0, 0), math.pi / 2.0) * _六角柱Z(
        0.0, wheel_diameter * 0.07, dn * 0.13
    )

    # ---------- 4. 顶部信号装置（微动开关盒 + 出线口） ----------
    box_width = body_outer_diameter * 0.42
    box_depth = body_outer_diameter * 0.34
    box_height = body_outer_diameter * 0.30
    # 信号装置装在传动机构的对侧，避免与蜗轮箱、手轮抢位置
    box_x = -sign_x * body_radius * 0.35
    signal_box = translate(
        box_x, -box_depth / 2.0, half_length * 0.35
    ) * scale(box_width, box_depth, box_height) * Cube()
    conduit = Cone(
        Vec3(box_x + box_width * 0.5, 0, half_length * 0.35 + box_height),
        Vec3(box_x + box_width * 0.5, 0,
             half_length * 0.35 + box_height + box_height * 0.55),
        box_width * 0.16, box_width * 0.16
    )
    signal_set = combine(signal_box, conduit)

    # 传动机构已由 sign_x 直接建在目标一侧，无需再对整体做 180° 旋转
    # （若整体绕 Z 翻转，手轮会一并转到 +Y 朝墙，与图面不符）
    return combine(
        valve_body.color(*_色_铸铁),
        valve_seat.color(0.20, 0.22, 0.24, 1.0),
        butterfly.color(*_色_钢),
        stem.color(*_色_钢),
        combine(bracket, gearbox).color(*_色_铸铁亮),
        wheel_shaft.color(*_色_钢),
        combine(wheel, wheel_nut).color(0.16, 0.26, 0.72, 1.0),
        signal_set.color(0.24, 0.26, 0.30, 1.0)
    )


# ============================================================
# 编号4：雨淋报警阀 ZSFY（系统控制阀，隔膜式）
# ============================================================
def _阀体半宽系数(center_z, body_bottom, body_top):
    """雨淋阀铸造阀体在给定标高处的名义半宽系数（相对最大半宽）。

    返回 None 表示该标高落在上下连接颈段上，此时接口凸台的根部应改用
    连接颈半径起算，否则凸台会与阀体脱空。
    系数曲线与 _雨淋报警阀 中 body_sections 的椭圆轮廓保持一致：
    自下而上先由 0.93 涨到 1.00（最大半宽在 0.42 高度处），再收敛到 0.68。
    """
    if center_z <= body_bottom or center_z >= body_top:
        return None
    body_height = max(body_top - body_bottom, 1.0)
    height_ratio = (center_z - body_bottom) / body_height
    if height_ratio < 0.42:
        return 0.93 + (height_ratio / 0.42) * 0.07
    return 1.00 - (height_ratio - 0.42) / 0.58 * 0.32



def _雨淋报警阀(total_height=265.0, dn=100.0, connection_bore=114.0,
            body_width=260.0, body_depth=200.0,
            cover_width=230.0, cover_height=130.0,
            control_port_z=200.0, control_port_dn=20.0,
            control_port_od=28.0, control_port_length=40.0,
            alarm_port_z=60.0, alarm_port_dn=20.0,
            alarm_port_od=28.0, alarm_port_length=40.0,
            drain_port_z=30.0, drain_port_dn=50.0,
            drain_port_od=60.0, drain_port_length=55.0):
    """ZSFY 系列雨淋报警阀单体（系统控制阀，平时常闭、开启时输出报警水流信号）。

    坐标约定：
      主流道沿 +Z；隔膜腔检修盖位于 -Y（正视图正前方）；
      局部原点 = 阀体底面中心（即与信号阀上端连接面的贴合面）；
      阀体总高 = total_height = 安装尺寸 A - 信号阀结构长度。

    侧向接口（自上而下）：
      control_port  -X  DN20 控制腔接口（接控制管路：止回阀/电磁阀/手动开启阀）
      alarm_port    -X  DN20 报警信号接口（接报警管路 → 水力警铃/压力开关）
      drain_port    +X  DN50 泄水接口（接泄水阀17）

    三个接口的标高由装配层按各回路的实际管件尺寸链算出后传入，
    保证凸台端面与所接管段严格对齐，不会出现脱空或插入过深。
    """
    half_width = body_width / 2.0
    half_depth = body_depth / 2.0
    bore_radius = dn / 2.0
    neck_radius = connection_bore / 2.0 * 1.18

    # 主流道贯通孔：贯穿整个阀体，供各部件做布尔减
    main_bore = Cone(
        Vec3(0, 0, -3.0), Vec3(0, 0, total_height + 3.0),
        bore_radius, bore_radius
    )

    # 关键标高
    neck_bottom_height = total_height * 0.13   # 底部连接颈
    neck_top_height = total_height * 0.13      # 顶部连接颈
    body_bottom = neck_bottom_height
    body_top = total_height - neck_top_height

    # ---------- 1. 上下连接颈 ----------
    bottom_neck = Cone(
        Vec3(0, 0, 0.0), Vec3(0, 0, body_bottom + 4.0),
        neck_radius, neck_radius
    ) - main_bore
    top_neck = Cone(
        Vec3(0, 0, body_top - 4.0), Vec3(0, 0, total_height),
        neck_radius, neck_radius
    ) - main_bore

    # ---------- 2. 上窄下宽的铸造阀体（隔膜腔） ----------
    body_height = body_top - body_bottom
    body_sections = [
        _椭圆截面Z(body_bottom - 0.5, neck_radius * 1.02, neck_radius * 1.02),
        _椭圆截面Z(body_bottom + body_height * 0.16,
                 half_width * 0.93, half_depth * 0.94),
        _椭圆截面Z(body_bottom + body_height * 0.42, half_width, half_depth),
        _椭圆截面Z(body_bottom + body_height * 0.70,
                 half_width * 0.95, half_depth * 0.96),
        _椭圆截面Z(body_bottom + body_height * 0.90,
                 half_width * 0.68, half_depth * 0.72),
        _椭圆截面Z(body_top + 0.5, neck_radius * 1.02, neck_radius * 1.02)
    ]
    body_blank = Loft(*body_sections)
    body_blank.smooth = True
    body = body_blank - main_bore

    # ---------- 3. 正面隔膜腔检修盖（圆角矩形盖板 + 螺钉圈） ----------
    cover_center_z = body_bottom + body_height * 0.44
    cover_thickness = body_depth * 0.09
    cover_back_y = -half_depth * 0.94
    cover_front_y = cover_back_y - cover_thickness
    def rounded_rect_section_y(y_position, width, height, center_z):
        """正视图中的圆角矩形盖板截面（法线沿 Y）。

        levels 为 (z 方向比例, x 方向半宽比例) 序列，自底边右端沿右侧圆角
        向上、再沿左侧圆角向下闭合。首末项半宽比例取 0.78（非 0），
        使顶边与底边保留平直段，避免左右两串点在顶/底出现重复点导致截面退化。
        """
        half_w = width / 2.0
        half_h = height / 2.0
        levels = [
            (-1.00, 0.78), (-0.94, 0.92), (-0.84, 0.98),
            (-0.50, 1.00), (0.00, 1.00), (0.50, 1.00),
            (0.84, 0.98), (0.94, 0.92), (1.00, 0.78)
        ]
        right_points = [
            Vec3(half_w * w_ratio, y_position, center_z + half_h * z_ratio)
            for z_ratio, w_ratio in levels
        ]
        left_points = [
            Vec3(-half_w * w_ratio, y_position, center_z + half_h * z_ratio)
            for z_ratio, w_ratio in reversed(levels)
        ]
        points = right_points + left_points
        points.append(points[0])
        return Section(Line(*points))

    def rounded_rect_plate(width, height, y_start, y_end, center_z):
        result = Loft(
            rounded_rect_section_y(y_start, width, height, center_z),
            rounded_rect_section_y(y_end, width, height, center_z)
        )
        result.smooth = False
        return result

    cover_seat = rounded_rect_plate(
        cover_width + 12.0, cover_height + 12.0,
        cover_back_y + 3.0, cover_front_y + cover_thickness * 0.45,
        cover_center_z
    )
    cover_plate = rounded_rect_plate(
        cover_width, cover_height,
        cover_front_y + cover_thickness * 0.40, cover_front_y, cover_center_z
    )

    # 盖板周边 8 颗螺钉（正视图中沿圆角矩形边缘均布）
    screw_positions = [
        (-0.40, 0.42), (0.00, 0.48), (0.40, 0.42),
        (-0.48, 0.00), (0.48, 0.00),
        (-0.40, -0.42), (0.00, -0.48), (0.40, -0.42)
    ]
    screw_head_width = min(cover_width, cover_height) * 0.085
    cover_screws = []
    for x_ratio, z_ratio in screw_positions:
        screw_x = cover_width * x_ratio
        screw_z = cover_center_z + cover_height * z_ratio
        washer = Cone(
            Vec3(screw_x, cover_front_y, screw_z),
            Vec3(screw_x, cover_front_y - 2.0, screw_z),
            screw_head_width * 0.72, screw_head_width * 0.72
        )
        # 螺钉头轴线垂直于盖板面（沿 -Y），直接用法线沿 Y 的六角柱
        head = _六角柱Y(
            cover_front_y - 1.8, cover_front_y - 7.0,
            screw_head_width, screw_x, screw_z
        )
        cover_screws.extend([washer, head])
    screw_set = combine(*cover_screws)

    # ---------- 4. 侧向接口凸台 ----------
    def make_side_port(center_z, sign_x, nominal_diameter,
                       outside_diameter, length):
        """沿 ±X 伸出的接口凸台：根部埋入阀体、端部带承口台肩。"""
        outer_radius = outside_diameter / 2.0
        inner_radius = nominal_diameter / 2.0
        # 该标高处阀体的名义半宽；落在上下连接颈段时改用连接颈半径起算
        width_factor = _阀体半宽系数(center_z, body_bottom, body_top)
        if width_factor is None:
            root_x = sign_x * neck_radius
        else:
            root_x = sign_x * half_width * max(width_factor, 0.55)
        tip_x = root_x + sign_x * length
        tube = Cone(
            Vec3(0, 0, center_z), Vec3(tip_x, 0, center_z),
            outer_radius, outer_radius
        ) - main_bore
        tube = tube - Cone(
            Vec3(0, 0, center_z), Vec3(tip_x + sign_x * 1.0, 0, center_z),
            inner_radius, inner_radius
        )
        collar = Cone(
            Vec3(tip_x - sign_x * 12.0, 0, center_z),
            Vec3(tip_x + sign_x * 2.0, 0, center_z),
            outer_radius * 1.30, outer_radius * 1.30
        ) - Cone(
            Vec3(tip_x - sign_x * 13.0, 0, center_z),
            Vec3(tip_x + sign_x * 3.0, 0, center_z),
            inner_radius, inner_radius
        )
        return combine(tube, collar)

    control_port = make_side_port(
        control_port_z, -1.0, control_port_dn,
        control_port_od, control_port_length
    )
    alarm_port = make_side_port(
        alarm_port_z, -1.0, alarm_port_dn,
        alarm_port_od, alarm_port_length
    )
    drain_port = make_side_port(
        drain_port_z, 1.0, drain_port_dn,
        drain_port_od, drain_port_length
    )
    side_ports = combine(control_port, alarm_port, drain_port)

    # ---------- 5. 正面铭牌 ----------
    nameplate_width = cover_width * 0.26
    nameplate_height = cover_height * 0.17
    nameplate = translate(
        -nameplate_width / 2.0, cover_front_y - 1.5,
        cover_center_z - cover_height * 0.36
    ) * scale(nameplate_width, 1.5, nameplate_height) * Cube()

    return combine(
        combine(body, bottom_neck, top_neck).color(*_色_阀体红),
        cover_seat.color(*_色_阀体红暗),
        cover_plate.color(*_色_阀体红亮),
        screw_set.color(*_色_钢),
        side_ports.color(*_色_阀体红),
        nameplate.color(*_色_标牌黄)
    )


# ============================================================
# 编号5：压力表 Y-100（进水口 / 控制腔 / 出水口 共 3 只）
# ============================================================
def _压力表(dial_diameter=100.0, rod_height=88.0, rod_diameter=14.0):
    """弹簧管压力表 Y-100。

    连系杆底端位于局部原点、杆轴沿 +Z，表盘位于上方、盘面法线沿 Y；
    表壳背板在 +Y 侧、开口面与指针在 -Y 侧，装配时不作旋转，
    读数面即朝向正视图观察者。
    """
    dial_radius = dial_diameter / 2.0
    rod_radius = rod_diameter / 2.0

    stem_height = rod_height * 0.30
    taper_height = rod_height * 0.15
    disc_height = rod_height * 0.05
    gap = dial_diameter * 0.05
    pointer_length = dial_diameter * 0.85
    pointer_width = dial_diameter * 0.15
    case_depth = rod_diameter * 1.20
    case_back_thickness = case_depth * 0.10
    disc_radius = dial_diameter * 0.20
    taper_large_radius = disc_radius * 0.70
    taper_small_radius = disc_radius * 0.60

    z1 = stem_height
    z2 = z1 + disc_height
    z3 = z2 + taper_height
    z4 = z3 + taper_height
    z5 = z4 + disc_height
    z6 = z5 + stem_height + gap

    下杆 = Cone(Vec3(0, 0, 0), Vec3(0, 0, z1), rod_radius, rod_radius)
    下片 = Cone(Vec3(0, 0, z1), Vec3(0, 0, z2), disc_radius, disc_radius)
    下圆台 = Cone(Vec3(0, 0, z2), Vec3(0, 0, z3),
                taper_small_radius, taper_large_radius)
    上圆台 = Cone(Vec3(0, 0, z3), Vec3(0, 0, z4),
                taper_large_radius, taper_small_radius)
    上片 = Cone(Vec3(0, 0, z4), Vec3(0, 0, z5), disc_radius, disc_radius)
    上杆 = Cone(Vec3(0, 0, z5), Vec3(0, 0, z6), rod_radius, rod_radius)
    连系杆 = combine(下杆, 下片, 下圆台, 上圆台, 上片, 上杆)

    # 表壳：背板在 +Y（朝墙），开口面朝 -Y（朝正前方观察者）
    dial_z = z6 + dial_radius
    y_back = case_depth / 2.0
    y_face = y_back - case_back_thickness

    表壳 = Cone(Vec3(0, -y_back, dial_z), Vec3(0, y_back, dial_z),
              dial_radius, dial_radius) - \
          Cone(Vec3(0, -y_back, dial_z), Vec3(0, y_face, dial_z),
               dial_radius - gap, dial_radius - gap)
    刻度盘 = Cone(
        Vec3(0, y_face - 0.8, dial_z), Vec3(0, y_face, dial_z),
        dial_radius - gap, dial_radius - gap
    )

    # 指针贴在刻度盘前方、沿 -Y 扫出厚度，从开口面可见
    三角平面 = Section(Line(
        Vec3(-pointer_width / 2.0, y_face - 0.8, 0),
        Vec3(pointer_width / 2.0, y_face - 0.8, 0),
        Vec3(0, y_face - 0.8, pointer_length)
    ))
    扫掠体 = Sweep(三角平面, Line(Vec3(0, 0, 0), Vec3(0, -0.6 * y_face, 0)))
    指针 = translate(0, 0, dial_z) * roty(math.pi / 6.0) * \
         translate(0, 0, -pointer_length / 2.0) * 扫掠体

    return combine(
        连系杆.color(*_色_钢),
        表壳.color(0.20, 0.21, 0.24, 1.0),
        刻度盘.color(0.94, 0.94, 0.96, 1.0),
        指针.color(0.82, 0.05, 0.04, 1.0)
    )


# ============================================================
# 编号6：水力警铃 ZSJL
# ============================================================
def _水力警铃(bell_diameter=160.0, inlet_dn=20.0, outlet_dn=25.0,
          port_length=38.0):
    """水力警铃 ZSJL（报警阀开启时发出音响信号）。

    局部原点 = DN20 进水口外端面中心，进水管沿 +X 方向接入；
    铃罩与水轮壳体位于 -X 侧，排水口朝 -Z（向下自由排放）；
    铃罩盘面法线沿 Y，与正视图中的圆形轮廓一致。
    """
    bell_depth = bell_diameter * 0.26
    bell_sections = 16
    rim_thickness = bell_diameter * 0.025
    housing_diameter = bell_diameter * 0.525
    housing_depth = bell_diameter * 0.3125
    cover_diameter = bell_diameter * 0.55
    cover_thickness = bell_diameter * 0.031
    bolt_count = 8
    bolt_diameter = bell_diameter * 0.05
    bolt_height = bell_diameter * 0.031
    inlet_od = inlet_dn * 1.50
    outlet_od = outlet_dn * 1.44
    shaft_diameter = bell_diameter * 0.075
    center_bolt_diameter = bell_diameter * 0.075
    center_bolt_height = bell_diameter * 0.05
    outlet_length = bell_diameter * 0.625

    bell_radius = bell_diameter / 2.0
    housing_radius = housing_diameter / 2.0

    housing_x = -port_length - housing_radius
    bell_x = housing_x
    housing_back_y = -housing_depth / 2.0
    housing_front_y = housing_depth / 2.0
    bell_front_y = housing_back_y + bell_diameter * 0.056
    bell_back_y = bell_front_y - bell_depth

    # ---------- 1. 红色铃罩（沿 Y 逐层放样的碗形罩） ----------
    bell_profiles = []
    for index in range(bell_sections + 1):
        t = index / float(bell_sections)
        y_position = bell_back_y + bell_depth * t
        radius_factor = 0.72 + 0.28 * math.sin(math.pi * t / 2.0)
        bell_profiles.append(
            _圆截面Y(y_position, bell_radius * radius_factor, bell_x, 0.0)
        )
    bell_cover = Loft(*bell_profiles)
    bell_cover.smooth = True

    bell_rim = Cone(
        Vec3(bell_x, bell_front_y - rim_thickness, 0),
        Vec3(bell_x, bell_front_y + rim_thickness, 0),
        bell_radius, bell_radius
    ) - Cone(
        Vec3(bell_x, bell_front_y - rim_thickness - 1.0, 0),
        Vec3(bell_x, bell_front_y + rim_thickness + 1.0, 0),
        bell_radius - rim_thickness, bell_radius - rim_thickness
    )
    center_bolt = Cone(
        Vec3(bell_x, bell_back_y - center_bolt_height, 0),
        Vec3(bell_x, bell_back_y, 0),
        center_bolt_diameter / 2.0, center_bolt_diameter / 2.0
    )
    bell_set = combine(bell_cover, bell_rim, center_bolt)

    # ---------- 2. 水轮壳体与正面检修盖 ----------
    housing = Cone(
        Vec3(housing_x, housing_back_y, 0), Vec3(housing_x, housing_front_y, 0),
        housing_radius, housing_radius
    )
    housing_boss = Cone(
        Vec3(housing_x, housing_back_y - bell_diameter * 0.0375, 0),
        Vec3(housing_x, housing_back_y + bell_diameter * 0.05, 0),
        housing_radius * 0.72, housing_radius * 0.72
    )
    center_shaft = Cone(
        Vec3(bell_x, bell_front_y - bell_diameter * 0.031, 0),
        Vec3(bell_x, housing_front_y + cover_thickness, 0),
        shaft_diameter / 2.0, shaft_diameter / 2.0
    )
    housing_set = combine(housing, housing_boss, center_shaft)

    cover_start_y = housing_front_y
    cover_end_y = cover_start_y + cover_thickness
    cover_plate = Cone(
        Vec3(housing_x, cover_start_y, 0), Vec3(housing_x, cover_end_y, 0),
        cover_diameter / 2.0, cover_diameter / 2.0
    )
    cover_bolts = []
    bolt_circle_radius = cover_diameter * 0.37
    for index in range(bolt_count):
        angle = 2.0 * math.pi * index / bolt_count
        bolt_x = housing_x + bolt_circle_radius * math.cos(angle)
        bolt_z = bolt_circle_radius * math.sin(angle)
        cover_bolts.append(Cone(
            Vec3(bolt_x, cover_end_y, bolt_z),
            Vec3(bolt_x, cover_end_y + bolt_height, bolt_z),
            bolt_diameter / 2.0, bolt_diameter / 2.0
        ))
    cover_set = combine(cover_plate, *cover_bolts)

    # ---------- 3. DN20 进水口（沿 +X）与 DN25 排水口（沿 -Z） ----------
    inlet_connection_x = housing_x + housing_radius
    inlet = Cone(
        Vec3(0, 0, 0), Vec3(inlet_connection_x - 4.0, 0, 0),
        inlet_od / 2.0, inlet_od / 2.0
    ) - Cone(
        Vec3(1.0, 0, 0), Vec3(inlet_connection_x - 5.0, 0, 0),
        inlet_dn / 2.0, inlet_dn / 2.0
    )
    inlet_collar = Cone(
        Vec3(-8.0, 0, 0), Vec3(0, 0, 0), inlet_od * 0.62, inlet_od * 0.62
    ) - Cone(
        Vec3(-9.0, 0, 0), Vec3(1.0, 0, 0), inlet_dn / 2.0, inlet_dn / 2.0
    )

    outlet_start_z = -housing_radius
    outlet_end_z = outlet_start_z - outlet_length
    outlet = Cone(
        Vec3(housing_x, 0, outlet_start_z + 4.0),
        Vec3(housing_x, 0, outlet_end_z),
        outlet_od / 2.0, outlet_od / 2.0
    ) - Cone(
        Vec3(housing_x, 0, outlet_start_z + 5.0),
        Vec3(housing_x, 0, outlet_end_z - 1.0),
        outlet_dn / 2.0, outlet_dn / 2.0
    )
    ports = combine(inlet, inlet_collar, outlet)

    # ---------- 4. 击锤与支架 ----------
    bracket_y = housing_back_y - 2.0
    bracket_z = housing_radius * 0.72
    bracket_base = translate(
        housing_x - bell_diameter * 0.125, bracket_y - 4.0,
        bracket_z - bell_diameter * 0.05
    ) * scale(bell_diameter * 0.25, 8.0, bell_diameter * 0.10) * Cube()
    bracket_arm = translate(
        housing_x + bell_diameter * 0.0625, bracket_y - 4.0,
        bracket_z - bell_diameter * 0.05
    ) * rotate(Vec3(0, 1, 0), -math.pi / 6.0) * \
        scale(bell_diameter * 0.075, 8.0, bell_diameter * 0.30) * Cube()
    hammer_stem = Cone(
        Vec3(housing_x + bell_diameter * 0.075, bracket_y,
             bracket_z + bell_diameter * 0.075),
        Vec3(bell_x + bell_radius * 0.25, bell_front_y + 2.0,
             -bell_radius * 0.08),
        bell_diameter * 0.022, bell_diameter * 0.022
    )
    hammer_head = translate(
        bell_x + bell_radius * 0.25, bell_front_y + 2.0, -bell_radius * 0.08
    ) * scale(bell_diameter * 0.09) * Sphere()
    hammer_set = combine(bracket_base, bracket_arm, hammer_stem, hammer_head)

    return combine(
        bell_set.color(*_色_阀体红),
        housing_set.color(0.29, 0.31, 0.33, 1.0),
        cover_set.color(*_色_钢),
        ports.color(0.48, 0.50, 0.52, 1.0),
        hammer_set.color(0.40, 0.42, 0.44, 1.0)
    )


# ============================================================
# 编号7：压力开关 ZSJF
# ============================================================
def _压力开关(box_width=95.0, box_depth=62.0, box_height=70.0,
           cover_height=9.0):
    """压力开关 ZSJF（雨淋阀开启时输出电信号）。

    方形壳体，局部原点位于壳体底面中心，不含取压接管。

    按《压力开关位置详细图纸》，本开关不是吊在顶部水平管上，而是挂在
    报警立管的 -X 侧：立管上引出一段水平支管，再向上接到开关盒底面。
    这段「向上短竖管 + 水平支管 + 弯头」由装配层用 _折弯管 统一绘制，
    故本函数只出壳体本身，避免接管画两遍。
    """
    box = translate(-box_width / 2.0, -box_depth / 2.0, 0.0) * \
          scale(box_width, box_depth, box_height) * Cube()
    cover = translate(
        -box_width * 0.44, -box_depth * 0.45, box_height
    ) * scale(box_width * 0.88, box_depth * 0.90, cover_height) * Cube()

    cover_screws = []
    for sign_x in (-1.0, 1.0):
        for sign_y in (-1.0, 1.0):
            cover_screws.append(Cone(
                Vec3(sign_x * box_width * 0.38, sign_y * box_depth * 0.36,
                     box_height),
                Vec3(sign_x * box_width * 0.38, sign_y * box_depth * 0.36,
                     box_height + cover_height + 2.0),
                3.0, 3.0
            ))

    # 侧面出线口（朝 -X，即背离报警立管一侧）
    conduit = Cone(
        Vec3(-box_width / 2.0, 0, box_height * 0.55),
        Vec3(-box_width / 2.0 - box_width * 0.16, 0, box_height * 0.55),
        box_width * 0.09, box_width * 0.09
    )

    return combine(
        box.color(0.24, 0.26, 0.30, 1.0),
        cover.color(0.34, 0.36, 0.40, 1.0),
        combine(*cover_screws).color(*_色_钢),
        conduit.color(0.34, 0.36, 0.40, 1.0)
    )


# ============================================================
# 编号9 / 11 / 12 / 13 / 15 / 17：内螺纹截止阀（手轮式）通用体
# ============================================================
def _截止阀(dn=20.0, total_length=None, hex_width=None,
         body_diameter=None, wheel_diameter=None,
         stem_axis='minus_y', wheel_color=None):
    """内螺纹手轮截止阀 / 球阀通用体。

    生成时主流道沿 X（进口 -X、出口 +X），阀杆与手轮沿 +Z；
    局部原点位于阀体中心。stem_axis 决定最终阀杆朝向：
      'plus_z'   阀杆朝上（顶部操作）
      'minus_y'  阀杆朝正视图观察者（手轮正对 -Y，图中星形手轮的画法）

    未给定的尺寸按公称直径推算，比例取自 DN20 内螺纹截止阀实测值。
    """
    if total_length is None:
        total_length = dn * 2.80
    if hex_width is None:
        hex_width = dn * 1.50
    if body_diameter is None:
        body_diameter = dn * 1.90
    if wheel_diameter is None:
        wheel_diameter = dn * 2.65
    if wheel_color is None:
        wheel_color = (0.72, 0.025, 0.018, 1.0)

    half_total = total_length / 2.0
    body_length = total_length * 0.62
    half_body = body_length / 2.0
    body_radius = body_diameter / 2.0
    body_end_radius = body_diameter * 0.36
    bonnet_radius = body_diameter * 0.38

    main_bore = Cone(
        Vec3(-half_total - 2.0, 0, 0), Vec3(half_total + 2.0, 0, 0),
        dn / 2.0, dn / 2.0
    )

    # ---------- 1. 鼓形黄铜阀体 ----------
    body_blank = Loft(
        _圆截面X(-half_body, body_end_radius),
        _圆截面X(-half_body * 0.62, body_radius * 0.92),
        _圆截面X(0.0, body_radius),
        _圆截面X(half_body * 0.62, body_radius * 0.92),
        _圆截面X(half_body, body_end_radius)
    )
    body_blank.smooth = True
    body = body_blank - main_bore
    lower_chamber = translate(0, 0, -body_radius * 0.34) * scale(
        body_radius * 0.74, body_radius * 0.74, body_radius * 0.60
    ) * Sphere()

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

    # ---------- 3. 端口内螺纹可视化 ----------
    thread_rings = []
    thread_count = 4
    connector_length = half_total - half_body
    thread_pitch = max(connector_length * 0.20, 1.2)
    for index in range(thread_count):
        offset = connector_length * 0.18 + index * thread_pitch
        for direction in (-1.0, 1.0):
            x_position = direction * (half_total - offset)
            thread_rings.append(
                Cone(Vec3(x_position - 0.35, 0, 0), Vec3(x_position + 0.35, 0, 0),
                     dn / 2.0 + 0.5, dn / 2.0 + 0.5) -
                Cone(Vec3(x_position - 0.7, 0, 0), Vec3(x_position + 0.7, 0, 0),
                     max(dn / 2.0 - 0.4, 0.5), max(dn / 2.0 - 0.4, 0.5))
            )
    internal_threads = combine(*thread_rings)

    # ---------- 4. 阀盖、填料压盖与阀杆 ----------
    bonnet_start_z = body_radius * 0.42
    bonnet_height = body_diameter * 0.72
    bonnet_top_z = bonnet_start_z + bonnet_height
    bonnet = Loft(
        _圆截面Z(bonnet_start_z, bonnet_radius * 0.66),
        _圆截面Z(bonnet_start_z + bonnet_height * 0.30, bonnet_radius),
        _圆截面Z(bonnet_top_z - bonnet_height * 0.22, bonnet_radius * 0.78),
        _圆截面Z(bonnet_top_z, bonnet_radius * 0.62)
    )
    bonnet.smooth = True
    gland_height = body_diameter * 0.19
    gland = _六角柱Z(
        bonnet_top_z - 1.0, bonnet_top_z + gland_height, bonnet_radius * 1.30
    )

    stem_radius = dn * 0.155
    wheel_center_z = bonnet_top_z + gland_height + wheel_diameter * 0.20
    wheel_thickness = wheel_diameter * 0.075
    stem = Cone(
        Vec3(0, 0, bonnet_top_z + gland_height - 0.5),
        Vec3(0, 0, wheel_center_z + wheel_thickness * 0.9),
        stem_radius, stem_radius
    )
    stem_nut = _六角柱Z(
        wheel_center_z + wheel_thickness * 0.5,
        wheel_center_z + wheel_thickness * 1.6, stem_radius * 3.0
    )

    # ---------- 5. 星形手轮（正视图中的六辐手轮） ----------
    handwheel = _手轮(
        wheel_center_z, wheel_diameter, wheel_diameter * 0.095,
        wheel_thickness, spoke_count=6,
        spoke_width=wheel_diameter * 0.085,
        hub_diameter=wheel_diameter * 0.26
    )

    assembly = combine(
        combine(body, lower_chamber).color(*_色_黄铜),
        connectors.color(*_色_黄铜),
        internal_threads.color(*_色_黄铜暗),
        combine(bonnet, gland).color(*_色_黄铜亮),
        combine(stem, stem_nut).color(*_色_钢),
        handwheel.color(*wheel_color)
    )

    if stem_axis == 'minus_y':
        # 绕 X 轴 +90°：阀杆 +Z 转到 -Y，手轮正对观察者，主流道仍沿 X
        assembly = rotate(Vec3(1, 0, 0), math.pi / 2.0) * assembly
    return assembly


# ============================================================
# 编号8：电磁阀 DN20（探测器报警后联动开启雨淋报警阀）
# ============================================================
def _电磁阀(dn=20.0, total_length=68.0, hex_width=32.0,
         body_diameter=42.0, coil_diameter=52.0, coil_height=56.0):
    """DN20 常闭电磁阀。

    主流道沿 X（进口 -X、出口 +X），电磁线圈与接线盒沿 +Z；
    局部原点位于阀体中心。
    """
    half_total = total_length / 2.0
    body_length = total_length * 0.58
    half_body = body_length / 2.0
    body_radius = body_diameter / 2.0
    coil_radius = coil_diameter / 2.0

    main_bore = Cone(
        Vec3(-half_total - 2.0, 0, 0), Vec3(half_total + 2.0, 0, 0),
        dn / 2.0, dn / 2.0
    )

    # ---------- 1. 方直阀体与两端六角接头 ----------
    body = Loft(
        _圆截面X(-half_body, body_radius * 0.74),
        _圆截面X(-half_body * 0.5, body_radius),
        _圆截面X(half_body * 0.5, body_radius),
        _圆截面X(half_body, body_radius * 0.74)
    )
    body.smooth = True
    body = body - main_bore
    left_hex = _六角柱X(-half_total, -half_body + 0.5, hex_width) - main_bore
    right_hex = _六角柱X(half_body - 0.5, half_total, hex_width) - main_bore

    # ---------- 2. 阀盖颈与电磁线圈 ----------
    neck_bottom_z = body_radius * 0.45
    neck_top_z = body_radius + body_diameter * 0.22
    neck = Cone(
        Vec3(0, 0, neck_bottom_z), Vec3(0, 0, neck_top_z),
        body_diameter * 0.24, body_diameter * 0.22
    )
    coil_bottom_z = neck_top_z
    coil_top_z = coil_bottom_z + coil_height
    coil = Cone(
        Vec3(0, 0, coil_bottom_z), Vec3(0, 0, coil_top_z),
        coil_radius, coil_radius
    )
    coil_cap = Cone(
        Vec3(0, 0, coil_top_z), Vec3(0, 0, coil_top_z + coil_height * 0.12),
        coil_radius * 0.62, coil_radius * 0.48
    )

    # ---------- 3. 接线盒与手动应急复位钮 ----------
    box_width = coil_diameter * 0.62
    box_depth = coil_diameter * 0.46
    box_height = coil_height * 0.40
    junction_box = translate(
        coil_radius * 0.55, -box_depth / 2.0, coil_bottom_z + coil_height * 0.30
    ) * scale(box_width, box_depth, box_height) * Cube()
    conduit = Cone(
        Vec3(coil_radius * 0.55 + box_width, 0,
             coil_bottom_z + coil_height * 0.30 + box_height / 2.0),
        Vec3(coil_radius * 0.55 + box_width + box_width * 0.42, 0,
             coil_bottom_z + coil_height * 0.30 + box_height / 2.0),
        box_width * 0.16, box_width * 0.16
    )
    reset_knob = Cone(
        Vec3(0, 0, coil_top_z + coil_height * 0.12),
        Vec3(0, 0, coil_top_z + coil_height * 0.28),
        coil_radius * 0.30, coil_radius * 0.30
    )

    return combine(
        combine(body, left_hex, right_hex).color(*_色_黄铜),
        neck.color(*_色_黄铜亮),
        combine(coil, coil_cap).color(0.20, 0.22, 0.26, 1.0),
        combine(junction_box, conduit).color(0.28, 0.30, 0.34, 1.0),
        reset_knob.color(*_色_阀体红)
    )


# ============================================================
# 编号10：止回阀 DN20（立式，防止控制腔水压不稳产生误动作）
# ============================================================
def _止回阀(dn=20.0, total_height=190.0, body_diameter=110.0,
         hex_width=32.0, port_length=26.0, port_od=28.0):
    """DN20 立式止回阀（单向补水）。

    主流道沿 +Z（进口在下、出口在上），局部原点位于阀体底部接口端面中心；
    正视图中该阀表现为控制管路上一段竖直的圆柱形阀体。
    """
    body_radius = body_diameter / 2.0
    bore_radius = dn / 2.0
    body_bottom = port_length
    body_top = total_height - port_length

    main_bore = Cone(
        Vec3(0, 0, -2.0), Vec3(0, 0, total_height + 2.0),
        bore_radius, bore_radius
    )

    # ---------- 1. 圆柱形阀体（上下带过渡锥） ----------
    body_height = body_top - body_bottom
    body_blank = Loft(
        _圆截面Z(body_bottom, body_radius * 0.52),
        _圆截面Z(body_bottom + body_height * 0.10, body_radius),
        _圆截面Z(body_bottom + body_height * 0.88, body_radius),
        _圆截面Z(body_top, body_radius * 0.52)
    )
    body_blank.smooth = True
    body = body_blank - main_bore

    # ---------- 2. 上下六角内螺纹接口 ----------
    bottom_port = _六角柱Z(0.0, body_bottom + 2.0, hex_width) - main_bore
    top_port = _六角柱Z(body_top - 2.0, total_height, hex_width) - main_bore

    # ---------- 3. 中部检修盖法兰环与螺钉 ----------
    cover_z = body_bottom + body_height * 0.72
    cover_ring = Cone(
        Vec3(0, 0, cover_z), Vec3(0, 0, cover_z + body_diameter * 0.075),
        body_radius * 1.10, body_radius * 1.10
    ) - main_bore
    cover_screws = []
    screw_circle_radius = body_radius * 0.92
    for index in range(6):
        angle = 2.0 * math.pi * index / 6.0
        screw_x = screw_circle_radius * math.cos(angle)
        screw_y = screw_circle_radius * math.sin(angle)
        cover_screws.append(_六角柱Z(
            cover_z + body_diameter * 0.075,
            cover_z + body_diameter * 0.135,
            body_diameter * 0.075, screw_x, screw_y
        ))

    # ---------- 4. 上下接口与阀体之间的过渡台肩 ----------
    collar_radius = port_od * 0.62
    bottom_collar = Cone(
        Vec3(0, 0, body_bottom - 2.0), Vec3(0, 0, body_bottom + 6.0),
        collar_radius, collar_radius
    ) - main_bore
    top_collar = Cone(
        Vec3(0, 0, body_top - 6.0), Vec3(0, 0, body_top + 2.0),
        collar_radius, collar_radius
    ) - main_bore

    # ---------- 5. 端口内螺纹可视化 ----------
    thread_rings = []
    for index in range(3):
        for z_base in (4.0 + index * 4.0, total_height - 4.0 - index * 4.0):
            thread_rings.append(
                Cone(Vec3(0, 0, z_base - 0.35), Vec3(0, 0, z_base + 0.35),
                     bore_radius + 0.5, bore_radius + 0.5) -
                Cone(Vec3(0, 0, z_base - 0.7), Vec3(0, 0, z_base + 0.7),
                     max(bore_radius - 0.4, 0.5), max(bore_radius - 0.4, 0.5))
            )

    return combine(
        body.color(*_色_黄铜),
        combine(bottom_port, top_port).color(*_色_黄铜),
        combine(bottom_collar, top_collar).color(*_色_黄铜),
        cover_ring.color(*_色_黄铜亮),
        combine(*cover_screws).color(*_色_钢),
        combine(*thread_rings).color(*_色_黄铜暗)
    )


# ============================================================
# 编号14：过滤器 DN20（Y 型，过滤水中杂质防止管路堵塞）
# ============================================================
def _过滤器(dn=20.0, total_length=90.0, hex_width=32.0,
         body_diameter=40.0, basket_length=62.0, basket_diameter=34.0,
         basket_angle_deg=45.0):
    """DN20 Y 型过滤器。

    主流道沿 X（进口 -X、出口 +X），滤篮自阀体沿 -Z 方向斜向下 45°伸出；
    局部原点位于阀体中心，与正视图中止回阀下方那只斜置件对应。
    """
    half_total = total_length / 2.0
    body_radius = body_diameter / 2.0
    basket_radius = basket_diameter / 2.0
    basket_angle = math.radians(basket_angle_deg)

    main_bore = Cone(
        Vec3(-half_total - 2.0, 0, 0), Vec3(half_total + 2.0, 0, 0),
        dn / 2.0, dn / 2.0
    )

    # ---------- 1. 直通阀体 ----------
    body_length = total_length * 0.56
    half_body = body_length / 2.0
    body = Loft(
        _圆截面X(-half_body, body_radius * 0.72),
        _圆截面X(-half_body * 0.45, body_radius),
        _圆截面X(half_body * 0.45, body_radius),
        _圆截面X(half_body, body_radius * 0.72)
    )
    body.smooth = True
    body = body - main_bore
    left_hex = _六角柱X(-half_total, -half_body + 0.5, hex_width) - main_bore
    right_hex = _六角柱X(half_body - 0.5, half_total, hex_width) - main_bore

    # ---------- 2. 斜向下 45° 的滤篮（含端部锥形螺塞） ----------
    # 滤篮轴线在 XOZ 平面内，自阀体中心指向 +X 下方，与水平面成 45°
    direction = Vec3(math.sin(basket_angle), 0.0, -math.cos(basket_angle))
    basket_start = Vec3(0.0, 0.0, 0.0)
    basket_end = Vec3(
        direction.x * basket_length, 0.0, direction.z * basket_length
    )
    basket = Cone(
        basket_start, basket_end, basket_radius, basket_radius * 0.86
    ) - main_bore
    plug_start = Vec3(
        direction.x * (basket_length - 2.0), 0.0,
        direction.z * (basket_length - 2.0)
    )
    plug_end = Vec3(
        direction.x * (basket_length + basket_diameter * 0.42), 0.0,
        direction.z * (basket_length + basket_diameter * 0.42)
    )
    plug = Cone(
        plug_start, plug_end, basket_radius * 0.86, basket_radius * 0.72
    )

    return combine(
        body.color(*_色_黄铜),
        combine(left_hex, right_hex).color(*_色_黄铜),
        basket.color(*_色_黄铜亮),
        plug.color(*_色_钢)
    )


# ============================================================
# 编号16：管卡（固定管道，抱箍 + 双侧螺栓耳）
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
        Vec3(0, 0, -half_height), Vec3(0, 0, half_height),
        band_outer, band_outer
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
# 装配用朝向变换与固定管件尺寸
# ============================================================
def _转为竖直阀(part):
    """把「主流道沿 X、阀杆沿 +Z」的阀件转成「主流道沿 +Z、阀杆朝 -Y」。

    绕 Y 轴 -90°：主流道 +X → +Z，阀杆 +Z → -X；
    再绕 Z 轴 +90°：阀杆 -X → -Y（手轮正对观察者），主流道 +Z 不变。
    """
    return rotate(Vec3(0, 0, 1), math.pi / 2.0) * \
           rotate(Vec3(0, 1, 0), -math.pi / 2.0) * part


# 控制/报警/试验/泄水各回路的管件均为 DN20 / DN40 / DN50 标准件，
# 不随主通路公称直径变化，故其结构长度在此固定，供竖向尺寸链累加使用。
_过滤器长度 = 90.0        # DN20 Y 型过滤器沿流道方向总长
_止回阀高度 = 190.0       # DN20 立式止回阀总高
_电磁阀长度 = 68.0        # DN20 电磁阀沿流道方向总长
_DN20阀长度 = 56.0        # DN20 内螺纹截止阀/球阀总长
_DN15阀长度 = 42.0        # DN15 压力表前小截止阀总长
_DN40阀长度 = 112.0       # DN40 试验放水阀总长
_DN50阀长度 = 140.0       # DN50 泄水阀总长
_压力表杆高 = 88.0        # Y-100 压力表连系杆高度
_压力表盘径 = 100.0       # Y-100 压力表表盘直径
_压力表杆底至盘心 = 143.0  # 杆底到表盘中心的竖向距离（由 _压力表 几何推得）
_水力警铃罩直径 = 160.0   # ZSJL 水力警铃铃罩外径
# 控制腔进水阀（原图集编号13）：通径与 DN40 控制腔进水管一致；结构长度取
# 紧凑的 100 而非 DN40 标准的 112 —— ZSFY100 下止回阀阀体外缘到雨淋阀
# 控制腔接口只有 113mm 可用，取 112 会把该段填满、两端接不上管。
_控制腔进水阀通径 = 40.0
_控制腔进水阀长度 = 100.0


# ============================================================
# ZSFY 系列雨淋报警阀组 —— 整体装配
# ============================================================
class ZSFY雨淋报警阀组(Component):
    """ZSFY 系列雨淋报警阀组整体（04S206 部件表编号 1~17 全部）。

    定位点 = 主立管与室内地面接触面的圆心。
    切换『型号』时先查 MODEL_DIMS 刷新全部驱动尺寸，再按新尺寸重建几何。

    竖向定位策略：主通路各件的标高严格由安装尺寸表的 A / D / H 确定；
    各支路（控制/报警/试验/泄水）内部标高则由该回路实际管件的结构长度
    自下而上累加得出，而不是逐个填入图面估读值——这样管段与阀件首尾相接，
    改型号或改管件尺寸时不会出现脱开或重叠。雨淋阀三个侧向接口的标高
    也由对应回路算出后回传给 _雨淋报警阀，保证凸台端面与管段严格对齐。
    """

    MODEL_DIMS = {
        'ZSFY100': {
            # ---- 04S206 安装尺寸表 ----
            '尺寸A': 420.0, '尺寸B': 500.0, '尺寸C': 400.0, '尺寸D': 500.0,
            '尺寸E': 400.0, '尺寸F': 300.0, '尺寸G': 100.0, '尺寸H': 990.0,
            # ---- 主通路 ----
            '主管公称直径': 100.0, '主管外径': 114.0, '主管壁厚': 7.0,
            '信号阀公称直径': 100.0, '试验信号阀公称直径': 100.0,
            '雨淋报警阀公称直径': 100.0,
            # 对夹式蝶阀结构长度（GB/T 12238），即法兰上下圆环的净距
            '信号阀结构长度': 64.0, '试验信号阀结构长度': 64.0,
            '信号阀手轮直径': 140.0,
            # ---- 法兰连接尺寸（螺栓孔中心圆按 GB/T 9119 PN16 补全）----
            # 面板显示项：严格照安装尺寸表「法兰连接尺寸」栏的名称与数值
            '公称直径': 'DN100', '外径': 220.0,
            '螺栓孔中心直径': 18.0, '螺栓尺寸及数量': '16xM16x160',
            # 建模补充尺寸（面板隐藏）：表中未给出，按 GB/T 9119 PN16 取值
            '法兰厚度': 22.0, '螺栓分布圆直径': 180.0,
            '法兰螺栓数量': 16.0, '法兰螺栓长度': 160.0,
            '法兰垫片厚度': 3.0,
            # ---- 雨淋报警阀阀体 ----
            '雨淋阀阀体宽度': 260.0, '雨淋阀阀体深度': 200.0,
            '雨淋阀盖板宽度': 230.0, '雨淋阀盖板高度': 130.0,
            '雨淋阀报警口标高': 60.0, '雨淋阀泄水口标高': 30.0,
            # ---- D 段内的竖向分配 ----
            '上部短管长度': 242.0, '主立管顶部延伸': 150.0,
            '试验放水管相对标高': 110.0,
            # ---- 控制回路 ----
            '控制管取水降低量': 50.0,
            '控制立管首段长度': 130.0, '手动开启阀相对标高': 322.0,
            # 止回阀回滚为竖直安装，其阀体中心即控制腔水管标高
            '止回阀下连接段长度': 10.0, '止回阀结构长度': 190.0,
            '止回阀阀体外径': 110.0,
            '控制腔水管外径': 48.0, '控制腔水管壁厚': 3.5,
            '控制立管X': -320.0, '最左立管X': -450.0, '控制管球阀X': -160.0,
            # ---- 报警回路 ----
            '报警立管X': -230.0, '顶部管卡X': 40.0,
            '压力开关支管长度': 78.0, '压力开关支管相对顶标高': 90.0,
            # ---- 试验放水回路 ----
            '试验放水阀X': 500.0, '试验放水立管X': 610.0,
            '试验放水立管下伸长度': 210.0, '出水口压力表X': 250.0,
            # ---- 泄水回路 ----
            '排水管出口标高': 150.0,
            # ---- 管卡 ----
            '管卡中心标高': 500.0, '管卡厚度': 20.0, '管卡箍径向厚度': 14.0,
            '支撑柱宽度': 40.0, '支撑柱厚度': 20.0,
        },
        'ZSFY150': {
            '尺寸A': 480.0, '尺寸B': 580.0, '尺寸C': 400.0, '尺寸D': 500.0,
            '尺寸E': 400.0, '尺寸F': 370.0, '尺寸G': 100.0, '尺寸H': 960.0,
            '主管公称直径': 150.0, '主管外径': 168.0, '主管壁厚': 8.0,
            '信号阀公称直径': 150.0, '试验信号阀公称直径': 150.0,
            '雨淋报警阀公称直径': 150.0,
            '信号阀结构长度': 76.0, '试验信号阀结构长度': 76.0,
            '信号阀手轮直径': 165.0,
            '公称直径': 'DN150', '外径': 280.0,
            '螺栓孔中心直径': 23.0, '螺栓尺寸及数量': '16xM18x165',
            '法兰厚度': 24.0, '螺栓分布圆直径': 240.0,
            '法兰螺栓数量': 16.0, '法兰螺栓长度': 165.0,
            '法兰垫片厚度': 3.0,
            '雨淋阀阀体宽度': 341.0, '雨淋阀阀体深度': 262.0,
            '雨淋阀盖板宽度': 300.0, '雨淋阀盖板高度': 170.0,
            '雨淋阀报警口标高': 69.0, '雨淋阀泄水口标高': 35.0,
            '上部短管长度': 226.0, '主立管顶部延伸': 150.0,
            '试验放水管相对标高': 104.0,
            '控制管取水降低量': 50.0,
            '控制立管首段长度': 150.0, '手动开启阀相对标高': 371.0,
            # 止回阀回滚为竖直安装，其阀体中心即控制腔水管标高
            '止回阀下连接段长度': 10.0, '止回阀结构长度': 190.0,
            '止回阀阀体外径': 110.0,
            '控制腔水管外径': 48.0, '控制腔水管壁厚': 3.5,
            '控制立管X': -371.0, '最左立管X': -530.0, '控制管球阀X': -185.0,
            '报警立管X': -267.0, '顶部管卡X': 40.0,
            '压力开关支管长度': 78.0, '压力开关支管相对顶标高': 90.0,
            '试验放水阀X': 520.0, '试验放水立管X': 630.0,
            '试验放水立管下伸长度': 210.0, '出水口压力表X': 275.0,
            '排水管出口标高': 150.0,
            '管卡中心标高': 500.0, '管卡厚度': 20.0, '管卡箍径向厚度': 14.0,
            '支撑柱宽度': 40.0, '支撑柱厚度': 20.0,
        },
        'ZSFY200': {
            '尺寸A': 690.0, '尺寸B': 680.0, '尺寸C': 500.0, '尺寸D': 500.0,
            '尺寸E': 480.0, '尺寸F': 470.0, '尺寸G': 150.0, '尺寸H': 855.0,
            '主管公称直径': 200.0, '主管外径': 219.0, '主管壁厚': 8.0,
            '信号阀公称直径': 200.0, '试验信号阀公称直径': 200.0,
            '雨淋报警阀公称直径': 200.0,
            '信号阀结构长度': 89.0, '试验信号阀结构长度': 89.0,
            '信号阀手轮直径': 190.0,
            '公称直径': 'DN200', '外径': 340.0,
            '螺栓孔中心直径': 23.0, '螺栓尺寸及数量': '32xM20x180',
            '法兰厚度': 26.0, '螺栓分布圆直径': 295.0,
            '法兰螺栓数量': 32.0, '法兰螺栓长度': 180.0,
            '法兰垫片厚度': 3.0,
            '雨淋阀阀体宽度': 421.0, '雨淋阀阀体深度': 324.0,
            '雨淋阀盖板宽度': 372.0, '雨淋阀盖板高度': 210.0,
            '雨淋阀报警口标高': 112.0, '雨淋阀泄水口标高': 56.0,
            '上部短管长度': 209.0, '主立管顶部延伸': 150.0,
            '试验放水管相对标高': 96.0,
            '控制管取水降低量': 50.0,
            '控制立管首段长度': 236.0, '手动开启阀相对标高': 583.0,
            # 止回阀回滚为竖直安装，其阀体中心即控制腔水管标高
            '止回阀下连接段长度': 10.0, '止回阀结构长度': 190.0,
            '止回阀阀体外径': 110.0,
            '控制腔水管外径': 48.0, '控制腔水管壁厚': 3.5,
            '控制立管X': -435.0, '最左立管X': -630.0, '控制管球阀X': -215.0,
            '报警立管X': -313.0, '顶部管卡X': 50.0,
            '压力开关支管长度': 78.0, '压力开关支管相对顶标高': 90.0,
            '试验放水阀X': 560.0, '试验放水立管X': 690.0,
            '试验放水立管下伸长度': 210.0, '出水口压力表X': 310.0,
            '排水管出口标高': 150.0,
            '管卡中心标高': 500.0, '管卡厚度': 20.0, '管卡箍径向厚度': 14.0,
            '支撑柱宽度': 40.0, '支撑柱厚度': 20.0,
        },
    }

    def __init__(self):
        Component.__init__(self)

        # 面板分组顺序严格对应 04S206《雨淋阀组安装尺寸表》的栏目结构：
        #   ① 型号  ② 尺寸 A~H  ③ 法兰连接尺寸（公称直径/外径/螺栓孔中心直径/
        #   螺栓尺寸及数量），三组置顶；其后再接图上直标但未入表的其他安装尺寸、
        #   部件公称直径、专业属性与图纸部件表。

        # ===== ① 型号（驱动源：切换后 replace 查表刷新全部尺寸并重建几何） =====
        self['型号'] = Attr('ZSFY100', obvious=True, group='型号',
                           combo=['ZSFY100', 'ZSFY150', 'ZSFY200'])

        # ===== ② 尺寸（安装尺寸表 A~H 栏，按表列顺序，置灰不可手改） =====
        self['尺寸A'] = Attr(420.0, obvious=True, readonly=True, group='尺寸')
        self['尺寸B'] = Attr(500.0, obvious=True, readonly=True, group='尺寸')
        self['尺寸C'] = Attr(400.0, obvious=True, readonly=True, group='尺寸')
        self['尺寸D'] = Attr(500.0, obvious=True, readonly=True, group='尺寸')
        self['尺寸E'] = Attr(400.0, obvious=True, readonly=True, group='尺寸')
        self['尺寸F'] = Attr(300.0, obvious=True, readonly=True, group='尺寸')
        self['尺寸G'] = Attr(100.0, obvious=True, readonly=True, group='尺寸')
        self['尺寸H'] = Attr(990.0, obvious=True, readonly=True, group='尺寸')

        # ===== ③ 法兰连接尺寸（表中该栏 4 列，名称与数值一律照表） =====
        # 注：表中「螺栓孔中心直径」列的 φ18/φ23/φ23 与法兰外径 φ220/φ280/φ340
        # 不成比例，其真实语义是螺栓通孔孔径，建模即按通孔孔径使用这一数值，
        # 面板与建模取值统一。螺栓在法兰上的分布圆直径表中未给出，
        # 按 GB/T 9119 PN16 取 φ180/φ240/φ295，作为隐藏参数『螺栓分布圆直径』。
        self['公称直径'] = Attr('DN100', obvious=True, readonly=True,
                            group='法兰连接尺寸')
        self['外径'] = Attr(220.0, obvious=True, readonly=True,
                          group='法兰连接尺寸')
        self['螺栓孔中心直径'] = Attr(18.0, obvious=True, readonly=True,
                               group='法兰连接尺寸')
        self['螺栓尺寸及数量'] = Attr('16xM16x160', obvious=True, readonly=True,
                               group='法兰连接尺寸')

        # ===== ④ 其他安装尺寸（图上直标或建模必需，未列入尺寸表） =====
        # 本组中除『管卡中心标高』外，其余各项均被下方管口特征点的公式引用。
        # 驱动点公式只能解析 obvious=True 的数值参数，隐藏参数会解析失败、
        # 使特征点退化到世界原点，故这些参数必须留在面板上（置灰不可改）。
        self['管卡中心标高'] = Attr(500.0, obvious=True, readonly=True,
                               group='其他安装尺寸')
        self['主立管顶部延伸'] = Attr(150.0, obvious=True, readonly=True,
                               group='其他安装尺寸')
        self['排水管出口标高'] = Attr(150.0, obvious=True, readonly=True,
                               group='其他安装尺寸')
        self['试验放水立管X'] = Attr(610.0, obvious=True, readonly=True,
                               group='其他安装尺寸')
        self['试验放水立管下伸长度'] = Attr(210.0, obvious=True, readonly=True,
                                  group='其他安装尺寸')

        # ===== ⑤ 各部件公称直径（对应部件表「型号」列） =====
        self['消防给水管公称直径'] = Attr(100.0, obvious=True, readonly=True,
                                 group='部件公称直径')
        self['信号阀公称直径'] = Attr(100.0, obvious=True, readonly=True,
                              group='部件公称直径')
        self['试验信号阀公称直径'] = Attr(100.0, obvious=True, readonly=True,
                                group='部件公称直径')
        self['雨淋报警阀公称直径'] = Attr(100.0, obvious=True, readonly=True,
                                group='部件公称直径')
        self['控制管路公称直径'] = Attr(20.0, obvious=True, readonly=True,
                               group='部件公称直径')
        self['控制腔进水管公称直径'] = Attr(40.0, obvious=True, readonly=True,
                                  group='部件公称直径')
        self['报警管路公称直径'] = Attr(20.0, obvious=True, readonly=True,
                               group='部件公称直径')
        self['试验放水阀公称直径'] = Attr(40.0, obvious=True, readonly=True,
                                group='部件公称直径')
        self['泄水阀公称直径'] = Attr(50.0, obvious=True, readonly=True,
                              group='部件公称直径')
        self['水力警铃罩直径'] = Attr(160.0, obvious=True, readonly=True,
                              group='部件公称直径')

        # ===== ⑥ 专业属性（部件型号与系统信息） =====
        self['名称'] = Attr('ZSFY系列雨淋报警阀组', obvious=True, readonly=True,
                          group='专业属性')
        self['图集编号'] = Attr('04S206 第28-29页', obvious=True, readonly=True,
                            group='专业属性')
        self['雨淋报警阀型号'] = Attr('ZSFY', obvious=True, group='专业属性')
        self['压力表型号'] = Attr('Y-100', obvious=True, group='专业属性')
        self['水力警铃型号'] = Attr('ZSJL', obvious=True, group='专业属性')
        self['压力开关型号'] = Attr('ZSJF', obvious=True, group='专业属性')
        self['泄水阀型号'] = Attr('Q11f-16', obvious=True, group='专业属性')
        self['系统类型'] = Attr('雨淋系统', obvious=True, group='专业属性')

        # ===== ⑦ 图纸部件表（编号 / 型号 / 用途 / 平时与失火时工作状态） =====
        self['01_消防给水管'] = Attr(
            'DN100/150/200 / 供水 / 平时：充满水 / 失火时：充满水',
            obvious=True, readonly=True, group='图纸部件表')
        self['02_信号阀'] = Attr(
            'DN100/150/200 / 供水控制阀，阀门关闭时有电信号输出 '
            '/ 平时：常开 / 失火时：开',
            obvious=True, readonly=True, group='图纸部件表')
        self['03_试验信号阀'] = Attr(
            'DN100/150/200 / 平时常开，试验雨淋阀时关闭，关闭时有电信号输出 '
            '/ 平时：常开 / 失火时：关',
            obvious=True, readonly=True, group='图纸部件表')
        self['04_雨淋报警阀'] = Attr(
            'ZSFY / 系统控制阀，开启时可输出报警水流信号 '
            '/ 平时：常闭 / 失火时：自动开启',
            obvious=True, readonly=True, group='图纸部件表')
        self['05_压力表'] = Attr(
            'Y-100 / 数量：3 / 显示水压',
            obvious=True, readonly=True, group='图纸部件表')
        self['06_水力警铃'] = Attr(
            'ZSJL / 报警阀开启时发出音响信号 / 平时：不动作 / 失火时：报警',
            obvious=True, readonly=True, group='图纸部件表')
        self['07_压力开关'] = Attr(
            'ZSJF / 雨淋阀开启时发出电信号 / 平时：不动作 / 失火时：输出电信号',
            obvious=True, readonly=True, group='图纸部件表')
        self['08_电磁阀'] = Attr(
            'DN20 / 探测器报警后联动开启雨淋报警阀 / 失火时：常闭',
            obvious=True, readonly=True, group='图纸部件表')
        self['09_手动开启阀'] = Attr(
            'DN20 / 火灾时现场手动应急开启雨淋报警阀 / 平时：常闭 / 失火时：常闭',
            obvious=True, readonly=True, group='图纸部件表')
        self['10_止回阀'] = Attr(
            'DN20 / 单向补水，防止控制腔水压不稳产生误动作 '
            '/ 平时：常开 / 失火时：常开',
            obvious=True, readonly=True, group='图纸部件表')
        self['11_控制管球阀'] = Attr(
            'DN20 / 控制控制腔供水 / 平时：常开 / 失火时：常开',
            obvious=True, readonly=True, group='图纸部件表')
        self['12_报警球阀'] = Attr(
            'DN20 / 手动关闭后可消除报警 / 平时：常开 / 失火时：常开',
            obvious=True, readonly=True, group='图纸部件表')
        self['13_控制腔进水阀'] = Attr(
            'DN40 / 图集原编号13为试警铃球阀（DN20，串在报警立管上）；本模型'
            '按现场做法移至控制腔进水管，作进水控制阀，通径随管改为 DN40 '
            '/ 平时：常开 / 失火时：常开',
            obvious=True, readonly=True, group='图纸部件表')
        self['14_过滤器'] = Attr(
            'DN20 / 过滤水中杂质，防止管路堵塞 / 平时：通流 / 失火时：通流',
            obvious=True, readonly=True, group='图纸部件表')
        self['15_试验放水阀'] = Attr(
            'DN40 / 系统调试或功能试验时打开放水 / 平时：常闭',
            obvious=True, readonly=True, group='图纸部件表')
        self['16_管卡'] = Attr(
            '数量：2 / 固定管道',
            obvious=True, readonly=True, group='图纸部件表')
        self['17_泄水阀'] = Attr(
            'Q11f-16 DN50 / 系统检修时排空放水',
            obvious=True, readonly=True, group='图纸部件表')

        # ===== 驱动尺寸（面板隐藏，切型号时由 MODEL_DIMS 刷新） =====
        for _隐藏参数 in (
            '主管公称直径', '主管外径', '主管壁厚',
            '法兰厚度', '螺栓分布圆直径', '法兰螺栓数量', '法兰螺栓长度',
            '法兰垫片厚度',
            '信号阀结构长度', '试验信号阀结构长度', '信号阀手轮直径',
            '雨淋阀阀体宽度', '雨淋阀阀体深度',
            '雨淋阀盖板宽度', '雨淋阀盖板高度',
            '雨淋阀报警口标高', '雨淋阀泄水口标高',
            '上部短管长度', '试验放水管相对标高',
            '控制管取水降低量', '控制立管首段长度', '手动开启阀相对标高',
            '止回阀下连接段长度', '止回阀结构长度', '止回阀阀体外径',
            '控制腔水管外径', '控制腔水管壁厚',
            '控制立管X', '最左立管X', '控制管球阀X',
            '报警立管X', '顶部管卡X',
            '压力开关支管长度', '压力开关支管相对顶标高',
            '试验放水阀X', '出水口压力表X',
            '管卡厚度', '管卡箍径向厚度', '支撑柱宽度', '支撑柱厚度',
        ):
            self[_隐藏参数] = Attr(
                float(self.MODEL_DIMS['ZSFY100'][_隐藏参数]), obvious=False
            )

        # ===== 输出属性（只让『整体』作为显示槽位，避免重复渲染） =====
        self['主立管'] = Attr(None)
        self['法兰连接'] = Attr(None)
        self['信号阀'] = Attr(None)
        self['雨淋报警阀'] = Attr(None)
        self['试验信号阀'] = Attr(None)
        self['控制回路'] = Attr(None)
        self['报警回路'] = Attr(None)
        self['水力警铃'] = Attr(None)
        self['压力开关'] = Attr(None)
        self['试验放水回路'] = Attr(None)
        self['泄水回路'] = Attr(None)
        self['管卡'] = Attr(None)
        self['整体'] = Attr(None, show=True)

        # ===== 驱动特征点：只设在【水管的进口与出口】 =====
        # 本阀组对外连通的水管口共 5 个（下列），其余位置（法兰面、阀体中心、
        # 设备外形中心等）不属于管口，一律不设特征点。
        #   进水 1 个：主立管下端（消防给水管进水口）
        #   出水 4 个：主立管上端（送往系统侧）、泄水排水管出口、
        #             试验放水立管出口、水力警铃排水口
        # 每个点都是管口圆截面的圆心，属于闭合截面的几何中心，
        # 一律用 GeometricCenter；EndPoint 只留给角点/顶点，本组件不涉及。
        #
        # 公式规则：三轴各自以 [定位点X/Y/Z] 起算；只引用 obvious=True 的数值
        # 参数；运算符限 + - * / ( ) . ^，不得出现逗号、** 或 Python 表达式。
        z_group_top = '[定位点Z]+[尺寸H]+[尺寸A]+[尺寸D]'

        # 1) 主立管进水口：主立管底端与地面接触面的圆心，即组件定位点本身
        self.setDrivenFeaturePoint(
            '主立管进水口', SnapMode.GeometricCenter,
            '[定位点X]', '[定位点Y]', '[定位点Z]')

        # 2) 主立管出水口：主立管顶端截面圆心，送往系统侧
        self.setDrivenFeaturePoint(
            '主立管出水口', SnapMode.GeometricCenter,
            '[定位点X]', '[定位点Y]',
            z_group_top + '+[主立管顶部延伸]')

        # 3) 泄水排水管出口：泄水阀(17)后 DN50 排水立管的下端管口
        self.setDrivenFeaturePoint(
            '泄水排水管出口', SnapMode.GeometricCenter,
            '[定位点X]+[尺寸E]', '[定位点Y]',
            '[定位点Z]+[排水管出口标高]')

        # 4) 试验放水立管出口：试验放水阀(15)后 DN40 排水立管的下端管口
        self.setDrivenFeaturePoint(
            '试验放水立管出口', SnapMode.GeometricCenter,
            '[定位点X]+[试验放水立管X]', '[定位点Y]',
            '[定位点Z]+[尺寸H]+[尺寸A]-[试验放水立管下伸长度]')

        # 5) 水力警铃排水口：警铃(6)下方 DN25 排水短管的下端管口。
        #    警铃壳体轴线距其进水口端面 38+罩径*0.2625，排水口自壳体轴线
        #    再向下 罩径*0.8875，两者均随『水力警铃罩直径』联动。
        self.setDrivenFeaturePoint(
            '水力警铃排水口', SnapMode.GeometricCenter,
            '[定位点X]+[尺寸C]-38-[水力警铃罩直径]*0.2625',
            '[定位点Y]+[尺寸F]-[尺寸G]',
            z_group_top + '-[水力警铃罩直径]*0.8875')

        self.replace()

    @export
    def replace(self):
        # ===== 0. 防止属性自更新触发递归调用 =====
        if not getattr(self, '_refreshing_dims', False):
            dims = self.MODEL_DIMS.get(self['型号'], self.MODEL_DIMS['ZSFY100'])
            self._refreshing_dims = True
            try:
                for key, value in dims.items():
                    self[key] = value
                # 部件表「型号」列中随主通路联动的公称直径
                self['消防给水管公称直径'] = dims['主管公称直径']
            finally:
                self._refreshing_dims = False

        # ===== 1. 读取参数 =====
        A = self['尺寸A']
        C = self['尺寸C']
        D = self['尺寸D']
        E = self['尺寸E']
        F = self['尺寸F']
        G = self['尺寸G']
        H = self['尺寸H']

        main_od = self['主管外径']
        main_id = main_od - 2.0 * self['主管壁厚']
        main_radius = main_od / 2.0
        main_dn = self['主管公称直径']

        flange_od = self['外径']
        flange_t = self['法兰厚度']
        # 表中「螺栓孔中心直径」列的 φ18/φ23/φ23 实为螺栓通孔孔径
        #（φ18 不可能是 16 个孔的分布圆），建模即按通孔孔径使用该数值，
        # 与面板显示保持同一个数；螺栓在法兰上的分布圆另取隐藏参数。
        bolt_hole_d = self['螺栓孔中心直径']
        bolt_hole_r = bolt_hole_d / 2.0
        bolt_circle_r = self['螺栓分布圆直径'] / 2.0
        bolt_count = int(round(self['法兰螺栓数量']))
        bolt_length = self['法兰螺栓长度']
        gasket_t = self['法兰垫片厚度']

        signal_length = self['信号阀结构长度']
        test_length = self['试验信号阀结构长度']
        wheel_diameter = self['信号阀手轮直径']
        valve_body_od = flange_od * 0.68

        deluge_body_width = self['雨淋阀阀体宽度']
        deluge_body_depth = self['雨淋阀阀体深度']
        deluge_cover_width = self['雨淋阀盖板宽度']
        deluge_cover_height = self['雨淋阀盖板高度']

        upper_stub = self['上部短管长度']
        top_margin = self['主立管顶部延伸']

        # 支路管径：均为标准件，不随主通路公称直径变化
        control_od, control_id = 28.0, 21.0     # 控制管路 DN20
        alarm_od, alarm_id = 28.0, 21.0         # 报警管路 DN20
        gauge_od, gauge_id = 22.0, 15.0         # 压力表支管 DN15
        test_od, test_id = 48.0, 41.0           # 试验放水管 DN40
        drain_od, drain_id = 60.0, 53.0         # 泄水/排水管 DN50
        # 接入雨淋阀控制腔的水管：按要求加大到 DN40，止回阀水平串接其上
        chamber_od = self['控制腔水管外径']
        chamber_id = chamber_od - 2.0 * self['控制腔水管壁厚']

        # 雨淋阀三个侧向接口的伸出长度（与传给 _雨淋报警阀 的值保持一致）
        control_port_length = 40.0
        alarm_port_length = 40.0
        drain_port_length = 55.0

        # ===== 2. 主通路竖向基准链（自地面起算） =====
        # 信号阀与试验信号阀均为【对夹式】：一个法兰连接 = 上下两个圆环夹住
        # 阀体、长螺栓贯穿，因此阀体上下各占一个法兰圆环的厚度，尺寸链必须计入。
        # 全模型自下而上只有 3 个法兰：法兰1(信号阀) / 法兰2(中部) / 法兰3(试验信号阀)。
        z_f1_ring0_bottom = H                          # 法兰1 下圆环底面 = 尺寸 H 终点
        z_f1_ring0_top = z_f1_ring0_bottom + flange_t
        z_signal_body_bottom = z_f1_ring0_top          # 信号阀阀体底面
        z_signal_body_top = z_signal_body_bottom + signal_length
        z_f1_ring1_bottom = z_signal_body_top          # 法兰1 上圆环底面
        z_f1_ring1_top = z_f1_ring1_bottom + flange_t
        z_deluge_bottom = z_f1_ring1_top               # 雨淋阀底面（与法兰1上圆环共面）

        # 法兰2（中部）两个圆环之间只隔一层垫片，其上圆环顶面 = 安装尺寸 A 的终点
        z_stub_base = H + A                            # 上部短管起点
        z_f2_ring1_top = z_stub_base
        z_f2_ring1_bottom = z_f2_ring1_top - flange_t
        z_f2_ring0_top = z_f2_ring1_bottom - gasket_t
        z_f2_ring0_bottom = z_f2_ring0_top - flange_t
        z_deluge_top = z_f2_ring0_bottom               # 雨淋阀阀体顶面
        deluge_height = z_deluge_top - z_deluge_bottom

        # 法兰3 与法兰1 构造完全相同，只是整体上移；下面用平移复制生成
        z_f3_ring0_bottom = z_stub_base + upper_stub
        z_f3_offset = z_f3_ring0_bottom - z_f1_ring0_bottom
        z_test_body_bottom = z_f3_ring0_bottom + flange_t
        z_test_body_top = z_test_body_bottom + test_length
        z_f3_ring1_top = z_test_body_top + flange_t

        z_group_top = H + A + D                        # 顶部报警水平管轴线
        z_main_top = z_group_top + top_margin          # 主立管顶（继续向上）

        y_alarm = F - G      # 报警回路所在的进深平面（贴墙侧）
        y_wall = F           # 墙内表面

        # ===== 3. 控制回路竖向尺寸链（由管件结构长度自下而上累加） =====
        z_ctrl_h = H - self['控制管取水降低量']       # 底部控制水平管轴线
        z_filter_0 = z_ctrl_h + self['控制立管首段长度']
        z_filter_1 = z_filter_0 + _过滤器长度
        # 止回阀竖直串在控制立管上；其【阀体中心】即控制腔进水管的轴线标高，
        # 即水管自阀体腰部水平引出，两者「相同高度」。
        z_check_0 = z_filter_1 + self['止回阀下连接段长度']
        check_length = self['止回阀结构长度']
        z_check_1 = z_check_0 + check_length
        z_chamber = (z_check_0 + z_check_1) / 2.0
        z_solenoid_0 = z_check_1 + 15.0
        z_solenoid_1 = z_solenoid_0 + _电磁阀长度
        z_gauge_control = z_solenoid_1 + 22.0         # 控制腔压力表(5)杆底

        z_manual_0 = z_ctrl_h + self['手动开启阀相对标高']
        z_manual_1 = z_manual_0 + _DN20阀长度
        z_gauge_supply = z_manual_1 + 22.0            # 进水侧压力表(5)杆底

        # ===== 4. 雨淋阀侧向接口标高与端部 X 坐标 =====
        # 控制腔接口标高由控制回路算出，保证凸台端面与 DN40 水管严格对齐
        control_port_z = z_chamber - z_deluge_bottom
        alarm_port_z = self['雨淋阀报警口标高']
        drain_port_z = self['雨淋阀泄水口标高']

        deluge_half_width = deluge_body_width / 2.0
        deluge_neck_radius = main_radius * 1.18
        deluge_body_bottom = deluge_height * 0.13
        deluge_body_top = deluge_height - deluge_height * 0.13

        def port_tip_x(port_z, sign_x, port_length):
            """接口凸台端面的 X 坐标（与 _雨淋报警阀 内部算法一致）。"""
            factor = _阀体半宽系数(port_z, deluge_body_bottom, deluge_body_top)
            if factor is None:
                root = deluge_neck_radius
            else:
                root = deluge_half_width * max(factor, 0.55)
            return sign_x * (root + port_length)

        x_control_tip = port_tip_x(control_port_z, -1.0, control_port_length)
        x_alarm_tip = port_tip_x(alarm_port_z, -1.0, alarm_port_length)
        x_drain_tip = port_tip_x(drain_port_z, 1.0, drain_port_length)

        z_alarm_port = z_deluge_bottom + alarm_port_z
        z_drain_port = z_deluge_bottom + drain_port_z

        # ===== 5. 主立管与三只主阀 =====
        main_pipe = combine(
            _空心管(Vec3(0, 0, 0.0), Vec3(0, 0, z_f1_ring0_bottom),
                  main_od, main_id),
            _空心管(Vec3(0, 0, z_stub_base), Vec3(0, 0, z_f3_ring0_bottom),
                  main_od, main_id),
            _空心管(Vec3(0, 0, z_f3_ring1_top), Vec3(0, 0, z_main_top),
                  main_od, main_id)
        ).color(*_色_管道)

        signal_valve = translate(
            0, 0, (z_signal_body_bottom + z_signal_body_top) / 2.0
        ) * _信号阀(
            structure_length=signal_length, dn=main_dn,
            body_outer_diameter=valve_body_od,
            wheel_diameter=wheel_diameter, wheel_on_minus_x=True
        )

        test_signal_valve = translate(
            0, 0, (z_test_body_bottom + z_test_body_top) / 2.0
        ) * _信号阀(
            structure_length=test_length, dn=main_dn,
            body_outer_diameter=valve_body_od,
            wheel_diameter=wheel_diameter, wheel_on_minus_x=True
        )

        deluge_valve = translate(0, 0, z_deluge_bottom) * _雨淋报警阀(
            total_height=deluge_height, dn=main_dn, connection_bore=main_od,
            body_width=deluge_body_width, body_depth=deluge_body_depth,
            cover_width=deluge_cover_width, cover_height=deluge_cover_height,
            control_port_z=control_port_z, control_port_dn=chamber_id,
            control_port_od=chamber_od, control_port_length=control_port_length,
            alarm_port_z=alarm_port_z, alarm_port_dn=20.0,
            alarm_port_od=alarm_od, alarm_port_length=alarm_port_length,
            drain_port_z=drain_port_z, drain_port_dn=50.0,
            drain_port_od=drain_od, drain_port_length=drain_port_length
        )

        # ===== 5A. 法兰1：信号阀的对夹式法兰连接 =====
        # 一个法兰 = 下圆环 + 上圆环 + 贯穿螺栓 + 上下两个六角螺帽。
        # 上圆环由下圆环【平移复制】得到，不另写通用函数。
        nut_across = bolt_hole_d * 1.60
        nut_height = bolt_hole_d * 0.80
        shank_r = bolt_hole_d * 0.44
        # 法兰1/3 为对夹式长螺栓，其总长严格取安装尺寸表标注的
        # 16xM16x160 / 16xM18x165 / 32xM20x180，故伸出螺帽的长度由总长反算；
        # 法兰2 上下圆环紧贴、用的是短螺栓，伸出量另取固定值。
        f13_span = 2.0 * flange_t + signal_length
        f13_stick_out = max(
            (bolt_length - f13_span - 2.0 * nut_height) / 2.0, 2.0
        )
        f2_stick_out = 6.0

        f1_ring0 = Cone(
            Vec3(0, 0, z_f1_ring0_bottom), Vec3(0, 0, z_f1_ring0_top),
            flange_od / 2.0, flange_od / 2.0
        ) - Cone(
            Vec3(0, 0, z_f1_ring0_bottom - 1.0),
            Vec3(0, 0, z_f1_ring0_top + 1.0),
            main_radius, main_radius
        )
        for _index in range(bolt_count):
            _angle = 2.0 * math.pi * _index / bolt_count
            _hx = bolt_circle_r * math.cos(_angle)
            _hy = bolt_circle_r * math.sin(_angle)
            f1_ring0 = f1_ring0 - Cone(
                Vec3(_hx, _hy, z_f1_ring0_bottom - 1.0),
                Vec3(_hx, _hy, z_f1_ring0_top + 1.0),
                bolt_hole_r, bolt_hole_r
            )
        # 上圆环 = 下圆环沿 Z 平移复制（净距即阀体结构长度）
        f1_ring1 = translate(
            0, 0, z_f1_ring1_bottom - z_f1_ring0_bottom
        ) * f1_ring0

        # 0 号位的一整根螺栓：贯穿杆 + 下螺帽 + 上螺帽；其余各根绕主轴复制
        f1_shank_z0 = z_f1_ring0_bottom - nut_height - f13_stick_out
        f1_shank_z1 = z_f1_ring1_top + nut_height + f13_stick_out
        f1_bolt = combine(
            Cone(Vec3(bolt_circle_r, 0, f1_shank_z0),
                 Vec3(bolt_circle_r, 0, f1_shank_z1), shank_r, shank_r),
            _六角柱Z(z_f1_ring0_bottom - nut_height, z_f1_ring0_bottom,
                  nut_across, bolt_circle_r, 0.0),
            _六角柱Z(z_f1_ring1_top, z_f1_ring1_top + nut_height,
                  nut_across, bolt_circle_r, 0.0)
        )
        f1_bolts = combine(*[
            rotate(Vec3(0, 0, 1), 2.0 * math.pi * _index / bolt_count) * f1_bolt
            for _index in range(bolt_count)
        ])

        flange_1 = combine(
            f1_ring0.color(*_色_铸铁亮),
            f1_ring1.color(*_色_铸铁亮),
            f1_bolts.color(*_色_钢)
        )

        # ===== 5B. 法兰2：中部法兰，上下圆环之间只隔一层垫片 =====
        f2_ring0 = Cone(
            Vec3(0, 0, z_f2_ring0_bottom), Vec3(0, 0, z_f2_ring0_top),
            flange_od / 2.0, flange_od / 2.0
        ) - Cone(
            Vec3(0, 0, z_f2_ring0_bottom - 1.0),
            Vec3(0, 0, z_f2_ring0_top + 1.0),
            main_radius, main_radius
        )
        for _index in range(bolt_count):
            _angle = 2.0 * math.pi * _index / bolt_count
            _hx = bolt_circle_r * math.cos(_angle)
            _hy = bolt_circle_r * math.sin(_angle)
            f2_ring0 = f2_ring0 - Cone(
                Vec3(_hx, _hy, z_f2_ring0_bottom - 1.0),
                Vec3(_hx, _hy, z_f2_ring0_top + 1.0),
                bolt_hole_r, bolt_hole_r
            )
        f2_ring1 = translate(
            0, 0, z_f2_ring1_bottom - z_f2_ring0_bottom
        ) * f2_ring0

        f2_gasket = Cone(
            Vec3(0, 0, z_f2_ring0_top), Vec3(0, 0, z_f2_ring1_bottom),
            bolt_circle_r - bolt_hole_r, bolt_circle_r - bolt_hole_r
        ) - Cone(
            Vec3(0, 0, z_f2_ring0_top - 1.0),
            Vec3(0, 0, z_f2_ring1_bottom + 1.0),
            main_radius, main_radius
        )

        f2_shank_z0 = z_f2_ring0_bottom - nut_height - f2_stick_out
        f2_shank_z1 = z_f2_ring1_top + nut_height + f2_stick_out
        f2_bolt = combine(
            Cone(Vec3(bolt_circle_r, 0, f2_shank_z0),
                 Vec3(bolt_circle_r, 0, f2_shank_z1), shank_r, shank_r),
            _六角柱Z(z_f2_ring0_bottom - nut_height, z_f2_ring0_bottom,
                  nut_across, bolt_circle_r, 0.0),
            _六角柱Z(z_f2_ring1_top, z_f2_ring1_top + nut_height,
                  nut_across, bolt_circle_r, 0.0)
        )
        f2_bolts = combine(*[
            rotate(Vec3(0, 0, 1), 2.0 * math.pi * _index / bolt_count) * f2_bolt
            for _index in range(bolt_count)
        ])

        flange_2 = combine(
            f2_ring0.color(*_色_铸铁亮),
            f2_ring1.color(*_色_铸铁亮),
            f2_gasket.color(0.12, 0.12, 0.14, 1.0),
            f2_bolts.color(*_色_钢)
        )

        # ===== 5C. 法兰3：与法兰1 完全相同，整体平移复制到试验信号阀处 =====
        flange_3 = translate(0, 0, z_f3_offset) * flange_1

        flange_set = combine(flange_1, flange_2, flange_3)

        # ===== 6. 控制回路（编号 5/8/9/10/11/14 及其连接管） =====
        x_mid = self['控制立管X']        # 过滤器/电磁阀所在立管
        x_left = self['最左立管X']       # 手动开启阀所在立管
        x_ball = self['控制管球阀X']     # 控制管球阀(11)中心
        half_dn20 = _DN20阀长度 / 2.0

        control_parts = []

        # 6.1 底部水平控制管：自主立管取水，经控制管球阀(11)接至最左立管
        control_parts.append(_空心管(
            Vec3(-(main_radius - 4.0), 0, z_ctrl_h),
            Vec3(x_ball + half_dn20, 0, z_ctrl_h), control_od, control_id
        ))
        # 球阀(11)出口 → 水平走到最左侧 → 【圆角弯头】拐向上 → 手动开启阀(9)下端。
        # 按《管口连接修改》详图，此处是一个连续的圆角弯管，用一根 _折弯管
        # 一次生成；原先水平管与立管各自到此为止、直角对接，两个管端面裸露在外。
        control_parts.append(_折弯管(
            [
                (x_ball - half_dn20, 0.0, z_ctrl_h),
                (x_left, 0.0, z_ctrl_h),
                (x_left, 0.0, z_manual_0)
            ],
            control_od, control_id
        ))
        ball_valve_11 = translate(x_ball, 0, z_ctrl_h) * _截止阀(
            dn=20.0, stem_axis='minus_y'
        )

        # 6.2 中间立管：过滤器(14) → 止回阀(10) → 电磁阀(8) → 压力表(5)
        control_parts.append(_空心管(
            Vec3(x_mid, 0, z_ctrl_h), Vec3(x_mid, 0, z_filter_0),
            control_od, control_id
        ))
        control_parts.append(_空心管(
            Vec3(x_mid, 0, z_filter_1), Vec3(x_mid, 0, z_check_0),
            control_od, control_id
        ))
        control_parts.append(_空心管(
            Vec3(x_mid, 0, z_check_1), Vec3(x_mid, 0, z_solenoid_0),
            control_od, control_id
        ))
        control_parts.append(_空心管(
            Vec3(x_mid, 0, z_solenoid_1), Vec3(x_mid, 0, z_gauge_control),
            control_od, control_id
        ))

        # 过滤器主流道转为沿 +Z；滤篮朝 -X 下方（绕 Y 轴 -90° 后的等效角度）
        strainer_14 = translate(0, 0, _过滤器长度 / 2.0) * \
            translate(x_mid, 0, z_filter_0) * \
            rotate(Vec3(0, 1, 0), -math.pi / 2.0) * _过滤器(
                dn=20.0, total_length=_过滤器长度, basket_angle_deg=-135.0
            )

        # 电磁阀主流道转为沿 +Z，线圈随之朝 -X 水平伸出
        solenoid_8 = translate(
            x_mid, 0, z_solenoid_0 + _电磁阀长度 / 2.0
        ) * rotate(Vec3(0, 1, 0), -math.pi / 2.0) * _电磁阀(
            dn=20.0, total_length=_电磁阀长度
        )

        gauge_control = translate(x_mid, 0, z_gauge_control) * _压力表(
            dial_diameter=_压力表盘径, rod_height=_压力表杆高
        )

        # 止回阀(10)：竖直安装（主流道沿 +Z），局部原点在进口端面
        check_body_od = self['止回阀阀体外径']
        check_valve_10 = translate(x_mid, 0, z_check_0) * _止回阀(
            dn=20.0, total_height=check_length, body_diameter=check_body_od
        )

        # 6.3 控制腔进水管：DN40，自止回阀【阀体腰部】水平引出，
        #     其轴线标高 z_chamber 与止回阀阀体中心齐平，两者「相同高度」。
        #     管起点取阀轴线，穿出阀体后即为可见的 DN40 水平管；
        #     立管 Ø28 与本管 Ø48 的变径由阀体内部承担，外观上看不到变径接头。
        #     本管上串一只控制腔进水阀（原图集编号13，自报警立管移来）：
        #     在「止回阀阀体外缘 → 雨淋阀控制腔接口」这段可见管长内居中布置，
        #     两端各留出一段管子，不与止回阀阀体和接口凸台顶死。
        chamber_run_start = x_mid + check_body_od / 2.0   # 止回阀阀体外缘
        chamber_valve_x = (chamber_run_start + x_control_tip) / 2.0
        half_chamber_valve = _控制腔进水阀长度 / 2.0
        control_parts.append(_空心管(
            Vec3(x_mid, 0, z_chamber),
            Vec3(chamber_valve_x - half_chamber_valve, 0, z_chamber),
            chamber_od, chamber_id
        ))
        control_parts.append(_空心管(
            Vec3(chamber_valve_x + half_chamber_valve, 0, z_chamber),
            Vec3(x_control_tip, 0, z_chamber), chamber_od, chamber_id
        ))
        chamber_valve_13 = translate(
            chamber_valve_x, 0, z_chamber
        ) * _截止阀(
            dn=_控制腔进水阀通径, total_length=_控制腔进水阀长度,
            stem_axis='minus_y'
        )

        # 6.4 最左立管：手动开启阀(9) → 进水侧压力表(5)
        # （立管下段连同底部拐角已并入上面的 _折弯管，此处不再单独出管）
        control_parts.append(_空心管(
            Vec3(x_left, 0, z_manual_1), Vec3(x_left, 0, z_gauge_supply),
            control_od, control_id
        ))
        manual_valve_9 = translate(
            x_left, 0, z_manual_0 + half_dn20
        ) * _转为竖直阀(_截止阀(dn=20.0, stem_axis='plus_z'))

        gauge_supply = translate(x_left, 0, z_gauge_supply) * _压力表(
            dial_diameter=_压力表盘径, rod_height=_压力表杆高
        )

        control_circuit = combine(
            combine(*control_parts).color(*_色_管道),
            ball_valve_11, strainer_14, check_valve_10, chamber_valve_13,
            solenoid_8, manual_valve_9, gauge_control, gauge_supply
        )

        # ===== 7. 报警回路（编号 6/7/12/13 及其连接管） =====
        x_alarm_riser = self['报警立管X']
        # 报警立管（压力开关所在的竖管）上只保留一个阀门：12 报警球阀。
        # 原先串在其下方的编号13 球阀已移至控制腔进水管上（见 6.3）。
        z_ball12_0 = z_alarm_port + 27.0
        z_ball12_1 = z_ball12_0 + _DN20阀长度

        # 7.1 自报警口向 -X 引出、后移至贴墙平面、再折向上（拐点非切点）
        alarm_lead = _折弯管(
            [
                (x_alarm_tip, 0.0, z_alarm_port),
                (x_alarm_riser, 0.0, z_alarm_port),
                (x_alarm_riser, y_alarm, z_alarm_port),
                (x_alarm_riser, y_alarm, z_ball12_0)
            ],
            alarm_od, alarm_id
        )

        # 7.2 立管上串接报警球阀(12)
        ball_valve_12 = translate(
            x_alarm_riser, y_alarm, z_ball12_0 + half_dn20
        ) * _转为竖直阀(_截止阀(dn=20.0, stem_axis='plus_z'))

        # 7.3 立管上段 + 顶部水平管接至水力警铃进水口
        alarm_top = _折弯管(
            [
                (x_alarm_riser, y_alarm, z_ball12_1),
                (x_alarm_riser, y_alarm, z_group_top),
                (C, y_alarm, z_group_top)
            ],
            alarm_od, alarm_id
        )

        # 7.4 水力警铃(6)：局部原点为进水口端面，铃罩最右点恰落在 X = +C
        water_gong = translate(C, y_alarm, z_group_top) * _水力警铃(
            bell_diameter=self['水力警铃罩直径'],
            inlet_dn=20.0, outlet_dn=25.0
        )

        # 7.5 压力开关(7)：按《压力开关位置详细图纸》，挂在【报警立管】的 -X 侧，
        #     而不是顶部水平管上。立管在 z_switch_branch 处引出水平支管，
        #     支管末端向上一小段接到开关盒底面。
        z_switch_branch = z_group_top - self['压力开关支管相对顶标高']
        x_switch_box = x_alarm_riser - self['压力开关支管长度']
        switch_stub_height = 20.0
        z_switch_box_bottom = z_switch_branch + switch_stub_height
        pressure_switch = translate(
            x_switch_box, y_alarm, z_switch_box_bottom
        ) * _压力开关()
        switch_pipe = _折弯管(
            [
                (x_switch_box, y_alarm, z_switch_box_bottom),
                (x_switch_box, y_alarm, z_switch_branch),
                (x_alarm_riser, y_alarm, z_switch_branch)
            ],
            alarm_od, alarm_id
        )

        alarm_circuit = combine(
            combine(alarm_lead, alarm_top, switch_pipe).color(*_色_管道),
            ball_valve_12
        )

        # ===== 8. 试验放水回路（编号 15 + 出水口压力表 5） =====
        # 试验放水管接在法兰2 上方的上部短管上，故以 z_stub_base(=H+A) 起算
        z_test_drain = z_stub_base + self['试验放水管相对标高']
        x_test_valve = self['试验放水阀X']
        x_test_riser = self['试验放水立管X']
        z_test_riser_bottom = z_stub_base - self['试验放水立管下伸长度']
        half_dn40 = _DN40阀长度 / 2.0

        test_drain_parts = [
            _空心管(
                Vec3(main_radius - 4.0, 0, z_test_drain),
                Vec3(x_test_valve - half_dn40, 0, z_test_drain),
                test_od, test_id
            ),
            _折弯管(
                [
                    (x_test_valve + half_dn40, 0.0, z_test_drain),
                    (x_test_riser, 0.0, z_test_drain),
                    (x_test_riser, 0.0, z_test_riser_bottom)
                ],
                test_od, test_id
            )
        ]
        test_valve_15 = translate(x_test_valve, 0, z_test_drain) * _截止阀(
            dn=40.0, stem_axis='minus_y'
        )

        # 出水口压力表支管：短立管 → DN15 小截止阀 → 压力表
        x_outlet_gauge = self['出水口压力表X']
        z_gauge_stub_top = z_test_drain + test_od / 2.0 + 22.0
        z_small_valve_1 = z_gauge_stub_top + _DN15阀长度
        test_drain_parts.append(_空心管(
            Vec3(x_outlet_gauge, 0, z_test_drain),
            Vec3(x_outlet_gauge, 0, z_gauge_stub_top), gauge_od, gauge_id
        ))
        small_valve = translate(
            x_outlet_gauge, 0, z_gauge_stub_top + _DN15阀长度 / 2.0
        ) * _转为竖直阀(_截止阀(dn=15.0, stem_axis='plus_z'))
        gauge_outlet = translate(x_outlet_gauge, 0, z_small_valve_1) * _压力表(
            dial_diameter=_压力表盘径, rod_height=_压力表杆高
        )

        test_drain_circuit = combine(
            combine(*test_drain_parts).color(*_色_管道),
            test_valve_15, small_valve, gauge_outlet
        )

        # ===== 9. 泄水回路（编号 17 + 排水立管） =====
        half_dn50 = _DN50阀长度 / 2.0
        x_drain_valve = x_drain_tip + half_dn50
        drain_pipe = _折弯管(
            [
                (x_drain_valve + half_dn50, 0.0, z_drain_port),
                (E, 0.0, z_drain_port),
                (E, 0.0, self['排水管出口标高'])
            ],
            drain_od, drain_id
        )
        drain_valve_17 = translate(x_drain_valve, 0, z_drain_port) * _截止阀(
            dn=50.0, stem_axis='minus_y'
        )
        drain_circuit = combine(drain_pipe.color(*_色_管道), drain_valve_17)

        # ===== 10. 编号16 管卡 ×2（主立管抱箍锚墙 + 顶部报警管管卡） =====
        z_clamp = self['管卡中心标高']
        band_radial = self['管卡箍径向厚度']
        band_height = self['管卡厚度']
        strut_width = self['支撑柱宽度']
        strut_thickness = min(self['支撑柱厚度'], band_height)

        main_clamp = translate(0, 0, z_clamp) * _管卡(
            pipe_od=main_od, band_radial_thickness=band_radial,
            band_height=band_height, ear_length=48.0, ear_width=26.0,
            bolt_diameter=12.0
        )

        # 支撑柱连接管卡与墙面：端面沿 -Y 退到抱箍外圆的弦位置再多埋一点，
        # 使整个端面嵌进抱箍而不是只有一条切线；埋深受抱箍径向厚度限制，
        # 不会触及被抱的管道。
        band_outer = main_radius + band_radial
        allowed_depth = band_radial * 0.70
        max_half_width = math.sqrt(max(
            band_outer ** 2 - (band_outer - allowed_depth) ** 2, 1.0
        ))
        strut_half_width = min(strut_width / 2.0, max_half_width)
        chord_y = math.sqrt(max(band_outer ** 2 - strut_half_width ** 2, 0.0))
        embed_depth = min(band_outer - chord_y + 1.5, allowed_depth)
        strut_start_y = band_outer - embed_depth
        strut_length = max(y_wall - strut_start_y, 1.0)
        wall_strut = translate(
            -strut_half_width, strut_start_y, z_clamp - strut_thickness / 2.0
        ) * scale(
            strut_half_width * 2.0, strut_length, strut_thickness
        ) * Cube()

        # 顶部报警水平管的管卡：抱箍轴线绕 Y 轴转 90° 后由 +Z 变为 +X
        top_band_radial = 6.0
        top_band_height = 14.0
        top_clamp_x = self['顶部管卡X']
        top_clamp = translate(
            top_clamp_x, y_alarm, z_group_top
        ) * rotate(Vec3(0, 1, 0), math.pi / 2.0) * _管卡(
            pipe_od=alarm_od, band_radial_thickness=top_band_radial,
            band_height=top_band_height,
            ear_length=18.0, ear_width=12.0, bolt_diameter=6.0
        )

        # 顶部管卡的锚固水平支撑板：做法与主立管管卡的支撑柱一致——
        # 自管卡抱箍沿 +Y 水平伸至墙面生根，端面按弦位嵌入抱箍，
        # 埋深受抱箍径向厚度限制，不会触及被抱的报警管。
        top_strut_width = 30.0
        top_strut_thickness = min(12.0, top_band_height)
        top_band_outer = alarm_od / 2.0 + top_band_radial
        top_allowed_depth = top_band_radial * 0.70
        top_max_half_width = math.sqrt(max(
            top_band_outer ** 2 - (top_band_outer - top_allowed_depth) ** 2, 1.0
        ))
        top_strut_half_width = min(top_strut_width / 2.0, top_max_half_width)
        top_chord_y = math.sqrt(max(
            top_band_outer ** 2 - top_strut_half_width ** 2, 0.0
        ))
        top_embed_depth = min(
            top_band_outer - top_chord_y + 1.5, top_allowed_depth
        )
        top_strut_start_y = y_alarm + top_band_outer - top_embed_depth
        top_strut_length = max(y_wall - top_strut_start_y, 1.0)
        top_wall_strut = translate(
            top_clamp_x - top_strut_half_width, top_strut_start_y,
            z_group_top - top_strut_thickness / 2.0
        ) * scale(
            top_strut_half_width * 2.0, top_strut_length, top_strut_thickness
        ) * Cube()

        clamp_set = combine(
            main_clamp, wall_strut.color(*_色_铸铁),
            top_clamp, top_wall_strut.color(*_色_铸铁)
        )

        # ===== 11. 整体组合与输出 =====
        overall = combine(
            main_pipe, flange_set, signal_valve, deluge_valve,
            test_signal_valve, control_circuit, alarm_circuit,
            water_gong, pressure_switch, test_drain_circuit,
            drain_circuit, clamp_set
        )

        self['主立管'] = main_pipe
        self['法兰连接'] = flange_set
        self['信号阀'] = signal_valve
        self['雨淋报警阀'] = deluge_valve
        self['试验信号阀'] = test_signal_valve
        self['控制回路'] = control_circuit
        self['报警回路'] = alarm_circuit
        self['水力警铃'] = water_gong
        self['压力开关'] = pressure_switch
        self['试验放水回路'] = test_drain_circuit
        self['泄水回路'] = drain_circuit
        self['管卡'] = clamp_set
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
