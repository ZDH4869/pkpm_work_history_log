# -*- coding: utf-8 -*-
from pyp3d import *
import math


# ============================================================
# 辅助函数
# ============================================================
def rect_section_xoy(length, width):
    # XOY面矩形截面：长沿X、宽沿Y，形心在原点，5点闭合
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
    # 矩形截面沿Z方向拉伸成长方体，截面形心在原点
    sec = rect_section_xoy(length, width)
    return Loft(
        translate(0, 0, z_bottom) * sec,
        translate(0, 0, z_top) * sec,
    )


def octagon_section_xoy(length, width, chamfer):
    # XOY面八边形截面（矩形四角45度切角），形心在原点，9点闭合，逆时针
    hl = length / 2.0
    hw = width / 2.0
    c = min(chamfer, hl, hw)
    return Section(
        Vec2(hl - c, -hw),
        Vec2(-hl + c, -hw),
        Vec2(-hl, -hw + c),
        Vec2(-hl, hw - c),
        Vec2(-hl + c, hw),
        Vec2(hl - c, hw),
        Vec2(hl, hw - c),
        Vec2(hl, -hw + c),
        Vec2(hl - c, -hw),
    )


def rounded_rect_slab(length, width, radius, z_bottom, z_top):
    # 四角圆角矩形薄板：XOY面圆角矩形轮廓（ExtrusionPlus，直线+三点圆弧），形心在原点
    hl = length / 2.0
    hw = width / 2.0
    r = min(radius, hl, hw)
    s = r / math.sqrt(2.0)  # 45度圆弧经过点相对圆角圆心的偏移量
    outer = ContourLine([
        Line(Vec3(hl - r, -hw, 0), Vec3(-hl + r, -hw, 0)),
        Arc(Vec3(-hl + r, -hw, 0), Vec3(-hl + r - s, -hw + r - s, 0), Vec3(-hl, -hw + r, 0)),
        Line(Vec3(-hl, -hw + r, 0), Vec3(-hl, hw - r, 0)),
        Arc(Vec3(-hl, hw - r, 0), Vec3(-hl + r - s, hw - r + s, 0), Vec3(-hl + r, hw, 0)),
        Line(Vec3(-hl + r, hw, 0), Vec3(hl - r, hw, 0)),
        Arc(Vec3(hl - r, hw, 0), Vec3(hl - r + s, hw - r + s, 0), Vec3(hl, hw - r, 0)),
        Line(Vec3(hl, hw - r, 0), Vec3(hl, -hw + r, 0)),
        Arc(Vec3(hl, -hw + r, 0), Vec3(hl - r + s, -hw + r - s, 0), Vec3(hl - r, -hw, 0)),
    ])
    return translate(0, 0, z_bottom) * ExtrusionPlus([outer], Vec3(0, 0, z_top - z_bottom))


class pythonModel(Component):
    def __init__(self):
        Component.__init__(self)
        # ===== 专业属性 =====
        self['设备名称'] = Attr('吸顶式风机盘管', obvious=True, group='专业属性')
        self['材质'] = Attr('镀锌钢板', obvious=True, group='专业属性')
        # ===== 机箱属性：上部主机箱（四角45度切角） =====
        self['机箱长'] = Attr(700.0, obvious=True, group='机箱属性')
        self['机箱宽'] = Attr(700.0, obvious=True, group='机箱属性')
        self['机箱高'] = Attr(230.0, obvious=True, group='机箱属性')
        # ===== 底板属性：底部装饰面板（四角大圆角） =====
        self['底板长'] = Attr(950.0, obvious=True, group='底板属性')
        self['底板宽'] = Attr(950.0, obvious=True, group='底板属性')
        self['底板厚'] = Attr(50.0, obvious=True, group='底板属性')
        # ===== 管口属性：-X侧切角面上三根水管 =====
        self['水管直径'] = Attr(25.0, obvious=True, group='管口属性')
        self['水管伸出长'] = Attr(80.0, obvious=True, group='管口属性')
        # ===== 最终几何输出槽位 =====
        self['吸顶式风机盘管'] = Attr(None, show=True)

        # ============================================================
        # 特征点定义：replace 之前定义，表达式仅引用 obvious=True 的数值参数
        # 内部固定值：机箱切角=100（切角面中点距直边 100/2=50），电气盒凸出=60
        # 45度切角面法线方向 (±1,±1)/sqrt(2)，表达式用 *(0.5**0.5) 表示 1/sqrt(2)
        # ============================================================
        # 水管×3 外端面圆心（左下切角面，法线 (-1,-1)/sqrt(2)，Z=0.75/0.5/0.25 机箱高）
        self.setDrivenFeaturePoint('水管上外端圆心', SnapMode.GeometricCenter,
            '[定位点X] - [机箱长]/2 + 50 - [水管伸出长]*(0.5**0.5)',
            '[定位点Y] - [机箱宽]/2 + 50 - [水管伸出长]*(0.5**0.5)',
            '[定位点Z] + [底板厚] + 0.75*[机箱高]')
        self.setDrivenFeaturePoint('水管中外端圆心', SnapMode.GeometricCenter,
            '[定位点X] - [机箱长]/2 + 50 - [水管伸出长]*(0.5**0.5)',
            '[定位点Y] - [机箱宽]/2 + 50 - [水管伸出长]*(0.5**0.5)',
            '[定位点Z] + [底板厚] + 0.5*[机箱高]')
        self.setDrivenFeaturePoint('水管下外端圆心', SnapMode.GeometricCenter,
            '[定位点X] - [机箱长]/2 + 50 - [水管伸出长]*(0.5**0.5)',
            '[定位点Y] - [机箱宽]/2 + 50 - [水管伸出长]*(0.5**0.5)',
            '[定位点Z] + [底板厚] + 0.25*[机箱高]')
        # 电气盒外端面矩形截面形心（左上切角面，法线 (-1,+1)/sqrt(2)，Z向居中于机箱）
        self.setDrivenFeaturePoint('电气盒外端形心', SnapMode.GeometricCenter,
            '[定位点X] - [机箱长]/2 + 50 - 60*(0.5**0.5)',
            '[定位点Y] + [机箱宽]/2 - 50 + 60*(0.5**0.5)',
            '[定位点Z] + [底板厚] + 0.5*[机箱高]')
        # 原点（底板底面中心，模型定位点）
        self.setDrivenFeaturePoint('原点', SnapMode.GeometricCenter,
            '[定位点X]', '[定位点Y]', '[定位点Z]')

        self.replace()

    @export
    def replace(self):
        # ---------- 读取参数 ----------
        Lb = float(self['机箱长'])
        Wb = float(self['机箱宽'])
        Hb = float(self['机箱高'])
        Lp = float(self['底板长'])
        Wp = float(self['底板宽'])
        Tp = float(self['底板厚'])
        pipe_d = float(self['水管直径'])
        pipe_len = float(self['水管伸出长'])

        # ---------- 内部固定尺寸（待后续尺寸联动式绑定，暂写死） ----------
        Rp = 100.0        # 底板圆角半径
        Cb = 100.0        # 机箱切角直角边
        elec_w = 120.0    # 电气盒宽（沿切角斜边方向）
        elec_t = 60.0     # 电气盒凸出（沿切角面法线方向）
        elec_h = 110.0    # 电气盒高

        # ---------- 格栅/风口派生尺寸（与底板长宽厚比例绑定，系数反推自默认值950×950×50） ----------
        gr_lx = (460.0 / 950.0) * Lp    # 格栅区X向尺寸
        gr_ly = (460.0 / 950.0) * Wp    # 格栅区Y向尺寸
        gr_bar = 10.0                   # 格栅筋条宽（固定，孔尺寸自适应）
        gr_nx = 3                       # 格栅孔列数（X向）
        gr_ny = 9                       # 格栅孔行数（Y向）
        gr_cut = 0.4 * Tp               # 格栅切深 = 0.4*底板厚
        vent_len_h = (400.0 / 950.0) * Lp   # 上/下风口长（横向，跟底板长）
        vent_wid_h = (80.0 / 950.0) * Wp    # 上/下风口宽（跟底板宽）
        vent_len_v = (400.0 / 950.0) * Wp   # 左/右风口长（竖向，跟底板宽）
        vent_wid_v = (80.0 / 950.0) * Lp    # 左/右风口宽（跟底板长）
        vent_cut = 0.4 * Tp                 # 风口切深 = 0.4*底板厚
        vent_gap = 20.0                     # 风口与格栅区间隙（固定）

        # ---------- 参数合法性检查 ----------
        if min(Lb, Wb, Hb, Lp, Wp, Tp, pipe_d, pipe_len) <= 0:
            raise ValueError('尺寸参数必须为正数，请检查输入')
        if Lb > Lp or Wb > Wp:
            raise ValueError('机箱尺寸不应大于底板尺寸，请检查输入')
        if Cb * 2.0 > min(Lb, Wb):
            raise ValueError('机箱尺寸过小，无法布置切角')

        inv_sqrt2 = 1.0 / math.sqrt(2.0)   # 45度切角面法线单位分量
        parts = []

        # ============================================================
        # 装饰底板：圆角矩形薄板，x∈[-Lp/2,Lp/2], y∈[-Wp/2,Wp/2], z∈[0,Tp]
        # ============================================================
        panel = rounded_rect_slab(Lp, Wp, Rp, 0.0, Tp)

        # ============================================================
        # 底面中央回风格栅：横竖双向网格，横梁密、竖梁疏
        # 用 140(X)×40(Y) 小长方体的 3列(X)×9行(Y) 阵列从底板底面向上 Bool 减，
        # 孔尺寸 = (格栅区 - (数量+1)*筋条) / 数量，剪切后保留横竖交叉梁
        # ============================================================
        gr_hx = (gr_lx - (gr_nx + 1) * gr_bar) / gr_nx   # 孔X向尺寸（默认140）
        gr_hy = (gr_ly - (gr_ny + 1) * gr_bar) / gr_ny   # 孔Y向尺寸（默认40）
        if gr_hx <= 0 or gr_hy <= 0:
            raise ValueError('底板尺寸过小，无法布置格栅孔')
        grille_slots = []
        for i in range(gr_nx):
            for j in range(gr_ny):
                cx = -gr_lx / 2.0 + gr_bar + i * (gr_hx + gr_bar) + gr_hx / 2.0
                cy = -gr_ly / 2.0 + gr_bar + j * (gr_hy + gr_bar) + gr_hy / 2.0
                grille_slots.append(
                    translate(cx, cy, 0.0) * loft_z_prism(gr_hx, gr_hy, 0.0, gr_cut))
        panel = panel - combine(*grille_slots)

        # ============================================================
        # 底面四边出风口：长条凹槽，上下横向、左右竖向
        # 紧贴回风格栅区外侧（间隙 vent_gap），从底板底面 Bool 减
        # 槽长/槽宽均随所在边的底板边长比例变化
        # ============================================================
        vent_cy = gr_ly / 2.0 + vent_gap + vent_wid_h / 2.0   # 上/下风口槽中心Y
        vent_cx = gr_lx / 2.0 + vent_gap + vent_wid_v / 2.0   # 左/右风口槽中心X
        if vent_cy + vent_wid_h / 2.0 > Wp / 2.0 or vent_cx + vent_wid_v / 2.0 > Lp / 2.0:
            raise ValueError('底板尺寸过小，出风口超出底板边缘')
        vent_slots = [
            translate(0.0, vent_cy, 0.0) * loft_z_prism(vent_len_h, vent_wid_h, 0.0, vent_cut),    # 上(+Y)
            translate(0.0, -vent_cy, 0.0) * loft_z_prism(vent_len_h, vent_wid_h, 0.0, vent_cut),   # 下(-Y)
            translate(-vent_cx, 0.0, 0.0) * loft_z_prism(vent_wid_v, vent_len_v, 0.0, vent_cut),   # 左(-X)
            translate(vent_cx, 0.0, 0.0) * loft_z_prism(vent_wid_v, vent_len_v, 0.0, vent_cut),    # 右(+X)
        ]
        panel = panel - combine(*vent_slots)
        panel = panel.color(0.88, 0.88, 0.9, 1)
        parts.append(panel)

        # ============================================================
        # 主机箱：八边形截面扁箱体，z∈[Tp, Tp+Hb]，四角45度切角
        # ============================================================
        sec_box = octagon_section_xoy(Lb, Wb, Cb)
        box = Loft(
            translate(0, 0, Tp) * sec_box,
            translate(0, 0, Tp + Hb) * sec_box,
        )
        parts.append(box.color(0.85, 0.85, 0.85, 1))

        # ============================================================
        # 水管×3：左下切角面（-X,-Y角）沿法线 (-1,-1)/sqrt(2) 伸出
        # 切角面中点 = (-Lb/2+Cb/2, -Wb/2+Cb/2)，三根管 Z = 0.75/0.5/0.25 机箱高
        # ============================================================
        pipe_r = pipe_d / 2.0
        chamfer_cx = -Lb / 2.0 + Cb / 2.0
        chamfer_cy = -Wb / 2.0 + Cb / 2.0
        for k in range(-1, 2):
            pz = Tp + 0.5 * Hb + k * 0.25 * Hb
            pipe = Cone(
                Vec3(chamfer_cx, chamfer_cy, pz),
                Vec3(chamfer_cx - pipe_len * inv_sqrt2,
                     chamfer_cy - pipe_len * inv_sqrt2, pz),
                pipe_r, pipe_r)
            parts.append(pipe.color(0.6, 0.62, 0.65, 1))

        # ============================================================
        # 电气盒：左上切角面（-X,+Y角）沿法线 (-1,+1)/sqrt(2) 外凸，Z向居中于机箱
        # 局部X向=法向、Y向=沿斜边向，rotz(135度) 后 +X 对齐法线
        # ============================================================
        elec_cx = -Lb / 2.0 + Cb / 2.0 - (elec_t / 2.0) * inv_sqrt2
        elec_cy = Wb / 2.0 - Cb / 2.0 + (elec_t / 2.0) * inv_sqrt2
        elec_z0 = Tp + (Hb - elec_h) / 2.0
        elec = loft_z_prism(elec_t, elec_w, elec_z0, elec_z0 + elec_h)
        elec = translate(elec_cx, elec_cy, 0.0) * rotz(0.75 * math.pi) * elec
        parts.append(elec.color(0.8, 0.8, 0.8, 1))

        # ============================================================
        # 整体组装输出
        # ============================================================
        self['吸顶式风机盘管'] = combine(*parts)


if __name__ == "__main__":
    FinalGeometry = pythonModel()
    place(FinalGeometry)
