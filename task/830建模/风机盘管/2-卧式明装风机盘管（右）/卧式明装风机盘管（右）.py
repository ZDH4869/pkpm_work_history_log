from pyp3d import *


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


class pythonModel(Component):
    def __init__(self):
        Component.__init__(self)
        # ===== 专业属性 =====
        self['设备名称'] = Attr('卧式明装风机盘管（右）', obvious=True, group='专业属性')
        self['材质'] = Attr('镀锌钢板', obvious=True, group='专业属性')
        # ===== 机箱属性：总体尺寸 =====
        self['机箱长'] = Attr(1000.0, obvious=True, group='机箱属性')
        self['机箱宽'] = Attr(460.0, obvious=True, group='机箱属性')
        self['机箱高'] = Attr(250.0, obvious=True, group='机箱属性')
        # ===== 管口属性：右端（+X）三根水管 =====
        self['水管直径'] = Attr(20.0, obvious=True, group='管口属性')
        self['水管伸出长'] = Attr(80.0, obvious=True, group='管口属性')
        # ===== 最终几何输出槽位 =====
        self['卧式明装风机盘管'] = Attr(None, show=True)

        # ============================================================
        # 驱动点（特征点）定义：replace 之前定义
        # 表达式仅引用 obvious=True 的数值参数
        # ============================================================
        # 百叶格栅群背面外表面矩形截面形心（-Y面，槽区长0.8L、区高0.27H~0.76H居中）
        self.setDrivenFeaturePoint('百叶格栅形心', SnapMode.GeometricCenter,
            '[定位点X]',
            '[定位点Y] - [机箱宽]/2',
            '[定位点Z] + 0.515*[机箱高]')

        # 底回风格栅群底面外表面矩形截面形心（Z=0面，排列长0.7L居中，槽区Y中心=0.39*机箱宽-52.5）
        self.setDrivenFeaturePoint('回风格栅形心', SnapMode.GeometricCenter,
            '[定位点X]',
            '[定位点Y] + 0.275*[机箱宽]',
            '[定位点Z]')

        # 三水管外端面圆心（+X侧）：下/中/上各一个点，Z=0.2H/0.5H/0.8H
        self.setDrivenFeaturePoint('水管下', SnapMode.GeometricCenter,
            '[定位点X] + [机箱长]/2 + [水管伸出长]',
            '[定位点Y]',
            '[定位点Z] + 0.2*[机箱高]')
        self.setDrivenFeaturePoint('水管中', SnapMode.GeometricCenter,
            '[定位点X] + [机箱长]/2 + [水管伸出长]',
            '[定位点Y]',
            '[定位点Z] + 0.5*[机箱高]')
        self.setDrivenFeaturePoint('水管上', SnapMode.GeometricCenter,
            '[定位点X] + [机箱长]/2 + [水管伸出长]',
            '[定位点Y]',
            '[定位点Z] + 0.8*[机箱高]')

        # 电气盒外表面（+X最外侧）矩形截面形心
        self.setDrivenFeaturePoint('电气盒形心', SnapMode.GeometricCenter,
            '[定位点X] + 0.54*[机箱长]',
            '[定位点Y] + 0.37*[机箱宽]',
            '[定位点Z] + 0.72*[机箱高]')

        self.replace()

    @export
    def replace(self):
        # ---------- 读取参数 ----------
        L = float(self['机箱长'])
        W = float(self['机箱宽'])
        H = float(self['机箱高'])
        pipe_d = float(self['水管直径'])
        pipe_len = float(self['水管伸出长'])

        # ---------- 派生尺寸（与机箱长宽高比例绑定，实现协调变化） ----------
        grille_n = 10               # 百叶格栅数量（固定）
        grille_bar_t = 0.024 * H    # 百叶槽间筋条厚(Z) = 0.024*机箱高
        grille_cut = 0.065 * W      # 百叶切深(Y) = 0.065*机箱宽
        ret_n = 30                  # 回风格栅数量（固定）
        ret_bar_t = 0.005 * L       # 回风槽间筋条厚(X) = 0.005*机箱长
        ret_depth = 0.23 * W        # 回风槽深(Y) = 0.23*机箱宽
        ret_cut = 0.12 * H          # 回风切深(Z) = 0.12*机箱高
        elec_t = 0.04 * L           # 电气盒厚(X) = 0.04*机箱长
        elec_w = 0.26 * W           # 电气盒宽(Y) = 0.26*机箱宽
        elec_h = 0.4 * H            # 电气盒高(Z) = 0.4*机箱高
        elec_top_gap = 0.08 * H     # 电气盒顶面距箱顶(Z) = 0.08*机箱高

        # ---------- 参数合法性检查 ----------
        if min(L, W, H, pipe_d, pipe_len) <= 0:
            raise ValueError('尺寸参数必须为正数，请检查输入')

        parts = []

        # ============================================================
        # 箱体外壳：x∈[-L/2,L/2], y∈[-W/2,W/2], z∈[0,H]，前表面=+Y
        # ============================================================
        box = loft_z_prism(L, W, 0.0, H)

        # ============================================================
        # 背面出风百叶格栅（水平槽，沿X通长、沿Z阵列，从-Y面向内切）
        # 槽长 = 0.8*机箱长（两端各留0.1L），区高 = 0.27H ~ 0.76H
        # ============================================================
        grille_len = 0.8 * L
        grille_z0 = 0.27 * H
        grille_z1 = 0.76 * H
        grille_gap = (grille_z1 - grille_z0 - (grille_n - 1) * grille_bar_t) / grille_n
        if grille_gap <= 0:
            raise ValueError('百叶格栅数量过多或筋条过厚，请检查输入')
        grille_cy = -W / 2.0 + grille_cut / 2.0       # 槽从-Y面向内切深
        grille_list = []
        for i in range(grille_n):
            slot_z0 = grille_z0 + i * (grille_gap + grille_bar_t)
            slot = loft_z_prism(grille_len, grille_cut, slot_z0, slot_z0 + grille_gap)
            slot = translate(0.0, grille_cy, 0.0) * slot
            grille_list.append(slot)
        box = box - combine(*grille_list)
        box = box.color(0.85, 0.85, 0.85, 1)

        # ============================================================
        # 底面回风格栅（竖槽，沿Y、沿X阵列，从底面向内切）
        # 排列区长 = 0.7*机箱长（两端各留0.15L），前边距 = 0.11*机箱宽
        # ============================================================
        ret_len = 0.7 * L
        ret_front_margin = 0.11 * W
        ret_cy = W / 2.0 - ret_front_margin - ret_depth / 2.0
        ret_gap = (ret_len - (ret_n - 1) * ret_bar_t) / ret_n
        if ret_gap <= 0:
            raise ValueError('回风格栅数量过多，请检查输入')
        ret_x0 = -ret_len / 2.0
        ret_list = []
        for i in range(ret_n):
            slot_x0 = ret_x0 + i * (ret_gap + ret_bar_t)
            slot_cx = slot_x0 + ret_gap / 2.0
            slot = loft_z_prism(ret_gap, ret_depth, 0.0, ret_cut)
            slot = translate(slot_cx, ret_cy, 0.0) * slot
            ret_list.append(slot)
        box = box - combine(*ret_list)
        box = box.color(0.85, 0.85, 0.85, 1)
        parts.append(box)

        # ============================================================
        # 水管×3：右端面（+X）伸出，Y=0居中，Z = 0.2H / 0.5H / 0.8H
        # ============================================================
        pipe_r = pipe_d / 2.0
        for k in range(-1, 2):
            pz = 0.5 * H + k * 0.3 * H
            pipe = Cone(Vec3(L / 2.0, 0.0, pz), Vec3(L / 2.0 + pipe_len, 0.0, pz),
                        pipe_r, pipe_r)
            parts.append(pipe.color(0.6, 0.62, 0.65, 1))

        # ============================================================
        # 电气盒：右端（+X）外凸，贴+Y前表面，顶面距箱顶20
        # x∈[L/2, L/2+40], y∈[W/2-120, W/2], z∈[H-120, H-20]
        # ============================================================
        elec = loft_z_prism(elec_t, elec_w, H - elec_top_gap - elec_h, H - elec_top_gap)
        elec = translate(L / 2.0 + elec_t / 2.0, W / 2.0 - elec_w / 2.0, 0.0) * elec
        parts.append(elec.color(0.8, 0.8, 0.8, 1))

        # ============================================================
        # 整体组装输出
        # ============================================================
        self['卧式明装风机盘管'] = combine(*parts)


if __name__ == "__main__":
    FinalGeometry = pythonModel()
    place(FinalGeometry)
