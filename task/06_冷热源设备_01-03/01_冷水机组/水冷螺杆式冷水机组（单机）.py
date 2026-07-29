from pyp3d import *

class 水冷螺杆式冷水机组单机(Component):
    def __init__(self):
        Component.__init__(self)

        # ==================== 用户可修改参数 ====================
        self['设备名称'] = Attr('水冷螺杆式冷水机组（单机）', obvious=True)
        self['外形尺寸长'] = Attr(2298.0, obvious=True)
        self['外形尺寸宽'] = Attr(817.0, obvious=True)
        self['外形尺寸高'] = Attr(1463.0, obvious=True)
        self['冷凝器管径'] = Attr(80.0, obvious=True)
        self['蒸发器管径'] = Attr(80.0, obvious=True)
        # ==================== 显示文本属性（只读，用户不可修改） ====================
        self['使用电源'] = Attr('3Φ-380V-50Hz', obvious=True, readonly=True)
        self['制冷量KW'] = Attr('120.3', obvious=True, readonly=True)
        self['制冷量Kcal_h'] = Attr('103500', obvious=True, readonly=True)
        self['运行电流A'] = Attr('52.2', obvious=True, readonly=True)
        self['冷冻水量m3_h'] = Attr('20.8', obvious=True, readonly=True)
        self['冷却水量m3_h'] = Attr('26', obvious=True, readonly=True)
        self['压缩机型式'] = Attr('半封闭螺杆式', obvious=True, readonly=True)
        self['压缩机数量PCS'] = Attr('1', obvious=True, readonly=True)
        self['压缩机启动方式'] = Attr('Y-△', obvious=True, readonly=True)
        self['压缩机容量控制%'] = Attr('0,33,66,100 或 0,25,50,75,100', obvious=True, readonly=True)
        self['压缩机功率KW'] = Attr('30', obvious=True, readonly=True)
        self['冷冻油种类'] = Attr('HBR-A01', obvious=True, readonly=True)
        self['冷冻油容量L'] = Attr('7', obvious=True, readonly=True)
        self['冷媒种类'] = Attr('R-22', obvious=True, readonly=True)
        self['冷媒控制方式'] = Attr('感温式外部均压膨胀阀', obvious=True, readonly=True)
        self['冷媒容量KG'] = Attr('25', obvious=True, readonly=True)
        self['蒸发器型式'] = Attr('壳管式', obvious=True, readonly=True)
        self['冷凝器型式'] = Attr('壳管式', obvious=True, readonly=True)
        self['保护装置'] = Attr('高低压开关,防冻保护,可溶栓/安全阀,过载保护装置,线圈过热保护器,温度自动保护开关等。', obvious=True, readonly=True)
        self['重量KG'] = Attr('1074', obvious=True, readonly=True)

        # ==================== 内部联动参数（驱动点公式引用，必须 obvious=True） ====================
        self['水平支撑板厚度'] = Attr(50.0, obvious=True, readonly=True)
        self['蒸发器球帽直径'] = Attr(700.0, obvious=True, readonly=True)
        self['冷凝器球帽直径'] = Attr(800.0, obvious=True, readonly=True)
        self['蒸发器竖向支撑板高度'] = Attr(714.0, obvious=True, readonly=True)
        self['冷凝器竖向支撑板高度'] = Attr(816.0, obvious=True, readonly=True)
        self['冷凝器副管直径'] = Attr(300.0, obvious=True, readonly=True)
        self['基准高度'] = Attr(500.0, obvious=True, readonly=True)
        self['Z偏移量'] = Attr(0.0, obvious=True, readonly=True)
        self['主管拉伸长度'] = Attr(899.7, obvious=True, readonly=True)

        # ==================== 特征点坐标偏移量（预计算，只读） ====================
        self['插入点Y'] = Attr(0.0, obvious=True, readonly=True)
        self['插入点Z'] = Attr(0.0, obvious=True, readonly=True)
        self['冷凝器Y'] = Attr(-194.0, obvious=True, readonly=True)
        self['蒸发器Y'] = Attr(-602.5, obvious=True, readonly=True)
        self['水管X'] = Attr(335.1, obvious=True, readonly=True)
        self['冷凝器水管Z上'] = Attr(622.4, obvious=True, readonly=True)
        self['冷凝器水管Z下'] = Attr(353.0, obvious=True, readonly=True)
        self['蒸发器水管Z上'] = Attr(601.9, obvious=True, readonly=True)
        self['蒸发器水管Z下'] = Attr(373.4, obvious=True, readonly=True)
        self['副压缩机X'] = Attr(-397.0, obvious=True, readonly=True)
        self['副压缩机Z'] = Attr(1206.3, obvious=True, readonly=True)
        self['显示屏X'] = Attr(-1520.0, obvious=True, readonly=True)
        self['显示屏Y'] = Attr(-173.6, obvious=True, readonly=True)
        self['显示屏Z'] = Attr(1463.0, obvious=True, readonly=True)

        # ==================== 输出槽位 ====================
        self['冷水机组'] = Attr(None, show=True)

        # ==================== 驱动点（特征点）定义 ====================
        # 插入点 = 水平支撑板 Y_max 角点
        self.setDrivenFeaturePoint(
            '插入点',
            SnapMode.GeometricCenter,
            '[定位点X]+0',
            '[定位点Y]+[插入点Y]',
            '[定位点Z]+[插入点Z]'
        )
        # 冷凝器上水管终点
        self.setDrivenFeaturePoint(
            '冷凝器上水管终点',
            SnapMode.GeometricCenter,
            '[定位点X]+[水管X]',
            '[定位点Y]+[冷凝器Y]',
            '[定位点Z]+[冷凝器水管Z上]'
        )
        # 冷凝器下水管终点
        self.setDrivenFeaturePoint(
            '冷凝器下水管终点',
            SnapMode.GeometricCenter,
            '[定位点X]+[水管X]',
            '[定位点Y]+[冷凝器Y]',
            '[定位点Z]+[冷凝器水管Z下]'
        )
        # 蒸发器上水管终点
        self.setDrivenFeaturePoint(
            '蒸发器上水管终点',
            SnapMode.GeometricCenter,
            '[定位点X]+[水管X]',
            '[定位点Y]+[蒸发器Y]',
            '[定位点Z]+[蒸发器水管Z上]'
        )
        # 蒸发器下水管终点
        self.setDrivenFeaturePoint(
            '蒸发器下水管终点',
            SnapMode.GeometricCenter,
            '[定位点X]+[水管X]',
            '[定位点Y]+[蒸发器Y]',
            '[定位点Z]+[蒸发器水管Z下]'
        )
        # 副压缩机终点
        self.setDrivenFeaturePoint(
            '副压缩机终点',
            SnapMode.GeometricCenter,
            '[定位点X]+[副压缩机X]',
            '[定位点Y]+[冷凝器Y]',
            '[定位点Z]+[副压缩机Z]'
        )
        # 显示屏特征点
        self.setDrivenFeaturePoint(
            '显示屏特征点',
            SnapMode.GeometricCenter,
            '[定位点X]+[显示屏X]',
            '[定位点Y]+[显示屏Y]',
            '[定位点Z]+[显示屏Z]'
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
        sx = 外形尺寸长_val / 4800.0
        sy = 外形尺寸宽_val / 2000.0
        sz = 外形尺寸高_val / 1425.0

        # ==================== 内部基准常量（未缩放） ====================
        T = 50.0                      # 水平支撑板厚度（基准）
        D_evap_cap = 700.0            # 蒸发器球帽直径（基准）
        D_cond_cap = 800.0            # 冷凝器球帽直径（基准）
        D_sub = 300.0                 # 蒸发器副管直径（基准）
        D_cond_sub = 300.0            # 冷凝器副管直径（基准）
        D_main_base = D_cond_sub + 200.0   # 500 主压缩机直径（基准）
        BASE_CAP_Z = 500.0            # 球帽球心基准Z坐标（基准）

        # ==================== 截面方向缩放因子（用于Cone半径） ====================
        # X方向Cone（YZ截面）、Z方向Cone（XY截面）、Y方向Cone（XZ截面）
        cs_yz = (sy + sz) / 2.0
        cs_xy = (sx + sy) / 2.0
        cs_xz = (sx + sz) / 2.0

        # ==================== X方向缩放后常量 ====================
        T_x = T * sx
        L_main_base = (外形尺寸长_val - D_evap_cap - 0.5 * D_cond_cap) / 2.0
        L_main = L_main_base * sx
        ext_plate_x = T_x * 4.0                              # 水平支撑板 X拉伸 = 200*sx
        cx2 = -T_x * 2.0                                     # 竖向支撑板 X形心 = -100*sx
        D_evap_cap_x = D_evap_cap * sx                       # 蒸发器球帽 X长度 = 700*sx
        ext_sub_half = 1000.0 * sx                           # 蒸发器副管 X半长
        ext_comp_half = 500.0 * sx                           # 主压缩机 X半长
        ext_conn = 150.0 * sx                                # 连接管 X长度
        ext_sub_comp = 400.0 * sx                            # 副压缩机 X长度
        ext_display = 600.0 * sx                            # 显示屏体 X拉伸
        supp_sect_x = 25.0 * sx                              # 显示屏支撑截面X
        supp_offset_x = 0.25 * ext_display - 0.5 * supp_sect_x  # 显示屏支撑X偏移
        conn_offset_x = 700.0 * sx                           # 蒸发冷凝连接管 X偏移

        # ==================== Y方向缩放后常量 ====================
        T_y = T * sy
        delta_w = 外形尺寸宽_val - 2000.0
        L_evap = (1100.0 + 0.5 * delta_w) * sy                # 蒸发器支撑板 Y长度
        L_cond = (900.0 + 0.5 * delta_w) * sy                 # 冷凝器支撑板 Y长度
        L_total_y = L_evap + L_cond                          # 总Y长度

        # ==================== 差值补偿：使实际外形尺寸等于用户输入值 ====================
        # X方向：外形尺寸长 = 2*L_main + 0.5*D_cond_cap*sy + D_evap_cap_x
        差值_X = 外形尺寸长_val - (2.0 * L_main + 0.5 * D_cond_cap * sy + D_evap_cap * sx)
        L_main = L_main + 0.5 * 差值_X                       # 补充到左右主管中
        # Y方向：外形尺寸宽 = 水平支撑板总长 = L_evap + L_cond
        差值_Y = 外形尺寸宽_val - L_total_y
        L_total_y = L_total_y + 差值_Y                       # 水平支撑板长度 = 外形尺寸宽
        L_evap = L_evap + 0.5 * 差值_Y                       # 蒸发器竖向支撑板
        L_cond = L_cond + 0.5 * 差值_Y                       # 冷凝器竖向支撑板

        offset_cond_y = (L_evap - L_cond) / 2.0               # 冷凝器支撑板Y平移（对齐蒸发器顶部）
        offset_plate_y = -300.0 * sy                         # 水平支撑板初始化Y平移
        display_sect_y = 100.0 * sy                          # 显示屏截面Y
        display_feat_y_off = 50.0 * sy                       # 显示屏特征点Y额外偏移

        # ==================== Z方向缩放后常量 ====================
        T_z = T * sz
        BASE_CAP_Z_s = BASE_CAP_Z * sz                       # 球帽球心Z
        H_evap = 1.02 * D_evap_cap * sz                           # 蒸发器支撑板 Z高度
        H_cond = 1.02 * D_cond_cap * sz                           # 冷凝器支撑板 Z高度
        offset_evap_z = 25.0 * sz - 0.5 * H_evap               # 蒸发器支撑板Z平移（保持原形心）
        offset_cond_z = 25.0 * sz - 0.5 * H_cond               # 冷凝器支撑板Z平移（保持原形心）
        ext_step11 = 700.0 * sz                              # 蒸发器副管支撑管 Z拉伸
        ext_step14 = 700.0 * sz                              # 冷凝器副管支撑管1 Z拉伸
        ext_step15 = 100.0 * sz                              # 冷凝器副管支撑管2 Z拉伸
        ext_step19 = 700.0 * sz                              # 冷凝器副管支撑管3 Z拉伸
        step15_shift = -(D_cond_sub / 2.0 + 100.0) * sz      # 步骤15 Z偏移 = -250*sz
        D_main_z = D_main_base * sz                          # 主压缩机直径(Z方向)
        ext_display_supp = (700.0 - D_main_base / 2.0) * sz  # 显示屏支撑 Z拉伸 = 450*sz

        # ==================== Cone半径（截面方向缩放） ====================
        R_evap_cap_yz = D_evap_cap / 2.0 * sy                 # 350 * sy（随外形尺寸宽等比缩放）
        R_cond_cap_yz = D_cond_cap / 2.0 * sy                 # 400 * sy（随外形尺寸宽等比缩放）
        R_sub_yz = D_sub / 2.0 * cs_yz                       # 150 * cs_yz
        R_main_yz = D_main_base / 2.0 * cs_yz                # 250 * cs_yz
        R_evap_pipe = 蒸发器管径_val / 2.0 * cs_yz
        R_evap_outer = (蒸发器管径_val + 50.0) / 2.0 * cs_yz
        R_cond_pipe = 冷凝器管径_val / 2.0 * cs_yz
        R_cond_outer = (冷凝器管径_val + 30.0) / 2.0 * cs_yz
        R_conn_yz = (D_sub - 100.0) / 2.0 * cs_yz            # 连接管半径(YZ截面)
        R_100_xy = 100.0 * cs_xy                             # 支撑管半径(XY截面)
        R_150_xy = 150.0 * cs_xy                             # 支撑管2半径(XY截面)
        R_100_xz = 100.0 * cs_xz                             # 连接管半径(XZ截面)

        # ==================== 球体半径（3D等比缩放） ====================
        R_evap_cap_sph = D_evap_cap / 2.0                    # 200（基准）
        R_cond_cap_sph = D_cond_cap / 2.0                    # 300（基准）
        R_sub_sph = D_sub / 2.0                              # 150（基准）

        # ==================== 更新内部Attrs（供驱动点表达式引用） ====================
        self['主管拉伸长度'] = L_main
        self['蒸发器竖向支撑板高度'] = H_evap
        self['冷凝器竖向支撑板高度'] = H_cond
        self['Z偏移量'] = 0.0
        self['基准高度'] = BASE_CAP_Z_s
        self['水平支撑板厚度'] = T_z
        self['蒸发器球帽直径'] = D_evap_cap_x          # X方向尺寸，供特征点X表达式
        self['冷凝器球帽直径'] = D_cond_cap * sz        # Z方向尺寸，供特征点Z表达式
        self['冷凝器副管直径'] = D_cond_sub * sz        # Z方向尺寸，供特征点Z表达式

        # ==================== 特征点坐标偏移量（预计算，更新Attrs） ====================
        self['插入点Y'] = L_total_y - L_evap / 2.0
        self['插入点Z'] = T_z / 2.0
        self['冷凝器Y'] = -T_y / 2.0 + L_total_y / 2.0
        self['蒸发器Y'] = -T_y / 2.0
        self['水管X'] = D_evap_cap_x
        self['冷凝器水管Z上'] = BASE_CAP_Z_s + 0.5 * D_cond_cap * sy - 0.5 * 冷凝器管径_val * cs_yz
        self['冷凝器水管Z下'] = BASE_CAP_Z_s - 0.5 * D_cond_cap * sy + 0.5 * 冷凝器管径_val * cs_yz
        self['蒸发器水管Z上'] = BASE_CAP_Z_s + 0.5 * D_evap_cap * sy - 0.5 * 蒸发器管径_val * cs_yz
        self['蒸发器水管Z下'] = BASE_CAP_Z_s - 0.5 * D_evap_cap * sy + 0.5 * 蒸发器管径_val * cs_yz
        self['副压缩机X'] = -L_main + 1050.0 * sx
        self['副压缩机Z'] = BASE_CAP_Z_s + 700.0 * sz
        self['显示屏X'] = -3175.0 * sx
        self['显示屏Y'] = self['冷凝器Y'] + display_feat_y_off
        self['显示屏Z'] = BASE_CAP_Z_s + 800.0 * sz + 0.5 * D_cond_sub * sz

        # ==================== 关键坐标点（球帽球心） ====================
        evap_cap_center = Vec3(0, -T_y / 2.0, BASE_CAP_Z_s)
        cond_cap_center = Vec3(0, evap_cap_center.y + L_evap / 2.0 + L_cond / 2.0, BASE_CAP_Z_s)

        # ==================== 支撑板定位（按约束公式） ====================
        evap_support_Z = T_z + 0.5 * H_evap
        cond_support_Z = T_z + 0.5 * H_cond
        evap_support_Y = -L_evap / 2.0
        cond_support_Y = L_cond / 2.0

        # ==================== 构建几何部件 ====================
        all_parts = []

        # ---- 步骤1：水平支撑板 ----
        # 截面形心 (0, 0, T_z/2)，沿X轴负向拉伸 ext_plate_x
        step1_plate = Box(
            Vec3(0, 0, T_z / 2.0),
            Vec3(-ext_plate_x, 0, T_z / 2.0),
            Vec3(0, 1, 0),
            Vec3(0, 0, 1),
            L_total_y, T_z,
            L_total_y, T_z
        )

        # ---- 步骤2：冷凝器竖向支撑板 ----
        step2_cond_support = Box(
            Vec3(cx2 - T_x / 2.0, cond_support_Y, cond_support_Z),
            Vec3(cx2 + T_x / 2.0, cond_support_Y, cond_support_Z),
            Vec3(0, 1, 0),
            Vec3(0, 0, 1),
            L_cond, H_cond,
            L_cond, H_cond
        )

        # ---- 步骤3：蒸发器竖向支撑板 ----
        step3_evap_support = Box(
            Vec3(cx2 - T_x / 2.0, evap_support_Y, evap_support_Z),
            Vec3(cx2 + T_x / 2.0, evap_support_Y, evap_support_Z),
            Vec3(0, 1, 0),
            Vec3(0, 0, 1),
            L_evap, H_evap,
            L_evap, H_evap
        )

        # ---- 初始化平移校正（镜像前执行） ----
        # 蒸发器竖向支撑板: 矢量平移 (0, 0, offset_evap_z)
        step3_evap_support = translate(0, 0, offset_evap_z) * step3_evap_support
        # 冷凝器竖向支撑板: 矢量平移 (0, offset_cond_y, offset_cond_z)
        step2_cond_support = translate(0, offset_cond_y, offset_cond_z) * step2_cond_support
        # 水平支撑板: Y-min 对齐蒸发器竖向支撑板 Y-min = -L_evap/2
        step1_plate = translate(0, -L_evap / 2.0, 0) * step1_plate

        all_parts.append(step1_plate)
        all_parts.append(step2_cond_support)
        all_parts.append(step3_evap_support)

        # ---- 步骤4：蒸发器球帽（3D等比缩放） ----
        step4_evap_cap = translate(evap_cap_center.x, evap_cap_center.y, evap_cap_center.z) * scale(
            R_evap_cap_sph * sy
        ) * Sphere()
        all_parts.append(step4_evap_cap)

        # ---- 步骤5a：蒸发器上水管 ----
        evap_pipe_z_top = evap_cap_center.z + 0.5 * D_evap_cap * sy - 0.5 * 蒸发器管径_val * cs_yz
        step5a = Cone(
            Vec3(evap_cap_center.x, evap_cap_center.y, evap_pipe_z_top),
            Vec3(evap_cap_center.x + D_evap_cap_x, evap_cap_center.y, evap_pipe_z_top),
            R_evap_pipe, R_evap_pipe
        )
        all_parts.append(step5a)

        # ---- 步骤5b：蒸发器水管上外环 ----
        step5b = Cone(
            Vec3(evap_cap_center.x + D_evap_cap_x, evap_cap_center.y, evap_pipe_z_top),
            Vec3(evap_cap_center.x + D_evap_cap_x - T_x, evap_cap_center.y, evap_pipe_z_top),
            R_evap_outer, R_evap_outer
        )
        all_parts.append(step5b)

        # ---- 步骤5c：蒸发器下水管+下外环（以球帽球心Z为镜像面） ----
        mirror_z_base = translate(0, 0, BASE_CAP_Z_s * 2.0) * scale(1, 1, -1)
        step5c_lower_pipe = (mirror_z_base * step5a)
        step5c_lower_ring = (mirror_z_base * step5b)
        all_parts.append(step5c_lower_pipe)
        all_parts.append(step5c_lower_ring)

        # ---- 步骤6：冷凝器球帽（3D等比缩放） ----
        step6_cond_cap = translate(cond_cap_center.x, cond_cap_center.y, cond_cap_center.z) * scale(
            R_cond_cap_sph * sy
        ) * Sphere()
        all_parts.append(step6_cond_cap)

        # ---- 步骤7a：冷凝器上水管 ----
        cond_pipe_z_top = cond_cap_center.z + 0.5 * D_cond_cap * sy - 0.5 * 冷凝器管径_val * cs_yz
        step7a = Cone(
            Vec3(cond_cap_center.x, cond_cap_center.y, cond_pipe_z_top),
            Vec3(cond_cap_center.x + D_evap_cap_x, cond_cap_center.y, cond_pipe_z_top),
            R_cond_pipe, R_cond_pipe
        )
        all_parts.append(step7a)

        # ---- 步骤7b：冷凝器水管上外环 ----
        step7b = Cone(
            Vec3(cond_cap_center.x + D_evap_cap_x, cond_cap_center.y, cond_pipe_z_top),
            Vec3(cond_cap_center.x + D_evap_cap_x - T_x, cond_cap_center.y, cond_pipe_z_top),
            R_cond_outer, R_cond_outer
        )
        all_parts.append(step7b)

        # ---- 步骤7c：冷凝器下水管+下外环 ----
        step7c_lower_pipe = (mirror_z_base * step7a)
        step7c_lower_ring = (mirror_z_base * step7b)
        all_parts.append(step7c_lower_pipe)
        all_parts.append(step7c_lower_ring)

        # ---- 步骤8：左侧蒸发器主管 ----
        step8_evap_main = Cone(
            Vec3(evap_cap_center.x, evap_cap_center.y, evap_cap_center.z),
            Vec3(evap_cap_center.x - L_main, evap_cap_center.y, evap_cap_center.z),
            R_evap_cap_yz, R_evap_cap_yz
        )
        all_parts.append(step8_evap_main)

        # ---- 步骤9：左侧冷凝器主管 ----
        step9_cond_main = Cone(
            Vec3(cond_cap_center.x, cond_cap_center.y, cond_cap_center.z),
            Vec3(cond_cap_center.x - L_main, cond_cap_center.y, cond_cap_center.z),
            R_cond_cap_yz, R_cond_cap_yz
        )
        all_parts.append(step9_cond_main)

        # ---- 步骤10：右侧部件群镜像（镜像面X = -L_main） ----
        mirror_x = translate(-L_main * 2.0, 0, 0) * scale(-1, 1, 1)
        step10_right_plate = (mirror_x * step1_plate)
        step10_right_cond_support = (mirror_x * step2_cond_support)
        step10_right_evap_support = (mirror_x * step3_evap_support)
        step10_right_evap_cap = (mirror_x * step4_evap_cap)
        step10_right_cond_cap = (mirror_x * step6_cond_cap)
        step10_right_evap_main = (mirror_x * step8_evap_main)
        step10_right_cond_main = (mirror_x * step9_cond_main)
        all_parts.extend([
            step10_right_plate,
            step10_right_cond_support,
            step10_right_evap_support,
            step10_right_evap_cap,
            step10_right_cond_cap,
            step10_right_evap_main,
            step10_right_cond_main,
        ])

        # ---- 步骤11：蒸发器副管支撑管 ----
        evap_main_end = Vec3(evap_cap_center.x - L_main, evap_cap_center.y, evap_cap_center.z)
        step11 = Cone(
            Vec3(evap_main_end.x, evap_main_end.y, evap_main_end.z),
            Vec3(evap_main_end.x, evap_main_end.y, evap_main_end.z + ext_step11),
            R_100_xy, R_100_xy
        )
        all_parts.append(step11)

        # ---- 步骤12：蒸发器副管 ----
        sub_pipe_z = evap_main_end.z + ext_step11
        step12 = Cone(
            Vec3(evap_main_end.x - ext_sub_half, evap_main_end.y, sub_pipe_z),
            Vec3(evap_main_end.x + ext_sub_half, evap_main_end.y, sub_pipe_z),
            R_sub_yz, R_sub_yz
        )
        all_parts.append(step12)

        # ---- 步骤13：蒸发器副管球帽×2（直径固定等于副管直径） ----
        step13_cap1 = translate(evap_main_end.x - ext_sub_half, evap_main_end.y, sub_pipe_z) * scale(
            R_sub_yz
        ) * Sphere()
        step13_cap2 = translate(evap_main_end.x + ext_sub_half, evap_main_end.y, sub_pipe_z) * scale(
            R_sub_yz
        ) * Sphere()
        all_parts.extend([step13_cap1, step13_cap2])

        # ---- 步骤14：冷凝器副管支撑管1 ----
        cond_main_end = Vec3(cond_cap_center.x - L_main, cond_cap_center.y, cond_cap_center.z)
        step14 = Cone(
            Vec3(cond_main_end.x, cond_main_end.y, cond_main_end.z),
            Vec3(cond_main_end.x, cond_main_end.y, cond_main_end.z + ext_step14),
            R_100_xy, R_100_xy
        )
        all_parts.append(step14)

        # ---- 步骤15：冷凝器副管支撑管2 ----
        step15_z_top = cond_main_end.z + ext_step14
        step15 = Cone(
            Vec3(cond_main_end.x, cond_main_end.y, step15_z_top + step15_shift),
            Vec3(cond_main_end.x, cond_main_end.y, step15_z_top + step15_shift - ext_step15),
            R_150_xy, R_150_xy
        )
        all_parts.append(step15)

        # ---- 步骤16：主压缩机 ----
        step16_comp_z = step15_z_top
        step16 = Cone(
            Vec3(cond_main_end.x - ext_comp_half, cond_main_end.y, step16_comp_z),
            Vec3(cond_main_end.x + ext_comp_half, cond_main_end.y, step16_comp_z),
            R_main_yz, R_main_yz
        )
        all_parts.append(step16)

        # ---- 步骤17：压缩机连接管 ----
        comp_end_x = cond_main_end.x + ext_comp_half
        step17 = Cone(
            Vec3(comp_end_x, cond_main_end.y, step16_comp_z),
            Vec3(comp_end_x + ext_conn, cond_main_end.y, step16_comp_z),
            R_conn_yz, R_conn_yz
        )
        all_parts.append(step17)

        # ---- 步骤18：副压缩机 ----
        conn_end_x = comp_end_x + ext_conn
        step18 = Cone(
            Vec3(conn_end_x, cond_main_end.y, step16_comp_z),
            Vec3(conn_end_x + ext_sub_comp, cond_main_end.y, step16_comp_z),
            R_main_yz, R_main_yz
        )
        all_parts.append(step18)

        # ---- 步骤19：冷凝器副管支撑管3 ----
        sub_comp_mid_x = (conn_end_x + conn_end_x + ext_sub_comp) / 2.0
        step19 = Cone(
            Vec3(sub_comp_mid_x, cond_main_end.y, step16_comp_z),
            Vec3(sub_comp_mid_x, cond_main_end.y, step16_comp_z - ext_step19),
            R_100_xy, R_100_xy
        )
        all_parts.append(step19)

        # ---- 步骤19b：蒸发冷凝连接管 ----
        main_comp_start_x = cond_main_end.x - ext_comp_half
        conn_pipe = Cone(
            Vec3(main_comp_start_x + conn_offset_x, cond_main_end.y, step16_comp_z),
            Vec3(main_comp_start_x + conn_offset_x, cond_main_end.y - L_total_y / 2.0, step16_comp_z),
            R_100_xz, R_100_xz
        )
        all_parts.append(conn_pipe)

        # ---- 步骤20：显示屏体 ----
        display_origin_x = cond_main_end.x - ext_comp_half - T_x * 4.0
        display_y = cond_main_end.y
        display_z = step16_comp_z - D_main_z * 0.5
        step20_display = Box(
            Vec3(display_origin_x, display_y, display_z),
            Vec3(display_origin_x - ext_display, display_y, display_z),
            Vec3(0, 1, 0),
            Vec3(0, 0, 1),
            display_sect_y, D_main_z,
            display_sect_y, D_main_z
        )

        # ---- 步骤21a：左侧显示屏支撑 ----
        display_face_z = display_z
        display_face_x = (display_origin_x + display_origin_x - ext_display) / 2.0
        support_centroid_x = display_face_x + supp_offset_x
        step21a = Box(
            Vec3(support_centroid_x, display_y, display_face_z),
            Vec3(support_centroid_x, display_y, display_face_z - ext_display_supp),
            Vec3(1, 0, 0),
            Vec3(0, 1, 0),
            supp_sect_x, display_sect_y,
            supp_sect_x, display_sect_y
        )

        # ---- 步骤21b：右侧显示屏支撑 ----
        mirror_display = translate(2.0 * display_face_x, 0, 0) * scale(-1, 1, 1)
        step21b = (mirror_display * step21a)

        all_parts.append(step20_display)
        all_parts.append(step21a)
        all_parts.append(step21b)

        # ==================== 组合全部几何体 ====================
        result = all_parts[0]
        for part in all_parts[1:]:
            result = combine(result, part)

        # ==================== 平移模型：使原'插入点'特征点对齐到定位点原点 ====================
        offset_insert_y = self['插入点Y']
        offset_insert_z = self['插入点Z']
        result = translate(0, -offset_insert_y, -offset_insert_z) * result

        # 更新全体Y/Z偏移Attrs（特征点偏移量同步平移）
        self['插入点Y'] = 0.0
        self['插入点Z'] = 0.0
        self['冷凝器Y'] -= offset_insert_y
        self['蒸发器Y'] -= offset_insert_y
        self['冷凝器水管Z上'] -= offset_insert_z
        self['冷凝器水管Z下'] -= offset_insert_z
        self['蒸发器水管Z上'] -= offset_insert_z
        self['蒸发器水管Z下'] -= offset_insert_z
        self['副压缩机Z'] -= offset_insert_z
        self['显示屏Y'] -= offset_insert_y
        self['显示屏Z'] -= offset_insert_z

        self['冷水机组'] = result


if __name__ == "__main__":
    FinalGeometry = 水冷螺杆式冷水机组单机()
    place(FinalGeometry)