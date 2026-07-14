# -*- coding: utf-8 -*-
"""
============================================================================
 BIMBase pyp3d 通用建模模板
 涵盖：参数定义、基础体、拉伸/放样/扫掠、布尔运算、变换、阵列、驱动点
 可运行：python 通用Python建模模版.py  或在 BIMBase 中作为参数化组件加载
============================================================================
使用说明：
  1. 删除不需要的板块，保留需要的部分
  2. 按需修改 Attr 默认值和参数名
  3. 组合时用 + 连接各个部件
============================================================================
"""

from pyp3d import *


class 通用模板(Component):
    """通用参数化建模组件模板"""

    def __init__(self):
        Component.__init__(self)

        # ────────────────────────────────────────────────────────────────
        # 【板块A】可调参数 —— 用户在属性面板中可修改的参数
        #   obvious=True   → 可见（默认 False 不可见）
        #   readonly=True  → 置灰不可调（默认 False 可调）
        #   combo=[...]    → 下拉选项
        # ────────────────────────────────────────────────────────────────
        self['组件名称'] = Attr('示例模型', obvious=True)
        self['长度'] = Attr(1000.0, obvious=True)
        self['宽度'] = Attr(500.0, obvious=True)
        self['高度'] = Attr(300.0, obvious=True)
        self['半径'] = Attr(100.0, obvious=True)
        self['角度'] = Attr(45.0, obvious=True)             # 度
        self['阵列数量'] = Attr(5.0, obvious=True)          # 整数用浮点声明
        self['阵列间距'] = Attr(185.5, obvious=True)
        self['是否启用'] = Attr(1.0, obvious=True)          # 0=禁用, 1=启用（Bool 型）

        # ────────────────────────────────────────────────────────────────
        # 【板块B】显示参数 —— 用户只可查看（派生/计算结果）
        #   readonly=True, show=True  → 只读显示
        # ────────────────────────────────────────────────────────────────
        self['对角线长度'] = Attr(1118.0, readonly=True, show=True)
        self['总面积'] = Attr(500000.0, readonly=True, show=True)

        # ────────────────────────────────────────────────────────────────
        # 【板块C】输出槽位 —— 用于插入点 / 被别的组件引用
        #   默认 None，replace() 中赋值
        # ────────────────────────────────────────────────────────────────
        self['模型'] = Attr(None, show=True)

        # ────────────────────────────────────────────────────────────────
        # 【板块D】驱动点 —— 用于捕捉/对齐（截面圆心、端点等）
        #   语法：self.setDrivenFeaturePoint('名称', SnapMode, 'X', 'Y', 'Z')
        #   SnapMode 可选：GeometricCenter（几何中心）, PointOnFace, MidPoint, ...
        #   坐标字符串中可用 [参数名] 引用面板参数
        # ────────────────────────────────────────────────────────────────
        self.setDrivenFeaturePoint(
            '左端圆心', SnapMode.GeometricCenter,
            '0', '0', '[半径]'
        )
        self.setDrivenFeaturePoint(
            '右端圆心', SnapMode.GeometricCenter,
            '[长度]', '0', '[半径]'
        )

        # 初始化
        self.replace()

    @export
    def replace(self):
        # ────────────────────────────────────────────────────────────────
        # 【板块E】提取参数 & 派生计算
        # ────────────────────────────────────────────────────────────────
        L = self['长度']
        W = self['宽度']
        H = self['高度']
        R = self['半径']
        angle_deg = self['角度']
        angle = angle_deg * pi / 180.0               # 角度 → 弧度
        n_array = int(self['阵列数量'])
        spacing = self['阵列间距']

        # 派生尺寸
        diagonal = sqrt(L**2 + H**2)                  # 示例：对角线
        half_L = L / 2.0

        # 更新只读属性
        self['对角线长度'] = diagonal

        # ────────────────────────────────────────────────────────────────
        # 【板块F】基础几何体
        # ────────────────────────────────────────────────────────────────

        # --- F1. 长方体 ---
        # scale(L, W, H) * Cube()  创建一个 L×W×H 的长方体，中心在原点
        box = scale(L, W, H) * Cube()

        # --- F2. 圆柱体（Cone 两端等半径即为圆柱）---
        # Cone(起点Vec3, 终点Vec3, 起点半径, 终点半径)
        # 下方 → 上方（竖直圆柱）
        cyl_vertical = Cone(
            Vec3(0, 0, 0),        # 底部圆心
            Vec3(0, 0, H),        # 顶部圆心
            R, R                   # 底部半径 = 顶部半径 = 圆柱
        )
        # 左 → 右（水平圆柱，沿 X 轴）
        cyl_horizontal = Cone(
            Vec3(0, 0, R),        # 左端圆心
            Vec3(L, 0, R),        # 右端圆心
            R, R
        )
        # 任意朝向圆柱（斜向，例如 Y 偏 Z 45°）
        cyl_oblique = Cone(
            Vec3(0, 0, 0),
            Vec3(0, L * cos(angle), L * sin(angle)),
            R * 0.5, R * 0.5
        )

        # --- F3. 圆锥台（两端半径不同）---
        # Cone(起点, 终点, 起点半径, 终点半径)
        cone_frustum = Cone(
            Vec3(0, 0, 0),
            Vec3(0, 0, H),
            R, R * 0.3             # 顶部半径 = 底部半径的 30%
        )

        # --- F4. 球体 ---
        # Sphere(圆心Vec3, 半径)
        sphere = Sphere(Vec3(0, 0, H/2), R)

        # --- F5. 圆环（Torus）---
        # Torus(中心Vec3, 法向Vec3, 环半径, 管半径)
        torus = Torus(Vec3(0, 0, 0), Vec3(0, 0, 1), R * 2, R * 0.3)

        # ────────────────────────────────────────────────────────────────
        # 【板块G】截面与放样（Section / Loft）
        # ────────────────────────────────────────────────────────────────

        # --- G1. 圆形截面 ---
        # Section(Arc(2*pi))  → 单位圆截面，半径1
        circle_sec = Section(Arc(2 * pi))

        # --- G2. 椭圆形截面（整圆缩放）---
        # scale(rx, ry) * Section(Arc(2*pi))  → 椭圆截面
        elliptical_sec = scale(R * 0.5, R) * Section(Arc(2 * pi))

        # --- G3. 矩形截面 ---
        # Section(p1, p2, p3, p4)  → 四边形截面（顺时针或逆时针）
        rect_sec = Section(
            Vec2(-50, -30),       # 左下
            Vec2( 50, -30),       # 右下
            Vec2( 50,  30),       # 右上
            Vec2(-50,  30)        # 左上
        )

        # --- G4. 放样（两端截面之间的过渡体）---
        # Loft(截面A, 截面B)
        sec_bottom = translate(0, 0, 0) * circle_sec
        sec_top = translate(0, 0, H) * elliptical_sec
        loft_body = Loft(sec_bottom, sec_top)

        # --- G5. 扫掠（截面沿路径生成体）---
        # Sweep(路径Line/Arc/列表, 截面)
        path = Line(Vec3(0, 0, 0), Vec3(L, 0, H))    # 直线路径
        sweep_body = Sweep(path, circle_sec)

        # --- G6. 多截面放样（两端+中间截面）---
        sec_mid = translate(0, 0, H/2) * (
            scale(R * 0.2, R * 0.2) * Section(Arc(2 * pi))
        )
        loft_multi = Loft(sec_bottom, sec_mid, sec_top)

        # ────────────────────────────────────────────────────────────────
        # 【板块H】几何变换
        #   注意：变换从右向左依次作用！
        #   例 translate * rotate * scale * Cube()
        #     → 先 scale，再 rotate，最后 translate
        # ────────────────────────────────────────────────────────────────

        # --- H1. 平移 ---
        # translate(x, y, z) 或 translate(Vec3(x,y,z))
        translated = translate(L/2, W/2, H/2) * box

        # --- H2. 旋转 ---
        # rotate(轴向量Vec3, 弧度)
        rotated_around_X = rotate(Vec3(1, 0, 0), angle) * box      # 绕 X 轴
        rotated_around_Y = rotate(Vec3(0, 1, 0), angle) * box      # 绕 Y 轴
        rotated_around_Z = rotate(Vec3(0, 0, 1), angle) * box      # 绕 Z 轴

        # --- H3. 缩放 ---
        # scale(sx, sy, sz)
        scaled = scale(0.5, 1.0, 2.0) * box

        # --- H4. 变换组合 ---
        # 先缩放 → 再旋转 → 最后平移
        combined = translate(L/2, 0, 0) * rotate(Vec3(0, 0, 1), pi/4) * scale(1, 2, 1) * box

        # ────────────────────────────────────────────────────────────────
        # 【板块I】阵列
        # ────────────────────────────────────────────────────────────────

        # --- I1. 线性阵列（沿 X 轴均布 n 个）---
        parts = []
        for i in range(n_array):
            x_offset = i * spacing                     # 递增方式
            # 或 居中排列：
            # x_offset = (i - (n_array - 1) / 2.0) * spacing
            part_i = translate(x_offset, 0, 0) * cyl_vertical
            parts.append(part_i)

        # --- I2. 阵列汇总 ---
        if parts:
            array_result = parts[0]
            for p in parts[1:]:
                array_result = array_result + p
        else:
            array_result = None

        # ────────────────────────────────────────────────────────────────
        # 【板块J】布尔运算
        # ────────────────────────────────────────────────────────────────

        # --- J1. 并集（+）---
        union = box + sphere

        # --- J2. 差集（-）---
        difference = box - sphere                       # 从 box 中挖掉 sphere

        # --- J3. 交集（*）---
        intersection = box * sphere

        # ────────────────────────────────────────────────────────────────
        # 【板块K】条件分支（可选部件）
        # ────────────────────────────────────────────────────────────────
        enable = self['是否启用'] > 0.5
        if enable:
            optional_part = cyl_vertical
        else:
            optional_part = None

        # ────────────────────────────────────────────────────────────────
        # 【板块L】最终组合
        # ────────────────────────────────────────────────────────────────
        # 将所有需要的部件用 + 连接
        model_parts = [box, cyl_vertical]               # ← 替换为实际需要的部件列表

        result = model_parts[0]
        for part in model_parts[1:]:
            result = result + part

        # 如果有阵列部件，也加入
        if array_result is not None:
            result = result + array_result

        # 如果有可选部件，也加入
        if optional_part is not None:
            result = result + optional_part

        self['模型'] = result


# ════════════════════════════════════════════════════════════════════════
# 运行入口
# ════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    FinalGeometry = 通用模板()
    place(FinalGeometry)
