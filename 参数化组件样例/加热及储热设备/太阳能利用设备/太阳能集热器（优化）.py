from pyp3d import *

# 太阳能集热器：上下横向集水管 + 斜置连接板 + 椭集水管群 + 支撑结构
# 插入点：下方集水管左端底部象限点 (0, 0, 0)

class 太阳能集热器(Component):
    def __init__(self):
        Component.__init__(self)
        # ========== 可调参数 ==========
        self['设备名称'] = Attr('太阳能集热器', obvious=True)
        self['支撑宽度'] = Attr(1000.0, obvious=True)
        self['支撑板倾角'] = Attr(45.0, obvious=True)
        self['集水管长度'] = Attr(1500.0, obvious=True)
        self['集水管直径'] = Attr(150.0, obvious=True)

        # ========== 显示参数 ==========
        self['圆心距离'] = Attr(1414.0,  obvious=True, readonly=True, show=True)
        self['竖向支撑高度'] = Attr(1075.0, obvious=True, readonly=True, show=True)

        # ========== 输出槽位 ==========
        self['集热器'] = Attr(None, show=True)

        # ========== 驱动点 ==========
        self.setDrivenFeaturePoint('下集水管左圆心', SnapMode.GeometricCenter,
            '[定位点X]', '[定位点Y]', '[定位点Z]+[集水管直径]/2')
        self.setDrivenFeaturePoint('下集水管右圆心', SnapMode.GeometricCenter,
            '[定位点X]+[集水管长度]', '[定位点Y]', '[定位点Z]+[集水管直径]/2')
        self.setDrivenFeaturePoint('上集水管左圆心', SnapMode.GeometricCenter,
            '[定位点X]', '[定位点Y]+[支撑宽度]',
            '[定位点Z]+[集水管直径]/2+[支撑宽度]*tan([支撑板倾角]*3.14159265/180.0)')
        self.setDrivenFeaturePoint('上集水管右圆心', SnapMode.GeometricCenter,
            '[定位点X]+[集水管长度]', '[定位点Y]+[支撑宽度]',
            '[定位点Z]+[集水管直径]/2+[支撑宽度]*tan([支撑板倾角]*3.14159265/180.0)')

        self.replace()

    @export
    def replace(self):
        base = self['支撑宽度']
        angle_deg = self['支撑板倾角']
        cyl_len = self['集水管长度']
        D_main = self['集水管直径']
        angle = angle_deg * pi / 180.0

        # ========== 派生尺寸 ==========
        R_main = D_main / 2.0
        height = base * tan(angle)
        hypotenuse = sqrt(base**2 + height**2)

        self['圆心距离'] = hypotenuse
        self['竖向支撑高度'] = R_main + height

        # ========== 1. 下方横向集水管 ==========
        bottom_cyl = Cone(Vec3(0, 0, R_main), Vec3(cyl_len, 0, R_main), R_main, R_main)

        # ========== 2. 上方横向集水管 ==========
        upper_center_Z = R_main + height
        top_cyl = Cone(
            Vec3(0, base, upper_center_Z),
            Vec3(cyl_len, base, upper_center_Z),
            R_main, R_main
        )

        # ========== 3. 连接板 ==========
        col_X_start, col_X_end = 20.0, cyl_len - 20.0
        plate_len_X = col_X_end - col_X_start
        plate_width = hypotenuse
        plate_thickness = 15.0

        plate_center_X = (col_X_start + col_X_end) / 2.0
        plate_center_Y = base / 2.0
        plate_center_Z = 0.5 * (R_main + upper_center_Z)

        plate_base = scale(plate_len_X, plate_width, plate_thickness) * Cube()
        plate_rotated = rotate(Vec3(1, 0, 0), angle) * plate_base
        plate = translate(plate_center_X, plate_center_Y, plate_center_Z) * plate_rotated

        # 向原点方向平移校正
        plate = translate(
            -plate_len_X / 2.0,
            -(plate_width / 2.0) * cos(angle),
            -(plate_width / 2.0) * sin(angle)
        ) * plate

        # ========== 4. 椭集水管群（10根）==========
        D_long, D_short = 75.0, 40.0
        n_cols = 10
        elliptical_section = scale(D_short / 2.0, D_long / 2.0) * Section(Arc(2 * pi))
        sec_rotation = rotate(Vec3(1, 0, 0), angle - pi / 2.0)

        elliptical_columns = []  
        for i in range(n_cols):
            x_pos = col_X_start + i * plate_len_X / (n_cols - 1)
            sec_bottom = translate(x_pos, 0, R_main) * (sec_rotation * elliptical_section)
            sec_top = translate(x_pos, base, upper_center_Z) * (sec_rotation * elliptical_section)
            elliptical_columns.append(Loft(sec_bottom, sec_top))

        # ========== 5. 竖向支撑集水管 ==========
        D_support, R_support = 32.0, 16.0
        support_X_offset = 50.0
        support_top_Z = upper_center_Z

        support_left = Cone(
            Vec3(support_X_offset, base, 0),
            Vec3(support_X_offset, base, support_top_Z),
            R_support, R_support
        )
        support_right = Cone(
            Vec3(cyl_len - support_X_offset, base, 0),
            Vec3(cyl_len - support_X_offset, base, support_top_Z),
            R_support, R_support
        )

        # ========== 6. 侧向支撑集水管 ==========
        lateral_start_Y, lateral_start_Z = base, support_top_Z / 3.0
        t_ratio = 1.0 / 6.0
        lateral_end_Y = plate_center_Y + t_ratio * plate_width * cos(angle)
        lateral_end_Z = plate_center_Z + t_ratio * plate_width * sin(angle)

        lateral_left = Cone(
            Vec3(support_X_offset, lateral_start_Y, lateral_start_Z),
            Vec3(support_X_offset, lateral_end_Y, lateral_end_Z),
            R_support, R_support
        )
        lateral_right = Cone(
            Vec3(cyl_len - support_X_offset, lateral_start_Y, lateral_start_Z),
            Vec3(cyl_len - support_X_offset, lateral_end_Y, lateral_end_Z),
            R_support, R_support
        )

        # ========== 7. 组合 ==========
        collector = bottom_cyl + top_cyl + plate
        for col in elliptical_columns:
            collector = collector + col
        collector = collector + support_left + support_right + lateral_left + lateral_right
        self['集热器'] = collector


if __name__ == "__main__":
    place(太阳能集热器())
