from pyp3d import *
import math

class 太阳能储热罐_立式(Component):
    def __init__(self):
        Component.__init__(self)
        self['设备名称'] = Attr('太阳能储热罐_立式', obvious=True)
        self['储热罐高度'] = Attr(1500, obvious=True)
        self['储热罐半径'] = Attr(250, obvious=True)
        self['外扩厚度'] = Attr(5, obvious=True)
        self['中部水管半径'] = Attr(25, obvious=True)
        self['顶部水管半径'] = Attr(12.5, obvious=True)
        self['太阳能储热罐'] = Attr(None, show=True)

        # ========== 特征点定义 ==========
        # 储热罐顶部截面圆心
        self.setDrivenFeaturePoint('储热罐顶部圆心', SnapMode.GeometricCenter,
            '[定位点X]', '[定位点Y]', '[定位点Z] + [储热罐高度]')
        # 储热罐底部截面圆心
        self.setDrivenFeaturePoint('储热罐底部圆心', SnapMode.GeometricCenter,
            '[定位点X]', '[定位点Y]', '[定位点Z]')
        # 底部水管拉伸终点
        self.setDrivenFeaturePoint('底部水管终点', SnapMode.EndPoint,
            '[定位点X]', '[定位点Y] - [储热罐半径] - [外扩厚度]', '[定位点Z] + 105 + [中部水管半径]')
        # 中部水管拉伸终点
        self.setDrivenFeaturePoint('中部水管终点', SnapMode.EndPoint,
            '[定位点X]', '[定位点Y] - [储热罐半径] - [外扩厚度]', '[定位点Z] + 675 + [中部水管半径]')
        # 镜像底部水管拉伸终点
        self.setDrivenFeaturePoint('上侧底部水管终点', SnapMode.EndPoint,
            '[定位点X]', '[定位点Y] - [储热罐半径] - [外扩厚度]', '[定位点Z] + [储热罐高度] - 105 - [中部水管半径]')
        # 镜像中部水管拉伸终点
        self.setDrivenFeaturePoint('上侧中部水管终点', SnapMode.EndPoint,
            '[定位点X]', '[定位点Y] - [储热罐半径] - [外扩厚度]', '[定位点Z] + [储热罐高度] - 675 - [中部水管半径]')
        # 左侧入水管顶部截面圆心（拉伸终点）
        self.setDrivenFeaturePoint('左侧入水管顶部圆心', SnapMode.EndPoint,
            '[定位点X] - 90 - [顶部水管半径]', '[定位点Y]', '[定位点Z] + [储热罐高度] + 25')
        # 右侧入水管顶部截面圆心（拉伸终点）
        self.setDrivenFeaturePoint('右侧入水管顶部圆心', SnapMode.EndPoint,
            '[定位点X] + 90 + [顶部水管半径]', '[定位点Y]', '[定位点Z] + [储热罐高度] + 25')

        self.replace()

    @export
    def replace(self):
        H = self['储热罐高度']
        R = self['储热罐半径']
        D = self['外扩厚度']
        r = self['中部水管半径']
        r2 = self['顶部水管半径']

        # ========== 步骤1: 储热罐圆柱体 ==========
        # 在xoy面，沿Z轴正向，拉伸起点为原点，半径R，拉伸H
        tank = Cone(Vec3(0, 0, 0), Vec3(0, 0, H), R, R).color(0.2, 0.5, 0.8, 1)

        # ========== 步骤2: 底板 ==========
        # 在xoy面，沿Z轴正向，拉伸起点为原点，半径R+D，拉伸25
        bottom_plate = Cone(Vec3(0, 0, 0), Vec3(0, 0, 25), R + D, R + D).color(0.35, 0.35, 0.45, 1)

        # ========== 步骤3: 顶板 ==========
        # 以(0,0,H)为临时原点，沿Z轴负向，半径R+D，拉伸25
        top_plate = Cone(Vec3(0, 0, H), Vec3(0, 0, H - 25), R + D, R + D).color(0.35, 0.35, 0.45, 1)

        # ========== 步骤4: 底部水管 ==========
        # 临时坐标系原点(0, 0, 105+r)，在zox面，沿Y轴负向拉伸R+D
        bottom_pipe_z = 105 + r
        bottom_pipe = Cone(
            Vec3(0, 0, bottom_pipe_z),
            Vec3(0, -(R + D), bottom_pipe_z),
            r, r
        ).color(0.3, 0.6, 0.9, 1)

        # ========== 步骤5: 中部水管 ==========
        # 临时坐标系原点(0, 0, 675+r)，在zox面，沿Y轴负向拉伸R+D
        middle_pipe_z = 675 + r
        middle_pipe = Cone(
            Vec3(0, 0, middle_pipe_z),
            Vec3(0, -(R + D), middle_pipe_z),
            r, r
        ).color(0.3, 0.6, 0.9, 1)

        # ========== 步骤6: 显示屏 ==========
        # 临时坐标系原点(0, 0, 330)，zoy面矩形截面230(Z)×12(Y)
        # 矩形截面形心(0, -R - 0.5*12, 0) = (0, -R - 6, 0) 在临时坐标下
        # 矩形内边与储热罐外表面齐平(Y = -R)
        display_half_z = 115.0
        display_half_y = 6.0

        # 矩形截面：在yoz面(YZ平面)，形心在临时原点
        # Section默认在XOY面，Vec2(x,y)经roty(pi/2)映射为(x,y,z)→(z,y,-x)
        # 目标：Y=±6(宽度12), Z=±115(长度230)，故Vec2中x控制Z、y控制Y
        rect_section = roty(math.pi / 2) * Section(
            Vec2(-display_half_z, -display_half_y),
            Vec2(display_half_z, -display_half_y),
            Vec2(display_half_z, display_half_y),
            Vec2(-display_half_z, display_half_y)
        )

        # 将截面平移到圆弧起点位置：形心(0, -R - display_half_y, 0)
        rect_at_arc = translate(0, -R - display_half_y, 0) * rect_section

        # 弧线a：以临时原点为圆心，起点(0,-R-6,0)，绕Z轴逆时针12°
        # Arc仅表示旋转角度，扫掠半径由截面位置决定
        path_a = Line(Arc(12 * math.pi / 180))
        sweep_a = Sweep(rect_at_arc, path_a)
        # 放样体a：平移到全局坐标(0, 0, 330)
        loft_a = translate(0, 0, 330) * sweep_a.color(0.5, 0.5, 0.6, 1)

        # 放样体b：以zoy面(X=0)为对称面镜像放样体a
        loft_b = scale(-1, 1, 1) * loft_a

        # ========== 步骤7: 镜像复制（关于Z=H/2的xoy面） ==========
        # mirror: translate(0,0,H/2) * scale(1,1,-1) * translate(0,0,-H/2)
        mirror_z = translate(0, 0, H / 2) * scale(1, 1, -1) * translate(0, 0, -H / 2)

        bottom_pipe_mirror = mirror_z * bottom_pipe
        middle_pipe_mirror = mirror_z * middle_pipe
        loft_a_mirror = mirror_z * loft_a
        loft_b_mirror = mirror_z * loft_b

        # ========== 步骤8: 顶部入水管群 ==========
        # 临时坐标系原点(0, 0, H)，在xoy面，以(90+r2, 0, 0)为圆心，沿Z轴正向拉伸25
        right_inlet_x = 90 + r2
        right_inlet = Cone(
            Vec3(right_inlet_x, 0, H),
            Vec3(right_inlet_x, 0, H + 25),
            r2, r2
        ).color(0.3, 0.7, 0.9, 1)

        # 左侧入水管：以yoz面为对称面镜像
        left_inlet = Cone(
            Vec3(-right_inlet_x, 0, H),
            Vec3(-right_inlet_x, 0, H + 25),
            r2, r2
        ).color(0.3, 0.7, 0.9, 1)

        # ========== 组合所有部件 ==========
        result = combine(
            tank,
            bottom_plate,
            top_plate,
            bottom_pipe,
            middle_pipe,
            loft_a,
            loft_b,
            bottom_pipe_mirror,
            middle_pipe_mirror,
            loft_a_mirror,
            loft_b_mirror,
            right_inlet,
            left_inlet
        )

        self['太阳能储热罐'] = result


if __name__ == "__main__":
    FinalGeometry = 太阳能储热罐_立式()
    place(FinalGeometry)