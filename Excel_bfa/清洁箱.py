from pyp3d import *
import math


class 清洁箱(Component):
    """清洁箱：底板 + 箱体 + 前表面柜门（显示屏/显示灯/门把手）+ 右侧水管。

    局部原点（插入点）位于底板前表面（X 最大面）的左下角点，
    即全局坐标 (250, -400, 0)。X 为长度、Y 为宽度、Z 为高度。
    正视图/前表面 = X 最大面；右侧面 = Y 最大面；顶面 = Z 最大面。
    """

    def __init__(self):
        Component.__init__(self)

        self['设备名称'] = Attr('清洁箱', obvious=True)
        self['设备长度'] = Attr(500.0, obvious=True, group='几何属性')
        self['设备宽度'] = Attr(800.0, obvious=True, group='几何属性')
        self['设备高度'] = Attr(1050.0, obvious=True, group='几何属性')
        self['下水管直径'] = Attr(100.0, obvious=True, group='几何属性')
        self['上水管直径'] = Attr(100.0, obvious=True, group='几何属性')
        self['清洁箱'] = Attr(None, show=True)

        # 特征点：水管顶面轴线圆心（突出末端）
        self.setDrivenFeaturePoint('下水管顶面轴线圆心', SnapMode.GeometricCenter,
            '[定位点X] - [设备长度]*0.25',
            '[定位点Y] + [设备宽度] + 100',
            '[定位点Z] + 50 + ([设备高度]-50)*0.125')
        self.setDrivenFeaturePoint('上水管顶面轴线圆心', SnapMode.GeometricCenter,
            '[定位点X] - [设备长度]*0.25',
            '[定位点Y] + [设备宽度] + 100',
            '[定位点Z] + 50 + ([设备高度]-50)*0.375')

        self.replace()

    @export
    def replace(self):
        L = self['设备长度']
        W = self['设备宽度']
        H = self['设备高度']
        d1 = self['下水管直径']
        d2 = self['上水管直径']

        底板_高 = 50.0
        箱体_高 = H - 底板_高

        # 矩形截面（形心在原点，L×W）
        rect_section = translate(-L / 2, -W / 2, 0) * Section(
            Vec2(0, 0), Vec2(L, 0), Vec2(L, W), Vec2(0, W)
        )

        # 1. 底板（x∈[-L/2, 0], y∈[0, W], z∈[0, 底板_高]）
        底板 = Loft(
            translate(-L / 2, W / 2, 0) * rect_section,
            translate(-L / 2, W / 2, 底板_高) * rect_section
        )

        # 2. 箱体（x∈[-L/2, 0], y∈[0, W], z∈[底板_高, 底板_高+箱体_高]）
        箱体 = Loft(
            translate(-L / 2, W / 2, 底板_高) * rect_section,
            translate(-L / 2, W / 2, 底板_高 + 箱体_高) * rect_section
        )

        # 3. 下柜门：在箱体前表面（x=0）挖槽，并内嵌门板
        门板_宽 = W - 100.0
        门板_高 = 箱体_高 - 100.0
        门板_厚 = 30.0
        门板_x0 = -门板_厚
        门板_y0 = (W - 门板_宽) / 2.0
        门板_z0 = 底板_高 + (箱体_高 - 门板_高) / 2.0

        挖空块 = translate(门板_x0, 门板_y0, 门板_z0) * scale(门板_厚, 门板_宽, 门板_高) * Cube()
        箱体 = 箱体 - 挖空块

        门板 = translate(门板_x0, 门板_y0, 门板_z0) * scale(门板_厚, 门板_宽, 门板_高) * Cube()

        # 4. 显示屏（2 个左右对称，截面在 yoz 面，凸出前表面 +X 10）
        屏幕_宽 = 0.2 * W            # Y 方向
        屏幕_高 = 0.2 * 箱体_高       # Z 方向
        屏幕_拉伸 = 10.0              # X 方向（固定值）
        # 截面（形心在原点）：旋转前 X 对应 Z(高)、Y 对应 Y(宽)
        rect_screen = translate(-屏幕_高 / 2, -屏幕_宽 / 2, 0) * Section(
            Vec2(0, 0), Vec2(屏幕_高, 0), Vec2(屏幕_高, 屏幕_宽), Vec2(0, 屏幕_宽)
        )
        section_yoz = roty(-math.pi / 2) * rect_screen
        屏幕_z = 底板_高 + 0.75 * 箱体_高
        屏幕_间距 = 0.5 * 门板_宽
        屏幕_y1 = W / 2 - 屏幕_间距 / 2
        屏幕_y2 = W / 2 + 屏幕_间距 / 2
        显示屏_1 = Loft(
            translate(0, 屏幕_y1, 屏幕_z) * section_yoz,
            translate(屏幕_拉伸, 屏幕_y1, 屏幕_z) * section_yoz
        )
        显示屏_2 = Loft(
            translate(0, 屏幕_y2, 屏幕_z) * section_yoz,
            translate(屏幕_拉伸, 屏幕_y2, 屏幕_z) * section_yoz
        )

        # 5. 显示灯（4 个圆柱，轴线沿 +X，凸出前表面 10）
        灯_直径 = 0.05 * W
        灯_半径 = 灯_直径 / 2.0
        灯_间距 = 0.2 * W
        灯_拉伸 = 10.0
        灯_z = 底板_高 + 0.6 * 箱体_高
        灯列表 = []
        for i in range(4):
            灯_y = W / 2 + (i - 1.5) * 灯_间距
            灯列表.append(
                Cone(
                    Vec3(0, 灯_y, 灯_z),
                    Vec3(灯_拉伸, 灯_y, 灯_z),
                    灯_半径, 灯_半径
                )
            )
        显示灯组 = combine(*灯列表)

        # 6. 门把手（柜门右侧，凸出前表面 +X）
        把手_y = W - 40.0
        把手_z = 底板_高 + 箱体_高 / 2.0
        握把 = Cone(
            Vec3(80, 把手_y, 把手_z - 50), Vec3(80, 把手_y, 把手_z + 50), 10.0, 10.0
        )
        安装座_上 = Cone(
            Vec3(0, 把手_y, 把手_z + 50), Vec3(90, 把手_y, 把手_z + 50), 12.0, 12.0
        )
        安装座_下 = Cone(
            Vec3(0, 把手_y, 把手_z - 50), Vec3(90, 把手_y, 把手_z - 50), 12.0, 12.0
        )
        门把手 = combine(握把, 安装座_上, 安装座_下)

        # 7. 水管（2 个，截面在 xoz 面，从右侧面沿 +Y 突出 100）
        水管_x = -0.25 * L
        水管_1_z = 底板_高 + 箱体_高 * 0.125
        水管_2_z = 底板_高 + 箱体_高 * 0.375
        水管_1 = Cone(
            Vec3(水管_x, W, 水管_1_z),
            Vec3(水管_x, W + 100, 水管_1_z),
            d1 / 2.0, d1 / 2.0
        )
        水管_2 = Cone(
            Vec3(水管_x, W, 水管_2_z),
            Vec3(水管_x, W + 100, 水管_2_z),
            d2 / 2.0, d2 / 2.0
        )

        # 组装
        self['清洁箱'] = combine(
            底板, 箱体, 门板,
            显示屏_1, 显示屏_2,
            显示灯组, 门把手,
            水管_1, 水管_2
        )


if __name__ == '__main__':
    FinalGeometry = 清洁箱()
    place(FinalGeometry)
