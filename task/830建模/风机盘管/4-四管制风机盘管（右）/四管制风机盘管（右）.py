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
        self['设备名称'] = Attr('四管制风机盘管（右）', obvious=True, group='专业属性')
        self['材质'] = Attr('镀锌钢板', obvious=True, group='专业属性')
        # ===== 机箱属性：总体尺寸 =====
        self['设备长'] = Attr(1000.0, obvious=True, group='机箱属性')
        self['设备宽'] = Attr(440.0, obvious=True, group='机箱属性')
        self['设备高'] = Attr(342.5, obvious=True, group='机箱属性')
        self['底板厚度'] = Attr(35.0, obvious=True, group='机箱属性')
        self['底板外伸长量'] = Attr(150.0, obvious=True, group='机箱属性')
        # ===== 风机属性：风机组件 =====
        self['风机直径'] = Attr(220.0, obvious=True, group='风机属性')
        self['风机长度'] = Attr(300.0, obvious=True, group='风机属性')
        # ===== 管口属性：水管接口 =====
        self['水管直径'] = Attr(20.0, obvious=True, group='管口属性')
        self['水管长度'] = Attr(80.0, obvious=True, group='管口属性')
        self['底板水管直径'] = Attr(25.0, obvious=True, group='管口属性')
        self['底板水管长度'] = Attr(50.0, obvious=True, group='管口属性')
        # ===== 最终几何输出槽位 =====
        self['四管制风机盘管'] = Attr(None, show=True)

        # ============================================================
        # 驱动点（特征点）定义：replace 之前定义
        # 内部常量：接口面板厚40、前面板外板厚20（内板厚40）
        # ============================================================
        # 水管×4外表面圆心（2×2，+X侧，穿过接口面板）
        self.setDrivenFeaturePoint('水管左上', SnapMode.GeometricCenter,
            '[定位点X] + [设备长]/2 + 40 + [水管长度]',
            '[定位点Y] - 0.25*[设备宽] + 30',
            '[定位点Z] + 0.75*[设备高] - 11.25')
        self.setDrivenFeaturePoint('水管右上', SnapMode.GeometricCenter,
            '[定位点X] + [设备长]/2 + 40 + [水管长度]',
            '[定位点Y] + 0.25*[设备宽] - 30',
            '[定位点Z] + 0.75*[设备高] - 11.25')
        self.setDrivenFeaturePoint('水管左下', SnapMode.GeometricCenter,
            '[定位点X] + [设备长]/2 + 40 + [水管长度]',
            '[定位点Y] - 0.25*[设备宽] + 30',
            '[定位点Z] + 0.25*[设备高] + 46.25')
        self.setDrivenFeaturePoint('水管右下', SnapMode.GeometricCenter,
            '[定位点X] + [设备长]/2 + 40 + [水管长度]',
            '[定位点Y] + 0.25*[设备宽] - 30',
            '[定位点Z] + 0.25*[设备高] + 46.25')

        # 底板排水管外表面圆心（+X侧底板壁外伸端）
        self.setDrivenFeaturePoint('排水管外圆心', SnapMode.GeometricCenter,
            '[定位点X] + [设备长]/2 + [底板外伸长量] + [底板水管长度]',
            '[定位点Y]',
            '[定位点Z] + [底板厚度]/2')

        # 剪切后-Y外侧表面板（前面板外板矩形环）矩形截面形心
        # Y = -设备宽/2 - 50（50 = 内板厚40 + 外板半厚10）；Z = 0.625*设备高（外板顶=设备顶，高0.75*设备高）
        self.setDrivenFeaturePoint('前面板形心', SnapMode.GeometricCenter,
            '[定位点X]',
            '[定位点Y] - [设备宽]/2 - 50',
            '[定位点Z] + 0.625*[设备高]')

        # 前面板形心沿Y轴正向偏移：设备宽 + 0.5*内板宽20 → 简化 +设备宽/2 - 30
        self.setDrivenFeaturePoint('前面板形心偏移', SnapMode.GeometricCenter,
            '[定位点X]',
            '[定位点Y] + [设备宽]/2 - 30',
            '[定位点Z] + 0.625*[设备高]')

        self.replace()

    @export
    def replace(self):
        # ---------- 读取参数 ----------
        L = float(self['设备长'])
        box_w = float(self['设备宽'])
        device_h = float(self['设备高'])
        base_h = float(self['底板厚度'])
        base_ext = float(self['底板外伸长量'])
        volute_d = float(self['风机直径'])
        fan_len = float(self['风机长度'])
        pipe_d = float(self['水管直径'])
        pipe_len = float(self['水管长度'])
        drain_d = float(self['底板水管直径'])
        drain_len = float(self['底板水管长度'])

        # ---------- 参数合法性检查 ----------
        if min(L, box_w, device_h, base_h, base_ext, volute_d, fan_len,
               pipe_d, pipe_len, drain_d, drain_len) <= 0:
            raise ValueError('尺寸参数必须为正数，请检查输入')

        # ---------- 内部固定尺寸（非面板参数，待用户补充正式联动式） ----------
        base_wall = 10.0         # 底座壁厚
        panel_t = 20.0           # 前面板外板厚
        conn_panel_t = 40.0      # +X水管接口面板厚

        # ---------- 派生尺寸（联动关系，待用户补充正式联动式） ----------
        base_l = L + base_ext                               # 底板长 = 设备长 + 外伸长量（仅+X增长）
        box_z0 = base_h                                     # 箱体底面Z（落于底板顶面）
        box_z1 = device_h                                   # 箱体顶面Z = 设备高
        H = box_z1 - box_z0                                 # 箱体高（派生）= 设备高 - 底板厚度（补偿）
        if H <= 0:
            raise ValueError('设备高必须大于底板厚度，请检查输入')

        volute_r = volute_d / 2.0                           # 蜗壳外半径 = 风机直径/2
        fan_r = volute_d * 9.0 / 11.0 / 2.0                 # 风轮半径 = 风机直径×9/11/2
        motor_r = volute_d * 5.0 / 11.0 / 2.0               # 电机半径 = 风机直径×5/11/2
        motor_l = L * 0.1                                   # 电机长 = 设备长×0.1
        fan_cz = 0.5 * device_h                             # 蜗壳中心Z固定 = 0.5×设备高
        fan_cy = box_w / 2.0 + volute_r + 50.0              # 蜗壳中心Y

        cavity_len = fan_len                                # 空腔长度 = 风机长度
        volute_len = cavity_len                             # 蜗壳主圆筒长度
        fan_rotor_len = cavity_len / 2.0                    # 风轮长度 = 0.5×风机长度
        shaft_d = 25.0
        shaft_r = shaft_d / 2.0

        parts = []

        # ============================================================
        # 底板：实心板（无空腔），初始长宽=箱体外壳长宽，
        # 仅沿+X方向增长[底板外伸长量]，形心X偏移 外伸长量/2
        # ============================================================
        base = loft_z_prism(base_l, box_w, 0.0, base_h)
        base = translate(base_ext / 2.0, 0.0, 0.0) * base
        parts.append(base.color(0.85, 0.85, 0.85, 1))

        # ============================================================
        # 底板排水短管：+X侧底板壁外伸圆柱
        # ============================================================
        drain_r = drain_d / 2.0
        drain_pipe = Cone(
            Vec3(L / 2.0 + base_ext, 0.0, base_h / 2.0),
            Vec3(L / 2.0 + base_ext + drain_len, 0.0, base_h / 2.0),
            drain_r, drain_r)
        parts.append(drain_pipe.color(0.6, 0.62, 0.65, 1))

        # ============================================================
        # 箱体外壳
        # ============================================================
        box = loft_z_prism(L, box_w, box_z0, box_z1)
        parts.append(box.color(0.85, 0.85, 0.85, 1))

        # ============================================================
        # 前面板（-Y面）：外板(矩形环)叠放在内板(实心板)-Y外面
        # 内板厚 = 2×外板厚；外板高 = 0.75×设备高（顶=设备顶）；
        # 内板高 = 0.75×外板高（垂直居中于外板）；挖孔 = 内板外轮廓
        # ============================================================
        panel_l = L - 60.0                                  # 外板X长（自拟，待联动式）
        inner_l = panel_l - 60.0                            # 内板X长（自拟，待联动式）
        outer_h = 0.75 * device_h                           # 外板高 = 0.75×设备高
        outer_z0 = device_h - outer_h                       # 外板底面（顶=设备顶）
        outer_z1 = device_h
        outer_cz = (outer_z0 + outer_z1) / 2.0              # 外板中心Z
        inner_h = 0.75 * outer_h                            # 内板高 = 0.75×外板高
        inner_z0 = outer_cz - inner_h / 2.0                 # 内板垂直居中于外板
        inner_z1 = outer_cz + inner_h / 2.0

        inner_thick = 2.0 * panel_t                         # 内板厚 = 2×外板厚 = 40
        outer_cy = -box_w / 2.0 - panel_t / 2.0 - inner_thick  # 外板环中心Y（叠在内板-Y外）
        inner_cy = -box_w / 2.0 - inner_thick / 2.0         # 内板中心Y（贴箱体-Y面）

        # 外板（实心板）减去内板轮廓刀 → 矩形环
        outer_solid = translate(0.0, outer_cy, 0.0) * loft_z_prism(panel_l, panel_t, outer_z0, outer_z1)
        cutter = translate(0.0, outer_cy, 0.0) * loft_z_prism(inner_l, inner_thick, inner_z0, inner_z1)
        outer_ring = (outer_solid - cutter).color(0.85, 0.85, 0.85, 1)
        parts.append(outer_ring)

        # 内板（实心板）
        inner = translate(0.0, inner_cy, 0.0) * loft_z_prism(inner_l, inner_thick, inner_z0, inner_z1)
        parts.append(inner.color(0.82, 0.82, 0.82, 1))

        # ============================================================
        # 风机组件X方向布局：左蜗壳-电机-右蜗壳（同三管制）
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
        # 风轮：居中半长 = 0.5 × 风机长度
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
        # 出风口连接段（矩形风道）：底面=蜗壳轴线，顶=蜗壳顶
        # 宽 = 0.5*风机直径 + 50，高 = 0.5*风机直径，长 = 风机长度
        # ============================================================
        duct_w = volute_r + 50.0
        duct_h = volute_r
        duct_z_bot = fan_cz                                 # 底面 = 蜗壳轴线Z
        duct_z_top = fan_cz + volute_r                      # 顶面 = 蜗壳顶Z
        duct_y0 = box_w / 2.0
        duct_y1 = fan_cy
        duct_cy = (duct_y0 + duct_y1) / 2.0

        duct1 = loft_z_prism(volute_len, duct_w, duct_z_bot, duct_z_top)
        duct1 = translate(volute1_cx, duct_cy, 0.0) * duct1
        duct1 = duct1 - cavity1
        duct1 = duct1.color(0.8, 0.8, 0.8, 1)
        duct2 = loft_z_prism(volute_len, duct_w, duct_z_bot, duct_z_top)
        duct2 = translate(volute2_cx, duct_cy, 0.0) * duct2
        duct2 = duct2 - cavity2
        duct2 = duct2.color(0.8, 0.8, 0.8, 1)
        parts.append(duct1)
        parts.append(duct2)

        # ============================================================
        # +X端面水管接口面板（右视图内矩形面板，无独立电气盒）
        # ============================================================
        conn_w = box_w - 120.0                              # 面板宽(Y)（自拟，待联动式）
        conn_z0 = box_z0 + 40.0                             # 面板底Z（自拟）
        conn_z1 = box_z1 - 40.0                             # 面板顶Z（自拟）
        conn_cz = (conn_z0 + conn_z1) / 2.0
        conn_panel = loft_z_prism(conn_panel_t, conn_w, conn_z0, conn_z1)
        conn_panel = translate(L / 2.0 + conn_panel_t / 2.0, 0.0, 0.0) * conn_panel
        parts.append(conn_panel.color(0.8, 0.8, 0.8, 1))

        # ============================================================
        # 水管×4：+X端面2×2穿出接口面板
        # 水平间距 = 0.5*接口面板宽度，竖直间距 = 0.5*接口面板高度
        # ============================================================
        pipe_r = pipe_d / 2.0
        pipe_space_y = 0.5 * conn_w
        pipe_space_z = 0.5 * (conn_z1 - conn_z0)
        pipe_x0 = L / 2.0
        pipe_x1 = L / 2.0 + conn_panel_t + pipe_len
        for iy in (-1, 1):
            for iz in (-1, 1):
                py = iy * pipe_space_y / 2.0
                pz = conn_cz + iz * pipe_space_z / 2.0
                pipe = Cone(Vec3(pipe_x0, py, pz), Vec3(pipe_x1, py, pz),
                            pipe_r, pipe_r)
                parts.append(pipe.color(0.6, 0.62, 0.65, 1))

        # ============================================================
        # 整体组装输出
        # ============================================================
        self['四管制风机盘管'] = combine(*parts)


if __name__ == "__main__":
    FinalGeometry = pythonModel()
    place(FinalGeometry)
