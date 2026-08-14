from pyp3d import *
import math


class 高压二氧化碳灭火装置(Component):
    """高压二氧化碳灭火装置（贮存瓶组、启动瓶组及管路）。

    外形依据江西清华实业有限公司产品页
    ``https://www.qhxf.com/product-detail/Bg2zOD9b`` 的产品照片建模：
    两只大容量 CO2 灭火剂贮存容器悬挂在红色主框架内，瓶口上方
    设置称重/悬挂机构；主框架右侧布置红色集流管、法兰、启动阀，
    下方独立小框架内设置一只启动瓶。

    产品页未公开可读取的外形尺寸表，因此本构件以照片比例给出
    BIM 默认尺寸，并开放瓶数、瓶径、瓶高、框架和管径等参数。
    灭火剂贮存容器沿用“柜式无管网预制灭火装置”中的多截面圆肩
    瓶体放样方法。本模型用于 BIM 外形和设备布置，不代替承压设备、
    管路或钢结构制造图；工程使用前应按厂家设备表复核尺寸与接口。

    局部原点位于主框架左前下角，X 向右，Y 向后，Z 向上。
    """

    def __init__(self):
        Component.__init__(self)

        self['名称'] = Attr(
            '高压二氧化碳灭火装置',
            obvious=True, readonly=True, group='标识'
        )
        self['规格型号'] = Attr(
            'QME70-QH', obvious=True, group='标识'
        )
        self['灭火剂'] = Attr(
            'CO2（二氧化碳）',
            obvious=True, readonly=True, group='标识'
        )
        
        self['贮存容器容积（L）'] = Attr(
            70.0, obvious=True, readonly=True, group='技术参数'
        )
        self['CO2充装量（Kg）'] = Attr(
            42.0, obvious=True, readonly=True, group='技术参数'
        )
        self['执行标准'] = Attr(
            'GB16669-2010', obvious=True, readonly=True, group='技术参数'
        )
        self['贮存压力'] = Attr(
            '5.7MPa（20℃）', obvious=True, readonly=True, group='技术参数'
        )
        self['贮存装置最大工作压力'] = Attr(
            '12.4MPa', obvious=True, readonly=True, group='技术参数'
        )
        self['阀驱动装置氮气源压力'] = Attr(
            '6.0MPa（20℃）', obvious=True, readonly=True, group='技术参数'
        )
        self['工作主电源'] = Attr(
            'AC220V/50Hz', obvious=True, readonly=True, group='技术参数'
        )
        self['工作备用电源'] = Attr(
            'DC24V', obvious=True, readonly=True, group='技术参数'
        )
        self['功率消耗'] = Attr(
            '警戒时不大于15W，报警时不大于30W', obvious=True, readonly=True, group='技术参数'
        )
        self['环境条件'] = Attr(
            '温度0℃~50℃，相对湿度不大于97%', obvious=True, readonly=True, group='技术参数'
        )
        self['启动方式'] = Attr(
            '自动、电气手动、机械应急操作', obvious=True, readonly=True, group='技术参数'
        )
        self['自动启动延时时间'] = Attr(
            '0~30s可调', obvious=True, readonly=True, group='技术参数'
        )

        self['贮存瓶数量'] = Attr(
            2, obvious=True, pivotal=True, group='灭火剂贮存容器'
        )
        self['贮存瓶外径'] = Attr(
            267.0, obvious=True, pivotal=True, group='灭火剂贮存容器'
        )
        self['贮存瓶瓶体高度'] = Attr(
            1470.0, obvious=True, pivotal=True, group='灭火剂贮存容器'
        )
        self['贮存瓶底部标高'] = Attr(
            65.0, obvious=True, group='灭火剂贮存容器'
        )
        self['贮存瓶间净距'] = Attr(
            45.0, obvious=True, group='灭火剂贮存容器'
        )
        self['瓶颈直径'] = Attr(
            58.0, obvious=True, group='灭火剂贮存容器'
        )
        self['顶部吊管外径'] = Attr(
            32.0, obvious=True, group='灭火剂贮存容器',
            description='顶部吊管外径（贮存瓶称重悬挂机构吊挂在此管上）。'
        )
        self['顶部吊管左伸长度'] = Attr(
            0, obvious=True, group='灭火剂贮存容器',
            description='顶部吊管从框架左外侧向左延伸的长度。'
        )
        self['顶部吊管右伸长度'] = Attr(
            100.0, obvious=True, group='灭火剂贮存容器',
            description='顶部吊管从最右贮存瓶中心向右延伸的长度。'
        )

        self['主框架宽度'] = Attr(
            820.0, obvious=True, pivotal=True, group='主框架'
        )
        self['主框架深度'] = Attr(
            500.0, obvious=True, pivotal=True, group='主框架'
        )
        self['主框架高度'] = Attr(
            2050.0, obvious=True, pivotal=True, group='主框架'
        )
        self['主框架立柱边长'] = Attr(
            50.0, obvious=True, group='主框架'
        )
        self['框架横梁高度'] = Attr(
            70.0, obvious=True, group='主框架'
        )

        self['集流管外径'] = Attr(
            65.0, obvious=True, pivotal=True, group='集流管及启动管路'
        )
        self['集流管右伸长度'] = Attr(
            620.0, obvious=True, group='集流管及启动管路'
        )
        self['集流管水平标高'] = Attr(
            900.0, obvious=True, group='集流管及启动管路'
        )
        self['法兰外径'] = Attr(
            112.0, obvious=True, group='集流管及启动管路'
        )

        self['启动瓶外径'] = Attr(
            160.0, obvious=True, pivotal=True, group='启动瓶组'
        )
        self['启动瓶瓶体高度'] = Attr(
            430.0, obvious=True, pivotal=True, group='启动瓶组'
        )
        self['启动瓶支架宽度'] = Attr(
            300.0, obvious=True, group='启动瓶组'
        )
        self['启动瓶支架深度'] = Attr(
            330.0, obvious=True, group='启动瓶组'
        )
        self['启动瓶支架高度'] = Attr(
            870.0, obvious=True, group='启动瓶组'
        )
        self['启动管外径'] = Attr(
            10.0, obvious=True, group='启动瓶组'
        )

        self['主框架'] = Attr(None)
        self['顶部吊管'] = Attr(None)
        self['灭火剂贮存容器'] = Attr(None)
        self['容器阀及瓶组支管'] = Attr(None)
        self['称重悬挂机构'] = Attr(None)
        self['集流管'] = Attr(None)
        self['启动瓶组'] = Attr(None)
        self['启动阀'] = Attr(None)
        self['整体'] = Attr(None, show=True)

        
        self.setDrivenFeaturePoint(
            '集流管出口中心', SnapMode.EndPoint,
            '[定位点X]+[主框架宽度]+[集流管右伸长度]',
            '[定位点Y]+[主框架深度]*0.38',
            '[定位点Z]+[集流管水平标高]'
        )
    
        self.replace()

    @staticmethod
    def _圆柱(start, end, diameter):
        return Cone(
            start, end,
            max(diameter / 2.0, 0.5),
            max(diameter / 2.0, 0.5)
        )

    @staticmethod
    def _圆截面Z(z_position, radius, center_x=0.0, center_y=0.0):
        return translate(center_x, center_y, z_position) * \
               Section(scale(radius) * Arc(2.0 * math.pi))

    @staticmethod
    def _圆截面X(x_position, radius, center_y=0.0, center_z=0.0):
        return translate(x_position, center_y, center_z) * \
               rotate(Vec3(0, 1, 0), math.pi / 2.0) * \
               Section(scale(radius) * Arc(2.0 * math.pi))

    @staticmethod
    def _六角截面Z(z_position, across_flats,
                 center_x=0.0, center_y=0.0):
        circumradius = across_flats / math.sqrt(3.0)
        points = []
        for index in range(6):
            angle = math.pi / 6.0 + index * math.pi / 3.0
            points.append(Vec3(
                center_x + circumradius * math.cos(angle),
                center_y + circumradius * math.sin(angle),
                z_position
            ))
        points.append(points[0])
        return Section(Line(*points))

    @classmethod
    def _六角柱Z(cls, z_start, z_end, across_flats,
               center_x=0.0, center_y=0.0):
        result = Loft(
            cls._六角截面Z(
                z_start, across_flats, center_x, center_y
            ),
            cls._六角截面Z(
                z_end, across_flats, center_x, center_y
            )
        )
        result.smooth = False
        return result

    @staticmethod
    def _环形抱箍(cx, cy, z0, diameter, height, thickness):
        outer = 高压二氧化碳灭火装置._圆柱(
            Vec3(cx, cy, z0),
            Vec3(cx, cy, z0 + height),
            diameter + 2.0 * thickness
        )
        inner = 高压二氧化碳灭火装置._圆柱(
            Vec3(cx, cy, z0 - 1.0),
            Vec3(cx, cy, z0 + height + 1.0),
            diameter
        )
        return outer - inner

    def _平焊法兰(self, cx, cy, z_center, axis_dir='Z',
              pipe_d=65.0, flange_d=112.0, flange_t=16.0,
              n_bolts=4, bolt_d=14.0,
              bolt_circle_d=None,
              seal_face=True, seal_d=None, seal_t=2.0,
              seal_dir='+Z',
              color=(0.7, 0.7, 0.7, 1.0)):
        """在 (cx, cy, z_center) 处生成一个平焊法兰几何体。

        几何构造参考 零件库_Py/平焊法兰参数化组件.py：
        主盘（带螺栓孔）+ 可选突面（RF）。
        seal_dir='+Z' 突面朝上；'-Z' 突面朝下（用于上方法兰与垫片贴合）。
        """
        pipe_r = pipe_d / 2.0
        flange_r = flange_d / 2.0
        if bolt_circle_d is None:
            bolt_circle_d = flange_d * 0.72
        bolt_r = bolt_d / 2.0
        bolt_circle_r = bolt_circle_d / 2.0
        if seal_d is None:
            seal_d = (flange_d + pipe_d) * 0.40
        seal_r = seal_d / 2.0

        if axis_dir == 'Z':
            z0 = z_center - flange_t / 2.0
            z1 = z_center + flange_t / 2.0
            main = Cone(
                Vec3(cx, cy, z0), Vec3(cx, cy, z1),
                flange_r, flange_r
            )
            main = main - Cone(
                Vec3(cx, cy, z0 - 1.0), Vec3(cx, cy, z1 + 1.0),
                pipe_r, pipe_r
            )
            bolt_holes = None
            for i in range(n_bolts):
                ang = 2.0 * math.pi * i / n_bolts
                hx = cx + bolt_circle_r * math.cos(ang)
                hy = cy + bolt_circle_r * math.sin(ang)
                hole = translate(Vec3(hx, hy, 0.0)) * Cone(
                    Vec3(0.0, 0.0, z0 - 1.0), Vec3(0.0, 0.0, z1 + 1.0),
                    bolt_r, bolt_r
                )
                bolt_holes = hole if bolt_holes is None else bolt_holes + hole
            main = main - bolt_holes
            if seal_face:
                if seal_dir == '+Z':
                    seal = Cone(
                        Vec3(cx, cy, z1), Vec3(cx, cy, z1 + seal_t),
                        seal_r, seal_r
                    )
                    seal = seal - Cone(
                        Vec3(cx, cy, z1 - 1.0),
                        Vec3(cx, cy, z1 + seal_t + 1.0),
                        pipe_r, pipe_r
                    )
                else:
                    seal = Cone(
                        Vec3(cx, cy, z0 - seal_t), Vec3(cx, cy, z0),
                        seal_r, seal_r
                    )
                    seal = seal - Cone(
                        Vec3(cx, cy, z0 - seal_t - 1.0),
                        Vec3(cx, cy, z0 + 1.0),
                        pipe_r, pipe_r
                    )
                main = main + seal
        return main.color(*color)

    def _圆肩瓶(self, cx, cy, bottom_z, diameter, body_height,
              neck_diameter, body_color):
        """圆肩贮存容器；截面比例取自柜式无管网装置瓶组代码。"""
        radius = diameter / 2.0
        neck_radius = neck_diameter / 2.0
        sections = [
            self._圆截面Z(bottom_z, radius * 0.78, cx, cy),
            self._圆截面Z(
                bottom_z + diameter * 0.020,
                radius * 0.92, cx, cy
            ),
            self._圆截面Z(
                bottom_z + diameter * 0.045,
                radius * 0.99, cx, cy
            ),
            self._圆截面Z(
                bottom_z + diameter * 0.090,
                radius, cx, cy
            ),
            self._圆截面Z(
                bottom_z + body_height - diameter * 0.30,
                radius, cx, cy
            ),
            self._圆截面Z(
                bottom_z + body_height - diameter * 0.22,
                radius * 0.98, cx, cy
            ),
            self._圆截面Z(
                bottom_z + body_height - diameter * 0.15,
                radius * 0.88, cx, cy
            ),
            self._圆截面Z(
                bottom_z + body_height - diameter * 0.09,
                radius * 0.68, cx, cy
            ),
            self._圆截面Z(
                bottom_z + body_height - diameter * 0.04,
                radius * 0.42, cx, cy
            ),
            self._圆截面Z(
                bottom_z + body_height,
                neck_radius * 1.30, cx, cy
            )
        ]
        shell = Loft(*sections)
        shell.smooth = True
        shell = shell.color(*body_color)

        neck_z = bottom_z + body_height
        neck = self._圆柱(
            Vec3(cx, cy, neck_z - 2.0),
            Vec3(cx, cy, neck_z + 32.0),
            neck_diameter
        ).color(*body_color)
        neck_ring = self._圆柱(
            Vec3(cx, cy, neck_z + 22.0),
            Vec3(cx, cy, neck_z + 34.0),
            neck_diameter * 1.24
        ).color(0.60, 0.015, 0.012, 1.0)
        return [shell, neck, neck_ring]

    def _容器阀(self, cx, cy, neck_top_z, brass, light_brass, steel):
        parts = []
        base = self._六角柱Z(
            neck_top_z - 2.0, neck_top_z + 22.0,
            66.0, cx, cy
        ).color(*brass)
        lower = self._圆柱(
            Vec3(cx, cy, neck_top_z + 18.0),
            Vec3(cx, cy, neck_top_z + 38.0),
            55.0
        ).color(*light_brass)
        body = Loft(
            self._圆截面Z(neck_top_z + 34.0, 22.0, cx, cy),
            self._圆截面Z(neck_top_z + 48.0, 31.0, cx, cy),
            self._圆截面Z(neck_top_z + 70.0, 31.0, cx, cy),
            self._圆截面Z(neck_top_z + 82.0, 21.0, cx, cy)
        )
        body.smooth = True
        body = body.color(*brass)
        upper = self._六角柱Z(
            neck_top_z + 78.0, neck_top_z + 102.0,
            48.0, cx, cy
        ).color(*light_brass)
        stem = self._圆柱(
            Vec3(cx, cy, neck_top_z + 100.0),
            Vec3(cx, cy, neck_top_z + 128.0),
            16.0
        ).color(*steel)
        parts.extend([base, lower, body, upper, stem])
        return parts

    def _称重悬挂机构(self, cx, cy, bottle_neck_top_z,
                  frame_height, bottle_diameter,
                  red, steel, light_steel, dark_gray,
                  top_pipe_z, top_pipe_d):
        """称重悬挂机构。

        结构（自下而上）：
          - 封闭吊笼：4 立柱 + 4 顶横梁 + 4 底横梁，
            形成完全封闭的方形框架，可将瓶口和容器阀完全包住并吊起
          - 瓶颈抱箍
          - 下立柱 + 下端盖 + 称重传感器 + 上端盖
          - 短吊杆（上端接入顶部主管的抱箍）
          - 顶部吊管抱箍（套在水平主管上）+ 锁紧螺母
        """
        parts = []
        # 封闭吊笼：方形框架，4 立柱 + 4 顶横梁 + 4 底横梁，
        # 完全包住瓶口和容器阀（顶部水平段、底部水平段均为同一根主集流管）
        cage_size = max(bottle_diameter * 0.5, 140.0)
        bar = 12.0
        cage_z0 = bottle_neck_top_z - 35.0
        cage_z1 = bottle_neck_top_z + 155.0
        half = cage_size / 2.0
        # 4 根立柱（位于吊笼四角）
        for dx, dy in [
            (-half, -half),
            (half - bar, -half),
            (-half, half - bar),
            (half - bar, half - bar)
        ]:
            v_bar = translate(
                cx + dx, cy + dy, cage_z0
            ) * scale(bar, bar, cage_z1 - cage_z0) * Cube()
            parts.append(v_bar.color(*steel))
        # 4 根顶部横梁（连接吊笼四角，形成封闭顶面）
        front_bar = translate(
            cx - half, cy - half, cage_z1 - bar
        ) * scale(cage_size, bar, bar) * Cube()
        back_bar = translate(
            cx - half, cy + half - bar, cage_z1 - bar
        ) * scale(cage_size, bar, bar) * Cube()
        left_bar_h = translate(
            cx - half, cy - half, cage_z1 - bar
        ) * scale(bar, cage_size, bar) * Cube()
        right_bar_h = translate(
            cx + half - bar, cy - half, cage_z1 - bar
        ) * scale(bar, cage_size, bar) * Cube()
        parts.extend([
            front_bar.color(*steel),
            back_bar.color(*steel),
            left_bar_h.color(*steel),
            right_bar_h.color(*steel)
        ])

        # 4 根底部横梁（连接吊笼四角，形成封闭底面；
        # 中央留有 116mm 开口，便于瓶体穿过）
        bot_front_bar = translate(
            cx - half, cy - half, cage_z0
        ) * scale(cage_size, bar, bar) * Cube()
        bot_back_bar = translate(
            cx - half, cy + half - bar, cage_z0
        ) * scale(cage_size, bar, bar) * Cube()
        bot_left_bar_h = translate(
            cx - half, cy - half, cage_z0
        ) * scale(bar, cage_size, bar) * Cube()
        bot_right_bar_h = translate(
            cx + half - bar, cy - half, cage_z0
        ) * scale(bar, cage_size, bar) * Cube()
        parts.extend([
            bot_front_bar.color(*steel),
            bot_back_bar.color(*steel),
            bot_left_bar_h.color(*steel),
            bot_right_bar_h.color(*steel)
        ])

        neck_saddle = self._环形抱箍(
            cx, cy, cage_z0 + 30.0, bottle_diameter * 0.31, 16.0, 8.0
        ).color(*dark_gray)
        parts.append(neck_saddle)

        load_cell_bottom = frame_height - 300.0
        load_cell_top = frame_height - 105.0
        load_cell_d = min(max(bottle_diameter * 0.25, 58.0), 82.0)
        lower_rod = self._圆柱(
            Vec3(cx, cy, cage_z1),
            Vec3(cx, cy, load_cell_bottom),
            12.0
        ).color(*steel)
        lower_cap = self._圆柱(
            Vec3(cx, cy, load_cell_bottom - 6.0),
            Vec3(cx, cy, load_cell_bottom + 12.0),
            load_cell_d * 1.12
        ).color(*steel)
        load_cell = self._圆柱(
            Vec3(cx, cy, load_cell_bottom + 8.0),
            Vec3(cx, cy, load_cell_top - 8.0),
            load_cell_d
        ).color(*light_steel)
        upper_cap = self._圆柱(
            Vec3(cx, cy, load_cell_top - 12.0),
            Vec3(cx, cy, load_cell_top + 5.0),
            load_cell_d * 1.12
        ).color(*steel)

        # 顶部主管抱箍：套在水平主管上，连接吊杆
        clamp_outer_r = top_pipe_d / 2.0 + 6.0
        clamp_inner_r = top_pipe_d / 2.0 + 1.0
        clamp_h = 28.0
        clamp_bottom_z = top_pipe_z - clamp_h / 2.0
        top_clamp = (
            self._圆柱(
                Vec3(cx, cy, top_pipe_z - clamp_h / 2.0),
                Vec3(cx, cy, top_pipe_z + clamp_h / 2.0),
                clamp_outer_r
            )
            - self._圆柱(
                Vec3(cx, cy, top_pipe_z - clamp_h / 2.0 - 2.0),
                Vec3(cx, cy, top_pipe_z + clamp_h / 2.0 + 2.0),
                clamp_inner_r
            )
        ).color(*steel)

        # 短吊杆：上端接入抱箍底部
        top_rod = self._圆柱(
            Vec3(cx, cy, load_cell_top),
            Vec3(cx, cy, clamp_bottom_z),
            13.0
        ).color(*steel)

        # 锁紧螺母：抱箍底部
        nut = self._圆柱(
            Vec3(cx, cy, clamp_bottom_z - 5.0),
            Vec3(cx, cy, clamp_bottom_z + 1.0),
            17.0
        ).color(*steel)

        parts.extend([
            lower_rod, lower_cap, load_cell,
            upper_cap, top_rod, top_clamp, nut
        ])
        return parts

    def _主框架(self, width, depth, height, post, beam_h,
              red, dark_red):
        parts = []
        for x in [0.0, width - post]:
            for y in [0.0, depth - post]:
                column = translate(x, y, 0) * \
                         scale(post, post, height) * Cube()
                parts.append(column.color(*red))

        for y in [0.0, depth - post]:
            top_beam = translate(0, y, height - beam_h) * \
                       scale(width, post, beam_h) * Cube()
            parts.append(top_beam.color(*red))
        for x in [0.0, width - post]:
            side_beam = translate(x, 0, height - beam_h) * \
                        scale(post, depth, beam_h) * Cube()
            parts.append(side_beam.color(*red))

        # 后部两道横撑固定瓶组，正面保持敞开，匹配产品照片。
        for z in [220.0, height * 0.48]:
            rear_rail = translate(
                post, depth - post, z
            ) * scale(width - 2.0 * post, post, post) * Cube()
            parts.append(rear_rail.color(*dark_red))
        return parts

    def _启动瓶支架(self, x0, y0, width, depth, height,
                post, red, dark_red):
        parts = []
        for x in [x0, x0 + width - post]:
            for y in [y0, y0 + depth - post]:
                column = translate(x, y, 0) * \
                         scale(post, post, height) * Cube()
                parts.append(column.color(*red))
        for z in [0.0, height - post]:
            for y in [y0, y0 + depth - post]:
                beam = translate(x0, y, z) * \
                       scale(width, post, post) * Cube()
                parts.append(beam.color(*red))
            for x in [x0, x0 + width - post]:
                beam = translate(x, y0, z) * \
                       scale(post, depth, post) * Cube()
                parts.append(beam.color(*red))

        tray = translate(
            x0 + post, y0 + post, post
        ) * scale(
            width - 2.0 * post,
            depth - 2.0 * post,
            22.0
        ) * Cube()
        parts.append(tray.color(*dark_red))
        return parts

    @export
    def replace(self):
        bottle_count = int(min(max(self['贮存瓶数量'], 1), 6))
        frame_w = max(self['主框架宽度'], 520.0)
        frame_d = max(self['主框架深度'], 360.0)
        frame_h = max(self['主框架高度'], 1450.0)
        post = min(
            max(self['主框架立柱边长'], 32.0),
            min(frame_w, frame_d) * 0.16
        )
        beam_h = min(
            max(self['框架横梁高度'], post),
            frame_h * 0.10
        )

        requested_bottle_d = max(self['贮存瓶外径'], 160.0)
        clear_gap = max(self['贮存瓶间净距'], 20.0)
        max_bottle_d_by_width = (
            frame_w - 2.0 * (post + 28.0) -
            (bottle_count - 1) * clear_gap
        ) / bottle_count
        bottle_d = min(
            requested_bottle_d,
            max(max_bottle_d_by_width, 80.0),
            frame_d - 2.0 * post - 60.0
        )
        bottle_h = min(
            max(self['贮存瓶瓶体高度'], bottle_d * 3.8),
            frame_h - 430.0
        )
        bottle_z = min(
            max(self['贮存瓶底部标高'], 25.0),
            frame_h - bottle_h - 360.0
        )
        neck_d = min(
            max(self['瓶颈直径'], bottle_d * 0.16),
            bottle_d * 0.34
        )
        bottle_group_w = (
            bottle_count * bottle_d +
            (bottle_count - 1) * clear_gap
        )
        first_bottle_x = (frame_w - bottle_group_w) / 2.0 + \
                         bottle_d / 2.0
        bottle_y = frame_d * 0.50

        pipe_d = min(max(self['集流管外径'], 40.0), 120.0)
        pipe_extension = max(self['集流管右伸长度'], 400.0)
        horizontal_z = min(
            max(self['集流管水平标高'], 620.0),
            frame_h * 0.66
        )
        flange_d = min(
            max(self['法兰外径'], pipe_d * 1.45),
            pipe_d * 2.4
        )

        pilot_d = min(max(self['启动瓶外径'], 110.0), 230.0)
        pilot_h = min(
            max(self['启动瓶瓶体高度'], pilot_d * 2.1),
            650.0
        )
        pilot_rack_w = max(self['启动瓶支架宽度'], pilot_d + 100.0)
        pilot_rack_d = max(self['启动瓶支架深度'], pilot_d + 110.0)
        pilot_rack_h = min(
            max(self['启动瓶支架高度'], pilot_h + 260.0),
            horizontal_z - 20.0
        )
        pilot_pipe_d = min(max(self['启动管外径'], 6.0), 18.0)

        red = (0.88, 0.025, 0.018, 1.0)
        dark_red = (0.60, 0.012, 0.010, 1.0)
        brass = (0.74, 0.47, 0.13, 1.0)
        light_brass = (0.86, 0.64, 0.25, 1.0)
        steel = (0.58, 0.61, 0.62, 1.0)
        light_steel = (0.86, 0.88, 0.87, 1.0)
        dark_gray = (0.12, 0.14, 0.15, 1.0)
        white = (0.97, 0.97, 0.94, 1.0)
        copper = (0.75, 0.40, 0.14, 1.0)

        frame_parts = self._主框架(
            frame_w, frame_d, frame_h, post, beam_h,
            red, dark_red
        )
        bottle_parts = []
        valve_branch_parts = []
        suspension_parts = []
        bottle_centers = []

        neck_top_z = bottle_z + bottle_h + 34.0

        # 顶部吊管参数：贮存瓶称重悬挂机构吊挂在主管顶部水平段上
        top_pipe_d = min(max(self['顶部吊管外径'], 16.0), 80.0)
        top_pipe_left_ext = min(max(self['顶部吊管左伸长度'], 0.0), 400.0)
        top_pipe_right_ext = min(max(self['顶部吊管右伸长度'], 0.0), 400.0)
        top_pipe_z = frame_h - 50.0
        top_pipe_y = bottle_y
        max_bottle_x = (
            first_bottle_x
            + (bottle_count - 1) * (bottle_d + clear_gap)
            + bottle_d / 2.0
        )
        # 注：顶部水平管道由主集流管的顶部水平段承担（见下方 main_pipe），
        # 贮存瓶称重悬挂机构通过抱箍直接吊挂在这根主管上。
        # 此处不再单独生成 top_pipe 和左端支撑板。

        for index in range(bottle_count):
            cx = first_bottle_x + index * (bottle_d + clear_gap)
            bottle_centers.append(cx)
            bottle_parts.extend(self._圆肩瓶(
                cx, bottle_y, bottle_z,
                bottle_d, bottle_h, neck_d, red
            ))
            bottle_parts.append(
                self._环形抱箍(
                    cx, bottle_y,
                    bottle_z + bottle_h * 0.88,
                    bottle_d + 3.0, 26.0, 7.0
                ).color(*dark_red)
            )

            valve_branch_parts.extend(self._容器阀(
                cx, bottle_y, neck_top_z,
                brass, light_brass, steel
            ))

            suspension_parts.extend(self._称重悬挂机构(
                cx, bottle_y, neck_top_z,
                frame_h, bottle_d,
                red, steel, light_steel, dark_gray,
                top_pipe_z, top_pipe_d
            ))

        # 红色主集流管：顶部水平段从框架左侧外水平延伸（用于吊挂贮存瓶），
        # 到右侧 riser_x 处下弯转为水平出口。顶部水平段 + 竖直段 + 底部水平段
        # 是同一根管道，Y 位置与贮存瓶中心一致，路径全部使用 90° 弯头。
        main_pipe_y = bottle_y
        riser_x = frame_w + 155.0
        outlet_x = frame_w + pipe_extension
        main_pipe = FilletPipe(
            [
                Vec3(-top_pipe_left_ext, main_pipe_y, top_pipe_z),
                Vec3(riser_x, main_pipe_y, top_pipe_z),
                Vec3(riser_x, main_pipe_y, horizontal_z),
                Vec3(outlet_x, main_pipe_y, horizontal_z)
            ],
            [0.0, 42.0, 42.0, 0.0],
            pipe_d / 2.0
        ).color(*red)
        collector_parts = [main_pipe]

        flange_z = min(
            frame_h - 420.0,
            horizontal_z + (frame_h - horizontal_z) * 0.47
        )
        flange_t = 16.0
        flange_gap = 6.0
        # 下方法兰：主盘 + 突面朝上（贴近垫片）
        lower_flange = self._平焊法兰(
            riser_x, main_pipe_y,
            flange_z - flange_gap / 2.0 - flange_t / 2.0,
            axis_dir='Z',
            pipe_d=pipe_d, flange_d=flange_d, flange_t=flange_t,
            n_bolts=4, bolt_d=14.0,
            bolt_circle_d=flange_d * 0.72,
            seal_face=True,
            seal_d=(flange_d + pipe_d) * 0.40,
            seal_t=2.0,
            seal_dir='+Z',
            color=dark_red
        )
        # 中间垫片
        gasket = self._圆柱(
            Vec3(riser_x, main_pipe_y, flange_z - flange_gap / 2.0),
            Vec3(riser_x, main_pipe_y, flange_z + flange_gap / 2.0),
            flange_d * 0.88
        ).color(*dark_gray)
        # 上方法兰：主盘 + 突面朝下（贴近垫片）
        upper_flange = self._平焊法兰(
            riser_x, main_pipe_y,
            flange_z + flange_gap / 2.0 + flange_t / 2.0,
            axis_dir='Z',
            pipe_d=pipe_d, flange_d=flange_d, flange_t=flange_t,
            n_bolts=4, bolt_d=14.0,
            bolt_circle_d=flange_d * 0.72,
            seal_face=True,
            seal_d=(flange_d + pipe_d) * 0.40,
            seal_t=2.0,
            seal_dir='-Z',
            color=red
        )
        collector_parts.extend([lower_flange, gasket, upper_flange])

        outlet_end = self._圆柱(
            Vec3(outlet_x - 22.0, main_pipe_y, horizontal_z),
            Vec3(outlet_x + 8.0, main_pipe_y, horizontal_z),
            pipe_d * 1.10
        ).color(*dark_red)
        collector_parts.append(outlet_end)

        # 启动瓶支架位于主集流管水平段下方。
        pilot_rack_x = frame_w + pipe_extension * 0.42
        pilot_rack_y = max(0.0, main_pipe_y - pilot_rack_d * 0.50)
        pilot_post = min(max(post * 0.62, 28.0), 42.0)
        pilot_frame_parts = self._启动瓶支架(
            pilot_rack_x, pilot_rack_y,
            pilot_rack_w, pilot_rack_d, pilot_rack_h,
            pilot_post, red, dark_red
        )

        pilot_cx = pilot_rack_x + pilot_rack_w / 2.0
        pilot_cy = pilot_rack_y + pilot_rack_d / 2.0
        pilot_bottom_z = pilot_post + 24.0
        pilot_neck_d = pilot_d * 0.25
        pilot_parts = list(pilot_frame_parts)
        pilot_parts.extend(self._圆肩瓶(
            pilot_cx, pilot_cy, pilot_bottom_z,
            pilot_d, pilot_h, pilot_neck_d, red
        ))
        pilot_neck_top_z = pilot_bottom_z + pilot_h + 34.0
        pilot_parts.extend(self._容器阀(
            pilot_cx, pilot_cy, pilot_neck_top_z,
            brass, light_brass, steel
        ))
        pilot_parts.append(
            self._环形抱箍(
                pilot_cx, pilot_cy,
                pilot_bottom_z + pilot_h * 0.56,
                pilot_d + 4.0, 25.0, 7.0
            ).color(*dark_red)
        )

        rear_clip = translate(
            pilot_rack_x + pilot_post,
            pilot_rack_y + pilot_rack_d - pilot_post * 1.8,
            pilot_bottom_z + pilot_h * 0.52
        ) * scale(
            pilot_rack_w - 2.0 * pilot_post,
            pilot_post,
            22.0
        ) * Cube()
        pilot_parts.append(rear_clip.color(*dark_red))

        # 水平主集流管上的启动阀和机械应急手柄。
        selector_x = pilot_cx
        selector_base = self._六角柱Z(
            horizontal_z + pipe_d * 0.20,
            horizontal_z + pipe_d * 0.75,
            pipe_d * 1.15,
            selector_x, main_pipe_y
        ).color(*brass)
        selector_body = self._圆柱(
            Vec3(selector_x, main_pipe_y, horizontal_z + pipe_d * 0.70),
            Vec3(selector_x, main_pipe_y, horizontal_z + pipe_d * 1.58),
            pipe_d * 0.72
        ).color(*light_brass)
        selector_cap = self._六角柱Z(
            horizontal_z + pipe_d * 1.48,
            horizontal_z + pipe_d * 1.82,
            pipe_d * 0.82,
            selector_x, main_pipe_y
        ).color(*steel)
        selector_stem_top = horizontal_z + pipe_d * 1.80
        lever_hub = self._圆柱(
            Vec3(selector_x, main_pipe_y - 20.0, selector_stem_top),
            Vec3(selector_x, main_pipe_y + 20.0, selector_stem_top),
            25.0
        ).color(*steel)
        lever = self._圆柱(
            Vec3(selector_x, main_pipe_y, selector_stem_top),
            Vec3(
                selector_x + 145.0,
                main_pipe_y,
                selector_stem_top + 205.0
            ),
            13.0
        ).color(*steel)
        lever_grip = self._圆柱(
            Vec3(
                selector_x + 137.0,
                main_pipe_y,
                selector_stem_top + 194.0
            ),
            Vec3(
                selector_x + 160.0,
                main_pipe_y,
                selector_stem_top + 228.0
            ),
            22.0
        ).color(*dark_gray)
        selector_parts = [
            selector_base, selector_body, selector_cap,
            lever_hub, lever, lever_grip
        ]

        # 启动瓶至启动阀的铜质控制管。
        pilot_outlet_z = pilot_neck_top_z + 58.0
        pilot_outlet = self._圆柱(
            Vec3(pilot_cx, pilot_cy, pilot_outlet_z),
            Vec3(pilot_cx, pilot_cy - 48.0, pilot_outlet_z),
            24.0
        ).color(*brass)
        pilot_control_pipe = FilletPipe(
            [
                Vec3(pilot_cx, pilot_cy - 48.0, pilot_outlet_z),
                Vec3(pilot_cx, main_pipe_y, pilot_outlet_z),
                Vec3(pilot_cx, main_pipe_y, horizontal_z + pipe_d * 1.10)
            ],
            [0.0, 25.0, 0.0],
            pilot_pipe_d / 2.0
        ).color(*copper)
        selector_parts.extend([pilot_outlet, pilot_control_pipe])

        # 注：原"主瓶支管与红色集流管之间的短接"已删除（细管全部移除）。

        frame_geometry = combine(*frame_parts)
        bottle_geometry = combine(*bottle_parts)
        valve_geometry = combine(*valve_branch_parts)
        suspension_geometry = combine(*suspension_parts)
        collector_geometry = combine(*collector_parts)
        pilot_geometry = combine(*pilot_parts)
        selector_geometry = combine(*selector_parts)

        self['主框架'] = frame_geometry
        self['顶部吊管'] = main_pipe
        self['灭火剂贮存容器'] = bottle_geometry
        self['容器阀及瓶组支管'] = valve_geometry
        self['称重悬挂机构'] = suspension_geometry
        self['集流管'] = collector_geometry
        self['启动瓶组'] = pilot_geometry
        self['启动阀'] = selector_geometry
        self['整体'] = combine(
            *frame_parts,
            *bottle_parts,
            *valve_branch_parts,
            *suspension_parts,
            *collector_parts,
            *pilot_parts,
            *selector_parts
        )


if __name__ == '__main__':
    FinalGeometry = 高压二氧化碳灭火装置()
    place(FinalGeometry)
