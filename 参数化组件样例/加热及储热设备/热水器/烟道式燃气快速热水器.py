from pyp3d import *
import math


class pythonModel(Component):
    def __init__(self):
        Component.__init__(self)
        # ========== 设备名称 ==========
        self['设备名称'] = Attr('烟道式燃气快速热水器', obvious=True)

        # ========== 用户可修改参数 ==========
        self['水箱长度'] = Attr(300.0, obvious=True)
        self['水箱宽度'] = Attr(200.0, obvious=True)
        self['水箱高度'] = Attr(500.0, obvious=True)
        self['入水管半径'] = Attr(40.0, obvious=True)
        self['中心出水管半径'] = Attr(5.0, obvious=True)
        self['中心出水管高度'] = Attr(350.0, obvious=True)
        self['左侧出水管群间距'] = Attr(100.0, obvious=True)
        self['右侧出水管群间距'] = Attr(50.0, obvious=True)
        self['中心出水管群X偏移'] = Attr(0.0, obvious=True)
        self['中心出水管群Y偏移'] = Attr(0.0, obvious=True)

        # ========== 绑定到中心出水管半径的参数（readonly，已隐藏） ==========
        self['螺栓a半径'] = Attr(10.0, obvious=False, readonly=True)
        self['螺栓b半径'] = Attr(15.0, obvious=False, readonly=True)
        self['螺栓c半径'] = Attr(8.0, obvious=False, readonly=True)
        self['球阀半径'] = Attr(8.0, obvious=False, readonly=True)
        self['阀轴柱半径'] = Attr(4.0, obvious=False, readonly=True)
        self['连接柱半径'] = Attr(1.0, obvious=False, readonly=True)
        self['套柱半径'] = Attr(2.0, obvious=False, readonly=True)
        self['把手边长'] = Attr(1.5, obvious=False, readonly=True)
        self['把手Bar边长'] = Attr(1.0, obvious=False, readonly=True)
        self['阀轴柱高度'] = Attr(20.0, obvious=False, readonly=True)
        self['连接柱高度'] = Attr(6.0, obvious=False, readonly=True)
        self['套柱半高'] = Attr(2.0, obvious=False, readonly=True)

        # ========== 绑定到中心出水管高度的参数（readonly，已隐藏） ==========
        self['螺栓a高度'] = Attr(10.0, obvious=False, readonly=True)
        self['螺栓b高度'] = Attr(10.0, obvious=False, readonly=True)
        self['螺栓c高度'] = Attr(3.0, obvious=False, readonly=True)
        self['螺栓间距'] = Attr(90.0, obvious=False, readonly=True)
        self['螺栓c与c2间距'] = Attr(90.0, obvious=False, readonly=True)
        self['螺栓c起始偏移'] = Attr(15.0, obvious=False, readonly=True)
        self['把手Bar高度'] = Attr(15.0, obvious=False, readonly=True)

        # ========== 固定参数（readonly，已隐藏） ==========
        self['水箱厚度'] = Attr(10.0, obvious=False, readonly=True)
        self['入水管高度'] = Attr(100.0, obvious=True, readonly=True)
        self['显示屏长度'] = Attr(100.0, obvious=False, readonly=True)
        self['显示屏宽度'] = Attr(10.0, obvious=False, readonly=True)
        self['仪表盘半径'] = Attr(10.0, obvious=False, readonly=True)

        # ========== 最终输出 ==========
        self['烟道式燃气快速热水器'] = Attr(None, show=True)

        # ========== 驱动点设置 ==========
        self.setDrivenFeaturePoint('入水管顶部', SnapMode.EndPoint,
            '[定位点X]', '[定位点Y]', '[定位点Z]+[水箱高度]+[入水管高度]')
        self.setDrivenFeaturePoint('中心出水管底部', SnapMode.EndPoint,
            '[定位点X]+[中心出水管群X偏移]',
            '[定位点Y]+[中心出水管群Y偏移]',
            '[定位点Z]-[中心出水管高度]')
        self.setDrivenFeaturePoint('左侧出水管底部', SnapMode.EndPoint,
            '[定位点X]+[中心出水管群X偏移]-[左侧出水管群间距]',
            '[定位点Y]+[中心出水管群Y偏移]',
            '[定位点Z]-[中心出水管高度]')
        self.setDrivenFeaturePoint('右侧出水管底部', SnapMode.EndPoint,
            '[定位点X]+[中心出水管群X偏移]+[右侧出水管群间距]',
            '[定位点Y]+[中心出水管群Y偏移]',
            '[定位点Z]-[中心出水管高度]')
        self.setDrivenFeaturePoint('配电口', SnapMode.EndPoint,
            '[定位点X]+[中心出水管群X偏移]-[左侧出水管群间距]-[中心出水管半径]-[水箱长度]/10',
            '[定位点Y]+[中心出水管群Y偏移]',
            '[定位点Z]')

        self.replace()

    @export
    def replace(self):
        # ========== 读取用户可修改参数 ==========
        L = self['水箱长度']
        W = self['水箱宽度']
        H = self['水箱高度']
        R_inlet = self['入水管半径']
        R_outlet = self['中心出水管半径']
        H_outlet = self['中心出水管高度']
        left_spacing = self['左侧出水管群间距']
        right_spacing = self['右侧出水管群间距']
        center_x = self['中心出水管群X偏移']
        center_y = self['中心出水管群Y偏移']

        # ========== 计算绑定到中心出水管半径的参数 ==========
        R_a = R_outlet * 2.0       # 10/5
        R_b = R_outlet * 3.0       # 15/5
        R_c = R_outlet * 1.6       # 8/5
        R_valve = R_outlet * 1.6   # 8/5
        R_valve_axis = R_outlet * 0.8   # 4/5
        R_conn = R_outlet * 0.2    # 1/5
        R_sleeve = R_outlet * 0.4  # 2/5
        handle_side = R_outlet * 0.3     # 1.5/5
        handle_bar_side = R_outlet * 0.2 # 1.0/5
        H_valve_axis = R_outlet * 4.0   # 20/5
        H_conn = R_outlet * 1.2          # 6/5
        H_sleeve = R_outlet * 0.4        # 2/5

        self['螺栓a半径'] = R_a
        self['螺栓b半径'] = R_b
        self['螺栓c半径'] = R_c
        self['球阀半径'] = R_valve
        self['阀轴柱半径'] = R_valve_axis
        self['连接柱半径'] = R_conn
        self['套柱半径'] = R_sleeve
        self['把手边长'] = handle_side
        self['把手Bar边长'] = handle_bar_side
        self['阀轴柱高度'] = H_valve_axis
        self['连接柱高度'] = H_conn
        self['套柱半高'] = H_sleeve

        # ========== 计算绑定到中心出水管高度的参数 ==========
        H_a = H_outlet * (10.0 / 350.0)
        H_b = H_outlet * (10.0 / 350.0)
        H_c = H_outlet * (3.0 / 350.0)
        gap = H_outlet * (90.0 / 350.0)
        gap_cc = H_outlet * (90.0 / 350.0)
        offset_c = H_outlet * (15.0 / 350.0)
        handle_bar_height = H_outlet * (15.0 / 350.0)

        self['螺栓a高度'] = H_a
        self['螺栓b高度'] = H_b
        self['螺栓c高度'] = H_c
        self['螺栓间距'] = gap
        self['螺栓c与c2间距'] = gap_cc
        self['螺栓c起始偏移'] = offset_c
        self['把手Bar高度'] = handle_bar_height

        # ========== 读取固定参数 ==========
        T = self['水箱厚度']
        H_inlet = self['入水管高度']

        # ========== 计算派生参数 ==========
        disp_L = L / 3.0
        R_inst = H / 50.0
        self['显示屏长度'] = disp_L
        self['仪表盘半径'] = R_inst

        # ====== Step 1: 空心水箱（外水箱-内水箱布尔减法）======
        inner_L = L - 2 * T
        inner_W = W - 2 * T
        inner_H = H - 2 * T
        outer_box = Box(
            Vec3(-L/2.0, -W/2.0, 0), Vec3(-L/2.0, -W/2.0, H),
            Vec3(1, 0, 0), Vec3(0, 1, 0),
            L, W, L, W
        )
        inner_box = Box(
            Vec3(T - L/2.0, T - W/2.0, T),
            Vec3(T - L/2.0, T - W/2.0, H - T),
            Vec3(1, 0, 0), Vec3(0, 1, 0),
            inner_L, inner_W, inner_L, inner_W
        )
        tank = outer_box - inner_box

        # ====== Step 2: 入水管 ======
        inlet_pipe = Cone(Vec3(0, 0, H), Vec3(0, 0, H + H_inlet), R_inlet, R_inlet)

        # ====== Step 3: 中心出水管 ======
        outlet_pipe = Cone(Vec3(0, 0, 0), Vec3(0, 0, -H_outlet), R_outlet, R_outlet)

        # ====== Step 4: 螺栓a ======
        a_top_z = 0.0
        a_bot_z = -H_a
        bolt_a = Cone(Vec3(0, 0, a_top_z), Vec3(0, 0, a_bot_z), R_a, R_a)

        # ====== Step 5: 螺栓a2 ======
        a2_shift = gap + H_a
        a2_top_z = -a2_shift
        a2_bot_z = a2_top_z - H_a
        bolt_a2 = Cone(Vec3(0, 0, a2_top_z), Vec3(0, 0, a2_bot_z), R_a, R_a)

        # ====== Step 6: 螺栓b ======
        b_top_z = a2_bot_z
        b_bot_z = b_top_z - H_b
        bolt_b = Cone(Vec3(0, 0, b_top_z), Vec3(0, 0, b_bot_z), R_b, R_b)

        # ====== Step 7: 螺栓a3 ======
        a3_shift = gap + H_a + H_a + H_b
        a3_top_z = -a3_shift
        a3_bot_z = a3_top_z - H_a
        bolt_a3 = Cone(Vec3(0, 0, a3_top_z), Vec3(0, 0, a3_bot_z), R_a, R_a)

        # ====== Step 8: 螺栓b2 ======
        b2_top_z = b_top_z - gap - H_a
        b2_bot_z = b2_top_z - H_b
        bolt_b2 = Cone(Vec3(0, 0, b2_top_z), Vec3(0, 0, b2_bot_z), R_b, R_b)

        # ====== Step 9: 螺栓c ======
        c_top_z = b2_bot_z - offset_c
        c_bot_z = c_top_z - H_c
        bolt_c = Cone(Vec3(0, 0, c_top_z), Vec3(0, 0, c_bot_z), R_c, R_c)

        # ====== Step 10: 螺栓c2 ======
        c2_top_z = c_top_z - gap_cc
        c2_bot_z = c2_top_z - H_c
        bolt_c2 = Cone(Vec3(0, 0, c2_top_z), Vec3(0, 0, c2_bot_z), R_c, R_c)

        # ====== Step 11: 球阀d ======
        valve_z = (c_bot_z + c2_top_z) / 2.0
        ball_valve = translate(0, 0, valve_z) * scale(R_valve) * Sphere()

        # ====== 阀轴柱 ======
        valve_axis = Cone(
            Vec3(0, 0, valve_z),
            Vec3(0, -H_valve_axis, valve_z),
            R_valve_axis, R_valve_axis
        )

        # ====== 连接柱 ======
        conn_start_y = 0.0
        conn_end_y = conn_start_y - H_conn
        conn_column = translate(0, -H_valve_axis, 0) * Cone(
            Vec3(0, conn_start_y, valve_z),
            Vec3(0, conn_end_y, valve_z),
            R_conn, R_conn
        )

        # ====== 套柱 ======
        sleeve_center_y = (conn_start_y + conn_end_y) / 2.0
        sleeve_column = translate(0, -H_valve_axis, 0) * Cone(
            Vec3(0, sleeve_center_y + H_sleeve, valve_z),
            Vec3(0, sleeve_center_y - H_sleeve, valve_z),
            R_sleeve, R_sleeve
        )

        # ====== 把手（垂直于套柱轴线，从套柱轴线中点沿-Z方向拉伸）======
        sleeve_mid_y_global = -H_valve_axis + sleeve_center_y
        half = handle_side / 2.0
        section = Section(
            Vec2(-half, -half),
            Vec2(half, -half),
            Vec2(half, half),
            Vec2(-half, half)
        )
        section_3d = rotate(Vec3(1, 0, 0), math.pi) * section
        h0 = Vec3(0, sleeve_mid_y_global, valve_z)
        h1 = Vec3(0, sleeve_mid_y_global, valve_z - 14)
        path = Line(h0, h1)
        handle = Sweep(section_3d, path)

        # ====== 把手Bar ======
        handle_bar = Box(
            Vec3(0, sleeve_mid_y_global, valve_z),
            Vec3(0, sleeve_mid_y_global, valve_z - handle_bar_height),
            Vec3(1, 0, 0), Vec3(0, 1, 0),
            handle_bar_side, handle_bar_side, handle_bar_side, handle_bar_side
        )

        # ====== 组装出水管+螺栓+阀部件 ======
        pipe_parts = combine(
            outlet_pipe, bolt_a, bolt_a2, bolt_b, bolt_a3, bolt_b2,
            bolt_c, bolt_c2, ball_valve,
            valve_axis, conn_column, sleeve_column, handle, handle_bar
        )

        # ====== Step 12: 三组出水管群 ======
        center_group = translate(center_x, center_y, 0) * pipe_parts
        right_group = translate(center_x + right_spacing, center_y, 0) * pipe_parts
        left_group = translate(center_x - left_spacing, center_y, 0) * pipe_parts

        # ====== Step 13: 显示屏体 ======
        tank_center_x = -L / 2.0
        tank_center_y = -W / 2.0
        tank_center_z = H / 2.0
        disp_H = H / 10.0
        disp_center_x = tank_center_x + L / 3.0
        disp_center_y = tank_center_y - W / 2.0 + W / 2.0
        disp_center_z = tank_center_z - H / 4.0
        display = translate(disp_center_x, disp_center_y, disp_center_z) * scale(disp_L, T, disp_H) * Cube()

        # ====== Step 14: 仪表盘体 ======
        inst_x = tank_center_x + L / 4.0 + L / 2.0
        inst_y = tank_center_y - W / 2.0 + W / 2.0
        inst_z = tank_center_z - H * 3.0 / 8.0
        instrument = Cone(
            Vec3(inst_x, inst_y, inst_z),
            Vec3(inst_x, inst_y + T, inst_z),
            R_inst, R_inst
        )

        # ====== 最终组合 ======
        result = combine(
            tank,
            inlet_pipe,
            center_group,
            right_group,
            left_group,
            display,
            instrument
        )
        self['烟道式燃气快速热水器'] = result


if __name__ == "__main__":
    FinalGeometry = pythonModel()
    place(FinalGeometry)