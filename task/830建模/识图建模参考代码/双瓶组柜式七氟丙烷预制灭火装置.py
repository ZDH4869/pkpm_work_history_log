from pyp3d import *
import math


class 柜式七氟丙烷预制灭火装置双瓶组(Component):
    """柜式（无管网）七氟丙烷预制灭火装置（双瓶组）。

    外形按 07S207 的双瓶柜尺寸参数化，**结构上是一个完整的
    柜壳、两个并排的柜内隔间**，而不是把两个单瓶组柜拼在一起。
    每个隔间 1:1 复刻单瓶组版本
    ``单瓶组柜式七氟丙烷预制灭火装置.py`` 的储瓶、容器阀、
    电磁驱动器、侧向出口、高压软管与顶面板喷嘴布局，两隔间
    共用整柜的左/右外侧墙、背板、底板、顶板、贯通上部分隔
    横梁以及贯通中央立柱——中央立柱把柜内空间在中间物理隔开，
    每瓶独立驱动对应喷嘴。

    整柜柜壳一次性贯通构建（左外侧墙 + 背板 + 右外侧墙 +
    底板 + 顶板 + 贯通上部分隔横梁 + 贯通中央立柱），无任何
    拼接接缝。两个隔间再各自贡献：内背板、底托、上部固定
    面板 + 喷嘴、柜门、铰链、储瓶、容器阀 + 驱动器、侧向
    出口、高压软管。左右两扇柜门和各自的上部固定面板都退
    到中央立柱两侧，形成"对开双门柜"形态。

    左隔间柜门铰链在左、向左外开，右隔间柜门铰链在右、
    向右外开（单瓶组原版布局的镜像）。局部原点位于整柜左前
    下角，X 为宽、Y 为深、Z 为高。

    ``左柜门开启角度``与``右柜门开启角度``分别控制左右两扇
    门，0°为关门、90°为全开。本构件用于 BIM 外形与设备布置
    表达，不代替承压设备制造图。
    """

    def __init__(self):
        Component.__init__(self)

        self['名称'] = Attr(
            '柜式（无管网）七氟丙烷预制灭火装置（双瓶组）',
            obvious=True, readonly=True, group='标识'
        )
        self['图集号'] = Attr(
            '07S207', obvious=True, readonly=True, group='标识'
        )
        self['规格型号'] = Attr(
            'GQQ120/2.5-XW', obvious=True, group='标识'
        )
        self['灭火剂'] = Attr(
            'HFC-227ea（七氟丙烷）',
            obvious=True, readonly=True, group='标识'
        )
        self['储瓶容积'] = Attr(
            120.0, obvious=True, readonly=True, group='技术参数'
        )
        self['贮存压力'] = Attr(
            '2.5MPa（20℃）', obvious=True, readonly=True, group='技术参数'
        )
        self['最大充装量'] = Attr(
            120.0, obvious=True, readonly=True, group='技术参数'
        )

        # 整柜宽度 = 1240 = 2 × 620（07S207 单瓶柜体宽度）。
        # 整柜柜壳一次性贯通构建（无拼接接缝），宽度直接由本参数控制。
        self['柜体宽度'] = Attr(1240.0, obvious=True, group='柜体')
        # 兼容历史参数：现已不再影响几何（整柜是单一柜壳，无"两柜"概念），
        # 保留仅为不破坏可能引用它的外部代码；驱动点公式中默认按 0 处理。
        self['两柜间隙'] = Attr(0.0, obvious=False, group='柜体')
        self['柜体深度'] = Attr(490.0, obvious=True, group='柜体')
        self['柜体高度'] = Attr(1880.0, obvious=True, group='柜体')
        self['上部固定面板高度'] = Attr(330.0, obvious=True, group='柜体')
        self['板厚'] = Attr(8.0, obvious=True, group='柜体')
        self['左柜门开启角度'] = Attr(0.0, obvious=True, group='柜门')
        self['右柜门开启角度'] = Attr(0.0, obvious=True, group='柜门')
        self['左门板透明度'] = Attr(0.0, obvious=True, group='柜门')
        self['右门板透明度'] = Attr(0.0, obvious=True, group='柜门')

        # 各单元储瓶、瓶阀、管路参数与单瓶组完全一致。
        self['储瓶外径'] = Attr(400.0, obvious=True, group='储瓶')
        self['储瓶总高'] = Attr(1200.0, obvious=True, group='储瓶')
        self['储瓶底部标高'] = Attr(40.0, obvious=True, group='储瓶')
        self['管径'] = Attr(25.0, obvious=True, group='管路')
        self['喷嘴外径'] = Attr(74.0, obvious=True, group='管路')
        self['软管外径'] = Attr(28.0, obvious=True, group='管路')

        self['柜体'] = Attr(None)
        self['左柜门'] = Attr(None)
        self['右柜门'] = Attr(None)
        self['左瓶组单元'] = Attr(None)
        self['右瓶组单元'] = Attr(None)
        self['阀门管路'] = Attr(None)
        self['固定面板及喷嘴'] = Attr(None)
        self['整体'] = Attr(None, show=True)

        self.setDrivenFeaturePoint(
            '左喷嘴中心', SnapMode.GeometricCenter,
            '[定位点X]+([柜体宽度]-[两柜间隙])/4',
            '[定位点Y]',
            '[定位点Z]+[柜体高度]-[上部固定面板高度]/2'
        )
        self.setDrivenFeaturePoint(
            '右喷嘴中心', SnapMode.GeometricCenter,
            '[定位点X]+([柜体宽度]*3+[两柜间隙])/4',
            '[定位点Y]',
            '[定位点Z]+[柜体高度]-[上部固定面板高度]/2'
        )

        self.replace()

    @staticmethod
    def _圆柱(p0, p1, diameter):
        radius = max(diameter / 2.0, 0.5)
        return Cone(p0, p1, radius, radius)

    @staticmethod
    def _球(center, diameter):
        return translate(center.x, center.y, center.z) * \
               scale(diameter, diameter, diameter) * Sphere()

    @staticmethod
    def _椭球(center, diameter_x, diameter_y, diameter_z):
        return translate(center.x, center.y, center.z) * \
               scale(diameter_x, diameter_y, diameter_z) * Sphere()

    def _抱箍(self, x, y, z, bottle_d, band_h):
        outer = self._圆柱(
            Vec3(x, y, z), Vec3(x, y, z + band_h), bottle_d + 18.0
        )
        inner = self._圆柱(
            Vec3(x, y, z - 2.0),
            Vec3(x, y, z + band_h + 2.0),
            bottle_d + 3.0
        )
        return outer - inner

    @staticmethod
    def _圆截面Z(z_position, radius, center_x=0.0, center_y=0.0):
        return translate(center_x, center_y, z_position) * \
               Section(scale(radius) * Arc(2.0 * math.pi))

    @staticmethod
    def _六角柱Z(z_start, z_end, across_flats,
                 center_x=0.0, center_y=0.0):
        circumradius = across_flats / math.sqrt(3.0)
        points = []
        for index in range(6):
            angle = math.pi / 6.0 + index * math.pi / 3.0
            points.append(Vec3(
                center_x + circumradius * math.cos(angle),
                center_y + circumradius * math.sin(angle),
                z_start
            ))
        points.append(points[0])
        start_section = Section(Line(*points))
        end_z = z_end
        points_end = []
        for index in range(6):
            angle = math.pi / 6.0 + index * math.pi / 3.0
            points_end.append(Vec3(
                center_x + circumradius * math.cos(angle),
                center_y + circumradius * math.sin(angle),
                end_z
            ))
        points_end.append(points_end[0])
        end_section = Section(Line(*points_end))
        result = Loft(start_section, end_section)
        result.smooth = False
        return result

    def _储瓶(self, cx, cy, bottle_z, bottle_d, bottle_h, color):
        bottle_radius = bottle_d / 2.0
        neck_d = bottle_d * 0.22
        neck_radius = neck_d / 2.0

        bottle_sections = [
            self._圆截面Z(bottle_z, bottle_radius * 0.78, cx, cy),
            self._圆截面Z(
                bottle_z + bottle_d * 0.020,
                bottle_radius * 0.92, cx, cy
            ),
            self._圆截面Z(
                bottle_z + bottle_d * 0.045,
                bottle_radius * 0.99, cx, cy
            ),
            self._圆截面Z(
                bottle_z + bottle_d * 0.090,
                bottle_radius, cx, cy
            ),
            self._圆截面Z(
                bottle_z + bottle_h - bottle_d * 0.30,
                bottle_radius, cx, cy
            ),
            self._圆截面Z(
                bottle_z + bottle_h - bottle_d * 0.22,
                bottle_radius * 0.98, cx, cy
            ),
            self._圆截面Z(
                bottle_z + bottle_h - bottle_d * 0.15,
                bottle_radius * 0.88, cx, cy
            ),
            self._圆截面Z(
                bottle_z + bottle_h - bottle_d * 0.09,
                bottle_radius * 0.68, cx, cy
            ),
            self._圆截面Z(
                bottle_z + bottle_h - bottle_d * 0.04,
                bottle_radius * 0.42, cx, cy
            ),
            self._圆截面Z(
                bottle_z + bottle_h,
                neck_radius * 1.30, cx, cy
            )
        ]
        bottle_shell = Loft(*bottle_sections)
        bottle_shell.smooth = True
        bottle_shell = bottle_shell.color(*color)

        neck_z = bottle_z + bottle_h
        neck = self._圆柱(
            Vec3(cx, cy, neck_z - 2.0),
            Vec3(cx, cy, neck_z + 12.0),
            neck_d
        ).color(*color)
        neck_ring = self._圆柱(
            Vec3(cx, cy, neck_z + 8.0),
            Vec3(cx, cy, neck_z + 14.0),
            neck_d * 1.25
        ).color(*color)
        return combine(bottle_shell, neck, neck_ring)

    def _容器阀组件(self, cx, cy, neck_z, color, brass):
        """返回容器阀 + 电磁驱动器的全部零件列表（不合并）。

        返回扁平 Graphics 列表，便于外层 ``combine(*parts)`` 一次性
        传入，避免 pyp3d ``Combine.__init__`` 中
        ``args[i] = Combine(*args[i])`` 在多层嵌套时报
        ``please input proper "Combine(Graphics)"``。
        """
        valve_z0 = neck_z + 14.0
        valve_base_nut = self._六角柱Z(
            valve_z0 - 2.0,
            valve_z0 + 22.0,
            82.0, cx, cy
        ).color(*brass)
        valve_body_lower = self._圆柱(
            Vec3(cx, cy, valve_z0 + 20.0),
            Vec3(cx, cy, valve_z0 + 34.0),
            64.0
        ).color(*brass)
        valve_body = Loft(
            self._圆截面Z(valve_z0 + 34.0, 22.0, cx, cy),
            self._圆截面Z(valve_z0 + 44.0, 36.0, cx, cy),
            self._圆截面Z(valve_z0 + 60.0, 36.0, cx, cy),
            self._圆截面Z(valve_z0 + 72.0, 22.0, cx, cy)
        )
        valve_body.smooth = True
        valve_body = valve_body.color(*brass)
        valve_upper_nut = self._六角柱Z(
            valve_z0 + 68.0,
            valve_z0 + 92.0,
            60.0, cx, cy
        ).color(*brass)

        actuator_z0 = valve_z0 + 92.0
        actuator_lower_flange = self._圆柱(
            Vec3(cx, cy, actuator_z0),
            Vec3(cx, cy, actuator_z0 + 8.0),
            78.0
        ).color(0.62, 0.65, 0.67, 1.0)
        actuator_body = self._圆柱(
            Vec3(cx, cy, actuator_z0 + 8.0),
            Vec3(cx, cy, actuator_z0 + 96.0),
            50.0
        ).color(0.78, 0.80, 0.82, 1.0)
        actuator_upper_flange = self._圆柱(
            Vec3(cx, cy, actuator_z0 + 94.0),
            Vec3(cx, cy, actuator_z0 + 108.0),
            62.0
        ).color(0.62, 0.65, 0.67, 1.0)
        button_stem = self._圆柱(
            Vec3(cx, cy, actuator_z0 + 106.0),
            Vec3(cx, cy, actuator_z0 + 122.0),
            14.0
        ).color(0.62, 0.65, 0.67, 1.0)
        manual_button = self._圆柱(
            Vec3(cx, cy, actuator_z0 + 118.0),
            Vec3(cx, cy, actuator_z0 + 144.0),
            22.0
        ).color(*color)

        return [
            valve_base_nut, valve_body_lower,
            valve_body, valve_upper_nut,
            actuator_lower_flange, actuator_body,
            actuator_upper_flange, button_stem,
            manual_button
        ]

    def _构建隔间(self, start_x, mirror_door, unit_width, depth, height,
                 wall, top_panel_h, door_h, divider_z, door_angle_deg,
                 door_opacity, bottle_d, bottle_h, bottle_z, pipe_d,
                 nozzle_d, hose_d, cabinet_color, inner_color, dark_gray,
                 steel, brass, red,
                 door_left_edge=None, door_right_edge=None,
                 fixed_panel_left_edge=None,
                 fixed_panel_right_edge=None,
                 fixed_panel_back_edge=None):
        """构建一个柜内隔间（仅含内背板、底托、上部固定面板+喷嘴、
        柜门、铰链、储瓶、容器阀+驱动器、侧向出口、高压软管）。

        隔间几何在 ``x ∈ [0, unit_width]`` 的局部坐标系下构建，
        最后通过 ``translate(start_x, 0, 0)`` 平移到整柜全局位置。
        镜象柜门时 ``mirror_door=True``：铰链在隔间左缘、
        ``door_angle`` 取负向（顺时针绕 Z 轴）外开。

        不再生成任何柜壳板件（外侧墙、背板、顶板、底板、上部
        分隔横梁），这些由 ``replace`` 中按整柜一次性贯通构建。
        这样整柜是一个柜壳、两个隔间，而不是两个单瓶组拼接。

        ``door_left_edge`` / ``door_right_edge`` 控制柜门板在
        隔间局部坐标系下的左右边界（默认 ``wall`` /
        ``unit_width - wall``），``fixed_panel_left_edge`` /
        ``fixed_panel_right_edge`` 控制上部固定面板的左右边界
        （默认同上）。``fixed_panel_back_edge`` 控制上部固定
        面板在 Y 方向的贯通深度（默认 ``-wall * 0.65``，仅
        前缘 wall 厚；设为 ``depth - wall`` 时可从前缘贯通到
        柜后，消除顶部敞开区域）。

        返回字典，键包括：
            - ``hinges``：铰链柱
            - ``inner_back``：隔间内背板
            - ``floor_tray``：隔间底托
            - ``fixed_front``：隔间上部固定面板（含喷嘴组件）
            - ``door``：隔间柜门（含门板、窗、把手、加强筋）
            - ``bottle``：储瓶本体（瓶身 + 颈 + 颈环）
            - ``valve_parts``：容器阀 + 驱动器 9 个零件列表（扁平）
            - ``valve_combined``：上述 9 个零件的 Combine
            - ``side_outlet``：瓶阀侧向出口短管
            - ``hose``：高压软管（FilletPipe）
        """
        # 门板和固定面板的左右边界（允许外层覆盖以贴合相邻隔间）
        if door_left_edge is None:
            door_left_edge = wall
        if door_right_edge is None:
            door_right_edge = unit_width - wall
        if fixed_panel_left_edge is None:
            fixed_panel_left_edge = wall
        if fixed_panel_right_edge is None:
            fixed_panel_right_edge = unit_width - wall
        # 固定面板的 Y 方向贯通深度：默认仅前缘 wall 厚
        if fixed_panel_back_edge is None:
            fixed_panel_back_edge = -wall * 0.65 + wall

        # ---- 隔间内背板、底托 ----
        inner_back = translate(
            wall * 1.5, depth - wall * 2.0, wall
        ) * scale(
            unit_width - 3.0 * wall,
            wall,
            divider_z - 2.0 * wall
        ) * Cube()
        inner_back = inner_back.color(*inner_color)

        floor_tray = translate(
            wall * 2.0, wall * 2.0, wall
        ) * scale(
            unit_width - 4.0 * wall,
            depth - 4.0 * wall,
            32.0
        ) * Cube()
        floor_tray = floor_tray.color(*inner_color)

        # ---- 上部固定面板 + 喷嘴 ----
        fixed_panel_w = fixed_panel_right_edge - fixed_panel_left_edge
        fixed_panel_d = fixed_panel_back_edge - (-wall * 0.65)
        fixed_panel = translate(
            fixed_panel_left_edge, -wall * 0.65, divider_z
        ) * scale(
            fixed_panel_w,
            fixed_panel_d,
            top_panel_h - wall
        ) * Cube()
        fixed_panel = fixed_panel.color(*cabinet_color)

        # 喷嘴放在隔间水平中心（不去贴合中线，保持各隔间独立驱动）
        nozzle_x = unit_width / 2.0
        nozzle_z = height - top_panel_h * 0.50
        nozzle_socket = self._圆柱(
            Vec3(nozzle_x, -wall * 0.15, nozzle_z),
            Vec3(nozzle_x, -wall - 18.0, nozzle_z),
            nozzle_d
        ).color(*brass)
        nozzle_face = self._圆柱(
            Vec3(nozzle_x, -wall - 18.0, nozzle_z),
            Vec3(nozzle_x, -wall - 28.0, nozzle_z),
            nozzle_d * 0.72
        ).color(0.88, 0.70, 0.31, 1.0)
        nozzle_core = self._圆柱(
            Vec3(nozzle_x, -wall - 29.0, nozzle_z),
            Vec3(nozzle_x, -wall - 34.0, nozzle_z),
            nozzle_d * 0.24
        ).color(*dark_gray)
        fixed_front = combine(
            fixed_panel, nozzle_socket, nozzle_face, nozzle_core
        )

        # ---- 储瓶 ----
        bx = unit_width / 2.0
        by = depth * 0.50
        bottle = self._储瓶(
            bx, by, bottle_z, bottle_d, bottle_h, red
        )

        # ---- 容器阀 + 电磁驱动器（9 个零件）----
        valve_parts = self._容器阀组件(
            bx, by, bottle_z + bottle_h, red, brass
        )

        # ---- 侧向出口 ----
        bottle_radius = bottle_d / 2.0
        outlet_z = bottle_z + bottle_h + 14.0 + 48.0
        outlet_y = by + bottle_radius * 0.80
        side_outlet = self._圆柱(
            Vec3(bx, by, outlet_z),
            Vec3(bx, outlet_y, outlet_z),
            pipe_d * 1.20
        ).color(*brass)

        # ---- 高压软管（与单瓶组原版完全一致：后侧→上→前）----
        hose_back_y = depth - wall - 30.0
        hose = FilletPipe(
            [
                Vec3(bx, outlet_y, outlet_z),
                Vec3(bx, hose_back_y, outlet_z),
                Vec3(bx, hose_back_y, nozzle_z),
                Vec3(bx, -wall * 0.15, nozzle_z)
            ],
            [0.0, 55.0, 55.0, 35.0],
            hose_d * 0.5
        ).color(0.32, 0.34, 0.36, 1.0)

        # ---- 柜门（镜象控制铰链位置与旋转方向）----
        door_w = door_right_edge - door_left_edge
        door_angle = math.radians(
            min(max(door_angle_deg, 0.0), 115.0)
        )
        if mirror_door:
            door_angle = -door_angle  # 向左外开用负角度

        closed_door_panel = translate(
            door_left_edge, -wall * 0.72, wall
        ) * scale(door_w, wall, door_h) * Cube()
        closed_door_panel = closed_door_panel.color(
            cabinet_color[0], cabinet_color[1], cabinet_color[2],
            door_opacity
        )

        # 观察窗（与单瓶组原版相同尺寸，按门板实际宽度居中布置）
        window_w = 220.0
        window_h = 150.0
        window_cy = wall + door_h * 0.8
        window_cx = (door_left_edge + door_right_edge) / 2.0
        window_cutout = translate(
            window_cx - window_w / 2.0,
            -wall * 0.72 - 2.0,
            window_cy - window_h / 2.0
        ) * scale(window_w, wall + 4.0, window_h) * Cube()
        closed_door_panel = closed_door_panel - window_cutout

        window_frame = translate(
            window_cx - window_w / 2.0 - 5.0,
            -wall * 0.72 - 4.0,
            window_cy - window_h / 2.0 - 5.0
        ) * scale(
            window_w + 10.0, 3.0, window_h + 10.0
        ) * Cube()
        window_frame = window_frame.color(*dark_gray)

        inner_rail_1 = translate(
            door_left_edge + 24.0, -wall * 0.72 + wall,
            wall + door_h * 0.30
        ) * scale(door_w - 48.0, 20.0, 34.0) * Cube()
        inner_rail_2 = translate(
            door_left_edge + 24.0, -wall * 0.72 + wall,
            wall + door_h * 0.68
        ) * scale(door_w - 48.0, 20.0, 34.0) * Cube()
        inner_rails = combine(
            inner_rail_1, inner_rail_2
        ).color(*cabinet_color)

        # 拉手放在远离铰链的门板自由缘上，把手中心距自由缘 57mm
        # （与单瓶组原版一致：handle_x = wall + 42, handle_grip = wall + 57）
        # 镜像到左门时，把手中心同样距右缘 57mm
        if mirror_door:
            handle_cx = door_right_edge - 57.0
        else:
            handle_cx = door_left_edge + 57.0
        handle_x = handle_cx - 15.0
        handle_plate = translate(
            handle_x, -wall - 17.0,
            wall + door_h * 0.43
        ) * scale(30.0, 18.0, 118.0) * Cube()
        handle_plate = handle_plate.color(*steel)
        handle_grip = self._圆柱(
            Vec3(handle_cx, -wall - 29.0,
                 wall + door_h * 0.46),
            Vec3(handle_cx, -wall - 29.0,
                 wall + door_h * 0.50),
            12.0
        ).color(*dark_gray)

        closed_door = combine(
            closed_door_panel, inner_rails,
            handle_plate, handle_grip, window_frame
        )

        # 铰链柱
        if mirror_door:
            hinge_x = wall
        else:
            hinge_x = unit_width - wall
        hinge_y = -wall * 0.72
        door_transform = translate(hinge_x, hinge_y, 0) * \
                         rotate(Vec3(0, 0, 1), door_angle) * \
                         translate(-hinge_x, -hinge_y, 0)
        door = door_transform * closed_door

        hinge_1 = self._圆柱(
            Vec3(hinge_x, hinge_y, wall + door_h * 0.18),
            Vec3(hinge_x, hinge_y, wall + door_h * 0.30),
            20.0
        )
        hinge_2 = self._圆柱(
            Vec3(hinge_x, hinge_y, wall + door_h * 0.70),
            Vec3(hinge_x, hinge_y, wall + door_h * 0.82),
            20.0
        )
        hinges = combine(hinge_1, hinge_2).color(*steel)

        # ---- 整体平移到 start_x ----
        unit_transform = translate(start_x, 0, 0)
        valve_combined = combine(*valve_parts)

        return {
            'hinges': unit_transform * hinges,
            'inner_back': unit_transform * inner_back,
            'floor_tray': unit_transform * floor_tray,
            'fixed_front': unit_transform * fixed_front,
            'door': unit_transform * door,
            'bottle': unit_transform * bottle,
            'valve_parts': [unit_transform * p for p in valve_parts],
            'valve_combined': unit_transform * valve_combined,
            'side_outlet': unit_transform * side_outlet,
            'hose': unit_transform * hose
        }

    @export
    def replace(self):
        # 整柜参数：先按整柜一次性确定外形与柜壳，再在内部装入两个隔间
        total_width = max(self['柜体宽度'], 800.0)
        depth = max(self['柜体深度'], 320.0)
        height = max(self['柜体高度'], 1200.0)
        unit_width = total_width / 2.0  # 每个隔间占整柜宽度的一半
        wall = min(max(self['板厚'], 3.0), min(unit_width, depth) / 8.0)
        top_panel_h = min(
            max(self['上部固定面板高度'], 180.0), height * 0.32
        )
        divider_z = height - top_panel_h
        door_h = height - top_panel_h - 2.0 * wall

        left_door_angle_deg = self['左柜门开启角度']
        right_door_angle_deg = self['右柜门开启角度']
        left_door_opacity = 1.0 - min(
            max(self['左门板透明度'], 0.0), 0.90
        )
        right_door_opacity = 1.0 - min(
            max(self['右门板透明度'], 0.0), 0.90
        )

        # 各隔间独立的储瓶、瓶阀、管路尺寸（与单瓶组原版一致）
        bottle_d = min(
            max(self['储瓶外径'], 220.0),
            unit_width - 8.0 * wall,
            depth - 8.0 * wall
        )
        bottle_h = min(
            max(self['储瓶总高'], bottle_d + 420.0),
            height - top_panel_h * 0.42
        )
        bottle_z = min(
            max(self['储瓶底部标高'], 2.0 * wall),
            height - bottle_h - 250.0
        )
        pipe_d = min(max(self['管径'], 12.0), 48.0)
        nozzle_d = min(max(self['喷嘴外径'], 44.0), 110.0)
        hose_d = min(max(self['软管外径'], 18.0), 56.0)

        cabinet_color = (0.86, 0.88, 0.89, 1.0)
        inner_color = (0.66, 0.70, 0.70, 1.0)
        dark_gray = (0.18, 0.20, 0.21, 1.0)
        steel = (0.62, 0.65, 0.67, 1.0)
        brass = (0.76, 0.51, 0.15, 1.0)
        red = (0.78, 0.035, 0.025, 1.0)

        # =====================================================================
        # 第一步：构建整柜柜壳（一个柜子，不再是两个单瓶组拼接）
        #   左外侧墙 + 背板 + 右外侧墙 + 底板 + 顶板 + 贯通上部分隔横梁
        #   + 贯通中央立柱 —— 一次成形，整柜外壳完全连续无接缝
        #   中央立柱把左右两扇门在中间分开（铰链各自在两侧），
        #   视觉上呈现为"对开双门柜"的形态
        # =====================================================================
        left_wall = scale(wall, depth, height) * Cube()
        right_wall = translate(total_width - wall, 0, 0) * \
                     scale(wall, depth, height) * Cube()
        back_panel = translate(0, depth - wall, 0) * \
                     scale(total_width, wall, height) * Cube()
        bottom_panel = scale(total_width, depth, wall) * Cube()
        top_panel = translate(0, 0, height - wall) * \
                    scale(total_width, depth, wall) * Cube()
        # 贯通上部分隔横梁：从 x=wall 一直贯通到 x=total_width-wall
        upper_divider = translate(wall, 0, divider_z - 16.0) * \
                        scale(total_width - 2.0 * wall, depth, 24.0) * Cube()
        # 贯通中央立柱：把左右柜门在中间分开（16mm 宽 × 全高 × 贯通前后）
        center_column = translate(
            unit_width - wall, -wall * 0.72, 0
        ) * scale(
            2.0 * wall, depth + wall * 0.72, height
        ) * Cube()
        cabinet_shell = combine(
            left_wall, right_wall, back_panel,
            bottom_panel, top_panel,
            upper_divider, center_column
        ).color(*cabinet_color)

        # =====================================================================
        # 第二步：在整柜内部装入两个隔间
        #   中央立柱已经把柜内空间在中间分开，所以两扇门和两块
        #   固定面板都退到各自的柜内空间里（不延伸到中线）：
        #   —— 门板/固定面板右缘 = unit_width - wall（贴中央立柱左面）
        #   —— 门板/固定面板左缘 = wall（贴中央立柱右面）
        # =====================================================================
        left_compartment = self._构建隔间(
            start_x=0,
            mirror_door=True,
            unit_width=unit_width,
            depth=depth, height=height,
            wall=wall, top_panel_h=top_panel_h,
            door_h=door_h, divider_z=divider_z,
            door_angle_deg=left_door_angle_deg,
            door_opacity=left_door_opacity,
            bottle_d=bottle_d, bottle_h=bottle_h, bottle_z=bottle_z,
            pipe_d=pipe_d, nozzle_d=nozzle_d, hose_d=hose_d,
            cabinet_color=cabinet_color, inner_color=inner_color,
            dark_gray=dark_gray, steel=steel, brass=brass, red=red,
            door_left_edge=wall,
            door_right_edge=unit_width - wall,      # 贴中央立柱左面
            fixed_panel_left_edge=wall,
            fixed_panel_right_edge=unit_width - wall,  # 贴中央立柱左面
            fixed_panel_back_edge=depth - wall     # 贯通到柜后
        )
        right_compartment = self._构建隔间(
            start_x=unit_width,
            mirror_door=False,
            unit_width=unit_width,
            depth=depth, height=height,
            wall=wall, top_panel_h=top_panel_h,
            door_h=door_h, divider_z=divider_z,
            door_angle_deg=right_door_angle_deg,
            door_opacity=right_door_opacity,
            bottle_d=bottle_d, bottle_h=bottle_h, bottle_z=bottle_z,
            pipe_d=pipe_d, nozzle_d=nozzle_d, hose_d=hose_d,
            cabinet_color=cabinet_color, inner_color=inner_color,
            dark_gray=dark_gray, steel=steel, brass=brass, red=red,
            door_left_edge=wall,                     # 贴中央立柱右面
            door_right_edge=unit_width - wall,
            fixed_panel_left_edge=wall,
            fixed_panel_right_edge=unit_width - wall,
            fixed_panel_back_edge=depth - wall     # 贯通到柜后
        )

        # ---- 汇总顶层属性 ----
        # 柜体 = 整柜柜壳 + 两个隔间的内背板、底托、铰链
        cabinet = combine(
            cabinet_shell,
            left_compartment['inner_back'],
            right_compartment['inner_back'],
            left_compartment['floor_tray'],
            right_compartment['floor_tray'],
            left_compartment['hinges'],
            right_compartment['hinges']
        )
        fixed_front = combine(
            left_compartment['fixed_front'],
            right_compartment['fixed_front']
        )
        bottle_group = combine(
            left_compartment['bottle'], right_compartment['bottle']
        )
        # 阀门管路：两个隔间的容器阀 + 驱动器 + 侧出口 + 高压软管
        # 全部扁平传入 combine，避免 pyp3d 嵌套 Combine 递归解包报错
        valve_and_pipe = combine(
            *left_compartment['valve_parts'],
            *right_compartment['valve_parts'],
            left_compartment['side_outlet'],
            right_compartment['side_outlet'],
            left_compartment['hose'],
            right_compartment['hose']
        )

        self['柜体'] = cabinet
        self['左柜门'] = left_compartment['door']
        self['右柜门'] = right_compartment['door']
        self['左瓶组单元'] = left_compartment['valve_combined']
        self['右瓶组单元'] = right_compartment['valve_combined']
        self['阀门管路'] = valve_and_pipe
        self['固定面板及喷嘴'] = fixed_front
        self['整体'] = combine(
            cabinet, fixed_front,
            left_compartment['door'], right_compartment['door'],
            bottle_group, valve_and_pipe
        )


if __name__ == '__main__':
    FinalGeometry = 柜式七氟丙烷预制灭火装置双瓶组()
    place(FinalGeometry)
