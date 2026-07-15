from pyp3d import *
import math

class 热水器(Component):
    def __init__(self):
        Component.__init__(self)
        # ========== 名称 ==========
        self['名称'] = Attr('Python参数化组件 8', obvious=True)

        # ========== 保温桶参数 ==========
        self['保温桶半径'] = Attr(400.0, obvious=True)
        self['保温桶长度'] = Attr(1500.0, obvious=True)

        # ========== 圆环参数 ==========
        self['圆环路径半径'] = Attr(300.0, obvious=True)
        self['圆环截面半径'] = Attr(30.0, obvious=True)

        # ========== 控水箱参数 ==========
        self['控水箱俯角'] = Attr(45.0, obvious=True)
        self['控水箱Y轴长度'] = Attr(100.0, obvious=True)
        self['控水箱Z轴长度'] = Attr(100.0, obvious=True)
        self['控水箱拉伸总距离'] = Attr(200.0, obvious=True)

        # ========== 出水管参数 ==========
        self['右侧出水管半径'] = Attr(10.0, obvious=True)
        self['左侧出水管半径'] = Attr(10.0, obvious=True)
        self['出水管长度'] = Attr(100.0, obvious=True, readonly=True)

        # ========== 隐藏计算参数（供驱动点表达式引用）==========
        self['控水箱原点偏移Y'] = Attr(0.0, obvious=True, readonly=True)
        self['控水箱原点偏移Z'] = Attr(0.0, obvious=True, readonly=True)

        # ========== 输出槽位 ==========
        self['热水器'] = Attr(None, show=True)

        # ========== 特征驱动点 ==========
        # 右侧出水管底部圆截面圆心
        self.setDrivenFeaturePoint('右侧出水管底圆心', SnapMode.GeometricCenter,
            '[定位点X] + [控水箱拉伸总距离]/2',
            '[定位点Y] + [控水箱原点偏移Y]',
            '[定位点Z] + [控水箱原点偏移Z] - [控水箱Y轴长度]/2 - [出水管长度]')

        # 左侧出水管底部圆截面圆心
        self.setDrivenFeaturePoint('左侧出水管底圆心', SnapMode.GeometricCenter,
            '[定位点X] - [控水箱拉伸总距离]/2',
            '[定位点Y] + [控水箱原点偏移Y]',
            '[定位点Z] + [控水箱原点偏移Z] - [控水箱Y轴长度]/2 - [出水管长度]')

        # 控水箱沿Y轴方向第一个表面形心（体心偏移(0, -控水箱Y轴长度/2, 0)）
        self.setDrivenFeaturePoint('控水箱前表面形心', SnapMode.GeometricCenter,
            '[定位点X]',
            '[定位点Y] + [控水箱原点偏移Y] - [控水箱Y轴长度]/2',
            '[定位点Z] + [控水箱原点偏移Z]')

        self.replace()

    @export
    def replace(self):
        # ========== 读取参数 ==========
        R_tank = float(self['保温桶半径'])
        L_tank = float(self['保温桶长度'])
        tank_half = L_tank / 2.0

        R_ring = float(self['圆环路径半径'])
        R_torus = float(self['圆环截面半径'])

        angle_deg = float(self['控水箱俯角'])
        angle_rad = angle_deg * math.pi / 180.0
        box_Y = float(self['控水箱Y轴长度'])
        box_Z = float(self['控水箱Z轴长度'])
        box_half_Y = box_Y / 2.0
        box_half_Z = box_Z / 2.0
        box_extrude = float(self['控水箱拉伸总距离'])
        box_half_extrude = box_extrude / 2.0

        R_pipe_right = float(self['右侧出水管半径'])
        R_pipe_left = float(self['左侧出水管半径'])
        L_pipe = float(self['出水管长度'])

        # ========== 派生坐标 ==========
        # 保温桶轴线中点位于 (0, -R_tank, 0)，沿X轴方向
        tank_center_Y = -R_tank
        tank_center_Z = 0.0

        # 控水箱临时坐标原点（控水箱俯角是沿负Y轴偏向负Z轴为45°）
        box_origin_Y = -R_tank - R_tank * math.cos(angle_rad)
        box_origin_Z = -R_tank * math.sin(angle_rad)

        # 更新隐藏计算参数，供驱动点表达式引用
        self['控水箱原点偏移Y'] = box_origin_Y
        self['控水箱原点偏移Z'] = box_origin_Z

        # 出水管圆心位置（在控水箱临时坐标系中）
        pipe_center_X = box_half_extrude         # 控水箱拉伸总距离*0.5
        pipe_center_Y = 0.0
        pipe_center_Z = -box_half_Y              # 控水箱底面Z=-box_half_Y，出水管顶面与控水箱底面重合

        # ==========================================
        # 1. 保温桶（圆柱体，沿X轴，轴线中点位于(0, -R_tank, 0)）
        # ==========================================
        tank = Cone(
            Vec3(-tank_half, tank_center_Y, tank_center_Z),
            Vec3(tank_half, tank_center_Y, tank_center_Z),
            R_tank, R_tank
        ).color(0.8, 0.8, 0.85, 1)

        # ==========================================
        # 2. 圆环（YOZ面，水箱两端各一个）
        # ==========================================
        section_2d = translate(R_ring, 0) * scale(R_torus, R_torus) * Section(Arc(2 * math.pi))
        section_3d = rotate(Vec3(1, 0, 0), -math.pi / 2.0) * section_2d
        # 默认圆环在XOY面（孔沿Z轴），旋转到YOZ面（孔沿X轴）
        torus_z = Sweep(section_3d, Line(Arc(2 * math.pi)))
        torus_x = rotate(Vec3(0, 1, 0), math.pi / 2.0) * torus_z

        ring_left = translate(-tank_half, tank_center_Y, tank_center_Z) * torus_x
        ring_right = translate(tank_half, tank_center_Y, tank_center_Z) * torus_x

        # ==========================================
        # 3. 控水箱（矩形截面在ZOY面，沿X轴拉伸±100，总长200）
        # ==========================================
        # 矩形截面先在XOY面创建，再旋转到ZOY面
        rect_section_xoy = Section(
            Vec2(-box_half_Y, -box_half_Z),
            Vec2(-box_half_Y, box_half_Z),
            Vec2(box_half_Y, box_half_Z),
            Vec2(box_half_Y, -box_half_Z),
            Vec2(-box_half_Y, -box_half_Z)
        )
        # 绕Y轴旋转-90°：XOY面 → ZOY面
        rect_section_zoy = rotate(Vec3(0, 1, 0), -math.pi / 2.0) * rect_section_xoy
        # 沿X轴扫掠形成长方体
        control_box = Sweep(rect_section_zoy, Line(Vec3(-box_half_extrude, 0, 0), Vec3(box_half_extrude, 0, 0)))
        # 平移到临时坐标原点
        control_box = translate(0, box_origin_Y, box_origin_Z) * control_box
        control_box = control_box.color(0.7, 0.75, 0.8, 1)

        # ==========================================
        # 4. 右侧出水管（在XOY面画圆，向Z轴负向拉伸）
        # ==========================================
        pipe_right = translate(0, box_origin_Y, box_origin_Z) * Cone(
            Vec3(pipe_center_X, pipe_center_Y, pipe_center_Z),
            Vec3(pipe_center_X, pipe_center_Y, pipe_center_Z - L_pipe),
            R_pipe_right, R_pipe_right
        )
        pipe_right = pipe_right.color(0.6, 0.65, 0.7, 1)

        # ==========================================
        # 5. 左侧出水管（对YOZ面镜像复制，半径独立控制）
        # ==========================================
        pipe_left = translate(0, box_origin_Y, box_origin_Z) * Cone(
            Vec3(-pipe_center_X, pipe_center_Y, pipe_center_Z),
            Vec3(-pipe_center_X, pipe_center_Y, pipe_center_Z - L_pipe),
            R_pipe_left, R_pipe_left
        )
        pipe_left = pipe_left.color(0.6, 0.65, 0.7, 1)

        # ==========================================
        # 6. 组合所有部件
        # ==========================================
        self['热水器'] = combine(tank, ring_left, ring_right, control_box, pipe_right, pipe_left)


if __name__ == "__main__":
    FinalGeometry = 热水器()
    place(FinalGeometry)