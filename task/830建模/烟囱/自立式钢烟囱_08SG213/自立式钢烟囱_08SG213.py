# -*- coding: utf-8 -*-
# ============================================================================
# 自立式钢烟囱 参数化组件（依据国标图集 08SG213-1《自立式钢烟囱》）
#
# 图纸信息提取（默认值对应图集 30/1.0-1、2、3-tn-M 型，30m 高、出口内径 1.0m）：
#   总说明(P5)  ：适用高度 30/40/50/60m；顶部出口内直径 1.0~4.0m；
#                 烟道入口净尺寸(30m/1.0m 型)=0.9x1.4m；筒身 Q235B、洞口区 Q345B；
#                 内衬厚度 100/75/50mm 三种。
#   立面图(P10) ：0.500~10.000m 为锥段(坡度 i=0.03，壁厚 14mm，底部外径 1.770m)；
#                 10~20m 直段壁厚 10mm；20~30m 直段壁厚 8mm；筒壁外径 1.200m；
#                 10m 处法兰 r660/30M24，20m 处法兰 r640/30M16；
#                 底座环板 r1075、地脚锚栓 20M33 分布圆 r1025、间隔 18 度、
#                 锚固垫板 -200x200x25；清灰口约 2.0m 标高，烟道口位于锥段。
#   基础图(P157)：圆形扩展基础，埋深 3.000m，基础顶 +0.500m 二次浇灌层，
#                 具体 r1/r2/h 按图集基础选用表；本组件按可调参数简化生成。
#   选用表(P9)  ：地震/风载组合控制代码为选型依据，不参与几何，未建模。
#
# 坐标约定：组件原点位于烟囱轴线与 ±0.000(基础短柱顶)交点，Z 轴竖直向上，单位 mm。
# ============================================================================

from pyp3d import *

class SelfSupportingSteelChimney(Component):
    def __init__(self):
        Component.__init__(self)

        # ---------------- 总体尺寸（图集 P5 / P10）----------------
        self['烟囱高度'] = Attr(30000, obvious=True, combo=[30000, 40000, 50000, 60000], group='几何属性')
        self['顶部筒壁外直径'] = Attr(1200.0, obvious=True, group='几何属性')
        self['筒底标高'] = Attr(500.0, obvious=True, group='几何属性')
        self['锥段顶标高'] = Attr(10000.0, obvious=True, group='几何属性')
        self['中段顶标高'] = Attr(20000.0, obvious=True, group='几何属性')
        self['锥段坡度'] = Attr(0.03, obvious=True, group='几何属性')

        # ---------------- 筒壁与内衬（P10 筒壁截面尺寸表）----------------
        self['下段壁厚'] = Attr(14.0, obvious=True, group='几何属性')
        self['中段壁厚'] = Attr(10.0, obvious=True, group='几何属性')
        self['上段壁厚'] = Attr(8.0, obvious=True, group='几何属性')
        self['内衬厚度'] = Attr(100.0, obvious=True, combo=[50.0, 75.0, 100.0], group='几何属性')
        self['生成内衬'] = Attr('是', obvious=True, combo=['是', '否'], group='几何属性')

        # ---------------- 烟道口与清灰口（P5 表1.3 / P10 立面）----------------
        self['烟道口宽'] = Attr(900.0, obvious=True, group='几何属性')
        self['烟道口高'] = Attr(1400.0, obvious=True, group='几何属性')
        self['烟道口底标高'] = Attr(3500.0, obvious=True, group='几何属性')
        self['烟道口方位角'] = Attr(0.0, obvious=True, group='几何属性')
        self['清灰口宽'] = Attr(500.0, obvious=True, group='几何属性')
        self['清灰口高'] = Attr(600.0, obvious=True, group='几何属性')
        self['清灰口底标高'] = Attr(1500.0, obvious=True, group='几何属性')
        self['清灰口方位角'] = Attr(180.0, obvious=True, group='几何属性')

        # ---------------- 法兰连接（P10 剖面 3-3 / 4-4）----------------
        self['下法兰外半径'] = Attr(660.0, obvious=True, group='几何属性')
        self['上法兰外半径'] = Attr(640.0, obvious=True, group='几何属性')
        self['法兰单板厚'] = Attr(20.0, obvious=True, group='几何属性')
        self['法兰螺栓数'] = Attr(30, obvious=True, group='几何属性')
        self['下法兰螺栓直径'] = Attr(24.0, obvious=True, group='几何属性')
        self['上法兰螺栓直径'] = Attr(16.0, obvious=True, group='几何属性')

        # ---------------- 底座与地脚锚栓（P10 剖面 1-1 / 2-2）----------------
        self['底环板内半径'] = Attr(700.0, obvious=True, group='几何属性')
        self['底环板外半径'] = Attr(1075.0, obvious=True, group='几何属性')
        self['底环板厚'] = Attr(25.0, obvious=True, group='几何属性')
        self['肋板数'] = Attr(20, obvious=True, group='几何属性')
        self['肋板高'] = Attr(300.0, obvious=True, group='几何属性')
        self['肋板厚'] = Attr(12.0, obvious=True, group='几何属性')
        self['地脚螺栓直径'] = Attr(33.0, obvious=True, group='几何属性')
        self['螺栓分布圆半径'] = Attr(1025.0, obvious=True, group='几何属性')
        self['锚固板边长'] = Attr(200.0, obvious=True, group='几何属性')
        self['锚固板厚'] = Attr(25.0, obvious=True, group='几何属性')

        # ---------------- 基础（P157 基础图，尺寸按选用表可调）----------------
        self['生成基础'] = Attr('是', obvious=True, combo=['是', '否'], group='几何属性')
        self['基础埋深'] = Attr(3000.0, obvious=True, group='几何属性')
        self['基础底板半径'] = Attr(3000.0, obvious=True, group='几何属性')
        self['基础底板厚'] = Attr(800.0, obvious=True, group='几何属性')
        self['基础短柱半径'] = Attr(1300.0, obvious=True, group='几何属性')

        # ---------------- 专业属性（P5 材料选用）----------------
        self['筒身材质'] = Attr('Q235B(N)', obvious=True, combo=['Q235B(N)', 'Q345B(N)'], group='专业属性')
        self['洞口区材质'] = Attr('Q345B(N)', obvious=True, readonly=True, group='专业属性')
        self['图集编号'] = Attr('08SG213-1', obvious=True, readonly=True, group='专业属性')

        # 输出槽位
        self['烟囱模型'] = Attr(None, show=True)

        # 默认驱动点：组件原点
        self.setDrivenFeaturePoint('point_origin', SnapMode.GeometricCenter, '[定位点X]', '[定位点Y]', '[定位点Z]')
        self.replace()

    # ------------------------------------------------------------------
    # 参数校验：给出可读错误信息，防止退化几何
    # ------------------------------------------------------------------
    def _check(self, z0, z1, z2, H, R_top, t1, t2, t3, tn):
        if not (0 <= z0 < z1 < z2 < H):
            raise Exception('标高参数错误: 需满足 0 <= 筒底标高 < 锥段顶标高 < 中段顶标高 < 烟囱高度')
        if min(t1, t2, t3) <= 0:
            raise Exception('壁厚参数错误: 各段壁厚必须为正值')
        if R_top - max(t1, t2, t3) - tn <= 50:
            raise Exception('直径参数错误: 顶部筒壁外直径过小，扣除壁厚与内衬后内腔不足')
        if self['锥段坡度'] < 0:
            raise Exception('坡度参数错误: 锥段坡度不能为负')
        if self['烟道口底标高'] + self['烟道口高'] > z1:
            raise Exception('烟道口参数错误: 烟道口顶部超出锥段范围，请调低底标高或高度')
        if self['清灰口底标高'] + self['清灰口高'] > z1:
            raise Exception('清灰口参数错误: 清灰口顶部超出锥段范围')
        if self['底环板外半径'] <= self['螺栓分布圆半径']:
            raise Exception('底座参数错误: 螺栓分布圆半径应小于底环板外半径')

    # ------------------------------------------------------------------
    # 工具：径向矩形开洞切刀（沿 +X 方向穿透单侧筒壁，再按方位角旋转）
    # ------------------------------------------------------------------
    def _opening_cutter(self, width, height, z_bottom, azimuth_deg, r_reach):
        cutter = Box(Vec3(0, -width / 2, z_bottom),
                     Vec3(0, -width / 2, z_bottom + height),
                     Vec3(1, 0, 0), Vec3(0, 1, 0),
                     r_reach, width, r_reach, width)
        return rotz(azimuth_deg * pi / 180.0) * cutter

    # ------------------------------------------------------------------
    # 工具：空心回转壳段（锥/柱通用），内腔切刀两端各外延 10mm 保证切穿
    # ------------------------------------------------------------------
    def _hollow_shell(self, zb, zt, r_out_b, r_out_t, wall):
        slope = (r_out_b - r_out_t) / (zt - zb)
        outer = Cone(Vec3(0, 0, zb), Vec3(0, 0, zt), r_out_b, r_out_t)
        inner = Cone(Vec3(0, 0, zb - 10), Vec3(0, 0, zt + 10),
                     r_out_b - wall + 10 * slope, r_out_t - wall - 10 * slope)
        return outer - inner

    @export
    def replace(self):
        # ---------------- 读取参数并派生尺寸 ----------------
        H = float(self['烟囱高度'])
        z0 = float(self['筒底标高'])
        z1 = float(self['锥段顶标高'])
        z2 = float(self['中段顶标高'])
        R_top = float(self['顶部筒壁外直径']) / 2.0
        slope = float(self['锥段坡度'])
        t1 = float(self['下段壁厚'])
        t2 = float(self['中段壁厚'])
        t3 = float(self['上段壁厚'])
        tn = float(self['内衬厚度'])
        R_bot = R_top + slope * (z1 - z0)   # 锥段底部外半径: 600+0.03x9500=885 -> 外径1770

        self._check(z0, z1, z2, H, R_top, t1, t2, t3, tn)

        parts = []
        steel_color = (0.72, 0.75, 0.80, 1.0)
        node_color = (0.45, 0.50, 0.58, 1.0)
        bolt_color = (0.30, 0.32, 0.38, 1.0)

        # ==================================================================
        # 一、钢筒壁：锥段(壁厚t1) + 中段(t2) + 上段(t3)，锥段开烟道口与清灰口
        # ==================================================================
        cone_shell = self._hollow_shell(z0, z1, R_bot, R_top, t1)

        flue_cut = self._opening_cutter(float(self['烟道口宽']), float(self['烟道口高']),
                                        float(self['烟道口底标高']), float(self['烟道口方位角']),
                                        R_bot + 300)
        ash_cut = self._opening_cutter(float(self['清灰口宽']), float(self['清灰口高']),
                                       float(self['清灰口底标高']), float(self['清灰口方位角']),
                                       R_bot + 300)
        cone_shell = cone_shell - flue_cut
        cone_shell = cone_shell - ash_cut
        parts.append(cone_shell.color(*steel_color))

        mid_shell = self._hollow_shell(z1, z2, R_top, R_top, t2)
        parts.append(mid_shell.color(*steel_color))

        top_shell = self._hollow_shell(z2, H, R_top, R_top, t3)
        parts.append(top_shell.color(*steel_color))

        # ==================================================================
        # 二、内衬：耐酸浇注料内衬贴筒壁内侧，同样在锥段开洞（可开关）
        # ==================================================================
        if self['生成内衬'] == '是':
            lining_color = (0.76, 0.48, 0.36, 1.0)

            cone_lining = self._hollow_shell(z0, z1, R_bot - t1, R_top - t1, tn)
            cone_lining = cone_lining - flue_cut
            cone_lining = cone_lining - ash_cut
            parts.append(cone_lining.color(*lining_color))

            mid_lining = self._hollow_shell(z1, z2, R_top - t2, R_top - t2, tn)
            parts.append(mid_lining.color(*lining_color))

            top_lining = self._hollow_shell(z2, H, R_top - t3, R_top - t3, tn)
            parts.append(top_lining.color(*lining_color))

        # ==================================================================
        # 三、法兰连接：z1、z2 处上下法兰板各一块 + 环向普通螺栓
        #     图集: 10m 处 r660/30M24, 20m 处 r640/30M16
        # ==================================================================
        tf = float(self['法兰单板厚'])
        n_fb = int(self['法兰螺栓数'])
        flange_defs = [
            (z1, float(self['下法兰外半径']), float(self['下法兰螺栓直径']), R_top - t2),
            (z2, float(self['上法兰外半径']), float(self['上法兰螺栓直径']), R_top - t3),
        ]
        for zf, rf_out, d_bolt, rf_in in flange_defs:
            ring_outer = Cone(Vec3(0, 0, zf - tf), Vec3(0, 0, zf + tf), rf_out, rf_out)
            ring_inner = Cone(Vec3(0, 0, zf - tf - 10), Vec3(0, 0, zf + tf + 10), rf_in, rf_in)
            flange_ring = ring_outer - ring_inner
            parts.append(flange_ring.color(*node_color))

            # 螺栓沿分布圆均布，取法兰外伸段中点为分布半径
            rb = (R_top + rf_out) / 2.0
            for k in range(n_fb):
                ang = 2 * pi * k / n_fb
                bx, by = rb * cos(ang), rb * sin(ang)
                bolt = Cone(Vec3(bx, by, zf - tf - 40), Vec3(bx, by, zf + tf + 40),
                            d_bolt / 2.0, d_bolt / 2.0)
                parts.append(bolt.color(*bolt_color))

        # ==================================================================
        # 四、底座节点：底环板(-25) + 径向肋板(-12) + 锚固板(200x200x25)
        #     + 地脚锚栓 20M33，分布圆 r1025，间隔 18 度；肋板与螺栓错开半档
        # ==================================================================
        ri = float(self['底环板内半径'])
        ro = float(self['底环板外半径'])
        tp = float(self['底环板厚'])
        n_rib = int(self['肋板数'])
        h_rib = float(self['肋板高'])
        t_rib = float(self['肋板厚'])
        rb_anchor = float(self['螺栓分布圆半径'])
        d_anchor = float(self['地脚螺栓直径'])
        a_pad = float(self['锚固板边长'])
        t_pad = float(self['锚固板厚'])

        base_ring = Cone(Vec3(0, 0, z0 - tp), Vec3(0, 0, z0), ro, ro) - \
                    Cone(Vec3(0, 0, z0 - tp - 10), Vec3(0, 0, z0 + 10), ri, ri)
        parts.append(base_ring.color(*node_color))

        for k in range(n_rib):
            # 肋板：贴筒壁外侧径向布置，转角与螺栓错开半档
            ang_rib = 2 * pi * k / n_rib + pi / n_rib
            rib = Box(Vec3(R_bot - 10, -t_rib / 2, z0),
                      Vec3(R_bot - 10, -t_rib / 2, z0 + h_rib),
                      Vec3(1, 0, 0), Vec3(0, 1, 0),
                      ro - R_bot + 10, t_rib, ro - R_bot + 10, t_rib)
            parts.append((rotz(ang_rib) * rib).color(*node_color))

            # 锚固板 + 地脚锚栓：位于分布圆上
            ang_bolt = 2 * pi * k / n_rib
            pad = Box(Vec3(rb_anchor - a_pad / 2, -a_pad / 2, z0 + h_rib),
                      Vec3(rb_anchor - a_pad / 2, -a_pad / 2, z0 + h_rib + t_pad),
                      Vec3(1, 0, 0), Vec3(0, 1, 0),
                      a_pad, a_pad, a_pad, a_pad)
            parts.append((rotz(ang_bolt) * pad).color(*node_color))

            bx, by = rb_anchor * cos(ang_bolt), rb_anchor * sin(ang_bolt)
            anchor = Cone(Vec3(bx, by, z0 - tp - 450),
                          Vec3(bx, by, z0 + h_rib + t_pad + 100),
                          d_anchor / 2.0, d_anchor / 2.0)
            parts.append(anchor.color(*bolt_color))

        # ==================================================================
        # 五、基础（可开关）：底板圆柱 + 放坡圆台 + 短柱到 +0.000，
        #     短柱顶至筒底之间为 C35 二次浇灌层，具体尺寸按图集选用表调整
        # ==================================================================
        if self['生成基础'] == '是':
            conc_color = (0.80, 0.80, 0.76, 1.0)
            depth = float(self['基础埋深'])
            r_slab = float(self['基础底板半径'])
            h_slab = float(self['基础底板厚'])
            r_col = float(self['基础短柱半径'])
            if depth <= h_slab:
                raise Exception('基础参数错误: 基础埋深必须大于底板厚')
            if r_slab <= r_col:
                raise Exception('基础参数错误: 底板半径应大于短柱半径')

            slab = Cone(Vec3(0, 0, -depth), Vec3(0, 0, -depth + h_slab), r_slab, r_slab)
            parts.append(slab.color(*conc_color))

            taper = Cone(Vec3(0, 0, -depth + h_slab), Vec3(0, 0, 0), r_slab, r_col)
            parts.append(taper.color(*conc_color))

            grout = Cone(Vec3(0, 0, 0), Vec3(0, 0, z0), ro + 100, ro + 100)
            parts.append(grout.color(0.85, 0.85, 0.82, 1.0))

        # ---------------- 汇总输出：并集统一用 combine ----------------
        self['烟囱模型'] = combine(*parts)


if __name__ == "__main__":
    FinalGeometry = SelfSupportingSteelChimney()
    place(FinalGeometry)
