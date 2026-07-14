from pyp3d import *

# 基础热水器：竖直圆柱A + 横向圆柱B + 排架圆柱C + 平行复制圆柱D + 竖向圆柱E
# 插入点：水箱 底面圆心 (0, 0, 0)

class 基础热水器(Component):
    def __init__(self):
        Component.__init__(self)
        # ========== 可调参数（用户可修改）==========
        self['设备名称'] = Attr('基础热水器', obvious=True)
        self['水箱直径'] = Attr(1000.0, obvious=True)
        self['水箱高度'] = Attr(1200.0, obvious=True)
        self['集水管直径'] = Attr(100.0, obvious=True)      # B 和 D 共用直径
        self['集水管长度'] = Attr(1000.0, obvious=True)     # X 向单侧拉伸长度
        self['排架倾角'] = Attr(45.0, obvious=True)           # 度，Y 轴向 Z 轴偏转
        self['排架管直径'] = Attr(50.0, obvious=True)
        self['排架管间距'] = Attr(185.5, obvious=True)       # 随B长度变化可调
        self['排架管总数'] = Attr(10.0, obvious=True)        # X 向正负对称排列总数
        self['支撑柱直径'] = Attr(20.0, obvious=True)

        # ========== 显示参数（用户只可查看）==========
        self['排架斜长'] = Attr(1214.0, readonly=True, show=True)
        self['支撑柱高度'] = Attr(1000.0, readonly=True, show=True)

        # ========== 输出槽位 ==========
        self['基础热水器'] = Attr(None, show=True)

        # ========== 特征驱动点 ==========
        # point1 = 水箱底面圆心 = 插入点
        self.setDrivenFeaturePoint('point1', SnapMode.EndPoint,
            '[定位点X]', '[定位点Y]', '[定位点Z]')
        # point2 = 水箱顶面圆心
        self.setDrivenFeaturePoint('point2', SnapMode.EndPoint,
            '[定位点X]', '[定位点Y]', '[定位点Z]+[水箱高度]')

        self.replace()

    @export
    def replace(self):
        # ========== 提取参数 ==========
        D_A = self['水箱直径']
        H_A = self['水箱高度']
        R_A = D_A / 2.0

        D_BD = self['集水管直径']
        R_BD = D_BD / 2.0
        L_BD = self['集水管长度']           # 圆柱 B/D 沿 X 单侧拉伸距离
        L_BD = L_BD/2.0

        angle_deg = self['排架倾角']
        angle = angle_deg * pi / 180.0

        D_C = self['排架管直径']
        R_C = D_C / 2.0

        array_spacing = self['排架管间距']
        n_total = int(self['排架管总数'])      # X 向正负对称排列总数（偶数居中）

        D_E = self['支撑柱直径']
        R_E = D_E / 2.0

        # ========== 派生尺寸 ==========
        L_a = D_A / cos(angle) - 2 * D_BD       # 排架斜长 = A直径/cos(倾角) - B直径 - D直径
        H_E = D_A * tan(angle)                 # 圆柱E高度 = A直径 * tan(倾角)

        self['排架斜长'] = L_a
        self['支撑柱高度'] = H_E

        # 排架方向单位向量（YZ 平面，Y 偏 Z）
        tilt_dir_Y = cos(angle)
        tilt_dir_Z = sin(angle)

        # ========== 1. 水箱（底面圆心原点，沿 Z 轴拉伸）==========
        cyl_A = Cone(Vec3(0, 0, 0), Vec3(0, 0, H_A), R_A, R_A)

        # ========== 2. 圆柱体B ==========
        # 圆心：(0, -R_A+R_BD, H_A+R_BD)，沿 X 正负各拉伸 L_BD
        cyl_B_center_Y = -R_A + R_BD
        cyl_B_center_Z = H_A + R_BD
        cyl_B = Cone(
            Vec3(-L_BD, cyl_B_center_Y, cyl_B_center_Z),
            Vec3( L_BD, cyl_B_center_Y, cyl_B_center_Z),
            R_BD, R_BD
        )

        # ========== 3. 排架管排架（沿排架方向，X 向阵列）==========
        cyl_D_center_Y = cyl_B_center_Y + L_a * tilt_dir_Y
        cyl_D_center_Z = cyl_B_center_Z + L_a * tilt_dir_Z

        cyl_C_list = []
        for i in range(n_total):
            x_offset = (i - (n_total - 1) / 2.0) * array_spacing
            cyl_C_start = Vec3(x_offset, cyl_B_center_Y, cyl_B_center_Z)
            cyl_C_end   = Vec3(x_offset, cyl_D_center_Y, cyl_D_center_Z)
            cyl_C = Cone(cyl_C_start, cyl_C_end, R_C, R_C)
            cyl_C_list.append(cyl_C)

        # ========== 4. 圆柱体D（B 平行复制到排架终点）==========
        cyl_D = Cone(
            Vec3(-L_BD, cyl_D_center_Y, cyl_D_center_Z),
            Vec3( L_BD, cyl_D_center_Y, cyl_D_center_Z),
            R_BD, R_BD
        )

        # ========== 5. 支撑柱（排架终点向下到圆柱A上表面）==========
        # 在 XOY 面画圆，沿 Z 负向拉伸至圆柱 A 顶面 Z = H_A
        cyl_E = Cone(
            Vec3(0, cyl_D_center_Y, cyl_D_center_Z),
            Vec3(0, cyl_D_center_Y, H_A),
            R_E, R_E
        )

        # ========== 6. 组合所有部件 ==========
        result = cyl_A + cyl_B + cyl_D + cyl_E
        for c in cyl_C_list:
            result = result + c

        self['基础热水器'] = result


if __name__ == "__main__":
    FinalGeometry = 基础热水器()
    place(FinalGeometry)
