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
        self['设备名称'] = Attr('三管制风机盘管', obvious=True, group='专业属性')
        self['材质'] = Attr('镀锌钢板', obvious=True, group='专业属性')
        # ===== 机箱属性：总体尺寸 =====
        # 设备高 = 设备总高（地面到箱体顶面）= 箱体高250 + 底座高35 + 支腿高70 - 0.5*内腔高12.5
        self['设备高'] = Attr(342.5, obvious=True, group='机箱属性')
        self['机箱长'] = Attr(1000.0, obvious=True, group='机箱属性')
        self['底座宽'] = Attr(440.0, obvious=True, group='机箱属性')
        self['底座高'] = Attr(35.0, obvious=True, group='机箱属性')
        self['底座壁厚'] = Attr(10.0, obvious=True, group='机箱属性')
        self['底座长度外伸量'] = Attr(30.0, obvious=True, group='机箱属性')
        # ===== 风机属性：风机组件 =====
        self['风机直径'] = Attr(220.0, obvious=True, group='风机属性')
        self['风机长度'] = Attr(300.0, obvious=True, group='风机属性')
        # ===== 管口属性：水管接口 =====
        self['水管直径'] = Attr(20.0, obvious=True, group='管口属性')
        self['水管伸出长'] = Attr(80.0, obvious=True, group='管口属性')
        self['底座排水口直径'] = Attr(25.0, obvious=True, group='管口属性')
        # ===== 最终几何输出槽位 =====
        self['三管制风机盘管'] = Attr(None, show=True)

        # ============================================================
        # 驱动点（特征点）定义：replace 之前定义
        # 箱底Z box_z0 = 2.5*[底座高] + 0.5*[底座壁厚]（支腿底面内腔半高 + 支腿高）
        # 箱体高 H = [设备高] - box_z0（派生）
        # ============================================================
        # 三水管轴线终点（圆柱表面圆心，-X侧）：三根各一个点
        self.setDrivenFeaturePoint('水管下', SnapMode.GeometricCenter,
            '[定位点X] - [机箱长]/2 - [水管伸出长]',
            '[定位点Y]',
            '[定位点Z] + 1.875*[底座高] + 0.375*[底座壁厚] + 0.25*[设备高]')
        self.setDrivenFeaturePoint('水管中', SnapMode.GeometricCenter,
            '[定位点X] - [机箱长]/2 - [水管伸出长]',
            '[定位点Y]',
            '[定位点Z] + 1.25*[底座高] + 0.25*[底座壁厚] + 0.5*[设备高]')
        self.setDrivenFeaturePoint('水管上', SnapMode.GeometricCenter,
            '[定位点X] - [机箱长]/2 - [水管伸出长]',
            '[定位点Y]',
            '[定位点Z] + 0.625*[底座高] + 0.125*[底座壁厚] + 0.75*[设备高]')

        # 水箱打孔剪切布尔圆柱表面圆心（-X侧）
        self.setDrivenFeaturePoint('排水孔圆心', SnapMode.GeometricCenter,
            '[定位点X] - ([机箱长] + 2*[底座长度外伸量])/2',
            '[定位点Y]',
            '[定位点Z] + 0.5*[底座高]')

        # 电气盒背面矩形截面形心（-X侧，最外侧X=-机箱长/2-40）
        self.setDrivenFeaturePoint('电气盒背面形心', SnapMode.GeometricCenter,
            '[定位点X] - [机箱长]/2 - 40',
            '[定位点Y] + [底座宽]/2 - 60',
            '[定位点Z] + [设备高] - 2*[底座壁厚] - 50')

        # 百叶格栅群左视图面矩形截面形心（X=0，格栅群长度中心）
        self.setDrivenFeaturePoint('格栅群形心', SnapMode.GeometricCenter,
            '[定位点X]',
            '[定位点Y] - [底座宽]/2 + 0.1*[底座宽]/2',
            '[定位点Z] + 0.6875*[底座高] + 0.1375*[底座壁厚] + 0.725*[设备高] - 15')

        # 格栅群形心沿Y轴正向偏移一个底座宽
        self.setDrivenFeaturePoint('格栅群形心偏移', SnapMode.GeometricCenter,
            '[定位点X]',
            '[定位点Y] - [底座宽]/2 + 0.1*[底座宽]/2 + [底座宽]',
            '[定位点Z] + 0.6875*[底座高] + 0.1375*[底座壁厚] + 0.725*[设备高] - 15')

        self.replace()

    @export
    def replace(self):
        # ---------- 读取参数 ----------
        L = float(self['机箱长'])
        box_w = float(self['底座宽'])
        device_h = float(self['设备高'])
        base_h = float(self['底座高'])
        base_wall = float(self['底座壁厚'])
        base_ext = float(self['底座长度外伸量'])
        drain_d = float(self['底座排水口直径'])
        volute_d = float(self['风机直径'])
        fan_len = float(self['风机长度'])
        pipe_d = float(self['水管直径'])
        pipe_len = float(self['水管伸出长'])

        # ---------- 参数合法性检查 ----------
        if min(L, box_w, device_h, base_h, base_wall, base_ext,
               drain_d, volute_d, fan_len, pipe_d, pipe_len) <= 0:
            raise ValueError('尺寸参数必须为正数，请检查输入')

        # ---------- 派生尺寸（联动关系） ----------
        base_l = L + 2.0 * base_ext                       # 底座长（长度方向外伸）
        base_w = box_w + 2.0 * base_wall                  # 底座外宽（宽度方向外伸=壁厚）
        leg_h = 2.0 * base_h                              # 支腿高 = 2 * 底座高
        leg_len = 5.0 * base_wall                         # 支腿长 = 5 * 底座壁厚
        leg_z_bot = base_wall + (base_h - base_wall) / 2.0  # 支腿底面 = 内腔底面 + 半高
        box_z0 = leg_z_bot + leg_h                        # 箱体底面Z（被支腿抬高）= 2.5*底座高 + 0.5*底座壁厚
        H = device_h - box_z0                             # 箱体高（派生）：设备高 - 箱底Z
        box_z1 = device_h                                 # 箱体顶面Z = 设备高
        if H <= 0:
            raise ValueError('设备高必须大于底座高度+支腿高度，请检查输入')

        fan_d = volute_d * 9.0 / 11.0                     # 风轮直径 = 风机直径 × 9/11
        fan_r = fan_d / 2.0                               # 风轮半径
        volute_r = volute_d / 2.0                         # 蜗壳外半径 = 风机直径/2
        motor_d = volute_d * 5.0 / 11.0                   # 电机直径 = 风机直径 × 5/11
        motor_r = motor_d / 2.0
        motor_l = L * 0.1                                 # 电机长 = 机箱长 × 0.1

        elec_z_top = box_z1 - 2.0 * base_wall             # 电气盒顶面Z = 设备高 - 2*底座壁厚
        fan_cz = elec_z_top - volute_r                    # 风机中心Z（右下角线对蜗壳轴线）
        fan_cy = box_w / 2.0 + volute_r + 50.0            # 风机中心Y（连接段左端贴箱体背面）

        cavity_len = fan_len                         # 空腔长度 = 风机长度 × 1.1
        volute_len = cavity_len                           # 蜗壳主圆筒长度 = 空腔长度
        fan_rotor_len = cavity_len / 2.0                  # 风轮长度 = 0.5 × 空腔长度
        pipe_space = 0.25 * H                             # 水管间距 = 0.25 * 箱体高
        pipe_z_mid = box_z0 + H / 2.0                     # 中管Z（箱体高度居中）
        shaft_d = 25.0
        shaft_r = shaft_d / 2.0

        parts = []

        # ============================================================
        # 底座（接水盘）：外长方体 - 内腔 = 顶部开口水箱
        # ============================================================
        base_outer = loft_z_prism(base_l, base_w, 0.0, base_h)
        base_inner = loft_z_prism(base_l - 2.0 * base_wall,
                                  base_w - 2.0 * base_wall,
                                  base_wall, base_h)
        base = base_outer - base_inner
        base = base.color(0.85, 0.85, 0.85, 1)

        # 冷凝水排水孔：对底座X-侧壁做圆柱布尔减（直径由底座排水口直径控制）
        drain_r = drain_d / 2.0
        drain_hole = Cone(
            Vec3(-base_l / 2.0 - 1.0, 0.0, base_h / 2.0),
            Vec3(-base_l / 2.0 + base_wall + 1.0, 0.0, base_h / 2.0),
            drain_r, drain_r)
        base = base - drain_hole
        base = base.color(0.85, 0.85, 0.85, 1)
        parts.append(base)

        # ============================================================
        # 支腿×2：贴箱体两端，底面置于水箱内腔半高处
        # ============================================================
        leg1 = loft_z_prism(leg_len, box_w, leg_z_bot, leg_z_bot + leg_h)
        leg1 = translate(-L / 2.0 + leg_len / 2.0, 0.0, 0.0) * leg1
        leg2 = loft_z_prism(leg_len, box_w, leg_z_bot, leg_z_bot + leg_h)
        leg2 = translate(L / 2.0 - leg_len / 2.0, 0.0, 0.0) * leg2
        parts.append(leg1.color(0.8, 0.8, 0.8, 1))
        parts.append(leg2.color(0.8, 0.8, 0.8, 1))

        # ============================================================
        # 箱体外壳 + 正面百叶格栅（内嵌长槽，宽=0.1*箱体外壳宽）
        # ============================================================
        box = loft_z_prism(L, box_w, box_z0, box_z1)

        grille_n = 10                                   # 槽数量
        grille_bar_t = 6.0                              # 槽间筋条厚度(Z)
        grille_w = 0.1 * box_w                          # 槽宽 = 0.1 * 箱体外壳宽
        grille_cy = -box_w / 2.0 + grille_w / 2.0       # 槽Y中心（嵌正面Y-侧壁内）
        grille_z0 = box_z0 + H * 0.45                   # 格栅区底
        grille_z1 = box_z1 - 30.0                       # 格栅区顶
        grille_gap = (grille_z1 - grille_z0 - (grille_n - 1) * grille_bar_t) / grille_n
        grille_list = []
        for i in range(grille_n):
            slot_z0 = grille_z0 + i * (grille_gap + grille_bar_t)
            slot = loft_z_prism(L - 160.0, grille_w, slot_z0, slot_z0 + grille_gap)
            slot = translate(0.0, grille_cy, 0.0) * slot
            grille_list.append(slot)
        box = box - combine(*grille_list)
        box = box.color(0.85, 0.85, 0.85, 1)
        parts.append(box)

        # ============================================================
        # 风机组件X方向布局：左蜗壳-电机-右蜗壳
        # ============================================================
        motor_x0 = -motor_l / 2.0
        motor_x1 = motor_l / 2.0
        shaft_exp = 50.0
        volute1_x1 = motor_x0 - shaft_exp + 15.0
        volute1_x0 = volute1_x1 - volute_len
        volute2_x0 = motor_x1 + shaft_exp - 15.0
        volute2_x1 = volute2_x0 + volute_len
        volute1_cx = (volute1_x0 + volute1_x1) / 2.0
        volute2_cx = (volute2_x0 + volute2_x1) / 2.0
        # 风轮：居中半长 = 0.5 * 空腔长度
        fan1_x0 = volute1_cx - fan_rotor_len / 2.0
        fan1_x1 = volute1_cx + fan_rotor_len / 2.0
        fan2_x0 = volute2_cx - fan_rotor_len / 2.0
        fan2_x1 = volute2_cx + fan_rotor_len / 2.0
        # 连接轴：风轮内端面到电机端面（左右对称）
        shaft_l_x0 = fan1_x1
        shaft_l_x1 = motor_x0
        shaft_r_x0 = motor_x1
        shaft_r_x1 = fan2_x0

        # 蜗壳：实心大圆柱 - 贯通内腔圆柱（两端开口为进风口）
        volute1 = Cone(Vec3(volute1_x0, fan_cy, fan_cz), Vec3(volute1_x1, fan_cy, fan_cz),
                       volute_r, volute_r)
        cavity1 = Cone(Vec3(volute1_x0, fan_cy, fan_cz), Vec3(volute1_x1, fan_cy, fan_cz),
                       fan_r, fan_r)
        volute1_hollow = (volute1 - cavity1).color(0.8, 0.8, 0.8, 1)
        volute2 = Cone(Vec3(volute2_x0, fan_cy, fan_cz), Vec3(volute2_x1, fan_cy, fan_cz),
                       volute_r, volute_r)
        cavity2 = Cone(Vec3(volute2_x0, fan_cy, fan_cz), Vec3(volute2_x1, fan_cy, fan_cz),
                       fan_r, fan_r)
        volute2_hollow = (volute2 - cavity2).color(0.8, 0.8, 0.8, 1)
        parts.append(volute1_hollow)
        parts.append(volute2_hollow)

        # 风轮（实心圆柱，居中半长）
        fan1 = Cone(Vec3(fan1_x0, fan_cy, fan_cz), Vec3(fan1_x1, fan_cy, fan_cz), fan_r, fan_r)
        fan2 = Cone(Vec3(fan2_x0, fan_cy, fan_cz), Vec3(fan2_x1, fan_cy, fan_cz), fan_r, fan_r)
        parts.append(fan1.color(0.45, 0.45, 0.5, 1))
        parts.append(fan2.color(0.45, 0.45, 0.5, 1))

        # 中间电机
        motor = Cone(Vec3(motor_x0, fan_cy, fan_cz), Vec3(motor_x1, fan_cy, fan_cz),
                     motor_r, motor_r)
        parts.append(motor.color(0.3, 0.3, 0.32, 1))

        # 连接轴（左右对称：风轮内端面到电机端面）
        shaft_l = Cone(Vec3(shaft_l_x0, fan_cy, fan_cz), Vec3(shaft_l_x1, fan_cy, fan_cz),
                       shaft_r, shaft_r)
        shaft_r = Cone(Vec3(shaft_r_x0, fan_cy, fan_cz), Vec3(shaft_r_x1, fan_cy, fan_cz),
                       shaft_r, shaft_r)
        parts.append(shaft_l.color(0.55, 0.55, 0.55, 1))
        parts.append(shaft_r.color(0.55, 0.55, 0.55, 1))

        # ============================================================
        # 出风口连接段（矩形风道）：
        # 宽 = 0.5*蜗壳直径 + 50，高 = 0.5*蜗壳直径，长 = 蜗壳拉伸距离
        # 右下角线（右端Y=蜗壳轴线、底面Z=蜗壳轴线）与蜗壳轴线重合
        # 左端Y贴合箱体背面；并对连接段做蜗壳内腔布尔减
        # ============================================================
        duct_w = volute_r + 50.0                          # 宽 = 0.5*蜗壳直径 + 50
        duct_h = volute_r                                  # 高 = 0.5*蜗壳直径
        duct_z_top = elec_z_top                            # 顶面与电气盒顶面同高
        duct_z_bot = duct_z_top - duct_h                   # 底面 = 蜗壳轴线Z
        duct_y0 = box_w / 2.0                              # 左端Y = 箱体背面
        duct_y1 = fan_cy                                   # 右端Y = 蜗壳轴线
        duct_cy = (duct_y0 + duct_y1) / 2.0

        duct1 = loft_z_prism(volute_len, duct_w, duct_z_bot, duct_z_top)
        duct1 = translate(volute1_cx, duct_cy, 0.0) * duct1
        duct1 = duct1 - cavity1                            # 挖去蜗壳内腔（进风口）部分
        duct1 = duct1.color(0.8, 0.8, 0.8, 1)
        duct2 = loft_z_prism(volute_len, duct_w, duct_z_bot, duct_z_top)
        duct2 = translate(volute2_cx, duct_cy, 0.0) * duct2
        duct2 = duct2 - cavity2
        duct2 = duct2.color(0.8, 0.8, 0.8, 1)
        parts.append(duct1)
        parts.append(duct2)

        # ============================================================
        # 水管×3：X-端面伸出，间距 = 0.25 * 箱体高，箱高居中
        # ============================================================
        pipe_r = pipe_d / 2.0
        for k in range(-1, 2):
            pz = pipe_z_mid + k * pipe_space
            pipe = Cone(Vec3(-L / 2.0 - pipe_len, 0.0, pz), Vec3(-L / 2.0, 0.0, pz),
                        pipe_r, pipe_r)
            parts.append(pipe.color(0.6, 0.62, 0.65, 1))

        # ============================================================
        # 电气盒：置于X-端面左上角（Y正侧），向Z负向平移2*底座壁厚
        # ============================================================
        elec_thick = 40.0
        elec_w = 120.0
        elec_h = 100.0
        elec = loft_z_prism(elec_thick, elec_w, elec_z_top - elec_h, elec_z_top)
        elec = translate(-L / 2.0 - elec_thick / 2.0, box_w / 2.0 - elec_w / 2.0, 0.0) * elec
        parts.append(elec.color(0.8, 0.8, 0.8, 1))

        # ============================================================
        # 整体组装输出
        # ============================================================
        self['三管制风机盘管'] = combine(*parts)


if __name__ == "__main__":
    FinalGeometry = pythonModel()
    place(FinalGeometry)
