from pyp3d import *
import math


class 柜式七氟丙烷预制灭火装置(Component):
    """柜式（无管网）七氟丙烷预制灭火装置。

    外形按 07S207 的 100 L 单瓶柜尺寸参数化，内部瓶组仿照
    全氟己酮瓶组的圆肩瓶身 + 容器阀 + 电磁驱动装置 + 压力表 +
    高压软管布局。局部原点位于柜体左前下角，X 为宽、Y 为深、
    Z 为高；柜门铰链位于右侧。

    ``柜门开启角度``设为 0°时为关门状态，设为 90°时为开门状态。
    本构件用于 BIM 外形与设备布置表达，不代替承压设备制造图。
    """

    def __init__(self):
        Component.__init__(self)

        self['名称'] = Attr(
            '柜式（无管网）七氟丙烷预制灭火装置（单瓶组）',
            obvious=True, readonly=True, group='标识'
        )
        self['图集号'] = Attr(
            '07S207', obvious=True, readonly=True, group='标识'
        )
        self['规格型号'] = Attr(
            'GQQ100/2.5-XW', obvious=True, group='标识'
        )
        self['灭火剂'] = Attr(
            'HFC-227ea（七氟丙烷）',
            obvious=True, readonly=True, group='标识'
        )
        self['储瓶容积'] = Attr(
            100.0, obvious=True, readonly=True, group='技术参数'
        )
        self['贮存压力'] = Attr(
            '2.5MPa（20℃）', obvious=True, readonly=True, group='技术参数'
        )
        self['最大充装量'] = Attr(
            100.0, obvious=True, readonly=True, group='技术参数'
        )

        self['柜体宽度'] = Attr(620.0, obvious=True, group='柜体')
        self['柜体深度'] = Attr(490.0, obvious=True, group='柜体')
        self['柜体高度'] = Attr(1880.0, obvious=True, group='柜体')
        self['上部固定面板高度'] = Attr(330.0, obvious=True, group='柜体')
        self['板厚'] = Attr(8.0, obvious=True, group='柜体')
        self['柜门开启角度'] = Attr(90.0, obvious=True, group='柜门')
        self['门板透明度'] = Attr(0.0, obvious=True, group='柜门')

        self['储瓶外径'] = Attr(400.0, obvious=True, group='储瓶')
        self['储瓶总高'] = Attr(1200.0, obvious=True, group='储瓶')
        self['储瓶底部标高'] = Attr(40.0, obvious=True, group='储瓶')
        self['管径'] = Attr(25.0, obvious=True, group='管路')
        self['喷嘴外径'] = Attr(74.0, obvious=True, group='管路')
        self['软管外径'] = Attr(28.0, obvious=True, group='管路')

        self['柜体'] = Attr(None)
        self['柜门'] = Attr(None)
        self['储瓶组件'] = Attr(None)
        self['阀门管路'] = Attr(None)
        self['固定面板及喷嘴'] = Attr(None)
        self['整体'] = Attr(None, show=True)

        self.setDrivenFeaturePoint(
            '正面喷嘴中心', SnapMode.GeometricCenter,
            '[定位点X]+[柜体宽度]/2',
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

    def _吊耳(self, x, y, z):
        outer = self._圆柱(
            Vec3(x, y - 18.0, z), Vec3(x, y + 18.0, z), 62.0
        )
        inner = self._圆柱(
            Vec3(x, y - 21.0, z), Vec3(x, y + 21.0, z), 32.0
        )
        ring = outer - inner
        stem = translate(x - 10.0, y - 17.0, z - 56.0) * \
               scale(20.0, 34.0, 48.0) * Cube()
        return ring + stem

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

    @export
    def replace(self):
        width = max(self['柜体宽度'], 360.0)
        depth = max(self['柜体深度'], 320.0)
        height = max(self['柜体高度'], 1200.0)
        wall = min(max(self['板厚'], 3.0), min(width, depth) / 8.0)
        top_panel_h = min(
            max(self['上部固定面板高度'], 180.0), height * 0.32
        )
        door_h = height - top_panel_h - 2.0 * wall
        door_angle = math.radians(
            min(max(self['柜门开启角度'], 0.0), 115.0)
        )
        door_opacity = 1.0 - min(max(self['门板透明度'], 0.0), 0.90)

        bottle_d = min(
            max(self['储瓶外径'], 220.0),
            width - 8.0 * wall,
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

        # 柜体外壳：左右侧板、背板、底板、顶板和开口分隔横梁。
        left_side = scale(wall, depth, height) * Cube()
        right_side = translate(width - wall, 0, 0) * \
                     scale(wall, depth, height) * Cube()
        back = translate(0, depth - wall, 0) * \
               scale(width, wall, height) * Cube()
        bottom = scale(width, depth, wall) * Cube()
        top = translate(0, 0, height - wall) * \
              scale(width, depth, wall) * Cube()
        divider_z = height - top_panel_h
        divider = translate(wall, 0, divider_z - 16.0) * \
                  scale(width - 2.0 * wall, depth, 24.0) * Cube()
        cabinet_shell = combine(
            left_side, right_side, back, bottom, top, divider
        ).color(*cabinet_color)

        inner_back = translate(
            wall * 1.5, depth - wall * 2.0, wall
        ) * scale(
            width - 3.0 * wall,
            wall,
            divider_z - 2.0 * wall
        ) * Cube()
        inner_back = inner_back.color(*inner_color)

        floor_tray = translate(
            wall * 2.0, wall * 2.0, wall
        ) * scale(
            width - 4.0 * wall,
            depth - 4.0 * wall,
            32.0
        ) * Cube()
        floor_tray = floor_tray.color(*inner_color)

        # 上部为固定面板，喷嘴直接朝柜体正面喷放。
        fixed_panel = translate(
            wall, -wall * 0.65, divider_z
        ) * scale(
            width - 2.0 * wall,
            wall,
            top_panel_h - wall
        ) * Cube()
        fixed_panel = fixed_panel.color(*cabinet_color)

        nozzle_z = height - top_panel_h * 0.50
        nozzle_socket = self._圆柱(
            Vec3(width / 2.0, -wall * 0.15, nozzle_z),
            Vec3(width / 2.0, -wall - 18.0, nozzle_z),
            nozzle_d
        ).color(*brass)
        nozzle_face = self._圆柱(
            Vec3(width / 2.0, -wall - 18.0, nozzle_z),
            Vec3(width / 2.0, -wall - 28.0, nozzle_z),
            nozzle_d * 0.72
        ).color(0.88, 0.70, 0.31, 1.0)
        nozzle_core = self._圆柱(
            Vec3(width / 2.0, -wall - 29.0, nozzle_z),
            Vec3(width / 2.0, -wall - 34.0, nozzle_z),
            nozzle_d * 0.24
        ).color(*dark_gray)
        fixed_front = combine(
            fixed_panel, nozzle_socket, nozzle_face, nozzle_core
        )

        # 下柜门：右侧铰接，整扇门连同内加强筋和拉手一起旋转。
        closed_door_panel = translate(
            wall, -wall * 0.72, wall
        ) * scale(
            width - 2.0 * wall, wall, door_h
        ) * Cube()
        closed_door_panel = closed_door_panel.color(
            cabinet_color[0], cabinet_color[1], cabinet_color[2],
            door_opacity
        )

        # 观察窗：在柜门上部开矩形观察窗，便于查看瓶内压力与液位。
        window_w = 220.0
        window_h = 150.0
        window_z = wall + door_h * 0.8
        window_cx = width / 2.0
        window_cutout = translate(
            window_cx - window_w / 2.0,
            -wall * 0.72 - 2.0,
            window_z - window_h / 2.0
        ) * scale(
            window_w, wall + 4.0, window_h
        ) * Cube()
        closed_door_panel = closed_door_panel - window_cutout
        frame_t = 5.0
        window_frame = translate(
            window_cx - window_w / 2.0 - frame_t,
            -wall * 0.72 - 4.0,
            window_z - window_h / 2.0 - frame_t
        ) * scale(
            window_w + 2.0 * frame_t,
            3.0,
            window_h + 2.0 * frame_t
        ) * Cube()
        window_frame = window_frame.color(*dark_gray)

        inner_rail_1 = translate(
            wall + 24.0, -wall * 0.72 + wall,
            wall + door_h * 0.30
        ) * scale(width - 2.0 * wall - 48.0, 20.0, 34.0) * Cube()
        inner_rail_2 = translate(
            wall + 24.0, -wall * 0.72 + wall,
            wall + door_h * 0.68
        ) * scale(width - 2.0 * wall - 48.0, 20.0, 34.0) * Cube()
        inner_rails = combine(inner_rail_1, inner_rail_2).color(*cabinet_color)

        handle_plate = translate(
            wall + 42.0, -wall - 17.0,
            wall + door_h * 0.43
        ) * scale(30.0, 18.0, 118.0) * Cube()
        handle_plate = handle_plate.color(*steel)
        handle_grip = self._圆柱(
            Vec3(wall + 57.0, -wall - 29.0, wall + door_h * 0.46),
            Vec3(wall + 57.0, -wall - 29.0, wall + door_h * 0.50),
            12.0
        ).color(*dark_gray)
        closed_door = combine(
            closed_door_panel, inner_rails, handle_plate, handle_grip,
            window_frame
        )

        hinge_x = width - wall
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

        # 储瓶：多截面放样形成平底、直筒和连续圆肩，仿全氟己酮瓶组设计。
        bx = width / 2.0
        by = depth * 0.50
        bottle_radius = bottle_d / 2.0
        neck_d = bottle_d * 0.22
        neck_radius = neck_d / 2.0

        bottle_sections = [
            self._圆截面Z(
                bottle_z, bottle_radius * 0.78, bx, by
            ),
            self._圆截面Z(
                bottle_z + bottle_d * 0.020,
                bottle_radius * 0.92, bx, by
            ),
            self._圆截面Z(
                bottle_z + bottle_d * 0.045,
                bottle_radius * 0.99, bx, by
            ),
            self._圆截面Z(
                bottle_z + bottle_d * 0.090,
                bottle_radius, bx, by
            ),
            self._圆截面Z(
                bottle_z + bottle_h - bottle_d * 0.30,
                bottle_radius, bx, by
            ),
            self._圆截面Z(
                bottle_z + bottle_h - bottle_d * 0.22,
                bottle_radius * 0.98, bx, by
            ),
            self._圆截面Z(
                bottle_z + bottle_h - bottle_d * 0.15,
                bottle_radius * 0.88, bx, by
            ),
            self._圆截面Z(
                bottle_z + bottle_h - bottle_d * 0.09,
                bottle_radius * 0.68, bx, by
            ),
            self._圆截面Z(
                bottle_z + bottle_h - bottle_d * 0.04,
                bottle_radius * 0.42, bx, by
            ),
            self._圆截面Z(
                bottle_z + bottle_h,
                neck_radius * 1.30, bx, by
            )
        ]
        bottle_shell = Loft(*bottle_sections)
        bottle_shell.smooth = True
        bottle_shell = bottle_shell.color(*red)

        neck_z = bottle_z + bottle_h
        neck = self._圆柱(
            Vec3(bx, by, neck_z - 2.0),
            Vec3(bx, by, neck_z + 12.0),
            neck_d
        ).color(*red)
        neck_ring = self._圆柱(
            Vec3(bx, by, neck_z + 8.0),
            Vec3(bx, by, neck_z + 14.0),
            neck_d * 1.25
        ).color(*red)

        bottle = combine(bottle_shell, neck, neck_ring)

        # 容器阀：六角压盖 + 黄铜阀体 + 上六角连接座。
        valve_z0 = neck_z + 14.0
        valve_base_nut = self._六角柱Z(
            valve_z0 - 2.0,
            valve_z0 + 22.0,
            82.0, bx, by
        ).color(*brass)
        valve_body_lower = self._圆柱(
            Vec3(bx, by, valve_z0 + 20.0),
            Vec3(bx, by, valve_z0 + 34.0),
            64.0
        ).color(*brass)
        valve_body = Loft(
            self._圆截面Z(valve_z0 + 34.0, 22.0, bx, by),
            self._圆截面Z(valve_z0 + 44.0, 36.0, bx, by),
            self._圆截面Z(valve_z0 + 60.0, 36.0, bx, by),
            self._圆截面Z(valve_z0 + 72.0, 22.0, bx, by)
        )
        valve_body.smooth = True
        valve_body = valve_body.color(*brass)
        valve_upper_nut = self._六角柱Z(
            valve_z0 + 68.0,
            valve_z0 + 92.0,
            60.0, bx, by
        ).color(*brass)
        container_valve = combine(
            valve_base_nut, valve_body_lower,
            valve_body, valve_upper_nut
        )

        # 电磁驱动器：钢制执行筒 + 上端盖 + 红色手动按钮。
        actuator_z0 = valve_z0 + 92.0
        actuator_lower_flange = self._圆柱(
            Vec3(bx, by, actuator_z0),
            Vec3(bx, by, actuator_z0 + 8.0),
            78.0
        ).color(*steel)
        actuator_body = self._圆柱(
            Vec3(bx, by, actuator_z0 + 8.0),
            Vec3(bx, by, actuator_z0 + 96.0),
            50.0
        ).color(0.78, 0.80, 0.82, 1.0)
        actuator_upper_flange = self._圆柱(
            Vec3(bx, by, actuator_z0 + 94.0),
            Vec3(bx, by, actuator_z0 + 108.0),
            62.0
        ).color(*steel)
        button_stem = self._圆柱(
            Vec3(bx, by, actuator_z0 + 106.0),
            Vec3(bx, by, actuator_z0 + 122.0),
            14.0
        ).color(*steel)
        manual_button = self._圆柱(
            Vec3(bx, by, actuator_z0 + 118.0),
            Vec3(bx, by, actuator_z0 + 144.0),
            22.0
        ).color(*red)
        actuator = combine(
            actuator_lower_flange, actuator_body,
            actuator_upper_flange, button_stem,
            manual_button
        )

        # 侧向出口：瓶体后侧水平引出，作为高压软管起点。
        outlet_z = valve_z0 + 48.0
        outlet_y = by + bottle_radius * 0.80
        side_outlet = self._圆柱(
            Vec3(bx, by, outlet_z),
            Vec3(bx, outlet_y, outlet_z),
            pipe_d * 1.20
        ).color(*brass)

        # 高压软管：后侧引出 → 水平延伸到柜后内壁 →
        # 竖直上行至喷嘴高度 → 水平接到喷嘴后端。
        # 两处 90° 拐弯用较大圆角实现平滑过渡。
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
        hose_group = hose

        cabinet = combine(
            cabinet_shell, inner_back, floor_tray, hinges
        )
        bottle_group = bottle
        valve_and_pipe = combine(
            container_valve, actuator,
            side_outlet, hose_group
        )

        self['柜体'] = cabinet
        self['柜门'] = door
        self['储瓶组件'] = bottle_group
        self['阀门管路'] = valve_and_pipe
        self['固定面板及喷嘴'] = fixed_front
        self['整体'] = combine(
            cabinet, fixed_front, door, bottle_group, valve_and_pipe
        )


if __name__ == '__main__':
    FinalGeometry = 柜式七氟丙烷预制灭火装置()
    place(FinalGeometry)
