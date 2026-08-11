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
        self['支撑板厚度'] = Attr(100.0, obvious=True, group='阳台尺寸')

        # ========== 栏杆尺寸组 ==========
        self['主栏杆截面宽度'] = Attr(100.0, obvious=True, group='栏杆尺寸')
        self['栅格栏杆截面宽度'] = Attr(50.0, obvious=True, group='栏杆尺寸')
        self['竖向栏杆群阵列数量'] = Attr(5, obvious=True, group='栏杆尺寸')
        self['栅格栏杆阵列数量'] = Attr(5, obvious=True, group='栏杆尺寸')
        self['主栏杆高度'] = Attr(1500.0, obvious=True, group='栏杆尺寸')
        self['栅格栏杆高度'] = Attr(1000.0, obvious=True, group='栏杆尺寸')
        self['水平栅格栏杆高度'] = Attr(150.0, obvious=True, group='栏杆尺寸')

        # ========== 排水洞位置尺寸组 ==========
        self['是否需要排水洞'] = Attr('是', obvious=True, combo=['是', '否'], group='排水洞')
        self['排水洞直径'] = Attr(100.0, obvious=True, group='排水洞')
        self['排水洞圆心X距离'] = Attr(700.0, obvious=True, group='排水洞')
        self['排水洞圆心Y距离'] = Attr(100.0, obvious=True, group='排水洞')
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
        T_support = float(self['支撑板厚度'])
        W_main = float(self['主栏杆截面宽度'])
        W_grid = float(self['栅格栏杆截面宽度'])
        N_main = int(self['竖向栏杆群阵列数量'])
        N_grid = int(self['栅格栏杆阵列数量'])
        H_rail = float(self['水平栅格栏杆高度'])
        H_main_rail = float(self['主栏杆高度'])
        H_grid_rail = float(self['栅格栏杆高度'])
        D_hole = float(self['排水洞直径'])
        X_hole_offset = float(self['排水洞圆心X距离'])
        Y_hole_offset = float(self['排水洞圆心Y距离'])
        need_hole = self['是否需要排水洞']

        R = D / 2.0
        rail_radius = R   # 栏杆弧形半径

        # ============================================================
        # Step 1: 支撑半圆柱
        # 插入点: (0, 0, H_support), 柱体从 Z=-H_support 到 Z=0
        # XOY面，半圆截面，弦沿X轴，半径沿+Y
        # ============================================================
        half_circle_sec = Section(
            Vec2(R, 0),
            scale(R) * Arc(math.pi),
            Vec2(-R, 0),
            Vec2(R, 0)
        )
        sec1_base = translate(0, 0, -H_support) * half_circle_sec
        sec1_top = half_circle_sec
        support_column = Loft(sec1_base, sec1_top)

        # ============================================================
        # Step 2: 外延半圆环柱
        # 临时原点: (0, 0, 0), 拉伸到 Z=H_extend
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

        sec2_base = ring_sec
        sec2_top = translate(0, 0, H_extend) * ring_sec
        extend_ring = Loft(sec2_base, sec2_top)

        # 步骤3及之后的临时坐标系Z基准
        Z_step3 = H_extend

        # ============================================================
        # Step 3: 竖向栏杆 (Loft) + 环形阵列
        # 临时原点: (0, 0, Z_step3)
        # 截面形心: (rail_radius, 0, 0)  在临时坐标下
        # ============================================================
        half_main = W_main / 2.0
        vert_rail_sec = translate(rail_radius, 0, 0) * Section(scale(half_main) * Arc(2*pi))
        sec3_base = translate(0, 0, Z_step3) * vert_rail_sec
        sec3_top = translate(0, 0, Z_step3 + H_main_rail) * vert_rail_sec
        vertical_rail = Loft(sec3_base, sec3_top)

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
        # 临时原点: 竖向栏杆截面形心 = (rail_radius, 0, 0) 在step3临时坐标下
        # 全局: (rail_radius, 0, Z_step3)
        # 截面在ZOY面, 形心: (0, 0, H_rail + 0.5*W_grid)
        # ============================================================
        half_grid = W_grid / 2.0
        Z_step4_grid = Z_step3   # 栅格栏杆临时原点Z
        z_center_lower = H_rail + half_grid

        # 圆形截面在XOZ面, 形心(rail_radius, 0, Z_step4_grid + z_center_lower)
        grid_sec_3d = translate(rail_radius, 0, Z_step4_grid + z_center_lower) * rotate(Vec3(1, 0, 0), -0.5 * math.pi) * Section(scale(half_grid) * Arc(2*pi))

        arc_path = Line(Arc(math.pi))  # XOY面半圆弧轨迹
        grid_rail_lower = Sweep(grid_sec_3d, arc_path)

        # 上部水平栅格栏杆: 下部沿+Z移动复制
        grid_rail_upper = translate(0, 0, H_grid_rail + W_grid) * grid_rail_lower

        # ============================================================
        # Step 5: 环形主栏杆 (Sweep)
        # 临时原点: 同step4 (rail_radius, 0, 0)
        # 全局: (rail_radius, 0, Z_step3)
        # 截面在ZOY面, 形心: (0, 0, H_main_rail - half_main)
        # ============================================================
        Z_step4_ring = Z_step3   # 环形主栏杆临时原点Z
        z_center_ring = H_main_rail - half_main

        # 圆形截面在XOZ面, 形心(rail_radius, 0, Z_step4_ring + z_center_ring)
        ring_main_sec_3d = translate(rail_radius, 0, Z_step4_ring + z_center_ring) * rotate(Vec3(1, 0, 0), -0.5 * math.pi) * Section(scale(half_main) * Arc(2*pi))

        ring_main_rail = Sweep(ring_main_sec_3d, arc_path)

        # ============================================================
        # Step 6: 竖向栅格栏杆 (Loft) + 环形阵列(交错)
        # 临时原点: 同step4 (rail_radius, 0, 0)
        # 全局: (rail_radius, 0, Z_step3)
        # 截面在XOY面, 形心: (rail_radius, 0, H_rail + 0.5*W_grid)
        # 拉伸+Z: H_grid_rail
        # ============================================================
        z_center_vert = H_rail + 2*half_grid

        vert_grid_sec = translate(rail_radius, 0, 0) * Section(scale(half_grid) * Arc(2*pi))
        sec6_base = translate(0, 0, Z_step3 + z_center_vert - half_grid) * vert_grid_sec
        sec6_top = translate(0, 0, Z_step3 + z_center_vert - half_grid + H_grid_rail + W_grid) * vert_grid_sec
        vert_grid_rail = Loft(sec6_base, sec6_top)

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
        # 排水洞X = X_hole_offset
        # 排水洞Y = Y_hole_offset
        # ============================================================
        hole_X = X_hole_offset
        hole_Y = Y_hole_offset
        hole_R = D_hole / 2.0

        drain_hole = Cone(
            Vec3(hole_X, hole_Y, -H_support),
            Vec3(hole_X, hole_Y, 0),
            hole_R,
            hole_R
        )

        # ============================================================
        # Step 7: 支撑剪切半圆柱
        # 临时原点: (0, 0, -H_support), 沿Z轴正向拉伸 H_support - T_support
        # 截面直径: D - 2*T_support
        # ============================================================
        R_cut = (D - 2*T_support) / 2.0
        cut_half_circle_sec = Section(
            Vec2(R_cut, 0),
            scale(R_cut) * Arc(math.pi),
            Vec2(-R_cut, 0),
            Vec2(R_cut, 0)
        )
        sec_cut_base = translate(0, 0, -H_support) * cut_half_circle_sec
        sec_cut_top = translate(0, 0, -T_support) * cut_half_circle_sec
        cut_cylinder = Loft(sec_cut_base, sec_cut_top)

        # ============================================================
        # 组装所有部件
        # 布尔: support_column + extend_ring - cut_cylinder [- drain_hole]
        # ============================================================
        support_combined = support_column + extend_ring - cut_cylinder
        if need_hole == '是':
            support_combined = support_combined - drain_hole

        # 栏杆部件整体沿Y轴正向平移 0.5 * W_main
        rail_offset_y = 0.5 * W_main
        vert_rails_arr = translate(0, rail_offset_y, 0) * vert_rails_arr
        grid_rail_lower = translate(0, rail_offset_y, 0) * grid_rail_lower
        grid_rail_upper = translate(0, rail_offset_y, 0) * grid_rail_upper
        ring_main_rail = translate(0, rail_offset_y, 0) * ring_main_rail
        vert_grid_arr = translate(0, rail_offset_y, 0) * vert_grid_arr

        all_parts = [
            support_combined,
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
