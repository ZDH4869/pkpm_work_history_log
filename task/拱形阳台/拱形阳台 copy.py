from pyp3d import *
import math

class 圆形阳台(Component):
    def __init__(self):
        Component.__init__(self)

        # ========== 基础信息组 ==========
        self['构件名称'] = Attr('圆形阳台', obvious=True, group='基础信息')

        # ========== 阳台尺寸组 ==========
        self['阳台直径'] = Attr(2000.0, obvious=True, group='阳台尺寸')
        self['阳台高度'] = Attr(500.0, obvious=True, group='阳台尺寸')
        self['阳台外延宽度'] = Attr(300.0, obvious=True, group='阳台尺寸')
        self['阳台外延高度'] = Attr(100.0, obvious=True, group='阳台尺寸')

        # ========== 栏杆尺寸组 ==========
        self['主栏杆截面宽度'] = Attr(100.0, obvious=True, group='栏杆尺寸')
        self['栅格栏杆截面宽度'] = Attr(50.0, obvious=True, group='栏杆尺寸')
        self['竖向栏杆群阵列数量'] = Attr(5, obvious=True, group='栏杆尺寸')
        self['栅格栏杆阵列数量'] = Attr(1, obvious=True, group='栏杆尺寸')
        self['栏杆高度'] = Attr(150.0, obvious=True, group='栏杆尺寸')

        # ========== 排水洞位置尺寸组 ==========
        self['排水洞直径'] = Attr(300.0, obvious=True, group='排水洞')
        self['排水洞X径向距离'] = Attr(700.0, obvious=True, group='排水洞')
        self['排水洞Y径向距离'] = Attr(500.0, obvious=True, group='排水洞')
        self['是否需要排水洞'] = Attr('是', obvious=True, combo=['是', '否'], group='排水洞')

        # ========== 最终几何输出槽位 ==========
        self['圆形阳台'] = Attr(None, show=True)

        self.replace()

    @export
    def replace(self):
        # ========== 读取参数 ==========
        D = float(self['阳台直径'])
        H_support = float(self['阳台高度'])
        W_extend = float(self['阳台外延宽度'])
        H_extend = float(self['阳台外延高度'])
        W_main = float(self['主栏杆截面宽度'])
        W_grid = float(self['栅格栏杆截面宽度'])
        N_main = int(self['竖向栏杆群阵列数量'])
        N_grid = int(self['栅格栏杆阵列数量'])
        H_rail = float(self['栏杆高度'])
        D_hole = float(self['排水洞直径'])
        X_hole_offset = float(self['排水洞X径向距离'])
        Y_hole_offset = float(self['排水洞Y径向距离'])
        need_hole = self['是否需要排水洞']

        R = D / 2.0
        rail_radius = D - 0.5 * W_extend  # 栏杆弧形半径

        # ============================================================
        # Step 1: 支撑半圆柱
        # XOY面，半圆截面，弦沿X轴，半径沿+Y
        # ============================================================
        half_circle_sec = Section(
            Vec2(R, 0),
            scale(R) * Arc(math.pi),
            Vec2(-R, 0),
            Vec2(R, 0)
        )
        sec1_base = half_circle_sec
        sec1_top = translate(0, 0, H_support) * half_circle_sec
        support_column = Loft(sec1_base, sec1_top).color(0.75, 0.75, 0.75, 1)

        # ============================================================
        # Step 2: 外延半圆环柱
        # 临时原点: (0, 0, H_support)
        # ============================================================
        R_outer = R + 0.5 * W_extend
        R_inner = R - 0.5 * W_extend

        sec_outer = Section(
            Vec2(R_outer, 0),
            scale(R_outer) * Arc(math.pi),
            Vec2(-R_outer, 0),
            Vec2(R_outer, 0)
        )
        sec_inner = Section(
            Vec2(R_inner, 0),
            scale(R_inner) * Arc(math.pi),
            Vec2(-R_inner, 0),
            Vec2(R_inner, 0)
        )
        ring_sec = sec_outer - sec_inner  # 半圆环截面

        sec2_base = translate(0, 0, H_support) * ring_sec
        sec2_top = translate(0, 0, H_support + H_extend) * ring_sec
        extend_ring = Loft(sec2_base, sec2_top).color(0.7, 0.7, 0.7, 1)

        # 步骤3及之后的临时坐标系Z基准
        Z_step3 = H_support + H_extend

        # ============================================================
        # Step 3: 竖向栏杆 (Loft) + 环形阵列
        # 临时原点: (0, 0, Z_step3)
        # 截面形心: (rail_radius, 0, W_main)  在临时坐标下
        # ============================================================
        half_main = W_main / 2.0
        vert_rail_sec = Section(
            Vec2(rail_radius - half_main, -half_main),
            Vec2(rail_radius + half_main, -half_main),
            Vec2(rail_radius + half_main, half_main),
            Vec2(rail_radius - half_main, half_main),
        )
        sec3_base = translate(0, 0, Z_step3 + W_main) * vert_rail_sec
        sec3_top = translate(0, 0, Z_step3 + W_main + 1500.0) * vert_rail_sec
        vertical_rail = Loft(sec3_base, sec3_top).color(0.6, 0.6, 0.6, 1)

        # 环形阵列: 0°~180°, 含首尾 N_main 个
        if N_main > 1:
            main_step = math.pi / (N_main - 1)
        else:
            main_step = 0
        vert_rails_arr = Array(vertical_rail)
        for i in range(N_main):
            angle = i * main_step
            vert_rails_arr.append(rotate(angle))

        # ============================================================
        # Step 4: 下部水平栅格栏杆 (Sweep)
        # 临时原点: 竖向栏杆截面形心 = (rail_radius, 0, W_main) 在step3临时坐标下
        # 全局: (rail_radius, 0, Z_step3 + W_main)
        # 截面在ZOY面, 形心: (0, 0, H_rail + 0.5*W_grid)
        # ============================================================
        half_grid = W_grid / 2.0
        Z_step4 = Z_step3 + W_main  # step4临时坐标系原点在全局坐标中的Z
        z_center_lower = H_rail + half_grid

        grid_sec_2d = Section(
            Vec2(-half_grid, z_center_lower - half_grid),
            Vec2(half_grid, z_center_lower - half_grid),
            Vec2(half_grid, z_center_lower + half_grid),
            Vec2(-half_grid, z_center_lower + half_grid),
        )
        # 截面法线对齐轨迹: 绕X轴旋转-90°, 平移至(rail_radius, 0, 0)
        grid_sec_3d = translate(rail_radius, 0, 0) * rotate(Vec3(1, 0, 0), -0.5 * math.pi) * grid_sec_2d
        # 平移到step4的临时坐标系原点在全局中的位置
        grid_sec_3d = translate(0, 0, Z_step4) * grid_sec_3d

        arc_path = Line(Arc(math.pi))  # XOY面半圆弧轨迹
        grid_rail_lower = Sweep(grid_sec_3d, arc_path).color(0.5, 0.5, 0.5, 1)

        # 上部水平栅格栏杆: 下部沿+Z移动复制
        grid_rail_upper = translate(0, 0, 1000.0 + W_grid) * grid_rail_lower

        # ============================================================
        # Step 5: 环形主栏杆 (Sweep)
        # 临时原点: 同step4
        # 截面在ZOY面, 形心: (0, 0, 1500 - 0.5*W_main)
        # ============================================================
        z_center_ring = 1500.0 - half_main

        ring_main_sec_2d = Section(
            Vec2(-half_main, z_center_ring - half_main),
            Vec2(half_main, z_center_ring - half_main),
            Vec2(half_main, z_center_ring + half_main),
            Vec2(-half_main, z_center_ring + half_main),
        )
        ring_main_sec_3d = translate(rail_radius, 0, 0) * rotate(Vec3(1, 0, 0), -0.5 * math.pi) * ring_main_sec_2d
        ring_main_sec_3d = translate(0, 0, Z_step4) * ring_main_sec_3d

        ring_main_rail = Sweep(ring_main_sec_3d, arc_path).color(0.55, 0.55, 0.55, 1)

        # ============================================================
        # Step 6: 竖向栅格栏杆 (Loft) + 环形阵列(交错)
        # 临时原点: 同step4
        # 截面在XOY面, 形心: (rail_radius, 0, H_rail + 0.5*W_grid)
        # 拉伸+Z: 1000
        # ============================================================
        z_center_vert = H_rail + half_grid

        vert_grid_sec = Section(
            Vec2(rail_radius - half_grid, -half_grid),
            Vec2(rail_radius + half_grid, -half_grid),
            Vec2(rail_radius + half_grid, half_grid),
            Vec2(rail_radius - half_grid, half_grid),
        )
        sec6_base = translate(0, 0, Z_step4 + z_center_vert) * vert_grid_sec
        sec6_top = translate(0, 0, Z_step4 + z_center_vert + 1000.0) * vert_grid_sec
        vert_grid_rail = Loft(sec6_base, sec6_top).color(0.45, 0.45, 0.45, 1)

        # 交错排列: 每两个主栏杆之间的间隙内放置 N_grid 个栅格栏杆
        if N_main > 1 and N_grid >= 1:
            gap_step = main_step  # 相邻主栏杆间的角度间隔
            vert_grid_arr = Array(vert_grid_rail)
            for i in range(N_main - 1):
                gap_start = i * gap_step
                for j in range(1, N_grid + 1):
                    angle = gap_start + j * gap_step / (N_grid + 1)
                    vert_grid_arr.append(rotate(angle))
        else:
            vert_grid_arr = vert_grid_rail

        # ============================================================
        # Step 7: 排水洞 (Cone圆柱体) + 布尔减
        # 排水洞X = R - X_hole_offset
        # 排水洞Y = Y_hole_offset
        # ============================================================
        hole_X = R - X_hole_offset
        hole_Y = Y_hole_offset
        hole_R = D_hole / 2.0

        drain_hole = Cone(
            Vec3(hole_X, hole_Y, 0),
            Vec3(hole_X, hole_Y, H_support),
            hole_R,
            hole_R
        )

        # ============================================================
        # 组装所有部件
        # ============================================================
        if need_hole == '是':
            support_with_hole = (support_column - drain_hole).color(0.75, 0.75, 0.75, 1)
        else:
            support_with_hole = support_column

        all_parts = [
            support_with_hole,
            extend_ring,
            vert_rails_arr,
            grid_rail_lower,
            grid_rail_upper,
            ring_main_rail,
            vert_grid_arr,
        ]
        result = combine(*all_parts)

        self['圆形阳台'] = result


if __name__ == "__main__":
    FinalGeometry = 圆形阳台()
    place(FinalGeometry)
