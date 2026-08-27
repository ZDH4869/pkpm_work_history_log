# -*- coding: utf-8 -*-
# ============================================================================
# 钢筋混凝土烟囱（带栏杆）参数化组件
# 依据国标图集 05G212《钢筋混凝土烟囱》P10 "60m 烟囱筒壁模板图"
#
# 图纸信息提取（默认值对应筒壁型号 TB60/2.0，囱口内径 2.0m，烟囱高度 60m）：
#   筒壁截面尺寸表：标高 ±0.00~60.00，每 10m 一个控制截面，坡度 i=0.02；
#     外径 5.22→2.82m（R(z)=2610-0.02z）；壁厚 0.26/0.24/0.22/0.20/0.18/0.16m
#     自下而上递减，4 种型号 TB60/1.4/1.7/2.0/2.5 共用同一壁厚表。
#   代号尺寸表：R=顶部筒壁内半径（经反推验证：2820/2-160=1250 ✓），
#     A=4500 顶部平台距顶距离，B=平台外挑宽(1000/1200/1400/1700 随型号)，
#     K=1100 栏杆高度。
#   剖面 1-1：顶部避雷针；2-2：顶部环形钢平台(12 等分)+钢梯；
#     3-3：筒壁/隔热层/内衬三层构造 + 20m 中部钢平台 + 钢梯；
#     4-4：底部烟气入口 3250x3050。
#   注：内衬/隔热层厚度图中未标注，按工程惯例默认 120/80 并参数化可调。
#
# 烟囱高度参数化：以图集基准高度 60m 为参照，用户修改"烟囱高度"后：
#   筒壁 6 段高度等比缩放（各段高度 = 烟囱高度/6），壁厚不变；
#   底部/顶部外径保持型号/参数不变（坡度相应变陡）；
#   顶部平台/中部平台/爬梯起步标高等比缩放（readonly 参数展示联动更新）；
#   踏步间距/支撑柱间距/栏杆高等固定尺寸不缩放。
#
# 坐标约定：组件原点位于烟囱轴线与 ±0.00 交点，Z 轴竖直向上，单位 mm。
# 方位约定：烟道口默认朝 +X（方位角 0 度），钢爬梯与中部平台默认朝 -X（180 度）。
# ============================================================================

from pyp3d import *

# ---------------------------------------------------------------------------
# 图集数据表
# ---------------------------------------------------------------------------
# 筒壁分段壁厚（自下而上 6 段，各段高度随烟囱高度等比缩放）—— 05G212 P10 筒壁截面尺寸表
WALL_THICKNESS = [260.0, 240.0, 220.0, 200.0, 180.0, 160.0]

# 筒壁型号: (囱口内径, 顶部平台外挑宽B) —— 05G212 P10 代号尺寸表
MODEL_DATA = {
    'TB60/1.4': (1400.0, 1000.0),
    'TB60/1.7': (1700.0, 1200.0),
    'TB60/2.0': (2000.0, 1400.0),
    'TB60/2.5': (2500.0, 1700.0),
}

REF_HEIGHT = 60000.0       # 图集基准高度（60m），派生标高等比换算基准


class ChimneyWithRailing(Component):
    def __init__(self):
        Component.__init__(self)

        # ---------------- 筒壁主体（05G212 P10 筒壁截面尺寸表）----------------
        self['烟囱高度'] = Attr(60000.0, obvious=True, group='几何属性')
        self['筒壁型号'] = Attr('TB60/2.0', obvious=True,
                                combo=['TB60/1.4', 'TB60/1.7', 'TB60/2.0', 'TB60/2.5'], group='几何属性')
        self['顶部筒壁外直径'] = Attr(2820.0, obvious=True, group='几何属性')

        # ---------------- 内衬与隔热层（厚度图中未标注，按工程惯例可调）----------------
        self['生成内衬隔热'] = Attr('是', obvious=True, combo=['是', '否'], group='几何属性')
        self['隔热层厚度'] = Attr(80.0, obvious=True, group='几何属性')
        self['内衬厚度'] = Attr(120.0, obvious=True, group='几何属性')

        # ---------------- 烟气入口（4-4 剖面，地面烟道 3250x3050）----------------
        self['烟道口宽'] = Attr(3250.0, obvious=True, group='几何属性')
        self['烟道口高'] = Attr(3050.0, obvious=True, group='几何属性')
        self['烟道口方位角'] = Attr(0.0, obvious=True, group='几何属性')

        # ---------------- 顶部平台与栏杆（2-2 剖面，A=4500，K=1100）----------------
        self['顶部平台标高'] = Attr(55500.0, obvious=True, readonly=True, group='几何属性')
        self['平台板厚'] = Attr(100.0, obvious=True, group='几何属性')
        self['栏杆高度'] = Attr(1100.0, obvious=True, group='几何属性')
        self['栏杆立柱数'] = Attr(12, obvious=True, group='几何属性')
        self['避雷针高度'] = Attr(3000.0, obvious=True, group='几何属性')

        # ---------------- 中部平台与钢爬梯（3-3 剖面，20m 标高）----------------
        self['生成中部平台'] = Attr('是', obvious=True, combo=['是', '否'], group='几何属性')
        self['中部平台标高'] = Attr(20000.0, obvious=True, readonly=True, group='几何属性')
        self['中部平台外挑'] = Attr(1200.0, obvious=True, group='几何属性')
        self['生成爬梯'] = Attr('是', obvious=True, combo=['是', '否'], group='几何属性')
        self['爬梯方位角'] = Attr(180.0, obvious=True, group='几何属性')
        self['爬梯起步标高'] = Attr(2500.0, obvious=True, readonly=True, group='几何属性')
        self['爬梯踏步间距'] = Attr(300.0, obvious=True, group='几何属性')
        self['支撑柱间距'] = Attr(5000.0, obvious=True, group='几何属性')
        self['支撑柱直径'] = Attr(20.0, obvious=True, group='几何属性')

        # ---------------- 专业属性 ----------------
        self['筒壁混凝土'] = Attr('C30', obvious=True, combo=['C30', 'C35', 'C40'], group='专业属性')
        self['钢件材质'] = Attr('Q235B', obvious=True, combo=['Q235B', 'Q355B'], group='专业属性')
        self['图集编号'] = Attr('05G212', obvious=True, readonly=True, group='专业属性')

        # 输出槽位
        self['烟囱模型'] = Attr(None, show=True)

        # 驱动点：组件原点（烟囱轴线与 ±0.00 交点）
        self.setDrivenFeaturePoint('point_origin', SnapMode.GeometricCenter,
                                   '[定位点X]', '[定位点Y]', '[定位点Z]')
        self.replace()

    # ------------------------------------------------------------------
    # 筒壁外半径：沿高度线性，底部外半径 → 顶部外半径
    # 验证 TB60/2.0: R(0)=2610(外径5.22m), R(60000)=1410(外径2.82m) ✓
    # ------------------------------------------------------------------
    def _r_out(self, z):
        return self._r_bot - (self._r_bot - self._r_top) * z / self._H

    # ------------------------------------------------------------------
    # 空心回转壳段（锥/柱通用），内腔切刀两端各外延 10mm 保证切穿
    # ------------------------------------------------------------------
    def _hollow_shell(self, zb, zt, r_out_b, r_out_t, wall):
        slope = (r_out_b - r_out_t) / (zt - zb)
        outer = Cone(Vec3(0, 0, zb), Vec3(0, 0, zt), r_out_b, r_out_t)
        inner = Cone(Vec3(0, 0, zb - 10), Vec3(0, 0, zt + 10),
                     r_out_b - wall + 10 * slope, r_out_t - wall - 10 * slope)
        return outer - inner

    # ------------------------------------------------------------------
    # 径向矩形开洞切刀（沿 +X 方向穿透，再按方位角旋转）
    # ------------------------------------------------------------------
    def _opening_cutter(self, width, height, z_bottom, azimuth_deg, r_reach):
        cutter = Box(Vec3(0, -width / 2, z_bottom),
                     Vec3(0, -width / 2, z_bottom + height),
                     Vec3(1, 0, 0), Vec3(0, 1, 0),
                     r_reach, width, r_reach, width)
        return rotz(azimuth_deg * pi / 180.0) * cutter

    # ------------------------------------------------------------------
    # 圆形截面圆环（栏杆横杆）：Sweep 沿圆形路径扫掠圆形截面
    # ------------------------------------------------------------------
    def _ring(self, ring_r, tube_r, z):
        section_2d = translate(ring_r, 0) * scale(tube_r, tube_r) * Section(Arc(2.0 * pi))
        section_3d = rotate(Vec3(1, 0, 0), -0.5 * pi) * section_2d
        return translate(0, 0, z) * Sweep(section_3d, Line(Arc(2.0 * pi)))

    @export
    def replace(self):
        # ---------------- 读取参数并派生尺寸 ----------------
        d_exit, plat_b = MODEL_DATA[self['筒壁型号']]
        r_exit = d_exit / 2.0
        H = float(self['烟囱高度'])
        k = H / REF_HEIGHT
        self._H = H
        self._r_bot = r_exit + 1610.0                 # 底部外半径（型号决定）
        self._r_top = float(self['顶部筒壁外直径']) / 2.0
        seg_h = H / 6.0                               # 每段高度（6 段等比）

        # 派生标高：随烟囱高度等比缩放（readonly 参数展示联动更新）
        z_plat = 55500.0 * k
        z_mid = 20000.0 * k
        z_lad0 = 2500.0 * k
        self['顶部平台标高'] = z_plat
        self['中部平台标高'] = z_mid
        self['爬梯起步标高'] = z_lad0

        t_ins = float(self['隔热层厚度'])
        t_lin = float(self['内衬厚度'])
        flue_w = float(self['烟道口宽'])
        flue_h = float(self['烟道口高'])
        flue_az = float(self['烟道口方位角'])
        t_plat = float(self['平台板厚'])
        h_rail = float(self['栏杆高度'])
        n_post = int(self['栏杆立柱数'])
        h_needle = float(self['避雷针高度'])
        b_mid = float(self['中部平台外挑'])
        lad_az = float(self['爬梯方位角'])
        rung_step = float(self['爬梯踏步间距'])
        brace_step = float(self['支撑柱间距'])
        d_brace = float(self['支撑柱直径'])

        # ---------------- 参数校验 ----------------
        if H <= 0:
            raise Exception('烟囱高度错误: 必须为正值')
        if self._r_top <= 0 or self._r_top >= self._r_bot:
            raise Exception('顶部筒壁外直径错误: 需为正值且小于底部外直径')
        if t_ins < 0 or t_lin < 0:
            raise Exception('厚度参数错误: 隔热层/内衬厚度不能为负')
        r_min_top = self._r_top - WALL_THICKNESS[-1] - t_ins - t_lin
        if r_min_top <= 100:
            raise Exception('厚度参数错误: 顶部扣除壁厚/隔热/内衬后内腔不足')
        if flue_h > seg_h:
            raise Exception('烟道口参数错误: 烟道口高度超出底部段范围(烟囱高度/6)')
        if n_post < 3:
            raise Exception('栏杆参数错误: 栏杆立柱数不少于 3')
        if brace_step <= 0 or d_brace <= 0:
            raise Exception('支撑柱参数错误: 支撑柱间距与直径必须为正值')

        parts = []
        conc_color = (0.75, 0.75, 0.73, 1.0)    # 混凝土筒壁
        ins_color = (0.90, 0.85, 0.60, 1.0)     # 隔热层
        lin_color = (0.76, 0.48, 0.36, 1.0)     # 内衬
        steel_color = (0.45, 0.50, 0.58, 1.0)   # 钢平台/爬梯/避雷针
        rail_color = (0.70, 0.72, 0.75, 1.0)    # 栏杆

        # 烟道口切刀：穿透筒壁+隔热层+内衬（共用）
        flue_cut = self._opening_cutter(flue_w, flue_h, 0.0, flue_az,
                                        self._r_out(0.0) + 300.0)

        # ==================================================================
        # 一、筒壁：6 段变坡空心圆台壳（外表面连续坡，内表面壁厚突变台阶），
        #     各段高度 = 烟囱高度/6，底段开烟道口
        # ==================================================================
        for i, tw in enumerate(WALL_THICKNESS):
            zb = i * seg_h
            zt = (i + 1) * seg_h
            shell = self._hollow_shell(zb, zt, self._r_out(zb), self._r_out(zt), tw)
            if i == 0:
                shell = shell - flue_cut
            parts.append(shell.color(*conc_color))

        # ==================================================================
        # 二、隔热层 + 内衬：贴筒壁内侧逐段跟随（可开关）
        # ==================================================================
        if self['生成内衬隔热'] == '是':
            for i, tw in enumerate(WALL_THICKNESS):
                zb = i * seg_h
                zt = (i + 1) * seg_h
                r_in_b = self._r_out(zb) - tw
                r_in_t = self._r_out(zt) - tw
                ins = self._hollow_shell(zb, zt, r_in_b, r_in_t, t_ins)
                lin = self._hollow_shell(zb, zt, r_in_b - t_ins, r_in_t - t_ins, t_lin)
                if i == 0:
                    ins = ins - flue_cut
                    lin = lin - flue_cut
                parts.append(ins.color(*ins_color))
                parts.append(lin.color(*lin_color))

        # ==================================================================
        # 三、顶部环形平台：标高随高度等比缩放（60m 时距顶 A=4500），
        #     内缘嵌入筒壁 50，外挑 B 随型号（TB60/2.0 时 B=1400），板厚 100
        # ==================================================================
        r_wall_plat = self._r_out(z_plat)
        r_plat_out = r_wall_plat + plat_b
        plat_ring = Cone(Vec3(0, 0, z_plat - t_plat), Vec3(0, 0, z_plat),
                         r_plat_out, r_plat_out) - \
                    Cone(Vec3(0, 0, z_plat - t_plat - 10), Vec3(0, 0, z_plat + 10),
                         r_wall_plat - 50.0, r_wall_plat - 50.0)
        parts.append(plat_ring.color(*steel_color))

        # ==================================================================
        # 四、栏杆：立柱 φ48 沿平台外缘内缩 50 均布（默认 12 根，对应 2-2
        #     剖面 12 等分），两道 φ30 圆环横杆（顶 K=1100 / 中 550）
        # ==================================================================
        r_rail = r_plat_out - 50.0
        for k in range(n_post):
            ang = 2.0 * pi * k / n_post
            px, py = r_rail * cos(ang), r_rail * sin(ang)
            post = Cone(Vec3(px, py, z_plat), Vec3(px, py, z_plat + h_rail), 24.0, 24.0)
            parts.append(post.color(*rail_color))
        parts.append(self._ring(r_rail, 15.0, z_plat + h_rail).color(*rail_color))
        parts.append(self._ring(r_rail, 15.0, z_plat + h_rail / 2.0).color(*rail_color))

        # ==================================================================
        # 五、避雷针：4 根环形阵列，间隔 90°，置于顶部筒壁圆环顶面的
        #     圆环截面中点半径处（内半径 + 0.5*(外半径-内半径)）
        # ==================================================================
        r_out_top = self._r_out(H)
        r_in_top = r_out_top - WALL_THICKNESS[-1]   # 顶部壁厚
        r_needle = r_in_top + 0.5 * (r_out_top - r_in_top)
        for k in range(4):
            ang = 2.0 * pi * k / 4.0
            px, py = r_needle * cos(ang), r_needle * sin(ang)
            needle = Cone(Vec3(px, py, H), Vec3(px, py, H + h_needle), 20.0, 8.0)
            parts.append(needle.color(*steel_color))

        # ==================================================================
        # 六、中部平台：标高随高度等比缩放（60m 时 20m），完整圆环外挑板，
        #     带一圈栏杆
        # ==================================================================
        if self['生成中部平台'] == '是':
            r_wall_mid = self._r_out(z_mid)
            r_mid_out = r_wall_mid + b_mid
            mid_ring = Cone(Vec3(0, 0, z_mid - t_plat), Vec3(0, 0, z_mid),
                            r_mid_out, r_mid_out) - \
                       Cone(Vec3(0, 0, z_mid - t_plat - 10), Vec3(0, 0, z_mid + 10),
                            r_wall_mid - 50.0, r_wall_mid - 50.0)
            parts.append(mid_ring.color(*steel_color))

            # 中部平台栏杆：完整圆环，立柱 φ48 沿整圈外缘内缩 50 均布
            # （与顶部同密度 n_post 根），两道 φ30 整圆横杆（顶/中）
            r_mid_rail = r_mid_out - 50.0
            for k in range(n_post):
                ang = 2.0 * pi * k / n_post
                px, py = r_mid_rail * cos(ang), r_mid_rail * sin(ang)
                post = Cone(Vec3(px, py, z_mid), Vec3(px, py, z_mid + h_rail), 24.0, 24.0)
                parts.append(post.color(*rail_color))
            parts.append(self._ring(r_mid_rail, 15.0, z_mid + h_rail).color(*rail_color))
            parts.append(self._ring(r_mid_rail, 15.0, z_mid + h_rail / 2.0).color(*rail_color))

        # ==================================================================
        # 七、钢爬梯：贴筒壁外皮外偏 250，双立柱 φ40 随坡度内收，
        #     踏步 φ20 按间距均布，自起步标高至顶部平台
        # ==================================================================
        if self['生成爬梯'] == '是':
            off = 250.0       # 梯中心距筒壁外表面
            half_w = 250.0    # 梯半宽
            az = lad_az * pi / 180.0
            ux, uy = cos(az), sin(az)      # 径向（朝向）
            vx, vy = -sin(az), cos(az)     # 切向（梯宽方向）

            def lad_point(z, along):
                r = self._r_out(z) + off
                return Vec3(ux * r + vx * along, uy * r + vy * along, z)

            # 双立柱
            for s in (-half_w, half_w):
                col = Cone(lad_point(z_lad0, s), lad_point(z_plat, s), 20.0, 20.0)
                parts.append(col.color(*steel_color))

            # 踏步
            n_rung = int((z_plat - z_lad0) / rung_step)
            for i in range(n_rung + 1):
                z = z_lad0 + i * rung_step
                rung = Cone(lad_point(z, -half_w), lad_point(z, half_w), 10.0, 10.0)
                parts.append(rung.color(*steel_color))

            # 附墙支撑柱：每 5000 一层，左右立柱各一根径向短柱连到筒壁外皮
            def wall_point(z, along):
                r = self._r_out(z)
                return Vec3(ux * r + vx * along, uy * r + vy * along, z)

            r_brace = d_brace / 2.0
            z_brace = z_lad0
            while z_brace <= z_plat + 1e-6:
                for s in (-half_w, half_w):
                    brace = Cone(lad_point(z_brace, s), wall_point(z_brace, s),
                                 r_brace, r_brace)
                    parts.append(brace.color(*steel_color))
                z_brace += brace_step

        # ---------------- 汇总输出：并集统一用 combine ----------------
        self['烟囱模型'] = combine(*parts)


if __name__ == "__main__":
    FinalGeometry = ChimneyWithRailing()
    place(FinalGeometry)
