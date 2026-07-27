from pyp3d import *

class 水冷螺杆式冷水机组单机(Component):
    def __init__(self):
        Component.__init__(self)

        # ==================== 用户可修改参数 ====================
        self['设备名称'] = Attr('水冷螺杆式冷水机组（单机）', obvious=True)
        self['型号'] = Attr('SPS-120W', obvious=True)
        self['外形尺寸长'] = Attr(4700.0, obvious=True)
        self['外形尺寸宽'] = Attr(1400.0, obvious=True)
        self['外形尺寸高'] = Attr(1425.0, obvious=True)
        self['冷凝器管径'] = Attr(75.0, obvious=True)
        self['蒸发器管径'] = Attr(50.0, obvious=True)

        # ==================== 显示文本属性（只读，用户不可修改） ====================
        self['型号'] = Attr('SPS-120W', obvious=True, readonly=True)
        self['使用电源'] = Attr('3Φ-380V-50Hz', obvious=True, readonly=True)
        self['制冷量_kW'] = Attr('120.3', obvious=True, readonly=True)
        self['制冷量_kcal'] = Attr('103500', obvious=True, readonly=True)
        self['运行电流'] = Attr('52.2', obvious=True, readonly=True)
        self['冷冻水量'] = Attr('20.8', obvious=True, readonly=True)
        self['冷却水量'] = Attr('26', obvious=True, readonly=True)
        self['压缩机型式'] = Attr('半封闭螺杆式', obvious=True, readonly=True)
        self['压缩机数量'] = Attr('1', obvious=True, readonly=True)
        self['压缩机启动方式'] = Attr('Y-△', obvious=True, readonly=True)
        self['压缩机容量控制'] = Attr('0,33,66,100 或 0,25,50,75,100', obvious=True, readonly=True)
        self['压缩机功率'] = Attr('30', obvious=True, readonly=True)
        self['冷冻油种类'] = Attr('HBR-A01', obvious=True, readonly=True)
        self['冷冻油容量'] = Attr('7', obvious=True, readonly=True)
        self['冷媒种类'] = Attr('R-22', obvious=True, readonly=True)
        self['冷媒控制方式'] = Attr('感温式外部均压膨胀阀', obvious=True, readonly=True)
        self['冷媒容量'] = Attr('25', obvious=True, readonly=True)
        self['蒸发器型式'] = Attr('壳管式', obvious=True, readonly=True)
        self['冷凝器型式'] = Attr('壳管式', obvious=True, readonly=True)
        self['保护装置'] = Attr('高低压开关,防冻保护,可溶栓/安全阀,过载保护装置,线圈过热保护器,温度自动保护开关等。', obvious=True, readonly=True)
        self['重量'] = Attr('1074', obvious=True, readonly=True)

        # ==================== 内部联动参数（驱动点公式引用，必须 obvious=True） ====================
        self['水平支撑板厚度'] = Attr(50.0, obvious=True, readonly=True)
        self['蒸发器球帽直径'] = Attr(400.0, obvious=True, readonly=True)
        self['冷凝器球帽直径'] = Attr(600.0, obvious=True, readonly=True)
        self['蒸发器竖向支撑板高度'] = Attr(1000.0, obvious=True, readonly=True)
        self['冷凝器竖向支撑板高度'] = Attr(1200.0, obvious=True, readonly=True)
        self['冷凝器副管直径'] = Attr(300.0, obvious=True, readonly=True)
        self['基准高度'] = Attr(500.0, obvious=True, readonly=True)
        self['Z偏移量'] = Attr(0.0, obvious=True, readonly=True)
        self['主管拉伸长度'] = Attr(2000.0, obvious=True, readonly=True)

        # ==================== 输出槽位 ====================
        self['冷水机组'] = Attr(None, show=True)

        # ==================== 驱动点（特征点）定义 ====================
        # 插入点 = 水平支撑板 Y_max 角点
        self.setDrivenFeaturePoint(
            '插入点',
            SnapMode.GeometricCenter,
            '[定位点X]+0',
            '[定位点Y]+0.25*[外形尺寸宽]-50+800+0.5*([外形尺寸宽]-1400)',
            '[定位点Z]+25'
        )
        # 冷凝器上水管终点
        self.setDrivenFeaturePoint(
            '冷凝器上水管终点',
            SnapMode.GeometricCenter,
            '[定位点X]+[蒸发器球帽直径]',
            '[定位点Y]-[水平支撑板厚度]/2+0.5*[外形尺寸宽]',
            '[定位点Z]+[基准高度]+0.25*[冷凝器球帽直径]+[Z偏移量]'
        )
        # 冷凝器下水管终点
        self.setDrivenFeaturePoint(
            '冷凝器下水管终点',
            SnapMode.GeometricCenter,
            '[定位点X]+[蒸发器球帽直径]',
            '[定位点Y]-[水平支撑板厚度]/2+0.5*[外形尺寸宽]',
            '[定位点Z]+[基准高度]-0.25*[冷凝器球帽直径]+[Z偏移量]'
        )
        # 蒸发器上水管终点
        self.setDrivenFeaturePoint(
            '蒸发器上水管终点',
            SnapMode.GeometricCenter,
            '[定位点X]+[蒸发器球帽直径]',
            '[定位点Y]-[水平支撑板厚度]/2',
            '[定位点Z]+[基准高度]+0.25*[蒸发器球帽直径]+[Z偏移量]'
        )
        # 蒸发器下水管终点
        self.setDrivenFeaturePoint(
            '蒸发器下水管终点',
            SnapMode.GeometricCenter,
            '[定位点X]+[蒸发器球帽直径]',
            '[定位点Y]-[水平支撑板厚度]/2',
            '[定位点Z]+[基准高度]-0.25*[蒸发器球帽直径]+[Z偏移量]'
        )
        # 副压缩机终点
        self.setDrivenFeaturePoint(
            '副压缩机终点',
            SnapMode.GeometricCenter,
            '[定位点X]-975-([外形尺寸长]-4700)/2',
            '[定位点Y]-[水平支撑板厚度]/2+0.5*[外形尺寸宽]',
            '[定位点Z]+[基准高度]+700+[Z偏移量]'
        )
        # 显示屏特征点
        self.setDrivenFeaturePoint(
            '显示屏特征点',
            SnapMode.GeometricCenter,
            '[定位点X]-3575',
            '[定位点Y]-[水平支撑板厚度]/2+0.5*[外形尺寸宽]+50',
            '[定位点Z]+[基准高度]+800+0.5*[冷凝器副管直径]+[Z偏移量]'
        )

        self.replace()

    @export
    def replace(self):
        # ==================== 读取用户可编辑参数 ====================
        外形尺寸长_val = float(self['外形尺寸长'])
        外形尺寸宽_val = float(self['外形尺寸宽'])
        外形尺寸高_val = float(self['外形尺寸高'])
        蒸发器管径_val = float(self['蒸发器管径'])
        冷凝器管径_val = float(self['冷凝器管径'])

        # ==================== 比例因子 ====================
        kL = 外形尺寸长_val / 4700.0      # 外形尺寸长比例
        kW = 外形尺寸宽_val / 1400.0      # 外形尺寸宽比例
        kH = 外形尺寸高_val / 1425.0      # 外形尺寸高比例

        # ==================== 内部联动参数（等比缩放） ====================
        T = 50.0                        # 水平支撑板厚度（不参与联动）
        D_evap_cap = 400.0 * kL         # 蒸发器球帽直径 → kL
        D_cond_cap = 600.0 * kL         # 冷凝器球帽直径 → kL
        D_sub = 300.0 * kL              # 蒸发器副管直径 → kL
        D_cond_sub = 300.0 * kL         # 冷凝器副管直径 → kL
        D_main = 500.0 * kL             # 主压缩机直径 → kL
        BASE_CAP_Z = 500.0 * kH         # 球帽球心基准Z坐标 → kH

        L_main = 2000.0 * kW            # 主管拉伸长度 → kW
        L_evap = 600.0 * kL             # 蒸发器支撑板长度 → kL
        L_cond = 800.0 * kL             # 冷凝器支撑板长度 → kL

        delta_w = 外形尺寸宽_val - 1400.0
        delta_h = 外形尺寸高_val - 1425.0
        H_evap = 1000.0 * kH            # 蒸发器支撑板高度 → kH
        H_cond = 1200.0 * kH            # 冷凝器支撑板高度 → kH

        # ==================== 更新内部Attrs（供驱动点表达式引用） ====================
        self['主管拉伸长度'] = L_main
        self['蒸发器竖向支撑板高度'] = H_evap
        self['冷凝器竖向支撑板高度'] = H_cond
        self['蒸发器球帽直径'] = D_evap_cap
        self['冷凝器球帽直径'] = D_cond_cap
        self['冷凝器副管直径'] = D_cond_sub
        self['基准高度'] = BASE_CAP_Z
        self['Z偏移量'] = delta_h

        # ==================== 半径等派生值 ====================
        R_evap_cap = D_evap_cap / 2.0
        R_cond_cap = D_cond_cap / 2.0
        D_evap_pipe = 蒸发器管径_val
        D_cond_pipe = 冷凝器管径_val
        R_evap_pipe = D_evap_pipe / 2.0
        R_evap_outer = (D_evap_pipe + 50.0 * (蒸发器管径_val / 50.0)) / 2.0
        R_cond_pipe = D_cond_pipe / 2.0
        R_cond_outer = (D_cond_pipe + 30.0 * (冷凝器管径_val / 75.0)) / 2.0
        R_sub = D_sub / 2.0
        R_cond_sub = D_cond_sub / 2.0
        R_main = D_main / 2.0
        L_total_y = L_evap + L_cond

        # ==================== 关键坐标点（球帽球心，基准高度） ====================
        evap_cap_center = Vec3(0, -T / 2.0, BASE_CAP_Z)
        cond_cap_center = Vec3(0, evap_cap_center.y + L_evap / 2.0 + L_cond / 2.0, BASE_CAP_Z)

        # ==================== 支撑板定位（按约束公式） ====================
        # 水平支撑板厚度 T，截面形心Z = T/2，顶部平面Z = T
        # 约束: 蒸发器形心到水平支撑板顶部平面的Z距离 = 0.5*H_evap → evap_support_Z = T + 0.5*H_evap
        # 约束: 冷凝器形心到水平支撑板顶部平面的Z距离 = 0.5*H_cond → cond_support_Z = T + 0.5*H_cond
        evap_support_Z = T + 0.5 * H_evap
        cond_support_Z = T + 0.5 * H_cond

        # 约束: 形心位置由公式 ±0.5×各自长度 直接确定，间距自动满足
        # 蒸发器形心Y = -0.5*L_evap（沿Y轴负方向）
        # 冷凝器形心Y = +0.5*L_cond（沿Y轴正方向）
        # 间距 = 0.5*L_cond - (-0.5*L_evap) = 0.5*(L_cond+L_evap) ✓
        evap_support_Y = -L_evap / 2.0
        cond_support_Y = L_cond / 2.0

        # 支撑板X方向形心
        cx2 = -T * 2.0  # -100

        # ==================== 构建几何部件 ====================
        all_parts = []
        support_parts = []  # 支撑板类部件（不受外形尺寸高Z偏移影响）

        # ---- 步骤1：水平支撑板 ----
        # 截面形心 (0, 0, T/2)，沿X轴负向拉伸200
        step1_plate = Box(
            Vec3(0, 0, T / 2.0),
            Vec3(-T * 4.0, 0, T / 2.0),
            Vec3(0, 1, 0),
            Vec3(0, 0, 1),
            L_total_y, T,
            L_total_y, T
        ).color(0.65, 0.65, 0.65, 1)

        # ---- 步骤2：冷凝器竖向支撑板 ----
        step2_cond_support = Box(
            Vec3(cx2 - T / 2.0, cond_support_Y, cond_support_Z),
            Vec3(cx2 + T / 2.0, cond_support_Y, cond_support_Z),
            Vec3(0, 1, 0),
            Vec3(0, 0, 1),
            L_cond, H_cond,
            L_cond, H_cond
        ).color(0.6, 0.6, 0.6, 1)

        # ---- 步骤3：蒸发器竖向支撑板 ----
        step3_evap_support = Box(
            Vec3(cx2 - T / 2.0, evap_support_Y, evap_support_Z),
            Vec3(cx2 + T / 2.0, evap_support_Y, evap_support_Z),
            Vec3(0, 1, 0),
            Vec3(0, 0, 1),
            L_evap, H_evap,
            L_evap, H_evap
        ).color(0.6, 0.6, 0.6, 1)

        # ---- 初始化平移校正（镜像前执行） ----
        # 蒸发器竖向支撑板: 矢量平移 (0, 0, -475)
        step3_evap_support = translate(0, 0, -475-0.5*delta_h) * step3_evap_support
        # 冷凝器竖向支撑板: 矢量平移 (0, -100, -575)
        step2_cond_support = translate(0, -100, -575-0.5*delta_h) * step2_cond_support
        # 水平支撑板: 矢量平移 (0, -0.25*delta_w, 0.5*delta_h) ，参数联动
        step1_plate = translate(0, -300-0.25 * delta_w, 0) * step1_plate

        all_parts.append(step1_plate)
        support_parts.append(step1_plate)
        all_parts.append(step2_cond_support)
        support_parts.append(step2_cond_support)
        all_parts.append(step3_evap_support)
        support_parts.append(step3_evap_support)

        # ---- 步骤4：蒸发器球帽 ----
        step4_evap_cap = translate(evap_cap_center.x, evap_cap_center.y, evap_cap_center.z) * scale(R_evap_cap) * Sphere()
        step4_evap_cap = step4_evap_cap.color(0.45, 0.65, 0.8, 1)
        all_parts.append(step4_evap_cap)

        # ---- 步骤5a：蒸发器上水管 ----
        evap_pipe_z_top = evap_cap_center.z + D_evap_cap * 0.25
        step5a = Cone(
            Vec3(evap_cap_center.x, evap_cap_center.y, evap_pipe_z_top),
            Vec3(evap_cap_center.x + D_evap_cap, evap_cap_center.y, evap_pipe_z_top),
            R_evap_pipe, R_evap_pipe
        ).color(0.2, 0.4, 0.8, 1)
        all_parts.append(step5a)

        # ---- 步骤5b：蒸发器水管上外环 ----
        step5b = Cone(
            Vec3(evap_cap_center.x + D_evap_cap, evap_cap_center.y, evap_pipe_z_top),
            Vec3(evap_cap_center.x + D_evap_cap - T, evap_cap_center.y, evap_pipe_z_top),
            R_evap_outer, R_evap_outer
        ).color(0.2, 0.4, 0.8, 1)
        all_parts.append(step5b)

        # ---- 步骤5c：蒸发器下水管+下外环（以球帽球心Z=基准高度为镜像面） ----
        mirror_z_base = translate(0, 0, BASE_CAP_Z * 2.0) * scale(1, 1, -1)
        step5c_lower_pipe = (mirror_z_base * step5a).color(0.2, 0.4, 0.8, 1)
        step5c_lower_ring = (mirror_z_base * step5b).color(0.2, 0.4, 0.8, 1)
        all_parts.append(step5c_lower_pipe)
        all_parts.append(step5c_lower_ring)

        # ---- 步骤6：冷凝器球帽 ----
        step6_cond_cap = translate(cond_cap_center.x, cond_cap_center.y, cond_cap_center.z) * scale(R_cond_cap) * Sphere()
        step6_cond_cap = step6_cond_cap.color(0.45, 0.65, 0.8, 1)
        all_parts.append(step6_cond_cap)

        # ---- 步骤7a：冷凝器上水管 ----
        cond_pipe_z_top = cond_cap_center.z + D_cond_cap * 0.25
        step7a = Cone(
            Vec3(cond_cap_center.x, cond_cap_center.y, cond_pipe_z_top),
            Vec3(cond_cap_center.x + D_evap_cap, cond_cap_center.y, cond_pipe_z_top),
            R_cond_pipe, R_cond_pipe
        ).color(0.2, 0.4, 0.8, 1)
        all_parts.append(step7a)

        # ---- 步骤7b：冷凝器水管上外环 ----
        step7b = Cone(
            Vec3(cond_cap_center.x + D_evap_cap, cond_cap_center.y, cond_pipe_z_top),
            Vec3(cond_cap_center.x + D_evap_cap - T, cond_cap_center.y, cond_pipe_z_top),
            R_cond_outer, R_cond_outer
        ).color(0.2, 0.4, 0.8, 1)
        all_parts.append(step7b)

        # ---- 步骤7c：冷凝器下水管+下外环 ----
        step7c_lower_pipe = (mirror_z_base * step7a).color(0.2, 0.4, 0.8, 1)
        step7c_lower_ring = (mirror_z_base * step7b).color(0.2, 0.4, 0.8, 1)
        all_parts.append(step7c_lower_pipe)
        all_parts.append(step7c_lower_ring)

        # ---- 步骤8：左侧蒸发器主管 ----
        step8_evap_main = Cone(
            Vec3(evap_cap_center.x, evap_cap_center.y, evap_cap_center.z),
            Vec3(evap_cap_center.x - L_main, evap_cap_center.y, evap_cap_center.z),
            R_evap_cap, R_evap_cap
        ).color(0.55, 0.55, 0.55, 1)
        all_parts.append(step8_evap_main)

        # ---- 步骤9：左侧冷凝器主管 ----
        step9_cond_main = Cone(
            Vec3(cond_cap_center.x, cond_cap_center.y, cond_cap_center.z),
            Vec3(cond_cap_center.x - L_main, cond_cap_center.y, cond_cap_center.z),
            R_cond_cap, R_cond_cap
        ).color(0.55, 0.55, 0.55, 1)
        all_parts.append(step9_cond_main)

        # ---- 步骤10：右侧部件群镜像（镜像面X = -L_main） ----
        mirror_x = translate(-L_main * 2.0, 0, 0) * scale(-1, 1, 1)
        step10_right_plate = (mirror_x * step1_plate).color(0.65, 0.65, 0.65, 1)
        step10_right_cond_support = (mirror_x * step2_cond_support).color(0.6, 0.6, 0.6, 1)
        step10_right_evap_support = (mirror_x * step3_evap_support).color(0.6, 0.6, 0.6, 1)
        step10_right_evap_cap = (mirror_x * step4_evap_cap).color(0.45, 0.65, 0.8, 1)
        step10_right_cond_cap = (mirror_x * step6_cond_cap).color(0.45, 0.65, 0.8, 1)
        step10_right_evap_main = (mirror_x * step8_evap_main).color(0.55, 0.55, 0.55, 1)
        step10_right_cond_main = (mirror_x * step9_cond_main).color(0.55, 0.55, 0.55, 1)
        all_parts.extend([
            step10_right_plate,
            step10_right_cond_support,
            step10_right_evap_support,
            step10_right_evap_cap,
            step10_right_cond_cap,
            step10_right_evap_main,
            step10_right_cond_main,
        ])
        support_parts.extend([
            step10_right_plate,
            step10_right_cond_support,
            step10_right_evap_support,
        ])

        # ---- 步骤11：蒸发器副管支撑管 ----
        evap_main_end = Vec3(evap_cap_center.x - L_main, evap_cap_center.y, evap_cap_center.z)
        step11_extrude = 700.0 * kH
        step11_radius = 100.0 * kW
        step11 = Cone(
            Vec3(evap_main_end.x, evap_main_end.y, evap_main_end.z),
            Vec3(evap_main_end.x, evap_main_end.y, evap_main_end.z + step11_extrude),
            step11_radius, step11_radius
        ).color(0.35, 0.35, 0.35, 1)
        all_parts.append(step11)

        # ---- 步骤12：蒸发器副管 ----
        sub_pipe_z = evap_main_end.z + step11_extrude
        sub_pipe_half = 1000.0 * kW
        step12 = Cone(
            Vec3(evap_main_end.x - sub_pipe_half, evap_main_end.y, sub_pipe_z),
            Vec3(evap_main_end.x + sub_pipe_half, evap_main_end.y, sub_pipe_z),
            R_sub, R_sub
        ).color(0.4, 0.4, 0.4, 1)
        all_parts.append(step12)

        # ---- 步骤13：蒸发器副管球帽×2 ----
        step13_cap1 = translate(evap_main_end.x - sub_pipe_half, evap_main_end.y, sub_pipe_z) * scale(R_sub) * Sphere()
        step13_cap1 = step13_cap1.color(0.45, 0.65, 0.8, 1)
        step13_cap2 = translate(evap_main_end.x + sub_pipe_half, evap_main_end.y, sub_pipe_z) * scale(R_sub) * Sphere()
        step13_cap2 = step13_cap2.color(0.45, 0.65, 0.8, 1)
        all_parts.extend([step13_cap1, step13_cap2])

        # ---- 步骤14：冷凝器副管支撑管1 ----
        cond_main_end = Vec3(cond_cap_center.x - L_main, cond_cap_center.y, cond_cap_center.z)
        step14_extrude = 700.0 * kH
        step14_radius = 100.0 * kW
        step14 = Cone(
            Vec3(cond_main_end.x, cond_main_end.y, cond_main_end.z),
            Vec3(cond_main_end.x, cond_main_end.y, cond_main_end.z + step14_extrude),
            step14_radius, step14_radius
        ).color(0.35, 0.35, 0.35, 1)
        all_parts.append(step14)

        # ---- 步骤15：冷凝器副管支撑管2 ----
        step15_z_top = cond_main_end.z + step14_extrude
        step15_shift = -D_cond_sub / 2.0 - 50.0 - 50.0
        step15_extrude = 100.0 * kH
        step15_radius = 150.0 * kW
        step15 = Cone(
            Vec3(cond_main_end.x, cond_main_end.y, step15_z_top + step15_shift),
            Vec3(cond_main_end.x, cond_main_end.y, step15_z_top + step15_shift - step15_extrude),
            step15_radius, step15_radius
        ).color(0.35, 0.35, 0.35, 1)
        all_parts.append(step15)

        # ---- 步骤16：主压缩机 ----
        step16_comp_z = step15_z_top
        main_comp_half = 500.0 * kW
        step16 = Cone(
            Vec3(cond_main_end.x - main_comp_half, cond_main_end.y, step16_comp_z),
            Vec3(cond_main_end.x + main_comp_half, cond_main_end.y, step16_comp_z),
            R_main, R_main
        ).color(0.3, 0.4, 0.55, 1)
        all_parts.append(step16)

        # ---- 步骤17：压缩机连接管 ----
        comp_end_x = cond_main_end.x + main_comp_half
        R_conn = 100.0 * kW
        step17_extrude = 150.0 * kW
        step17 = Cone(
            Vec3(comp_end_x, cond_main_end.y, step16_comp_z),
            Vec3(comp_end_x + step17_extrude, cond_main_end.y, step16_comp_z),
            R_conn, R_conn
        ).color(0.3, 0.4, 0.55, 1)
        all_parts.append(step17)

        # ---- 步骤18：副压缩机 ----
        conn_end_x = comp_end_x + step17_extrude
        sub_comp_length = 400.0 * kW
        step18 = Cone(
            Vec3(conn_end_x, cond_main_end.y, step16_comp_z),
            Vec3(conn_end_x + sub_comp_length, cond_main_end.y, step16_comp_z),
            R_main, R_main
        ).color(0.3, 0.4, 0.55, 1)
        all_parts.append(step18)

        # ---- 步骤19：冷凝器副管支撑管3 ----
        sub_comp_mid_x = (conn_end_x + conn_end_x + sub_comp_length) / 2.0
        step19_extrude = 700.0 * kH
        step19_radius = 100.0 * kW
        step19 = Cone(
            Vec3(sub_comp_mid_x, cond_main_end.y, step16_comp_z),
            Vec3(sub_comp_mid_x, cond_main_end.y, step16_comp_z - step19_extrude),
            step19_radius, step19_radius
        ).color(0.35, 0.35, 0.35, 1)
        all_parts.append(step19)

        # ---- 步骤19b：蒸发冷凝连接管 ----
        main_comp_start_x = cond_main_end.x - main_comp_half
        conn_offset_x = 700.0 * kW
        conn_pipe_radius = 100.0 * kW
        conn_pipe = Cone(
            Vec3(main_comp_start_x + conn_offset_x, cond_main_end.y, step16_comp_z),
            Vec3(main_comp_start_x + conn_offset_x, cond_main_end.y - L_total_y / 2.0, step16_comp_z),
            conn_pipe_radius, conn_pipe_radius
        ).color(0.35, 0.45, 0.55, 1)
        all_parts.append(conn_pipe)

        # ---- 步骤20：显示屏体 ----
        display_origin_x = cond_main_end.x - 700.0 * kL
        display_y = cond_main_end.y
        display_z = step16_comp_z - D_main * 0.5
        step20_display = Box(
            Vec3(display_origin_x, display_y, display_z),
            Vec3(display_origin_x - 1000.0, display_y, display_z),
            Vec3(0, 1, 0),
            Vec3(0, 0, 1),
            100.0, D_main,
            100.0, D_main
        ).color(0.18, 0.18, 0.18, 1)

        # ---- 步骤21a：左侧显示屏支撑 ----
        display_face_z = display_z
        display_face_x = (display_origin_x + display_origin_x - 1000.0) / 2.0
        support_extrude = 450.0 * kH
        support_offset_x = 0.25 * 1000.0 - 0.5 * 25.0
        support_centroid_x = display_face_x + support_offset_x
        step21a = Box(
            Vec3(support_centroid_x, display_y, display_face_z),
            Vec3(support_centroid_x, display_y, display_face_z - support_extrude),
            Vec3(1, 0, 0),
            Vec3(0, 1, 0),
            25.0, 100.0,
            25.0, 100.0
        ).color(0.5, 0.5, 0.5, 1)

        # ---- 步骤21b：右侧显示屏支撑 ----
        mirror_display = translate(2.0 * display_face_x, 0, 0) * scale(-1, 1, 1)
        step21b = (mirror_display * step21a).color(0.5, 0.5, 0.5, 1)

        all_parts.append(step20_display)
        all_parts.append(step21a)
        all_parts.append(step21b)

        # ==================== 外形尺寸高偏移（非支撑板部件沿Z轴平移） ====================
        if delta_h != 0.0:
            # 建立支撑板集合用于快速判断
            support_set = set(id(p) for p in support_parts)
            for i in range(len(all_parts)):
                if id(all_parts[i]) not in support_set:
                    all_parts[i] = translate(0, 0, delta_h) * all_parts[i]

        # ==================== 组合全部几何体 ====================
        result = all_parts[0]
        for part in all_parts[1:]:
            result = combine(result, part)

        self['冷水机组'] = result


if __name__ == "__main__":
    FinalGeometry = 水冷螺杆式冷水机组单机()
    place(FinalGeometry)
