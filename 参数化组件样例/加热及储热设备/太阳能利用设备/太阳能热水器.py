from pyp3d import *

# 太阳能热水器 - 截面重建
# 插入点 = point1 = 集水管左端面圆心 = ([定位点X], [定位点Y], [定位点Z])
# [定位点X/Y/Z] 是 BIMBase 隐式内置变量，不可定义为 Attr

class 太阳能热水器(Component):
    def __init__(self):
        Component.__init__(self)
        # ========== 显示和可调参数（按顺序）==========
        self['设备名称'] = Attr('太阳能热水器', obvious=True)
        # 保温桶中心高度：竖向柱Z起点到保温桶中心Z的距离，修改此值 → 竖向柱高度联动
        self['保温桶中心高度'] = Attr(1100.0, obvious=True)
        self['保温桶长度'] = Attr(1500.0, obvious=True)
        self['保温桶半径'] = Attr(250.0, obvious=True)           # 实际控制保温桶半径
        # 支撑宽度 = 水平柱长度 + 竖向柱半径 + 集水管半径（用户修改此值 → 水平柱长度联动）
        self['支撑宽度'] = Attr(762.5, obvious=True)
        self['集水管半径'] = Attr(50.0, obvious=True)
        self['集水管长度'] = Attr(1500.0, obvious=True)
        self['集热管间距'] = Attr(125.0, obvious=True)
        self['集热管数量'] = Attr(9.0, obvious=True)
        self['左侧水管半径'] = Attr(25.0, obvious=True)
        self['右侧水管半径'] = Attr(25.0, obvious=True)
        self['支撑柱直径'] = Attr(25.0, obvious=True)            # 统一控制水平柱和竖向柱直径

        # ========== 隐藏参数（仅内部计算用）==========
        self['水平柱直径'] = Attr(25.0)
        self['水平柱长度'] = Attr(700.0)
        self['竖向柱直径'] = Attr(25.0)
        self['竖向柱Z起点'] = Attr(-50.0)                     # = -集水管半径，在replace()中联动计算
        self['竖向柱Z终点'] = Attr(1050.0)
        self['排架管直径'] = Attr(50.0)
        self['太阳能板厚'] = Attr(10.0)
        self['圆环路径直径'] = Attr(400.0)
        self['圆环截面直径'] = Attr(40.0)

        # ========== 输出槽位 ==========
        self['热水器'] = Attr(None, show=True)

        # ========== 特征驱动点 ==========
        # 规则：1) 三轴都必须含 [定位点X/Y/Z]  2) 用 /2 替代 *0.5  3) 引用参数必须 obvious=True
        # point1 = 集水管左端面圆心 = 插入点
        self.setDrivenFeaturePoint('point1', SnapMode.GeometricCenter,
            '[定位点X]', '[定位点Y]', '[定位点Z]')
        # 保温桶左端面圆心  实际=(0, 700, 1050)  Z=保温桶中心高度-集水管半径
        self.setDrivenFeaturePoint('保温桶左端面圆心', SnapMode.GeometricCenter,
            '[定位点X]+[集水管长度]/2-[保温桶长度]/2',
            '[定位点Y]+[支撑宽度]-[支撑柱直径]/2-[集水管半径]',
            '[定位点Z]+[保温桶中心高度]-[集水管半径]')
        # 保温桶右端面圆心  实际=(1500, 700, 1050)
        self.setDrivenFeaturePoint('保温桶右端面圆心', SnapMode.GeometricCenter,
            '[定位点X]+[集水管长度]/2+[保温桶长度]/2',
            '[定位点Y]+[支撑宽度]-[支撑柱直径]/2-[集水管半径]',
            '[定位点Z]+[保温桶中心高度]-[集水管半径]')
        # 左侧水管底部截面圆心  实际=(150, 700, 750)  Z=保温桶中心高度-集水管半径-保温桶半径-50
        self.setDrivenFeaturePoint('左侧水管底圆心', SnapMode.GeometricCenter,
            '[定位点X]+[集水管长度]/2-[支撑宽度]+[支撑柱直径]/2+[集水管半径]+100',
            '[定位点Y]+[支撑宽度]-[支撑柱直径]/2-[集水管半径]',
            '[定位点Z]+[保温桶中心高度]-[集水管半径]-[保温桶半径]-50')
        # 右侧水管底部截面圆心  实际=(1350, 700, 750)
        self.setDrivenFeaturePoint('右侧水管底圆心', SnapMode.GeometricCenter,
            '[定位点X]+[集水管长度]/2+[支撑宽度]-[支撑柱直径]/2-[集水管半径]-100',
            '[定位点Y]+[支撑宽度]-[支撑柱直径]/2-[集水管半径]',
            '[定位点Z]+[保温桶中心高度]-[集水管半径]-[保温桶半径]-50')

        self.replace()

    @export
    def replace(self):
        # —— 提取参数 ——
        R_outlet = self['集水管半径']
        L_outlet = self['集水管长度']

        D_support = self['支撑柱直径']
        self['水平柱直径'] = D_support
        self['竖向柱直径'] = D_support

        R_h_support = self['水平柱直径'] / 2.0

        R_v_support = self['竖向柱直径'] / 2.0
        # 竖向柱Z起点 = 负的集水管半径
        v_start_Z = -R_outlet
        self['竖向柱Z起点'] = v_start_Z

        L_h_support = self['支撑宽度'] - R_v_support - R_outlet
        self['水平柱长度'] = L_h_support

        L_tank = self['保温桶长度']
        R_tank = self['保温桶半径']

        # 保温桶中心高度 = 竖向柱Z起点到保温桶中心Z的距离
        # 保温桶中心Z = 保温桶中心高度 - |v_start_Z| = 保温桶中心高度 - 集水管半径
        v_end_Z = self['保温桶中心高度'] - R_outlet
        self['竖向柱Z终点'] = v_end_Z

        R_rack = self['排架管直径'] / 2.0
        rack_spacing = self['集热管间距']
        n_rack = int(self['集热管数量'])

        plate_T = self['太阳能板厚']

        R_ring = R_tank * 0.8       # 随保温桶半径等比缩放（200/250）
        R_torus = R_tank * 0.08     # 随保温桶半径等比缩放（20/250）

        # 水管参数
        R_pipe_left = self['左侧水管半径']
        R_pipe_right = self['右侧水管半径']

        # —— 派生量 ——
        # hx 使集水管左端面圆心落在 X=0（插入点位置）
        # center_X = hx + plate_len_X/2, outlet 左端 = center_X - L_outlet/2 = 0
        # → hx = L_outlet/2 - plate_len_X/2
        hx = L_outlet / 2.0 - (n_rack - 1) * rack_spacing / 2.0
        h_origin = (hx, 0.0, 0.0)
        hx, hy, hz = h_origin
        v_origin = (hx, hy + L_h_support, hz)
        vx, vy, vz = v_origin
        v_top = (vx, vy, vz + v_end_Z)
        tx, ty, tz = v_top

        rack_vec_Y = ty - hy
        rack_vec_Z = tz - hz
        rack_length = sqrt(rack_vec_Y**2 + rack_vec_Z**2)
        rack_angle = atan2(rack_vec_Z, rack_vec_Y)

        plate_len_X = (n_rack - 1) * rack_spacing

        # —— 对称中心 ——
        center_X = hx + plate_len_X / 2.0

        # —— 支撑柱：轴线间距 = 2 × 水平柱长度 ——
        support_spacing = 2.0 * L_h_support
        left_support_X = center_X - support_spacing / 2.0
        right_support_X = center_X + support_spacing / 2.0

        # —— 水管：从支撑柱轴线向内100，轴线间距 = 支撑柱间距 - 200 ——
        pipe_offset = 100.0             # 向内偏移量（可调整）
        pipe_left_X = left_support_X + pipe_offset
        pipe_right_X = right_support_X - pipe_offset
        pipe_Y = ty - R_tank + R_tank   # 原保温桶底部 + 沿Y正向移动R_tank = 保温桶中心Y (ty)
        pipe_Z_center = tz - R_tank     # 保温桶轴线往Z轴负方向移动保温桶半径
        pipe_Z_bottom = pipe_Z_center - 50.0
        pipe_Z_top = pipe_Z_center + 50.0

        # ==========================================
        # 1. 底部集水管（center_X 对称）
        # ==========================================
        outlet_half = L_outlet / 2.0
        outlet = Cone(
            Vec3(center_X - outlet_half, 0, 0),
            Vec3(center_X + outlet_half, 0, 0),
            R_outlet, R_outlet
        )

        # ==========================================
        # 2. 水平支撑柱（左侧，X = left_support_X）
        # ==========================================
        h_support = Cone(
            Vec3(left_support_X, hy, hz),
            Vec3(left_support_X, hy + L_h_support, hz),
            R_h_support, R_h_support
        )

        # ==========================================
        # 3. 竖向支撑柱（左侧，X = left_support_X）
        # ==========================================
        v_support = Cone(
            Vec3(left_support_X, vy, vz + v_start_Z),
            Vec3(left_support_X, vy, vz + v_end_Z),
            R_v_support, R_v_support
        )

        # ==========================================
        # 3b. 左右水管（保温桶底部，截面半径可调，Z轴拉伸-50到50）
        # ==========================================
        pipe_left = Cone(
            Vec3(pipe_left_X, pipe_Y, pipe_Z_bottom),
            Vec3(pipe_left_X, pipe_Y, pipe_Z_top),
            R_pipe_left, R_pipe_left
        )
        pipe_right = Cone(
            Vec3(pipe_right_X, pipe_Y, pipe_Z_bottom),
            Vec3(pipe_right_X, pipe_Y, pipe_Z_top),
            R_pipe_right, R_pipe_right
        )

        # ==========================================
        # 4. 顶部水箱（center_X 对称）
        # ==========================================
        tank_half = L_tank / 2.0
        tank = Cone(
            Vec3(center_X - tank_half, ty, tz),
            Vec3(center_X + tank_half, ty, tz),
            R_tank, R_tank
        )

        # ==========================================
        # 5. 导水排架柱群（center_X 对称）
        # ==========================================
        upper_half_span = plate_len_X / 2.0
        rack_list = []
        for i in range(n_rack):
            x_pos = center_X - upper_half_span + i * (2.0 * upper_half_span) / (n_rack - 1)
            col = Cone(Vec3(x_pos, hy, hz), Vec3(x_pos, ty, tz), R_rack, R_rack)
            col = col - tank     # 删除与水箱相交部分
            col = col - outlet   # 删除与集水管相交部分
            rack_list.append(col)

        # ==========================================
        # 6. 太阳能板（center_X 对称）
        # ==========================================
        plate_total_span = 2.0 * upper_half_span
        plate_center_X = center_X
        plate_center_Y = rack_vec_Y / 2.0
        plate_center_Z = rack_vec_Z / 2.0

        plate = translate(plate_center_X, plate_center_Y, plate_center_Z) * (
            rotate(Vec3(1, 0, 0), rack_angle) * scale(plate_total_span, rack_length, plate_T) * Cube()
        )
        plate = translate(
            -upper_half_span,
            -(rack_length / 2.0) * cos(rack_angle),
            -(rack_length / 2.0) * sin(rack_angle)
        ) * plate
        plate = plate - tank    # 删除与水箱相交部分
        plate = plate - outlet  # 删除与集水管相交部分

        # ==========================================
        # 7. 圆环（YOZ面，水箱两端各一个）
        # ==========================================
        section_2d = translate(R_ring, 0) * scale(R_torus, R_torus) * Section(Arc(2 * pi))
        section_3d = rotate(Vec3(1, 0, 0), -pi / 2.0) * section_2d
        torus_z = Sweep(section_3d, Line(Arc(2 * pi)))
        torus_x = rotate(Vec3(0, 1, 0), pi / 2.0) * torus_z

        ring_left = translate(center_X - tank_half, ty, tz) * torus_x       # 水箱左端面
        ring_right = translate(center_X + tank_half, ty, tz) * torus_x      # 水箱右端面

        # ==========================================
        # 8. 支撑柱平行复制（右侧，X = right_support_X）
        # ==========================================
        h_support2 = Cone(
            Vec3(right_support_X, hy, hz),
            Vec3(right_support_X, hy + L_h_support, hz),
            R_h_support, R_h_support
        )
        v_support2 = Cone(
            Vec3(right_support_X, vy, vz + v_start_Z),
            Vec3(right_support_X, vy, vz + v_end_Z),
            R_v_support, R_v_support
        )

        # ==========================================
        # 9. 组合
        # ==========================================
        # 主体布尔融合
        main_result = (outlet + h_support + h_support2 + v_support + v_support2
                       + tank + plate)
        for col in rack_list:
            main_result = main_result + col
        # 管道和圆环不做布尔减，用 combine() 保留完整圆柱体
        self['热水器'] = combine(main_result, pipe_left, pipe_right, ring_left, ring_right)


if __name__ == "__main__":
    place(太阳能热水器())
