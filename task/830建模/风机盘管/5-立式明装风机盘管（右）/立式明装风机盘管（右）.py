from pyp3d import *
import math


# ============================================================
# 辅助函数
# ============================================================
def rect_section_xoy(length, width):
    """XOY面矩形截面：长沿X、宽沿Y，形心在原点"""
    hl = length / 2.0
    hw = width / 2.0
    return Section(
        Vec2(-hl, -hw),
        Vec2(hl, -hw),
        Vec2(hl, hw),
        Vec2(-hl, hw),
        Vec2(-hl, -hw),
    )


def loft_z_prism(length, width, z_bottom, z_top):
    """矩形截面沿Z方向拉伸成长方体，截面形心在原点"""
    sec = rect_section_xoy(length, width)
    return Loft(
        translate(0, 0, z_bottom) * sec,
        translate(0, 0, z_top) * sec,
    )


def back_rounded_section_xoy(length, width, radius):
    """仅背面(-Y)上下两角带圆角的矩形截面，形心在原点"""
    L = length
    W = width
    r = max(radius, 1e-3)
    r = min(r, L / 2.0 - 1e-3, W / 2.0 - 1e-3)

    # 背面(-Y)两个圆角圆心
    c_br = Vec2(L / 2.0 - r, -W / 2.0 + r)     # 背面右下
    c_bl = Vec2(-L / 2.0 + r, -W / 2.0 + r)    # 背面左下

    # 关键节点
    p0 = Vec2(-L / 2.0, -W / 2.0 + r)          # 左下角弧起点
    p1 = Vec2(-L / 2.0, W / 2.0)                # 左上直角点
    p2 = Vec2(L / 2.0, W / 2.0)                 # 右上直角点
    p3 = Vec2(L / 2.0, -W / 2.0 + r)            # 右下角弧起点
    p4 = Vec2(L / 2.0 - r, -W / 2.0)            # 背面底边右端点
    p5 = Vec2(-L / 2.0 + r, -W / 2.0)           # 背面底边左端点

    # 两个1/4圆弧
    arc_br = translate(c_br.x, c_br.y) * rotation(-math.pi / 2.0) * scale(r) * Arc(math.pi / 2.0)
    arc_bl = translate(c_bl.x, c_bl.y) * rotation(math.pi) * scale(r) * Arc(math.pi / 2.0)

    return Section(
        p0, p1,
        p2, p3,
        arc_br,
        p4, p5,
        arc_bl,
    )


class pythonModel(Component):
    def __init__(self):
        Component.__init__(self)

        # ===== 专业属性 =====
        self['设备名称'] = Attr('立式明装风机盘管（右）', obvious=True, group='专业属性')
        self['材质'] = Attr('镀锌钢板', obvious=True, group='专业属性')

        # ===== 用户可修改属性 =====
        self['机箱长'] = Attr(1000.0, obvious=True, group='机箱属性')
        self['机箱宽'] = Attr(500.0, obvious=True, group='机箱属性')
        self['机箱高'] = Attr(800.0, obvious=True, group='机箱属性')
        self['圆角直径'] = Attr(150.0, obvious=True, group='机箱属性')
        self['缺口长'] = Attr(500.0, obvious=True, group='机箱属性')
        self['缺口高'] = Attr(100.0, obvious=True, group='机箱属性')
        self['水管直径'] = Attr(20.0, obvious=True, group='管口属性')
        self['水管伸出长'] = Attr(80.0, obvious=True, group='管口属性')

        # ===== 内部派生参数（不暴露给用户修改） =====
        self['格栅条数'] = Attr(13, obvious=False, group='机箱属性')
        self['格栅区长'] = Attr(800.0, obvious=False, group='机箱属性')
        self['格栅区宽'] = Attr(400.0, obvious=False, group='机箱属性')
        self['格栅切深'] = Attr(40.0, obvious=False, group='机箱属性')
        self['格栅筋条宽'] = Attr(10.0, obvious=False, group='机箱属性')
        self['控制盒厚'] = Attr(40.0, obvious=False, group='控制盒属性')
        self['控制盒宽'] = Attr(120.0, obvious=False, group='控制盒属性')
        self['控制盒高'] = Attr(180.0, obvious=False, group='控制盒属性')
        self['控制盒顶距'] = Attr(40.0, obvious=False, group='控制盒属性')
        self['控制盒前距'] = Attr(0.0, obvious=False, group='控制盒属性')

        # ===== 特征点（驱动点）=====
        # 三个水管外端面圆心，间距=0.15*机箱高，整体中心高度=0.75*机箱高
        self.setDrivenFeaturePoint('水管下', SnapMode.GeometricCenter,
            '[定位点X] + [机箱长]/2 + [水管伸出长]',
            '[定位点Y]',
            '[定位点Z] + 0.75*[机箱高] - 0.15*[机箱高]')
        self.setDrivenFeaturePoint('水管中', SnapMode.GeometricCenter,
            '[定位点X] + [机箱长]/2 + [水管伸出长]',
            '[定位点Y]',
            '[定位点Z] + 0.75*[机箱高]')
        self.setDrivenFeaturePoint('水管上', SnapMode.GeometricCenter,
            '[定位点X] + [机箱长]/2 + [水管伸出长]',
            '[定位点Y]',
            '[定位点Z] + 0.75*[机箱高] + 0.15*[机箱高]')

        # 控制盒外表面矩形截面形心
        # 控制盒厚=0.04*机箱长, 控制盒宽=0.24*机箱宽, 控制盒高=0.225*机箱高,
        # 控制盒顶距=0.05*机箱高, 控制盒前距=0
        self.setDrivenFeaturePoint('控制盒形心', SnapMode.GeometricCenter,
            '[定位点X] + [机箱长]/2 + 0.04*[机箱长]/2',
            '[定位点Y] + [机箱宽]/2 - 0.24*[机箱宽]/2',
            '[定位点Z] + [机箱高] - 0.05*[机箱高] - 0.225*[机箱高]/2')

        # ===== 最终几何输出槽位 =====
        self['立式明装风机盘管'] = Attr(None, show=True)

        self.replace()

    @export
    def replace(self):
        # ---------- 读取用户可修改参数 ----------
        L = float(self['机箱长'])
        W = float(self['机箱宽'])
        H = float(self['机箱高'])
        D = float(self['圆角直径'])
        gap_w = float(self['缺口长'])
        gap_h = float(self['缺口高'])
        pipe_d = float(self['水管直径'])
        pipe_len = float(self['水管伸出长'])

        # ---------- 派生参数（与机箱长/宽/高比例绑定） ----------
        R = D/2   # 圆角半径
        grille_n = 13                                         # 格栅条数固定为13
        grille_len = 0.8 * L                                  # 格栅区长 = 0.8*机箱长
        grille_width = 0.7 * W                                # 格栅区宽 = 0.7*机箱宽
        grille_depth = 0.05 * H                               # 格栅切深 = 0.05*机箱高
        grille_bar = 0.02 * W                                 # 格栅筋条宽 = 0.02*机箱宽

        ctrl_t = 0.04 * L                                     # 控制盒厚 = 0.04*机箱长
        ctrl_w = 0.24 * W                                     # 控制盒宽 = 0.24*机箱宽
        ctrl_h = 0.225 * H                                    # 控制盒高 = 0.225*机箱高
        ctrl_top_gap = 0.05 * H                               # 控制盒顶距 = 0.05*机箱高
        ctrl_front_gap = 0.0                                  # 控制盒前距 = 0

        # ---------- 参数合法性检查 ----------
        if min(L, W, H, pipe_d, pipe_len) <= 0:
            raise ValueError('尺寸参数必须为正数，请检查输入')
        if gap_w >= L or gap_h >= H:
            raise ValueError('底部缺口尺寸超出机箱范围，请检查输入')
        R = min(R, L / 2.0 - 1e-3, W / 2.0 - 1e-3)

        # ============================================================
        # 主体机箱外壳：仅背面(-Y)两角带圆角，+Y正面保持直角
        # x∈[-L/2,L/2], y∈[-W/2,W/2], z∈[0,H]
        # ============================================================
        base_section = back_rounded_section_xoy(L, W, R)
        body = Loft(
            translate(0, 0, 0) * base_section,
            translate(0, 0, H) * base_section,
        )

        # ============================================================
        # 底部前后贯穿缺口：居中挖去底部中间一段
        # x∈[-缺口长/2, 缺口长/2], y 贯穿机箱，z∈[0, 缺口高]
        # ============================================================
        gap = loft_z_prism(gap_w, W + 100.0, -5.0, gap_h)

        # ============================================================
        # 顶部格栅：长槽平行于X，居中区域阵列
        # ============================================================
        if grille_n < 1:
            raise ValueError('格栅条数至少为1')
        slot_w = (grille_width - (grille_n - 1) * grille_bar) / grille_n
        if slot_w <= 0:
            raise ValueError('格栅区宽不足或筋条过宽，请检查输入')
        slot_list = []
        start_y = -(grille_width - slot_w) / 2.0
        for i in range(grille_n):
            cy = start_y + i * (slot_w + grille_bar)
            slot = loft_z_prism(grille_len, slot_w, H - grille_depth, H + 5.0)
            slot = translate(0, cy, 0) * slot
            slot_list.append(slot)
        grille_cuts = combine(*slot_list)

        # 一次性布尔减缺口与格栅
        body = body - combine(gap, grille_cuts)
        body = body.color(0.85, 0.85, 0.85, 1)

        parts = [body]

        # ============================================================
        # 水管×3：+X侧伸出，Y居中
        # 间距=0.15H，整体中心高度=0.75H
        # ============================================================
        pipe_r = pipe_d / 2.0
        for k in [-1, 0, 1]:
            pz = 0.75 * H + k * 0.15 * H
            pipe = Cone(Vec3(L / 2.0, 0.0, pz),
                        Vec3(L / 2.0 + pipe_len, 0.0, pz),
                        pipe_r, pipe_r)
            parts.append(pipe.color(0.6, 0.62, 0.65, 1))

        # ============================================================
        # 控制盒：+X侧前上方凸出矩形盒
        # ============================================================
        ctrl = loft_z_prism(ctrl_t, ctrl_w,
                            H - ctrl_top_gap - ctrl_h,
                            H - ctrl_top_gap)
        ctrl = translate(
            L / 2.0 + ctrl_t / 2.0,
            W / 2.0 - ctrl_front_gap - ctrl_w / 2.0,
            0.0
        ) * ctrl
        parts.append(ctrl.color(0.8, 0.8, 0.8, 1))

        # ============================================================
        # 整体组装输出
        # ============================================================
        self['立式明装风机盘管'] = combine(*parts)


if __name__ == "__main__":
    FinalGeometry = pythonModel()
    place(FinalGeometry)
