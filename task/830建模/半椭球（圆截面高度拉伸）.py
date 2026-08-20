from pyp3d import *
import math


class 超细干粉灭火装置_吊环式(Component):
    def __init__(self):
        Component.__init__(self)
        # ========== 参数定义 ==========
        self['构件名称'] = Attr('超细干粉灭火装置（吊环式）', obvious=True, readonly=True)
        self['罐体直径'] = Attr(1500, obvious=True)
        self['罐体高度'] = Attr(1000, obvious=True)
        self['仪表盘直径'] = Attr(105, obvious=True)
        self['连系杆高度'] = Attr(90, obvious=True)
        self['连系杆直径'] = Attr(15, obvious=True)
        self['超细干粉灭火装置_吊环式'] = Attr(None, show=True)

        # ========== 特征点定义 ==========
        # 圆柱体4下底面圆心：Z = -罐体高度/4 - 罐体直径/20
        self.setDrivenFeaturePoint('圆柱体4下底面圆心', SnapMode.GeometricCenter,
            '[定位点X]',
            '[定位点Y]',
            '[定位点Z] - [罐体高度]/4 - [罐体直径]/20')

        self.replace()

    @export
    def replace(self):
        # ========== 读取参数 ==========
        D_tank = self['罐体直径']          # 罐体直径
        R_tank = D_tank / 2               # 罐体半径
        H_tank = self['罐体高度']          # 罐体高度
        D_dash = self['仪表盘直径']         # 仪表盘直径
        H_rod = self['连系杆高度']          # 连系杆高度
        D_rod = self['连系杆直径']          # 连系杆直径

        # ========== 派生参数 ==========
        H_ellip = H_tank / 4              # 半椭球高度
        D_cyl1 = D_tank / 10              # 圆柱体1直径
        R_cyl1 = D_cyl1 / 2               # 圆柱体1半径
        H_cyl1 = H_tank + H_ellip * 1.5   # 圆柱体1高度（原始，含被减部分）
        D_cyl2 = D_tank / 6 + 50           # 圆柱体2直径 = (D_tank/3+100)/2
        R_cyl2 = D_cyl2 / 2               # 圆柱体2半径
        D_cyl3 = D_tank / 6 - 50           # 圆柱体3直径 = (D_tank/3-100)/2
        R_cyl3 = D_cyl3 / 2               # 圆柱体3半径
        Z_cyl23 = H_cyl1 + R_cyl2         # 圆柱体2/3共同圆心Z = 圆柱体1高 + 圆柱体2半径
        half_L_23 = D_tank / 30           # X轴半长 = 50 = D_tank/15/2
        D_cyl4 = D_tank / 5               # 圆柱体4直径
        R_cyl4 = D_cyl4 / 2               # 圆柱体4半径
        H_cyl4 = D_cyl4 / 4               # 圆柱体4高度 = 四分之一自身直径
        Z_cyl4_bottom = -(H_cyl4 + H_ellip)       # 圆柱体4下底面圆心Z坐标（圆心在罐体圆心(0,0,0)）

        # ============================================================
        # Step 1: 罐体（xoy面，圆心=插入点(0,0,0)，直径=D_tank，高=H_tank，+Z）
        # ============================================================
        罐体 = Cone(Vec3(0, 0, 0), Vec3(0, 0, H_tank), R_tank, R_tank)

        # ============================================================
        # Step 2: 上半椭球（xoy面，形心=罐体上底面圆心(0,0,H_tank)）
        #         直径=罐体直径，高度=H_tank/4，+Z方向
        #         下半椭球：以上半椭球关于罐体中心轴线中点(0,0,H_tank/2)镜像
        # ============================================================
        ax = R_tank
        by = R_tank
        cz = H_ellip
        n = 25
        if n % 2 == 0:
            n += 1
        sections_upper = []
        eps = 1e-3
        for i in range(n):
            t = 1.0 * i / (n - 1)                # t ∈ [0, 1]，上半椭球
            z_local = cz * t
            scale_xy = math.sqrt(max(0.0, 1.0 - t * t))
            rx = max(ax * scale_xy, eps)
            ry = max(by * scale_xy, eps)
            sections_upper.append(
                translate(0, 0, z_local) * scale(rx, ry) * Section(Arc(2 * math.pi))
            )
        ellipsoid_upper_half = Loft(*sections_upper)
        ellipsoid_upper_half.smooth = True
        上椭球 = translate(0, 0, H_tank) * ellipsoid_upper_half

        # 镜像：以罐体中心轴线中点 z=H_tank/2 为镜像面
        下椭球 = translate(0, 0, H_tank / 2) * scale(1, 1, -1) * translate(0, 0, -H_tank / 2) * 上椭球

        # ============================================================
        # Step 3: 圆柱体1（xoy面，圆心(0,0,0)，直径=D_cyl1，高=H_cyl1，+Z）
        #         布尔减：圆柱体1 = 圆柱体原始 - (罐体 + 上椭球 + 下椭球)
        #         保留部分为圆柱体1在罐体+椭球外部的部分
        # ============================================================
        圆柱体原始 = Cone(Vec3(0, 0, 0), Vec3(0, 0, H_cyl1), R_cyl1, R_cyl1)
        罐体椭球组 = combine(罐体, 上椭球, 下椭球)
        圆柱体1 = (圆柱体原始 - 罐体椭球组)

        # ============================================================
        # Step 4-5-6: 圆柱体2、圆柱体3（yoz面，共同圆心Z=Z_cyl23）
        #            圆柱体2直径=D_cyl2，圆柱体3直径=D_cyl3
        #            沿X轴±各50（总长100=D_tank/15）
        #            布尔减：吊环 = 圆柱体2 - 圆柱体3
        # ============================================================
        圆柱体2 = Cone(
            Vec3(-half_L_23, 0, Z_cyl23),
            Vec3(half_L_23, 0, Z_cyl23),
            R_cyl2, R_cyl2
        )
        圆柱体3 = Cone(
            Vec3(-half_L_23, 0, Z_cyl23),
            Vec3(half_L_23, 0, Z_cyl23),
            R_cyl3, R_cyl3
        )
        吊环 = 圆柱体2 - 圆柱体3

        # ============================================================
        # Step 7: 圆柱体4（xoy面，圆心=罐体圆心(0,0,0)）
        #         直径=D_cyl4，高度=H_cyl4+H_ellip，-Z方向
        #         布尔减：圆柱体4 = 圆柱体4原始 - 下椭球（减去重合部分）
        # ============================================================
        圆柱体4原始 = Cone(
            Vec3(0, 0, 0),
            Vec3(0, 0, Z_cyl4_bottom),
            R_cyl4, R_cyl4
        )
        圆柱体4 = 圆柱体4原始 - 下椭球

        # ============================================================
        # Step 8: 仪表盘内联
        #         接入点 = 圆柱体4下底面圆周长上一点(R_cyl4, 0, Z_cyl4_bottom)，罐体正视图面（XOZ面）
        #         以接入点对仪表盘镜像（scale(1,1,-1)翻转Z向），
        #         再以接入点为基点右手法则顺时针旋转45°
        # ============================================================
        # --- 仪表盘子组件参数 ---
        D = D_dash
        R = D / 2
        H = H_rod
        DG = D_rod
        RG = DG / 2

        HG = H * 0.3       # 上下杆高度
        HT = H * 0.15      # 上下圆台高度
        HP = H * 0.05      # 上下片高度
        S = D * 0.05       # 仪表盘壁厚
        L = D * 0.85       # 指针长度
        B = D * 0.15       # 指针宽度
        SY = DG * 1.2      # 仪表盘厚度
        SQ = SY * 0.1      # 仪表盘切割厚度
        RP = D * 0.2       # 上下片半径
        RT1 = RP * 0.7     # 上下圆台长半径
        RT2 = RP * 0.6     # 上下圆台短半径
        R_ctrl1 = RP * 0.3 # 圆台阀件控制手杆半径
        R_ctrl2 = RP * 0.2 # 圆台阀件控制手杆端部半径

        # 仪表盘零件
        下杆 = Cone(Vec3(0, 0, 0), Vec3(0, 0, HG), RG, RG)
        下片 = Cone(Vec3(0, 0, HG), Vec3(0, 0, HG + HP), RP, RP)
        下圆台 = Cone(Vec3(0, 0, HG + HP), Vec3(0, 0, HG + HP + HT), RT2, RT1)
        上圆台 = Cone(Vec3(0, 0, HG + HP + HT), Vec3(0, 0, HG + HP + HT * 2), RT1, RT2)
        上片 = Cone(Vec3(0, 0, HG + HP + HT * 2), Vec3(0, 0, HG + HP + HT * 2 + HP), RP, RP)
        上杆 = Cone(Vec3(0, 0, HG + HP + HT * 2 + HP),
                     Vec3(0, 0, HG + HP + HT * 2 + HP + HG + S), RG, RG)
        控制手杆 = Cone(Vec3(0, 0, HG + HP + HT),
                        Vec3(0, -HT * 3, HG + HP + HT), R_ctrl1, R_ctrl1)
        控制手杆端部 = Cone(Vec3(0, -HT * 2.4, HG + HP + HT),
                            Vec3(HT * 6, -HT * 2.4, HG + HP + HT), R_ctrl2, R_ctrl2)

        # 仪表盘外壳
        仪表盘外壳 = Cone(
            Vec3(0, -SY / 2, HG + HP + HT * 2 + HP + HG + R),
            Vec3(0, SY / 2, HG + HP + HT * 2 + HP + HG + R),
            R, R
        )
        仪表盘切割 = Cone(
            Vec3(0, -SY / 2, HG + HP + HT * 2 + HP + HG + R),
            Vec3(0, SY / 2 - SQ, HG + HP + HT * 2 + HP + HG + R),
            R - S, R - S
        )
        仪表盘雏形 = 仪表盘外壳 - 仪表盘切割

        # 指针
        三角平面 = Section(Line(
            Vec3(-B / 2, SY / 2 - SQ, 0),
            Vec3(B / 2, SY / 2 - SQ, 0),
            Vec3(0, SY / 2 - SQ, L)
        ))
        扫掠路径 = Line(Vec3(0, 0, 0), Vec3(0, 0.6 * (SY / 2 - SQ), 0))
        扫掠体 = Sweep(三角平面, 扫掠路径)
        指针雏形 = roty(pi / 6) * translate(0, 0, -L / 2) * 扫掠体
        指针 = translate(0, 0, HG + HP + HT * 2 + HP + HG + R) * 指针雏形

        # 仪表盘组合
        yibiaopan_body = combine(
            下杆, 下片, 下圆台, 上圆台, 上片, 上杆,
            仪表盘雏形, 指针, 控制手杆, 控制手杆端部
        )

        # 仪表盘定位：
        # 接入点 P = (R_cyl4, 0, Z_cyl4_bottom)，位于罐体正视图面（XOZ面）
        # 变换链（从右到左）：scale(1,1,-1)翻转Z → 以接入点为临时原点roty(pi/4)绕Y逆时针45° → translate到接入点
        仪表盘 = translate(R_cyl4, 0, Z_cyl4_bottom) * roty(-pi / 4) * scale(1, 1, -1) * yibiaopan_body

        # ============================================================
        # 总装：组合所有部件
        # ============================================================
        result = combine(
            罐体, 上椭球, 下椭球,
            圆柱体1, 吊环, 圆柱体4,
            仪表盘
        )
        self['超细干粉灭火装置_吊环式'] = result.color(1, 0, 0, 1)


if __name__ == "__main__":
    FinalGeometry = 超细干粉灭火装置_吊环式()
    place(FinalGeometry)