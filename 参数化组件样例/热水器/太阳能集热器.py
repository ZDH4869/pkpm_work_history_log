from pyp3d import *

# 太阳能集热器：三棱台外形，上下横向圆柱 + 连接板 + 椭圆柱子 + 支撑结构
# 左视图：等腰直角三角形（默认腰长 1000mm）
# 正视图：上方圆柱 + 下方圆柱 + 中间连接板
# 插入点：下方圆柱左端底部象限点 (0, 0, 0)

class 太阳能集热器(Component):
    def __init__(self):
        Component.__init__(self)
        # ========== 可调参数（用户可修改）===========
        self['设备名称'] = Attr('太阳能集热器', obvious=True)
        self['底边长度'] = Attr(1000.0, obvious=True)    # 左视图三角形底边 Y 向长度
        self['支撑板倾角'] = Attr(45.0, obvious=True)    # 连接板与地面夹角（度）
        self['圆柱长度'] = Attr(1500.0, obvious=True)    # 上下横向圆柱总长

        # ========== 显示参数（用户只可查看）===========
        self['圆心距离'] = Attr(1414.0, readonly=True, show=True)
        self['竖向支撑高度'] = Attr(1075.0, readonly=True, show=True)

        # ========== 输出槽位 ==========
        self['集热器'] = Attr(None, show=True)

        # ========== 驱动点：上下圆柱左右两端截面圆心 ==========
        # 下方圆柱左端圆心
        self.setDrivenFeaturePoint(
            '下圆柱左圆心', SnapMode.GeometricCenter,
            '0', '0', '75'
        )
        # 下方圆柱右端圆心
        self.setDrivenFeaturePoint(
            '下圆柱右圆心', SnapMode.GeometricCenter,
            '[圆柱长度]', '0', '75'
        )
        # 上方圆柱左端圆心
        self.setDrivenFeaturePoint(
            '上圆柱左圆心', SnapMode.GeometricCenter,
            '0', '[底边长度]',
            '75 + [底边长度] * tan([支撑板倾角] * 3.14159265 / 180.0)'
        )
        # 上方圆柱右端圆心
        self.setDrivenFeaturePoint(
            '上圆柱右圆心', SnapMode.GeometricCenter,
            '[圆柱长度]', '[底边长度]',
            '75 + [底边长度] * tan([支撑板倾角] * 3.14159265 / 180.0)'
        )

        self.replace()

    @export
    def replace(self):
        # ========== 提取参数 ==========
        base = self['底边长度']
        angle_deg = self['支撑板倾角']
        cyl_len = self['圆柱长度']
        angle = angle_deg * pi / 180.0

        # ========== 派生尺寸 ==========
        D_main = 150.0                              # 主圆柱直径
        R_main = D_main / 2.0                       # 主圆柱半径 75
        height = base * tan(angle)                  # 上方圆柱相对下方圆柱的 Z 向高差
        hypotenuse = sqrt(base**2 + height**2)      # 圆心距离 = 斜边长度

        # 更新显示参数
        self['圆心距离'] = hypotenuse
        self['竖向支撑高度'] = R_main + height  # 竖向支撑柱总高度

        # 斜边方向单位向量（YZ 平面）
        dir_Y = base / hypotenuse       # cos(angle)
        dir_Z = height / hypotenuse     # sin(angle)

        # 板厚法向（垂直于斜边，指向竖向支撑柱侧）（YZ 平面）
        normal_Y = dir_Z                # sin(angle)
        normal_Z = -dir_Y               # -cos(angle)

        # ========== 1. 下方横向圆柱 ==========
        # 圆心从 (0, 0, R_main) 到 (cyl_len, 0, R_main)，直径 150
        lower_center_Z = R_main  # 75
        bottom_cyl = Cone(
            Vec3(0, 0, lower_center_Z),
            Vec3(cyl_len, 0, lower_center_Z),
            R_main, R_main
        )

        # ========== 2. 上方横向圆柱 ==========
        upper_center_Y = base
        upper_center_Z = R_main + height
        top_cyl = Cone(
            Vec3(0, upper_center_Y, upper_center_Z),
            Vec3(cyl_len, upper_center_Y, upper_center_Z),
            R_main, R_main
        )

        # ========== 3. 连接板（长方板，连接上下圆柱）==========
        # X向：从第一个椭圆柱轴线到最后一个椭圆柱轴线
        # Y向（板宽方向，旋转后对齐斜边）= 椭圆柱长度 = 斜边长
        col_X_start = 20.0                    # 第一根椭圆柱轴心 X
        col_X_end = cyl_len - 20.0            # 最后一根椭圆柱轴心 X
        plate_len_X = col_X_end - col_X_start  # 板长 X = 柱群X跨度（首柱→末柱轴线距）
        plate_width = hypotenuse               # 板宽 Y = 椭圆柱长度 = 斜边长
        plate_thickness = 15.0

        # 连接板定位：X中点 = 柱群X中点；YZ中心 = 两圆柱YZ中点
        plate_center_X = (col_X_start + col_X_end) / 2.0
        plate_center_Y = base / 2.0
        plate_center_Z = 0.5 * (lower_center_Z + upper_center_Z)

        # Cube 创建（X=长度, Y=板宽, Z=板厚）
        plate_base = scale(plate_len_X, plate_width, plate_thickness) * Cube()
        # 绕 X 轴旋转 angle：板宽方向对齐斜边（与椭圆柱长度方向平行），板厚方向垂直于斜边
        plate_rotated = rotate(Vec3(1, 0, 0), angle) * plate_base
        plate = translate(plate_center_X, plate_center_Y, plate_center_Z) * plate_rotated

        # 平移校正：将斜置板向原点方向偏移
        # ΔX = 板长X的1/2; ΔY = 板宽Y的1/2 * cos(angle); ΔZ = 板宽Y的1/2 * cos(angle) * tan(angle)
        plate_offset_X = plate_len_X / 2.0
        plate_offset_Y = (plate_width / 2.0) * cos(angle)
        plate_offset_Z = (plate_width / 2.0) * cos(angle) * tan(angle)
        plate = translate(-plate_offset_X, -plate_offset_Y, -plate_offset_Z) * plate

        # ========== 4. 连接板上的 10 根椭圆柱子 ==========
        # 长轴 75（垂直于板面），短轴 40（沿 X 向）
        # 柱子从下方圆柱圆心延伸到上方圆柱圆心
        D_long = 75.0
        D_short = 40.0
        R_long = D_long / 2.0
        R_short = D_short / 2.0
        n_cols = 10

        # 椭圆柱子两端：下方到上方圆柱圆心
        col_bottom_Y = 0.0
        col_bottom_Z = lower_center_Z   # 75
        col_top_Y = upper_center_Y      # base
        col_top_Z = upper_center_Z      # 75 + height

        # 椭圆截面：整圆 scale 为椭圆（短轴 X=40，长轴 Y=75）
        elliptical_section = scale(R_short, R_long) * Section(Arc(2*pi))

        # 截面旋转至垂直于斜边方向（法线对齐斜边，长轴对齐板厚法向）
        sec_rotation = rotate(Vec3(1, 0, 0), angle - pi / 2.0)

        elliptical_columns = []
        for i in range(n_cols):
            x_pos = col_X_start + i * (col_X_end - col_X_start) / (n_cols - 1)

            # 下截面：位于下方圆柱圆心处
            sec_bottom = translate(x_pos, col_bottom_Y, col_bottom_Z) * (
                sec_rotation * elliptical_section
            )
            # 上截面：位于上方圆柱圆心处
            sec_top = translate(x_pos, col_top_Y, col_top_Z) * (
                sec_rotation * elliptical_section
            )

            col = Loft(sec_bottom, sec_top)
            elliptical_columns.append(col)

        # ========== 5. 竖向支撑圆柱（上圆柱下方，左右各一根）==========
        D_support = 32.0
        R_support = 16.0
        support_X_offset = 50.0  # 距圆柱端部偏移

        # 支撑柱底部 Z = 0（与下方圆柱底部象限点同高）
        # 支撑柱顶部 Z = 上方圆柱圆心（延伸到圆心）
        support_bottom_Z = 0.0
        support_top_Z = upper_center_Z  # R_main + height

        # 左侧竖向支撑
        support_left = Cone(
            Vec3(support_X_offset, base, support_bottom_Z),
            Vec3(support_X_offset, base, support_top_Z),
            R_support, R_support
        )

        # 右侧竖向支撑
        support_right = Cone(
            Vec3(cyl_len - support_X_offset, base, support_bottom_Z),
            Vec3(cyl_len - support_X_offset, base, support_top_Z),
            R_support, R_support
        )

        # ========== 6. 侧向支撑圆柱（竖向支撑 1/3 高度 → 板斜长 2/3 处）==========
        # 起点：竖向支撑柱 Z = support_top_Z / 3 处
        lateral_start_Y = base
        lateral_start_Z = support_top_Z / 3.0

        # 终点：板上斜边方向 2/3 处（从下方圆心起算）
        t_ratio = 2.0 / 3.0 - 0.5  # = 1/6（板中心在中点，2/3处距中心偏移 1/6 板宽）
        lateral_end_Y = plate_center_Y + t_ratio * plate_width * dir_Y  # base/2 + base/6 = 2*base/3
        lateral_end_Z = plate_center_Z + t_ratio * plate_width * dir_Z  # 中心Z + height/6

        # 左侧侧向支撑
        lateral_left = Cone(
            Vec3(support_X_offset, lateral_start_Y, lateral_start_Z),
            Vec3(support_X_offset, lateral_end_Y, lateral_end_Z),
            R_support, R_support
        )

        # 右侧侧向支撑（对称）
        lateral_right = Cone(
            Vec3(cyl_len - support_X_offset, lateral_start_Y, lateral_start_Z),
            Vec3(cyl_len - support_X_offset, lateral_end_Y, lateral_end_Z),
            R_support, R_support
        )

        # ========== 7. 组合所有部件 ==========
        all_parts = [bottom_cyl, top_cyl, plate]
        all_parts.extend(elliptical_columns)
        all_parts.extend([support_left, support_right, lateral_left, lateral_right])

        collector = all_parts[0]
        for part in all_parts[1:]:
            collector = collector + part

        self['集热器'] = collector


if __name__ == "__main__":
    FinalGeometry = 太阳能集热器()
    place(FinalGeometry)
