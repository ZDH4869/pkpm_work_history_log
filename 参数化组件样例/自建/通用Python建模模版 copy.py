# -*- coding: utf-8 -*-
from pyp3d import *

class 通用模板(Component):
    def __init__(self):
        Component.__init__(self)
        self['组件名称'] = Attr('圆环柱体', obvious=True)
        self['圆环半径'] = Attr(500.0, obvious=True)       # YOZ 面圆路径半径
        self['截面半径'] = Attr(50.0, obvious=True)        # 扫掠截面半径
        self['模型'] = Attr(None, show=True)
        self.replace()

    @export
    def replace(self):
        # —— 参数提取 ——
        ring_r = self['圆环半径']    # 扫掠路径（YOZ面圆）半径
        tube_r = self['截面半径']    # 扫掠截面（圆形）半径

        # —— 截面：XOY面画 unit circle → 平移 → 缩放为 tube_r 圆 ——
        unit_circle = Section(Arc(pi * 2))                         # Arc(2π)：XOY面单位圆
        sec_translated = translate(ring_r, 0) * unit_circle        # 圆心平移至 (ring_r, 0)
        sec_scaled = scale(tube_r, tube_r) * sec_translated        # 缩放为半径 tube_r
        # —— 截面旋转：法线从 Z 轴转至对齐扫掠方向（绕 X 旋转 -90°→XOY→XOZ） ——
        section_3d = rotate(Vec3(1, 0, 0), -pi / 2.0) * sec_scaled  # 截面进 XOZ 平面

        # —— 扫掠路径：Z 轴方向的单位圆 ——
        path_unit_circle = Line(Arc(pi * 2))                       # Arc → Line：单位圆（绕 Z）

        # —— 扫掠生成绕 Z 轴的圆环 ——
        torus_z = Sweep(section_3d, path_unit_circle)              # 截面沿路径扫掠

        # —— 旋转：Z 轴圆环转至绕 X 轴（即 YOZ 平面圆路径） ——
        torus_x = rotate(Vec3(0, 1, 0), pi / 2.0) * torus_z       # 绕 Y 转 90°：Z→X

        self['模型'] = torus_x


if __name__ == "__main__":
    place(通用模板())
