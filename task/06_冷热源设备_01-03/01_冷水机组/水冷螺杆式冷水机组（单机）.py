from pyp3d import *

class 水冷螺杆式冷水机组单机(Component):
    def __init__(self):
        Component.__init__(self)
        # ========== 基础几何参数（内部，只读） ==========
        self['水平支撑板厚度'] = Attr(50.0, obvious=True, readonly=True)
        self['蒸发器竖向支撑板长度'] = Attr(600.0, obvious=True, readonly=True)
        self['冷凝器竖向支撑板长度'] = Attr(800.0, obvious=True, readonly=True)
        self['冷凝器竖向支撑板高度'] = Attr(1200.0, obvious=True, readonly=True)
        self['蒸发器竖向支撑板高度'] = Attr(1000.0, obvious=True, readonly=True)
        self['蒸发器球帽直径'] = Attr(400.0, obvious=True, readonly=True)
        self['冷凝器球帽直径'] = Attr(600.0, obvious=True, readonly=True)
        self['蒸发器水管直径'] = Attr(50.0, obvious=True)
        self['蒸发器水管外环直径'] = Attr(100.0, obvious=True, readonly=True)
        self['冷凝器水管直径'] = Attr(75.0, obvious=True)
        self['冷凝器水管外环直径'] = Attr(125.0, obvious=True, readonly=True)
        self['主管拉伸长度'] = Attr(2000.0, obvious=True, readonly=True)
        self['蒸发器副管直径'] = Attr(300.0, obvious=True, readonly=True)
        self['冷凝器副管直径'] = Attr(300.0, obvious=True, readonly=True)

        # ========== 用户可修改参数 ==========
        self['设备长度'] = Attr(4700.0, obvious=True, readonly=True)
        self['设备宽度'] = Attr(1400.0, obvious=True, readonly=True)
        self['设备高度'] = Attr(1400.0, obvious=True, readonly=True)
        self['冷凝器管口直径'] = Attr(75.0, obvious=True)
        self['蒸发器管口直径'] = Attr(50.0, obvious=True)

        # ========== 显示文本属性 ==========
        self['型号'] = Attr('SPS-120W', obvious=True)
        self['使用电源'] = Attr('3Φ-380V-50Hz', obvious=True)
        self['制冷量_kW'] = Attr('120.3', obvious=True)
        self['制冷量_kcal'] = Attr('103500', obvious=True)
        self['运行电流'] = Attr('52.2', obvious=True)
        self['冷冻水量'] = Attr('20.8', obvious=True)
        self['冷却水量'] = Attr('26', obvious=True)
        self['压缩机型式'] = Attr('半封闭螺杆式', obvious=True)
        self['压缩机数量'] = Attr('1', obvious=True)
        self['压缩机启动方式'] = Attr('Y-△', obvious=True)
        self['压缩机容量控制'] = Attr('0,33,66,100 或 0,25,50,75,100', obvious=True)
        self['压缩机功率'] = Attr('30', obvious=True)
        self['冷冻油种类'] = Attr('HBR-A01', obvious=True)
        self['冷冻油容量'] = Attr('7', obvious=True)
        self['冷媒种类'] = Attr('R-22', obvious=True)
        self['冷媒控制方式'] = Attr('感温式外部均压膨胀阀', obvious=True)
        self['冷媒容量'] = Attr('25', obvious=True)
        self['蒸发器型式'] = Attr('壳管式', obvious=True)
        self['蒸发器管径'] = Attr('DN80', obvious=True)
        self['冷凝器型式'] = Attr('壳管式', obvious=True)
        self['冷凝器管径'] = Attr('DN80', obvious=True)
        self['保护装置'] = Attr('', obvious=True)
        self['外形尺寸长'] = Attr('2298', obvious=True)
        self['外形尺寸宽'] = Attr('817', obvious=True)
        self['外形尺寸高'] = Attr('1463', obvious=True)
        self['重量'] = Attr('1074', obvious=True)

        # ========== 输出槽位 ==========
        self['冷水机组'] = Attr(None, show=True)

        # ========== 驱动点（特征点）定义 ==========
        # 插入点为(0, L_cond, 0)=(0, 800, 0)，特征点Y偏移 = 全局Y - 800
        self.setDrivenFeaturePoint(
            '冷凝器上水管终点',
            SnapMode.GeometricCenter,
            '[定位点 X] + [蒸发器球帽直径]',
            '[定位点 Y] - 125',
            '[定位点 Z] + 650'
        )
        self.setDrivenFeaturePoint(
            '冷凝器下水管终点',
            SnapMode.GeometricCenter,
            '[定位点 X] + [蒸发器球帽直径]',
            '[定位点 Y] - 125',
            '[定位点 Z] + 350'
        )
        self.setDrivenFeaturePoint(
            '蒸发器上水管终点',
            SnapMode.GeometricCenter,
            '[定位点 X] + [蒸发器球帽直径]',
            '[定位点 Y] - 825',
            '[定位点 Z] + 600'
        )
        self.setDrivenFeaturePoint(
            '蒸发器下水管终点',
            SnapMode.GeometricCenter,
            '[定位点 X] + [蒸发器球帽直径]',
            '[定位点 Y] - 825',
            '[定位点 Z] + 400'
        )
        self.setDrivenFeaturePoint(
            '副压缩机终点',
            SnapMode.GeometricCenter,
            '[定位点 X] - 950',
            '[定位点 Y] - 125',
            '[定位点 Z] + 1200'
        )
        self.setDrivenFeaturePoint(
            '显示屏特征点',
            SnapMode.GeometricCenter,
            '[定位点 X] - 3950',
            '[定位点 Y] - 125',
            '[定位点 Z] + 1000'
        )

        self.replace()

    @export
    def replace(self):
        # ==================== 读取基础参数 ====================
        T = float(self['水平支撑板厚度'])                    # 50
        L_evap = float(self['蒸发器竖向支撑板长度'])          # 600
        L_cond = float(self['冷凝器竖向支撑板长度'])          # 800
        H_cond = float(self['冷凝器竖向支撑板高度'])          # 1200
        H_evap = float(self['蒸发器竖向支撑板高度'])          # 1000
        D_evap_cap = float(self['蒸发器球帽直径'])            # 400
        D_cond_cap = float(self['冷凝器球帽直径'])            # 600
        D_evap_pipe = float(self['蒸发器水管直径'])           # 50
        D_evap_outer = float(self['蒸发器水管外环直径'])       # 100
        D_cond_pipe = float(self['冷凝器水管直径'])           # 75
        D_cond_outer = float(self['冷凝器水管外环直径'])       # 125
        L_main = float(self['主管拉伸长度'])                  # 2000
        D_sub = float(self['蒸发器副管直径'])                 # 300
        D_cond_sub = float(self['冷凝器副管直径'])            # 300
        D_main = D_cond_sub + 100.0                          # 400 (主压缩机直径)

        # 派生值
        R_evap_cap = D_evap_cap / 2.0       # 200
        R_cond_cap = D_cond_cap / 2.0       # 300
        R_evap_pipe = D_evap_pipe / 2.0     # 25
        R_evap_outer = D_evap_outer / 2.0   # 50
        R_cond_pipe = D_cond_pipe / 2.0     # 37.5
        R_cond_outer = D_cond_outer / 2.0   # 62.5
        R_sub = D_sub / 2.0                 # 150
        R_cond_sub = D_cond_sub / 2.0       # 150
        R_main = D_main / 2.0               # 200
        L_total_y = L_evap + L_cond         # 1400

        # ==================== 关键坐标点 ====================
        # 蒸发器球帽球心（步骤4的临时坐标系原点）
        evap_cap_center = Vec3(0, -T/2.0, H_evap/2.0)         # (0, -25, 500)
        # 冷凝器球帽球心（步骤6的临时坐标系原点）
        cond_cap_center = Vec3(0, evap_cap_center.y + L_evap/2.0 + L_cond/2.0, H_evap/2.0)  # (0, 675, 500)

        all_parts = []

        # ============================================================
        #  步骤1：水平支撑板
        #  YOZ面，形心(0,0,T/2=25)，Y长=1400，Z高=50，沿-X拉伸200
        # ============================================================
        step1_plate = Box(
            Vec3(0, 0, T/2.0),
            Vec3(-T*4.0, 0, T/2.0),  # -200
            Vec3(0, 1, 0),
            Vec3(0, 0, 1),
            L_total_y, T,
            L_total_y, T
        ).color(0.65, 0.65, 0.65, 1)
        #  镜像前平移(0,-300,0)
        step1_plate = translate(0, -300, 0) * step1_plate
        all_parts.append(step1_plate)

        # ============================================================
        #  步骤2：冷凝器竖向支撑板
        #  临时原点(-100,0,50)，矢量平移(0, L_cond/2=400,0) → 形心(-100,400,50)
        #  YOZ面，Y长=800，Z高=1200，X±25拉伸(总50)
        # ============================================================
        cx2 = -T*2.0                      # -100
        cy2 = L_cond/2.0                  # 400
        cz2 = T                           # 50
        step2_cond_support = Box(
            Vec3(cx2 - T/2.0, cy2, cz2),   # (-125, 400, 50)
            Vec3(cx2 + T/2.0, cy2, cz2),   # (-75, 400, 50)
            Vec3(0, 1, 0),
            Vec3(0, 0, 1),
            L_cond, H_cond,
            L_cond, H_cond
        ).color(0.6, 0.6, 0.6, 1)
        #  镜像前平移(0,-100,25)
        step2_cond_support = translate(0, -100, 25) * step2_cond_support
        all_parts.append(step2_cond_support)

        # ============================================================
        #  步骤3：蒸发器竖向支撑板
        #  临时原点(-100,0,50)，矢量平移(0, -L_evap/2=-300,0) → 形心(-100,-300,50)
        #  YOZ面，Y长=600，Z高=1000，X±25拉伸(总50)
        # ============================================================
        cy3 = -L_evap/2.0                 # -300
        step3_evap_support = Box(
            Vec3(cx2 - T/2.0, cy3, cz2),   # (-125, -300, 50)
            Vec3(cx2 + T/2.0, cy3, cz2),   # (-75, -300, 50)
            Vec3(0, 1, 0),
            Vec3(0, 0, 1),
            L_evap, H_evap,
            L_evap, H_evap
        ).color(0.6, 0.6, 0.6, 1)
        #  镜像前平移(0,0,25)
        step3_evap_support = translate(0, 0, 25) * step3_evap_support
        all_parts.append(step3_evap_support)

        # ============================================================
        #  步骤4：蒸发器球帽（球心(0,-25,500)，直径400 → r=200）
        # ============================================================
        step4_evap_cap = translate(evap_cap_center.x, evap_cap_center.y, evap_cap_center.z) * scale(R_evap_cap) * Sphere()
        step4_evap_cap = step4_evap_cap.color(0.45, 0.65, 0.8, 1)
        all_parts.append(step4_evap_cap)

        # ============================================================
        #  步骤5a：蒸发器上水管（圆心Z = 0.25*D_evap_cap = 100）
        #  临时原点=蒸发器球帽球心(0,-25,500)
        #  圆心(0,0,100) → 全局(0,-25,600)，r=25，沿+X拉伸400
        # ============================================================
        evap_pipe_z_top = evap_cap_center.z + D_evap_cap * 0.25   # 600
        step5a = Cone(
            Vec3(evap_cap_center.x, evap_cap_center.y, evap_pipe_z_top),
            Vec3(evap_cap_center.x + D_evap_cap, evap_cap_center.y, evap_pipe_z_top),
            R_evap_pipe, R_evap_pipe
        ).color(0.2, 0.4, 0.8, 1)
        all_parts.append(step5a)

        #  步骤5b：蒸发器水管上外环
        #  圆心=上水管拉伸终点(400,-25,600)，r=50，沿-X拉伸50
        # ============================================================
        step5b = Cone(
            Vec3(evap_cap_center.x + D_evap_cap, evap_cap_center.y, evap_pipe_z_top),
            Vec3(evap_cap_center.x + D_evap_cap - T, evap_cap_center.y, evap_pipe_z_top),
            R_evap_outer, R_evap_outer
        ).color(0.2, 0.4, 0.8, 1)
        all_parts.append(step5b)

        #  步骤5c：蒸发器下水管+下外环（沿临时坐标系xoy面 Z=500 镜像）
        # ============================================================
        mirror_z500 = translate(0, 0, H_evap) * scale(1, 1, -1)  # 1000 = 2*500
        step5c_lower_pipe = (mirror_z500 * step5a).color(0.2, 0.4, 0.8, 1)
        step5c_lower_ring = (mirror_z500 * step5b).color(0.2, 0.4, 0.8, 1)
        all_parts.append(step5c_lower_pipe)
        all_parts.append(step5c_lower_ring)

        # ============================================================
        #  步骤6：冷凝器球帽（球心(0,675,500)，直径600 → r=300）
        # ============================================================
        step6_cond_cap = translate(cond_cap_center.x, cond_cap_center.y, cond_cap_center.z) * scale(R_cond_cap) * Sphere()
        step6_cond_cap = step6_cond_cap.color(0.45, 0.65, 0.8, 1)
        all_parts.append(step6_cond_cap)

        # ============================================================
        #  步骤7a：冷凝器上水管
        #  临时原点=冷凝器球帽球心(0,675,500)
        #  圆心(0,0,0.25*D_cond_cap=150) → 全局(0,675,650)，r=37.5，沿+X拉伸400
        # ============================================================
        cond_pipe_z_top = cond_cap_center.z + D_cond_cap * 0.25  # 650
        step7a = Cone(
            Vec3(cond_cap_center.x, cond_cap_center.y, cond_pipe_z_top),
            Vec3(cond_cap_center.x + D_evap_cap, cond_cap_center.y, cond_pipe_z_top),
            R_cond_pipe, R_cond_pipe
        ).color(0.2, 0.4, 0.8, 1)
        all_parts.append(step7a)

        #  步骤7b：冷凝器水管上外环
        #  圆心=上水管拉伸终点(400,675,650)，r=62.5，沿-X拉伸50
        # ============================================================
        step7b = Cone(
            Vec3(cond_cap_center.x + D_evap_cap, cond_cap_center.y, cond_pipe_z_top),
            Vec3(cond_cap_center.x + D_evap_cap - T, cond_cap_center.y, cond_pipe_z_top),
            R_cond_outer, R_cond_outer
        ).color(0.2, 0.4, 0.8, 1)
        all_parts.append(step7b)

        #  步骤7c：冷凝器下水管+下外环（沿临时坐标系xoy面 Z=500 镜像）
        # ============================================================
        step7c_lower_pipe = (mirror_z500 * step7a).color(0.2, 0.4, 0.8, 1)
        step7c_lower_ring = (mirror_z500 * step7b).color(0.2, 0.4, 0.8, 1)
        all_parts.append(step7c_lower_pipe)
        all_parts.append(step7c_lower_ring)

        # ============================================================
        #  步骤8：左侧蒸发器主管
        #  圆心=蒸发器球帽球心(0,-25,500)，r=200，沿-X拉伸2000
        # ============================================================
        step8_evap_main = Cone(
            Vec3(evap_cap_center.x, evap_cap_center.y, evap_cap_center.z),
            Vec3(evap_cap_center.x - L_main, evap_cap_center.y, evap_cap_center.z),
            R_evap_cap, R_evap_cap
        ).color(0.55, 0.55, 0.55, 1)
        all_parts.append(step8_evap_main)

        # ============================================================
        #  步骤9：左侧冷凝器主管
        #  圆心=冷凝器球帽球心(0,675,500)，r=300，沿-X拉伸2000
        # ============================================================
        step9_cond_main = Cone(
            Vec3(cond_cap_center.x, cond_cap_center.y, cond_cap_center.z),
            Vec3(cond_cap_center.x - L_main, cond_cap_center.y, cond_cap_center.z),
            R_cond_cap, R_cond_cap
        ).color(0.55, 0.55, 0.55, 1)
        all_parts.append(step9_cond_main)

        # ============================================================
        #  步骤10：右侧部件群镜像
        #  临时坐标系原点 = 蒸发器球帽球心 + (-L_main, 0, 0) = (-2000, -25, 500)
        #  沿临时坐标系zoy面（X=-2000）镜像
        #  mirror: translate(-4000, 0, 0) * scale(-1, 1, 1)
        # ============================================================
        mirror_x_neg2000 = translate(-L_main * 2.0, 0, 0) * scale(-1, 1, 1)
        step10_right_plate = (mirror_x_neg2000 * step1_plate).color(0.65, 0.65, 0.65, 1)
        step10_right_cond_support = (mirror_x_neg2000 * step2_cond_support).color(0.6, 0.6, 0.6, 1)
        step10_right_evap_support = (mirror_x_neg2000 * step3_evap_support).color(0.6, 0.6, 0.6, 1)
        step10_right_evap_cap = (mirror_x_neg2000 * step4_evap_cap).color(0.45, 0.65, 0.8, 1)
        step10_right_cond_cap = (mirror_x_neg2000 * step6_cond_cap).color(0.45, 0.65, 0.8, 1)
        step10_right_evap_main = (mirror_x_neg2000 * step8_evap_main).color(0.55, 0.55, 0.55, 1)
        step10_right_cond_main = (mirror_x_neg2000 * step9_cond_main).color(0.55, 0.55, 0.55, 1)
        all_parts.extend([
            step10_right_plate,
            step10_right_cond_support,
            step10_right_evap_support,
            step10_right_evap_cap,
            step10_right_cond_cap,
            step10_right_evap_main,
            step10_right_cond_main,
        ])

        # ============================================================
        #  步骤11：蒸发器副管支撑管
        #  临时原点=左侧蒸发器主管终点(-2000,-25,500)
        #  XOY面圆，r=100，沿+Z拉伸700 → 终点(-2000,-25,1200)
        # ============================================================
        evap_main_end = Vec3(evap_cap_center.x - L_main, evap_cap_center.y, evap_cap_center.z)  # (-2000,-25,500)
        step11_extrude = 700.0  # 沿Z轴正向拉伸700
        step11 = Cone(
            Vec3(evap_main_end.x, evap_main_end.y, evap_main_end.z),
            Vec3(evap_main_end.x, evap_main_end.y, evap_main_end.z + step11_extrude),
            100.0, 100.0
        ).color(0.35, 0.35, 0.35, 1)
        all_parts.append(step11)

        # ============================================================
        #  步骤12：蒸发器副管
        #  临时原点=支撑管拉伸终点(-2000,-25,1200)
        #  YOZ面圆，r=150，X±1000拉伸(总2000)
        # ============================================================
        sub_pipe_z = evap_main_end.z + step11_extrude  # 1200
        step12 = Cone(
            Vec3(evap_main_end.x - 1000.0, evap_main_end.y, sub_pipe_z),
            Vec3(evap_main_end.x + 1000.0, evap_main_end.y, sub_pipe_z),
            R_sub, R_sub
        ).color(0.4, 0.4, 0.4, 1)
        all_parts.append(step12)

        # ============================================================
        #  步骤13：蒸发器副管球帽×2
        #  球心=副管两端面圆心(-3000,-25,1200)、(-1000,-25,1200)
        #  直径=蒸发器副管直径=300 → r=150
        # ============================================================
        step13_cap1 = translate(evap_main_end.x - 1000.0, evap_main_end.y, sub_pipe_z) * scale(R_sub) * Sphere()
        step13_cap1 = step13_cap1.color(0.45, 0.65, 0.8, 1)
        step13_cap2 = translate(evap_main_end.x + 1000.0, evap_main_end.y, sub_pipe_z) * scale(R_sub) * Sphere()
        step13_cap2 = step13_cap2.color(0.45, 0.65, 0.8, 1)
        all_parts.extend([step13_cap1, step13_cap2])

        # ============================================================
        #  步骤14：冷凝器副管支撑管1
        #  临时原点=左侧冷凝器主管终点(-2000,675,500)
        #  XOY面圆，d=200(r=100)，沿+Z拉伸700 → 终点(-2000,675,1200)
        # ============================================================
        cond_main_end = Vec3(cond_cap_center.x - L_main, cond_cap_center.y, cond_cap_center.z)  # (-2000,675,500)
        step14_extrude = 700.0  # 沿Z轴正向拉伸700
        step14 = Cone(
            Vec3(cond_main_end.x, cond_main_end.y, cond_main_end.z),
            Vec3(cond_main_end.x, cond_main_end.y, cond_main_end.z + step14_extrude),
            100.0, 100.0
        ).color(0.35, 0.35, 0.35, 1)
        all_parts.append(step14)

        # ============================================================
        #  步骤15：冷凝器副管支撑管2
        #  临时原点=支撑管1终点(-2000,675,1200)
        #  矢量平移(0,0,-0.5*D_cond_sub-0.5*100)=(0,0,-200) → 圆心(-2000,675,1000)
        #  XOY面圆，r=150（d=300），沿-Z拉伸100 → 终点(-2000,675,900)
        # ============================================================
        step15_z_top = cond_main_end.z + step14_extrude         # 1200
        step15_shift = -D_cond_sub/2.0 - 50.0                    # -200
        step15_extrude = 100.0
        step15 = Cone(
            Vec3(cond_main_end.x, cond_main_end.y, step15_z_top + step15_shift),
            Vec3(cond_main_end.x, cond_main_end.y, step15_z_top + step15_shift - step15_extrude),
            150.0, 150.0
        ).color(0.35, 0.35, 0.35, 1)
        all_parts.append(step15)

        # ============================================================
        #  步骤16：主压缩机
        #  临时原点=支撑管1终点(-2000,675,1200)
        #  YOZ面圆，d=D_cond_sub+100=400 → r=200，X±500拉伸(总1000)
        # ============================================================
        step16_comp_z = step15_z_top  # 1200
        step16 = Cone(
            Vec3(cond_main_end.x - 500.0, cond_main_end.y, step16_comp_z),
            Vec3(cond_main_end.x + 500.0, cond_main_end.y, step16_comp_z),
            R_main, R_main
        ).color(0.3, 0.4, 0.55, 1)
        all_parts.append(step16)

        # ============================================================
        #  步骤17：压缩机连接管
        #  临时原点=主压缩机+X终点(-1500,675,1200)
        #  YOZ面圆，d=D_sub-200=100 → r=50，沿+X拉伸150 → 终点(-1350,675,1200)
        # ============================================================
        comp_end_x = cond_main_end.x + 500.0     # -1500
        R_conn = (D_sub - 200.0) / 2.0           # 50
        step17_extrude = 150.0
        step17 = Cone(
            Vec3(comp_end_x, cond_main_end.y, step16_comp_z),
            Vec3(comp_end_x + step17_extrude, cond_main_end.y, step16_comp_z),
            R_conn, R_conn
        ).color(0.3, 0.4, 0.55, 1)
        all_parts.append(step17)

        # ============================================================
        #  步骤18：副压缩机
        #  临时原点=连接管终点(-1350,675,1200)
        #  YOZ面圆，d=D_cond_sub+100=400 → r=200，沿+X拉伸400 → 终点(-950,675,1200)
        # ============================================================
        conn_end_x = comp_end_x + step17_extrude   # -1350
        step18 = Cone(
            Vec3(conn_end_x, cond_main_end.y, step16_comp_z),
            Vec3(conn_end_x + 400.0, cond_main_end.y, step16_comp_z),
            R_main, R_main
        ).color(0.3, 0.4, 0.55, 1)
        all_parts.append(step18)

        # ============================================================
        #  步骤19：冷凝器副管支撑管3
        #  临时原点=副压缩机轴线中点(-1150,675,1200)
        #  XOY面圆，r=100（d=200），沿-Z拉伸700 → 终点(-1150,675,500)
        # ============================================================
        sub_comp_mid_x = (conn_end_x + conn_end_x + 400.0) / 2.0  # -1150
        step19_extrude = 700.0
        step19 = Cone(
            Vec3(sub_comp_mid_x, cond_main_end.y, step16_comp_z),
            Vec3(sub_comp_mid_x, cond_main_end.y, step16_comp_z - step19_extrude),
            100.0, 100.0
        ).color(0.35, 0.35, 0.35, 1)
        all_parts.append(step19)

        # ============================================================
        #  步骤20：显示屏体
        #  临时原点=主压缩机-X拉伸端点(-2500,675,1200) + (-200,0,0) = (-2700,675,1200)
        #  YOZ面矩形，Y宽=100，Z高=D_main=400，沿-X拉伸1000
        # ============================================================
        display_origin_x = cond_main_end.x - 500.0 - 200.0  # -2000-500-200 = -2700
        display_y = cond_main_end.y                          # 675
        display_z = step16_comp_z                            # 1200
        step20_display = Box(
            Vec3(display_origin_x, display_y, display_z),
            Vec3(display_origin_x - 1000.0, display_y, display_z),
            Vec3(0, 1, 0),
            Vec3(0, 0, 1),
            100.0, D_main,
            100.0, D_main
        ).color(0.18, 0.18, 0.18, 1)

        # ============================================================
        #  步骤21a：左侧显示屏支撑
        #  临时原点=显示屏体+Z面形心(-3200,675,1400)
        #  XOY面，形心(237.5,0,0)→全局(-2962.5,675,1400)
        #  矩形X长=25，Y宽=100，沿-Z拉伸 700-0.5*D_main=500
        # ============================================================
        display_face_z = display_z + D_main/2.0              # 1400 (+Z面)
        display_face_x = (display_origin_x + display_origin_x - 1000.0) / 2.0  # -3200
        support_extrude = 700.0 - D_main/2.0                # 500
        support_offset_x = 0.25 * 1000.0 - 0.5 * 25.0        # 237.5
        support_centroid_x = display_face_x + support_offset_x  # -2962.5
        step21a = Box(
            Vec3(support_centroid_x, display_y, display_face_z),
            Vec3(support_centroid_x, display_y, display_face_z - support_extrude),
            Vec3(1, 0, 0),
            Vec3(0, 1, 0),
            25.0, 100.0,
            25.0, 100.0
        ).color(0.5, 0.5, 0.5, 1)

        #  步骤21b：右侧显示屏支撑（沿临时坐标系zoy面 X=-3200 镜像）
        # ============================================================
        mirror_display = translate(2.0 * display_face_x, 0, 0) * scale(-1, 1, 1)
        step21b = (mirror_display * step21a).color(0.5, 0.5, 0.5, 1)

        #  显示屏体、显示屏支撑整体下移 D_main*0.5
        step20_display = translate(0, 0, -D_main*0.5) * step20_display
        step21a = translate(0, 0, -D_main*0.5) * step21a
        step21b = translate(0, 0, -D_main*0.5) * step21b

        all_parts.append(step20_display)
        all_parts.append(step21a)
        all_parts.append(step21b)


        # ==================== 组合全部几何体 ====================
        result = all_parts[0]
        for part in all_parts[1:]:
            result = combine(result, part)

        self['冷水机组'] = result


if __name__ == "__main__":
    FinalGeometry = 水冷螺杆式冷水机组单机()
    place(FinalGeometry)
