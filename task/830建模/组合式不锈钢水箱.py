from pyp3d import *
import math

# ============================================================
# 辅助函数：半椭球体（Z+方向，n=25，匹配椭底面高度拉伸.py）
# ============================================================
def semi_ellipsoid_25(ax, by, cz):
    """创建上半椭球体，使用n=25截面（匹配椭底面高度拉伸.py）"""
    n = 25
    if n % 2 == 0:
        n += 1
    sections = []
    eps = 1e-3
    for i in range(n):
        t = 1.0 * i / (n - 1)                # t ∈ [0, 1]，底面→顶点
        z_local = cz * t                      # 当前截面高度
        scale_xy = math.sqrt(max(0.0, 1.0 - t * t))
        rx = max(ax * scale_xy, eps)
        ry = max(by * scale_xy, eps)
        sections.append(translate(0, 0, z_local) * scale(rx, ry) * Section(Arc(2 * math.pi)))
    solid = Loft(*sections)
    solid.smooth = True
    return solid


# ============================================================
# 辅助函数：通过Loft拉伸矩形截面
# ============================================================
def extrude_rect(cx, cy, h):
    """拉伸矩形截面：形心在原点，半宽(cx,cy)，拉伸高度h(Z+)"""
    sec = Section(Vec2(-cx, -cy), Vec2(cx, -cy), Vec2(cx, cy), Vec2(-cx, cy))
    return Loft(sec, translate(0, 0, h) * sec)


# ============================================================
# 辅助函数：通过Loft拉伸圆形截面
# ============================================================
def extrude_circle(r, h):
    """拉伸圆形截面：圆心在原点，半径r，拉伸高度h(Z+)"""
    sec = Section(scale(r, r) * Arc(2 * math.pi))
    return Loft(sec, translate(0, 0, h) * sec)


# ============================================================
# 辅助函数：通过Loft拉伸椭圆截面
# ============================================================
def extrude_ellipse(rx, ry, h):
    """拉伸椭圆截面：形心在原点，半轴(rx,ry)，拉伸高度h(Z+)"""
    sec = Section(scale(rx, ry) * Arc(2 * math.pi))
    return Loft(sec, translate(0, 0, h) * sec)


# ============================================================
# 组合体1：外正方形1000×1000 + 内正方形950×950 + 圆d=900 + 半椭球h=75
# ============================================================
def make_comb1(outer_x, outer_y, inner_x, inner_y, circle_r, ext_h, semi_h):
    """创建组合体1，形心在原点，Z+方向。"""
    # 外正方形
    outer = extrude_rect(outer_x / 2, outer_y / 2, ext_h)
    # 内正方形
    inner = extrude_rect(inner_x / 2, inner_y / 2, ext_h)
    # 圆
    circle = extrude_circle(circle_r, ext_h)
    # 半椭球（在挤出体上方z=ext_h处）
    semi = translate(0, 0, ext_h) * semi_ellipsoid_25(circle_r, circle_r, semi_h)
    return combine(outer, inner, circle, semi)


# ============================================================
# 组合体2：外矩形500×1000 + 内矩形450×950 + 椭圆400×900 + 半椭球(椭底面高度拉伸)
# ============================================================
def make_comb2(outer_x, outer_y, inner_x, inner_y, ellipse_rx, ellipse_ry, ext_h, semi_a, semi_b, semi_h):
    """创建组合体2，形心在原点，Z+方向。
    椭球使用椭底面高度拉伸.py方法：半长轴/半短轴/椭球高度。"""
    # 外矩形
    outer = extrude_rect(outer_x / 2, outer_y / 2, ext_h)
    # 内矩形
    inner = extrude_rect(inner_x / 2, inner_y / 2, ext_h)
    # 椭圆
    ellipse = extrude_ellipse(ellipse_rx, ellipse_ry, ext_h)
    # 半椭球：semi_b→X半轴, semi_a→Y半轴（与椭圆rx,ry对齐），rotz(pi/2)等效
    semi = translate(0, 0, ext_h) * semi_ellipsoid_25(semi_b, semi_a, semi_h)
    return combine(outer, inner, ellipse, semi)


# ============================================================
# 组合体3：外正方形500×500 + 内正方形450×450 + 圆d=400 + 半椭球h=75
# ============================================================
def make_comb3(outer_x, outer_y, inner_x, inner_y, circle_r, ext_h, semi_h):
    """创建组合体3，形心在原点，Z+方向"""
    # 外正方形
    outer = extrude_rect(outer_x / 2, outer_y / 2, ext_h)
    # 内正方形
    inner = extrude_rect(inner_x / 2, inner_y / 2, ext_h)
    # 圆
    circle = extrude_circle(circle_r, ext_h)
    # 半椭球（在挤出体上方）
    semi = translate(0, 0, ext_h) * semi_ellipsoid_25(circle_r, circle_r, semi_h)
    return combine(outer, inner, circle, semi)


# ============================================================
# 主模型类
# ============================================================
class 组合式不锈钢水箱(Component):
    def __init__(self):
        Component.__init__(self)
        # 主参数
        # 参变约束：每个面组合体总长/宽/高+间隔 < 矩形面长/宽/高
        self['构件名称'] = Attr('组合式不锈钢水箱', obvious=True, readonly=True)
        self['水箱长'] = Attr(4200, obvious=True)
        self['水箱宽'] = Attr(2580, obvious=True)
        self['水箱高'] = Attr(1540, obvious=True)

        # 输出槽位
        self['箱体'] = Attr(None, show=True)

        # 组合体1/3基准尺寸（隐藏，随水箱参变）
        self['组合体1外长'] = Attr(1000, obvious=False)
        self['组合体1外宽'] = Attr(1000, obvious=False)
        self['组合体3外长'] = Attr(500, obvious=False)
        self['组合体3外宽'] = Attr(500, obvious=False)

        # ========== 特征点定义 ==========
        # 右视图(X=L面)：矩形右下方点（靠近右下角但在面上）
        self.setDrivenFeaturePoint('右视图_右下点', SnapMode.GeometricCenter,
            '[定位点X] + [水箱长]',
            '[定位点Y] + [水箱宽]*0.1',
            '[定位点Z] + [水箱高]*0.1')
        # 右视图：矩形右上方点（靠近右上角但在面上）
        self.setDrivenFeaturePoint('右视图_右上点', SnapMode.GeometricCenter,
            '[定位点X] + [水箱长]',
            '[定位点Y] + [水箱宽]*0.1',
            '[定位点Z] + [水箱高]*0.9')
        # 上视图(Z=H面)：上面第4个组合体1的形心
        self.setDrivenFeaturePoint('上视图_组合体1形心', SnapMode.GeometricCenter,
            '[定位点X] + [水箱长]*183/210',
            '[定位点Y] + [水箱宽]*104/129',
            '[定位点Z] + [水箱高]')

        self.replace()

    @export
    def replace(self):
        L = float(self['水箱长'])   # 4200
        W = float(self['水箱宽'])   # 2580
        H = float(self['水箱高'])   # 1540

        # 比例系数
        kx = L / 4200.0
        ky = W / 2580.0
        kz = H / 1540.0
        kr = (kx + ky) / 2.0  # 圆形/径向比例（取XY平均）

        # ================================================================
        # 参变关系约束（必须满足，保证任何组合体始终在水箱面内部，不超模）：
        #
        # --- 比例系数 ---
        # kx = L/4200, ky = W/2580, kz = H/1540
        # 所有组合体尺寸 = 基准值 × 比例系数，随水箱长宽高自动参变
        #
        # --- 内部约束 ---
        # 组合体1/3：圆直径 < 内矩形长、内矩形宽
        #   组合体1: (min(外长,外宽)-100) < (外长-50) 且 < (外宽-50)（恒成立）
        #   组合体3: (min(外长,外宽)-100) < (外长-50) 且 < (外宽-50)（恒成立）
        # 组合体2：椭圆长轴 < 内矩形长，椭圆短轴 < 内矩形宽（恒成立）
        #
        # --- 底座约束 ---
        #   底座随水箱参变：长=L+400，宽=W/10，高=400，Y间隔=(W-4*宽)/3
        #   4个底座均匀分布：第1个Y∈[0,宽]，第4个Y∈[W-宽,W] ✓
        #
        # --- 每面尺寸约束（已验证无超模） ---
        # 正后视图(XOZ, L×H)：
        #   X: 4*c_x_item + 4*c_x_gap = 104L/105 < L ✓
        #   Z: 500*kz + 1000*kz = 1500*kz < H（H=1540*kz时） ✓
        #
        # 左右视图(YOZ, W×H)：
        #   Y: 2500*ky + 4*y_gap_side = 0.95W + 0.05*2500*ky < W ✓
        #   Z: 500*kz + 1000*ky + 40 < H（H=1540*kz时） ✓
        #
        # 上视图(XOY, L×W)：
        #   X: 同正后视图 ✓
        #   Y: 2500*ky + 2*(W-2500*ky)/2 = W（底对齐+顶对齐，组合体在面内） ✓
        # ================================================================

        # ================================================================
        # 步骤1：箱体 (XOY面起点(0,0,0)，X+4200, Y+2580, Z+1540)
        # 使用Loft命令，以(0,0,0)为顶点绘制长方体
        # ================================================================
        tank_section = Section(Vec2(0, 0), Vec2(L, 0), Vec2(L, W), Vec2(0, W))
        tank_body = Loft(tank_section, translate(0, 0, H) * tank_section)

        # ================================================================
        # 步骤2：底座 (XOY面，顶点(-200,0,0)，Z-拉伸，Y向复制4个)
        # 底座随水箱参变：长=L+400，宽=W/10，高=400，间隔=(W-4*宽)/3
        # 保证第1个和第4个底座承载水箱两端
        # ================================================================
        base_l = L + 400          # 底座长（X方向留余量）
        base_w = W / 10.0          # 底座宽（Y方向）
        base_h = 400              # 底座高（Z负方向）
        base_y_gap = (W - 4 * base_w) / 3.0  # Y间隔（确保4个底座均匀分布在水箱下）

        base_section = Section(
            Vec2(-200, 0),
            Vec2(-200 + base_l, 0),
            Vec2(-200 + base_l, base_w),
            Vec2(-200, base_w)
        )
        base_loft = Loft(base_section, translate(0, 0, -base_h) * base_section)

        bases = []
        for i in range(4):
            b = translate(0, i * (base_w + base_y_gap), 0) * base_loft
            bases.append(b)
        all_bases = combine(*bases)

        # ================================================================
        # 步骤3：创建3种组合体（在局部坐标系原点，Z+方向）
        # ================================================================
        # 组合体1参数（外部矩形，长宽可分别参变）
        c1_outer_x = float(self['组合体1外长']) * kx
        c1_outer_y = float(self['组合体1外宽']) * ky
        c1_inner_x = c1_outer_x - 50       # 壁厚25×2
        c1_inner_y = c1_outer_y - 50
        c1_circle_r = (min(c1_outer_x, c1_outer_y) - 100) / 2  # 圆直径=外矩形短边-100
        c1_ext_h = 30 * kz
        c1_semi_h = 75 * kz

        # 组合体2参数
        c2_outer_x = 500 * kx
        c2_outer_y = 1000 * ky
        c2_inner_x = 450 * kx
        c2_inner_y = 950 * ky
        c2_ellipse_rx = 200 * kx   # 短半轴(长方向)
        c2_ellipse_ry = 450 * ky   # 长半轴(宽方向)
        c2_ext_h = 30 * kz
        c2_semi_a = 450 * ky       # 半长轴=二分之一长轴(宽方向)
        c2_semi_b = 200 * kx       # 半短轴=二分之一短轴(长方向)
        c2_semi_h = 75 * kz        # 椭球高度

        # 组合体3参数（外部矩形，长宽可分别参变）
        c3_outer_x = float(self['组合体3外长']) * kx
        c3_outer_y = float(self['组合体3外宽']) * ky
        c3_inner_x = c3_outer_x - 50       # 壁厚25×2
        c3_inner_y = c3_outer_y - 50
        c3_circle_r = (min(c3_outer_x, c3_outer_y) - 100) / 2  # 圆直径=外矩形短边-100
        c3_ext_h = 30 * kz
        c3_semi_h = 75 * kz

        # 创建组合体实例（在局部原点）
        comb1 = make_comb1(c1_outer_x, c1_outer_y, c1_inner_x, c1_inner_y,
                           c1_circle_r, c1_ext_h, c1_semi_h)

        comb2 = make_comb2(c2_outer_x, c2_outer_y, c2_inner_x, c2_inner_y,
                           c2_ellipse_rx, c2_ellipse_ry, c2_ext_h,
                           c2_semi_a, c2_semi_b, c2_semi_h)

        comb3 = make_comb3(c3_outer_x, c3_outer_y, c3_inner_x, c3_inner_y,
                           c3_circle_r, c3_ext_h, c3_semi_h)

        # 翻转版组合体（rotx(pi)使挤出+半椭球均朝Z-方向，用于正后视图往箱体内侧）
        comb1_rev = rotx(math.pi) * comb1
        comb2_rev = rotx(math.pi) * comb2

        # ================================================================
        # 步骤4：正视图(XOZ, Y=W) 和 后视图(XOZ, Y=0)
        # 上面4个组合体2(旋转90°→长X=1000,宽Z=500)，下面4个组合体1(长X=1000,宽Z=1000)
        # ================================================================
        # X方向均匀分布4个
        c_x_gap = L / 105.0                     # X间隙
        c_x_item = 5 * L / 21.0                 # X项宽(1000*kx)
        c_x_centers = [c_x_gap + c_x_item / 2 + i * (c_x_item + c_x_gap) for i in range(4)]

        # Z方向：顶部行(组合体2, Z高500*kz)顶对齐，底部行(组合体1, Z高1000*kz)底对齐
        c2_z_h = 500 * kz
        c1_z_h = 1000 * kz
        top_z = H - c2_z_h / 2                    # 顶部行中心Z（顶对齐到Z=H）
        bot_z = c1_z_h / 2                         # 底部行中心Z（底对齐到Z=0）

        front_parts = []
        back_parts = []
        for i in range(4):
            cx = c_x_centers[i]
            # 正视图(Y=W)：矩形+半椭球均朝内侧(Y-)，rotx(pi)使整体翻转
            c2_front = translate(cx, W, top_z) * rotx(math.pi / 2) * rotz(math.pi / 2) * comb2_rev
            front_parts.append(c2_front)
            # 正视图：组合体1放在底部（矩形+半椭球翻转朝内侧）
            c1_front = translate(cx, W, bot_z) * rotx(math.pi / 2) * comb1_rev
            front_parts.append(c1_front)

            # 后视图(Y=0)：矩形+半椭球均朝内侧(Y+)，rotx(pi)使整体翻转
            c2_back = translate(cx, 0, top_z) * rotx(-math.pi / 2) * rotz(math.pi / 2) * comb2_rev
            back_parts.append(c2_back)
            c1_back = translate(cx, 0, bot_z) * rotx(-math.pi / 2) * comb1_rev
            back_parts.append(c1_back)

        # ================================================================
        # 步骤5：右视图(YOZ, X=L) 和 左视图(YOZ, X=0)
        # 上面3个：组合体2(长Y=1000,宽Z=500), 组合体3(长Y=500,宽Z=500), 组合体2
        # 下面3个：组合体1(长Y=1000,宽Z=500), 组合体2(长Y=500,宽Z=1000), 组合体1
        # ================================================================
        # Y方向均匀分布3个，约束：2500*ky + 4*y_gap_side < W
        y_gap_side = (W - 2500 * ky) / 4.0 * 0.95  # Y间隙（留5%余量确保不超模）
        # 顶部行3个的Y宽度
        c2_y_w = 1000 * ky
        c3_y_w = 500 * ky
        c1_y_w = 1000 * ky
        c2b_y_w = 500 * ky  # 底部行组合体2的Y宽度

        # 顶部行Y中心
        top_y_centers = [
            y_gap_side + c2_y_w / 2,
            y_gap_side + c2_y_w + y_gap_side + c3_y_w / 2,
            y_gap_side + c2_y_w + y_gap_side + c3_y_w + y_gap_side + c2_y_w / 2
        ]
        # 底部行Y中心
        bot_y_centers = [
            y_gap_side + c1_y_w / 2,
            y_gap_side + c1_y_w + y_gap_side + c2b_y_w / 2,
            y_gap_side + c1_y_w + y_gap_side + c2b_y_w + y_gap_side + c1_y_w / 2
        ]

        # Z方向：顶部行顶对齐到Z=H，底部行与顶部行间距40
        side_top_z = H - 250 * kz                  # 顶部行中心Z（顶对齐）
        # 底部行：间距=40，保证矩形在箱体面上
        side_bot_z_c1 = H - 500 * kz - 500 * ky - 40  # 组合体1 Z中心（Z高=1000*ky，与正视图一致）
        side_bot_z_c2 = H - 1000 * kz - 40         # 组合体2 Z中心

        right_parts = []
        left_parts = []

        # 顶部行 —— 右视图(X=L)：半椭球朝外侧(X+)，roty(pi/2)使Z+→X+
        # 组合体2(长Y=1000,宽Z=500)：roty(pi/2)放到YOZ面
        right_parts.append(translate(L, top_y_centers[0], side_top_z) * roty(math.pi / 2) * comb2)
        # 组合体3(长Y=500,宽Z=500)
        right_parts.append(translate(L, top_y_centers[1], side_top_z) * roty(math.pi / 2) * comb3)
        # 组合体2
        right_parts.append(translate(L, top_y_centers[2], side_top_z) * roty(math.pi / 2) * comb2)

        # 底部行 —— 右视图
        # 组合体1(Z高=1000*ky，与正视图一致)：rotz(pi/2)交换XY使Z=1000*ky
        right_parts.append(translate(L, bot_y_centers[0], side_bot_z_c1) * roty(math.pi / 2) * rotz(math.pi / 2) * comb1)
        # 组合体2(长Y=500,宽Z=1000)：rotz(pi/2)交换XY使Y=500,Z=1000
        right_parts.append(translate(L, bot_y_centers[1], side_bot_z_c2) * roty(math.pi / 2) * rotz(math.pi / 2) * comb2)
        # 组合体1(Z高=1000*ky)
        right_parts.append(translate(L, bot_y_centers[2], side_bot_z_c1) * roty(math.pi / 2) * rotz(math.pi / 2) * comb1)

        # 顶部行 —— 左视图(X=0)：半椭球朝外侧(X-)，roty(-pi/2)使Z+→X-
        left_parts.append(translate(0, top_y_centers[0], side_top_z) * roty(-math.pi / 2) * comb2)
        left_parts.append(translate(0, top_y_centers[1], side_top_z) * roty(-math.pi / 2) * comb3)
        left_parts.append(translate(0, top_y_centers[2], side_top_z) * roty(-math.pi / 2) * comb2)

        # 底部行 —— 左视图
        # 组合体1(Z高=1000*ky，与正视图一致)：rotz(pi/2)交换XY使Z=1000*ky
        left_parts.append(translate(0, bot_y_centers[0], side_bot_z_c1) * roty(-math.pi / 2) * rotz(math.pi / 2) * comb1)
        # 组合体2(长Y=500,宽Z=1000)：rotz(pi/2)交换XY
        left_parts.append(translate(0, bot_y_centers[1], side_bot_z_c2) * roty(-math.pi / 2) * rotz(math.pi / 2) * comb2)
        # 组合体1(Z高=1000*ky)
        left_parts.append(translate(0, bot_y_centers[2], side_bot_z_c1) * roty(-math.pi / 2) * rotz(math.pi / 2) * comb1)

        # ================================================================
        # 步骤6：上视图(XOY, Z=H)
        # 上面4个组合体1(长X=1000,宽Y=1000)
        # 中间4个组合体2(旋转90°→长X=1000,宽Y=500)
        # 下面4个组合体1
        # ================================================================
        top_c1_y_h = 1000 * ky                   # 组合体1 Y高度
        top_c2_y_h = 500 * ky                    # 组合体2 Y高度

        # 3行Y中心：下面行底对齐Y=0，上面行顶对齐Y=W，中间行居中
        bot_row_y = top_c1_y_h / 2                                      # 下面行中心Y（底对齐）
        top_row_y = W - top_c1_y_h / 2                                  # 上面行中心Y（顶对齐）
        mid_row_y = (bot_row_y + top_c1_y_h / 2 + top_row_y - top_c1_y_h / 2) / 2  # 中间行中心Y

        top_face_parts = []
        for i in range(4):
            cx = c_x_centers[i]
            # 上面行：组合体1
            top_face_parts.append(translate(cx, top_row_y, H) * comb1)
            # 中间行：组合体2旋转90°（rotz(pi/2)使长X=1000,宽Y=500）
            top_face_parts.append(translate(cx, mid_row_y, H) * rotz(math.pi / 2) * comb2)
            # 下面行：组合体1
            top_face_parts.append(translate(cx, bot_row_y, H) * comb1)

        # ================================================================
        # 组装所有部件
        # ================================================================
        all_parts = [tank_body, all_bases]
        all_parts.extend(front_parts)
        all_parts.extend(back_parts)
        all_parts.extend(right_parts)
        all_parts.extend(left_parts)
        all_parts.extend(top_face_parts)

        self['箱体'] = combine(*all_parts)


# ================================================================
# 输出模型
# ================================================================
if __name__ == "__main__":
    FinalGeometry = 组合式不锈钢水箱()
    place(FinalGeometry)