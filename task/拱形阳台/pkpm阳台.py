from pyp3d import *
import math

class 圆形阳台(Component):
    def __init__(self):
        Component.__init__(self)
        # ========== 基础信息 ==========
        self['构件名称'] = Attr('圆形阳台', obvious=True, group='基础信息')
        # ========== 阳台尺寸 ==========
        self['阳台直径'] = Attr(2000.0, obvious=True, group='阳台尺寸')
        self['阳台高度'] = Attr(500.0, obvious=True, group='阳台尺寸')
        self['阳台外延宽度'] = Attr(300.0, obvious=True, group='阳台尺寸')
        self['阳台外延高度'] = Attr(100.0, obvious=True, group='阳台尺寸')
        self['支撑板厚度'] = Attr(100.0, obvious=True, group='阳台尺寸')
        # ========== 栏杆尺寸 ==========
        self['主栏杆截面宽度'] = Attr(100.0, obvious=True, group='栏杆尺寸')
        self['栅格栏杆截面宽度'] = Attr(50.0, obvious=True, group='栏杆尺寸')
        self['竖向栏杆群阵列数量'] = Attr(5, obvious=True, group='栏杆尺寸')
        self['栅格栏杆阵列数量'] = Attr(5, obvious=True, group='栏杆尺寸')
        self['主栏杆高度'] = Attr(1500.0, obvious=True, group='栏杆尺寸')
        self['栅格栏杆高度'] = Attr(1000.0, obvious=True, group='栏杆尺寸')
        self['水平栅格栏杆高度'] = Attr(150.0, obvious=True, group='栏杆尺寸')
        # ========== 排水洞 ==========
        self['是否需要排水洞'] = Attr('是', obvious=True, combo=['是', '否'], group='排水洞')
        self['排水洞直径'] = Attr(100.0, obvious=True, group='排水洞')
        self['排水洞圆心X距离'] = Attr(700.0, obvious=True, group='排水洞')
        self['排水洞圆心Y距离'] = Attr(100.0, obvious=True, group='排水洞')
        # ========== 输出槽位 ==========
        self['圆形阳台'] = Attr(None, show=True)
        self.replace()

    @export
    def replace(self):
        # ========== 1. 读取参数 ==========
        balcony_diameter = float(self['阳台直径'])
        balcony_height = float(self['阳台高度'])
        extend_width = float(self['阳台外延宽度'])
        extend_height = float(self['阳台外延高度'])
        support_thickness = float(self['支撑板厚度'])
        main_rail_width = float(self['主栏杆截面宽度'])
        grid_rail_width = float(self['栅格栏杆截面宽度'])
        N_main = int(self['竖向栏杆群阵列数量'])
        N_grid = int(self['栅格栏杆阵列数量'])
        main_height = float(self['主栏杆高度'])
        grid_height = float(self['栅格栏杆高度'])
        grid_offset = float(self['水平栅格栏杆高度'])
        need_drain = self['是否需要排水洞']
        drain_diameter = float(self['排水洞直径'])
        drain_x = float(self['排水洞圆心X距离'])
        drain_y = float(self['排水洞圆心Y距离'])

        # ========== 2. 派生变量 ==========
        R = balcony_diameter / 2.0
        rail_radius = R
        R_outer = R + 0.5 * extend_width
        R_inner = R - 0.5 * extend_width
        R_cut = (balcony_diameter - 2.0 * support_thickness) / 2.0
        half_main = main_rail_width / 2.0
        half_grid = grid_rail_width / 2.0
        Z_step3 = extend_height
        main_step = math.pi / (N_main - 1) if N_main > 1 else 0.0

        # ========== 步骤1：支撑半圆柱体 ==========
        # XOY面半圆截面：起点(R,0) -> 上半圆弧 -> 终点(-R,0) -> 弦闭合回(R,0)
        support_sec = Section(
            Vec2(R, 0),
            scale(R) * Arc(math.pi),
            Vec2(-R, 0),
            Vec2(R, 0)
        )
        # 沿-Z方向拉伸阳台高度：底面Z=-阳台高度，顶面Z=0
        support_column = Loft(
            translate(0, 0, -balcony_height) * support_sec,
            support_sec
        )

        # ========== 步骤2：外延半圆环柱 ==========
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
        ring_sec = sec_outer - sec_inner
        # 沿+Z方向拉伸阳台外延高度：底面Z=0，顶面Z=阳台外延高度
        extend_ring = Loft(
            ring_sec,
            translate(0, 0, extend_height) * ring_sec
        )

        # ========== 步骤3：竖向主栏杆（Loft圆形截面 + 环形阵列） ==========
        # 圆形截面：圆心(rail_radius, 0)，半径half_main
        vert_rail_sec = translate(rail_radius, 0, 0) * Section(scale(half_main) * Arc(2 * math.pi))
        # 沿+Z方向拉伸主栏杆高度
        vertical_rail = Loft(
            translate(0, 0, Z_step3) * vert_rail_sec,
            translate(0, 0, Z_step3 + main_height) * vert_rail_sec
        )
        # 环形阵列：以Z轴为旋转轴，0到180度，N_main个
        vert_rails_arr = Array(vertical_rail)
        for i in range(N_main):
            vert_rails_arr.append(rotate(i * main_step))

        # ========== 步骤4：下部水平栅格栏杆（Sweep圆形截面沿半圆弧扫掠） ==========
        z_center_lower = grid_offset + half_grid
        # 圆形截面：半径half_grid，旋转-90度使法线对齐圆弧轨迹，平移至全局位置
        grid_sec_lower = translate(rail_radius, 0, Z_step3 + z_center_lower) * \
            rotate(Vec3(1, 0, 0), -0.5 * math.pi) * \
            Section(scale(half_grid) * Arc(2 * math.pi))
        # 半圆弧扫掠路径：半径1，XOY面
        arc_path = Line(Arc(math.pi))
        grid_rail_lower = Sweep(grid_sec_lower, arc_path)

        # ========== 步骤5：上部水平栅格栏杆（平移复制） ==========
        grid_rail_upper = translate(0, 0, grid_height + grid_rail_width) * grid_rail_lower

        # ========== 步骤6：环形主栏杆（Sweep圆形截面沿半圆弧扫掠） ==========
        z_center_ring = main_height - half_main
        ring_main_sec = translate(rail_radius, 0, Z_step3 + z_center_ring) * \
            rotate(Vec3(1, 0, 0), -0.5 * math.pi) * \
            Section(scale(half_main) * Arc(2 * math.pi))
        ring_main_rail = Sweep(ring_main_sec, arc_path)

        # ========== 步骤7：竖向栅格栏杆（Loft圆形截面 + 交错环形阵列） ==========
        vert_grid_sec = translate(rail_radius, 0, 0) * Section(scale(half_grid) * Arc(2 * math.pi))
        z_start_grid = Z_step3 + grid_offset + half_grid
        z_end_grid = z_start_grid + grid_height + grid_rail_width
        vertical_grid_rail = Loft(
            translate(0, 0, z_start_grid) * vert_grid_sec,
            translate(0, 0, z_end_grid) * vert_grid_sec
        )
        vert_grid_arr = Array(vertical_grid_rail)
        if N_main > 1 and N_grid >= 1:
            gap_step = main_step
            for i in range(N_main - 1):
                for j in range(1, N_grid + 1):
                    angle = i * gap_step + j * gap_step / (N_grid + 1)
                    vert_grid_arr.append(rotate(angle))

        # ========== 步骤8：排水洞（Cone圆柱体 + 布尔减） ==========
        drain_hole = None
        if need_drain == '是':
            drain_r = drain_diameter / 2.0
            drain_hole = Cone(
                Vec3(drain_x, drain_y, -balcony_height),
                Vec3(drain_x, drain_y, 0),
                drain_r, drain_r
            )

        # ========== 步骤9：支撑剪切半圆柱（挖空支撑体） ==========
        cut_sec = Section(
            Vec2(R_cut, 0),
            scale(R_cut) * Arc(math.pi),
            Vec2(-R_cut, 0),
            Vec2(R_cut, 0)
        )
        # 沿+Z方向拉伸：底面Z=-阳台高度，顶面Z=-支撑板厚度（底部保留完整厚度）
        cut_cylinder = Loft(
            translate(0, 0, -balcony_height) * cut_sec,
            translate(0, 0, -support_thickness) * cut_sec
        )

        # ========== 步骤10：整体组装 ==========
        # 支撑体布尔组装：支撑柱 + 外延环 - 剪切体
        support_combined = support_column + extend_ring - cut_cylinder
        if drain_hole is not None:
            support_combined = support_combined - drain_hole

        # 栏杆Y向偏移：所有栏杆部件沿+Y平移0.5*主栏杆截面宽度
        y_offset = 0.5 * main_rail_width
        all_parts = [
            support_combined,
            translate(0, y_offset, 0) * vert_rails_arr,
            translate(0, y_offset, 0) * grid_rail_lower,
            translate(0, y_offset, 0) * grid_rail_upper,
            translate(0, y_offset, 0) * ring_main_rail,
            translate(0, y_offset, 0) * vert_grid_arr,
        ]
        self['圆形阳台'] = combine(*all_parts)

if __name__ == "__main__":
    FinalGeometry = 圆形阳台()
    place(FinalGeometry)
