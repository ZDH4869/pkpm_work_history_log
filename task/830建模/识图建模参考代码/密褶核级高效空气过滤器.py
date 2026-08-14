from pyp3d import *
import math
from math import pi, sqrt, tan


# ============================================================
# 辅助函数: 生成单片板式密褶滤芯(平行四边形大板)
# 俯视X-Y平面, 单片滤芯为平行四边形:
#   长边 = 沿板方向(从y1斜穿到y2)
#   短边 = thickness (板厚, 沿X水平方向)
# 沿Z方向从z_base拉伸高度H
# ============================================================
def make_filter_board(x1, y1, x2, y2, thickness, H, z_base):
    dx = x2 - x1
    dy = y2 - y1
    L = sqrt(dx * dx + dy * dy)
    if L < 1e-6:
        return None

    half_t = thickness / 2.0

    # 短边沿X方向(水平), 俯视四边形短边水平
    p1 = Vec2(x1 - half_t, y1)
    p2 = Vec2(x1 + half_t, y1)
    p3 = Vec2(x2 + half_t, y2)
    p4 = Vec2(x2 - half_t, y2)

    sec_bot = translate(0, 0, z_base) * Section(p1, p2, p3, p4)
    sec_top = translate(0, 0, z_base + H) * Section(p1, p2, p3, p4)
    return Loft(sec_bot, sec_top)


# ============================================================
# 方形核级高效空气过滤器(密褶) 参数化组件
# 执行标准: GB/T 17939-2015
# 结构形式: 密褶(图2)
#   - 按所需褶幅高度将滤料往返折叠
#   - 用滤纸条或纤维线支撑被折叠的滤料
#   - 制成单片板式密褶滤芯(平行四边形大板)
#   - 将若干单片滤芯装配成"V"型结构
#   - 每片滤芯斜穿过滤器内部(y=sealant_t到y=D-sealant_t)
#   - 两个板子之间夹角=V型夹角(30度)
# 坐标约定: 原点为过滤器底面左前角点
#   X轴: 宽度方向(+X向右)  Y轴: 深度方向(+Y向后, 气流方向)  Z轴: 高度方向(+Z向上)
# 过滤器占据 x in [0,W], y in [0,D], z in [0,H]
# 进风端面在y=0, 出风端面在y=D; 密封垫在y<0侧(进风端面外侧)
# V型结构: V开口朝向进风面, 顶点在出风面
#   D_eff = D - 2*sealant_t (扣除密封胶后的有效深度)
#   hw = D_eff * tan(V型夹角/2)
#   左板: 从(cx-hw, sealant_t)斜穿到(cx-fold_h/2, D-sealant_t)
#   右板: 从(cx+hw, sealant_t)斜穿到(cx+fold_h/2, D-sealant_t)
#   短边=褶幅高度(板厚, 沿X水平方向, 10-20mm)
# ============================================================
class 密褶核级高效空气过滤器(Component):
    def __init__(self):
        Component.__init__(self)

        # === 主尺寸参数 (GB/T 17939-2015 表1) ===
        self['宽度'] = Attr(610.0, obvious=True, group='主尺寸',
                            description='GB/T 17939-2015表1: 203/305/610')
        self['高度'] = Attr(610.0, obvious=True, group='主尺寸',
                            description='GB/T 17939-2015表1: 203/305/610')
        self['深度'] = Attr(292.0, obvious=True, group='主尺寸',
                            description='GB/T 17939-2015表1: 78/150/292')

        # === 边框参数 ===
        self['边框边宽'] = Attr(18.0, obvious=True, group='边框参数',
                              description='密褶>=18mm')
        self['边框厚度'] = Attr(1.0, obvious=True, group='边框参数',
                              description='碳钢>=1mm, 不锈钢>=1mm, 冲压成型')

        # === 滤芯参数 ===
        self['滤芯折数'] = Attr(5, obvious=True, group='滤芯参数',
                             description='V型单元数, 对应型号-5V/-6V/-8V, 每个V含2片滤芯')
        self['滤料厚度'] = Attr(1.0, obvious=True, group='滤芯参数',
                             description='建模厚度, 实际滤纸<1mm')
        self['褶幅高度'] = Attr(15.0, obvious=True, group='滤芯参数',
                             description='单片滤芯板厚(平行四边形短边), 10-25mm')

        # === 密封参数 ===
        self['密封胶厚度'] = Attr(5.0, obvious=True, group='密封参数',
                              description='密封胶用于滤芯/防护网与边框的密封')
        self['密封垫宽度'] = Attr(17.0, obvious=True, group='密封参数',
                              description='GB/T 17939 6.5.3.1: 长方形断面17mm+-1mm')
        self['密封垫厚度'] = Attr(7.0, obvious=True, group='密封参数',
                              description='GB/T 17939 6.5.3.1: 厚度7mm')

        # === 防护网参数 ===
        self['防护网丝径'] = Attr(1.5, obvious=True, group='防护网参数',
                              description='GB/T 17939 6.4.7: 0.5mm, 建模放大')
        self['防护网网孔'] = Attr(6.4, obvious=True, group='防护网参数',
                              description='GB/T 17939 6.4.7: 6.4mm正方形(4目)')

        # === 部件显示开关 ===
        self['显示边框'] = Attr(True, obvious=True, group='显示开关')
        self['显示滤芯'] = Attr(True, obvious=True, group='显示开关')
        self['显示防护网'] = Attr(True, obvious=True, group='显示开关')
        self['显示密封垫'] = Attr(True, obvious=True, group='显示开关')
        self['显示密封胶'] = Attr(True, obvious=True, group='显示开关')

        # === 业务属性 ===
        self['厂家'] = Attr('河南核净', obvious=True, group='业务属性',
                         description='GB/T 17939-2015起草单位')
        self['标准'] = Attr('GB/T 17939-2015', obvious=True, group='业务属性')
        self['型号'] = Attr('610x610x292-5V', obvious=True, group='业务属性',
                         description='表1序号7: 610x610x292-5V, 2100m3/h')
        self['额定风量'] = Attr('2100 m^3/h', obvious=True, group='业务属性')
        self['初阻力'] = Attr('<=250 Pa', obvious=True, group='业务属性')
        self['效率'] = Attr('>=99.99% (钠焰法)', obvious=True, group='业务属性')
        self['边框材质'] = Attr('不锈钢板', obvious=True, group='业务属性',
                         description='碳钢板(镀锌)/不锈钢板(GB/T 3280)')
        self['滤材'] = Attr('超细玻璃纤维滤纸', obvious=True, group='业务属性')
        self['分隔物材质'] = Attr('滤纸条或纤维线', obvious=True, group='业务属性',
                         description='玻璃纤维滤纸条/不可燃纤维线, 具有自熄性')
        self['密封垫材质'] = Attr('闭孔海绵氯丁橡胶', obvious=True, group='业务属性',
                         description='闭孔海绵氯丁橡胶/硅橡胶, 邵尔AO硬度28+-5')
        self['防护网材质'] = Attr('不锈钢电焊网', obvious=True, group='业务属性')
        self['运行温度'] = Attr('<=80 摄氏度', obvious=True, group='业务属性',
                         description='常温型<=80C, 耐高温型<=250C')
        self['耐辐照剂量'] = Attr('6x10^5 Gy', obvious=True, group='业务属性',
                         description='累积吸收剂量>=6x10^5 Gy')

        # === 输出几何 ===
        self['过滤器'] = Attr(None, show=True)

        # === 定位驱动点 ===
        self.setDrivenFeaturePoint('定位点', SnapMode.EndPoint,
                                   '[定位点X]', '[定位点Y]', '[定位点Z]')
        self.setDrivenFeaturePoint('进风面中心', SnapMode.GeometricCenter,
                                   '[定位点X] + [宽度]/2',
                                   '[定位点Y]',
                                   '[定位点Z] + [高度]/2')
        self.setDrivenFeaturePoint('出风面中心', SnapMode.GeometricCenter,
                                   '[定位点X] + [宽度]/2',
                                   '[定位点Y] + [深度]',
                                   '[定位点Z] + [高度]/2')

        self.replace()

    @export
    def replace(self):
        # === 读取参数 ===
        W = float(self['宽度'])
        H = float(self['高度'])
        D = float(self['深度'])
        fw = float(self['边框边宽'])
        ft = float(self['边框厚度'])
        n_v = max(int(self['滤芯折数']), 4)
        n_v = min(n_v, 15)
        
        fold_h = float(self['褶幅高度'])
        sealant_t = float(self['密封胶厚度'])
        gasket_w = float(self['密封垫宽度'])
        gasket_t = float(self['密封垫厚度'])
        net_wire = float(self['防护网丝径'])
        net_mesh = float(self['防护网网孔'])

        # === 硬约束 ===
        W = max(W, 200.0)
        W = min(W, 700.0)
        H = max(H, 200.0)
        H = min(H, 700.0)
        D = max(D, 70.0)
        D = min(D, 300.0)
        fw = min(fw, W / 3.0, H / 3.0)
        fw = max(fw, 10.0)
        ft = max(min(ft, fw / 2.0), 0.5)
        fold_h = max(min(fold_h, 25.0), 10.0)
        sealant_t = min(sealant_t, fw / 2.0, D / 4.0)
        gasket_w = min(gasket_w, W / 4.0, H / 4.0)
        net_wire = max(net_wire, 1.0)
        net_wire = min(net_wire, 2.5)
        net_mesh = max(net_mesh, 6.0)
        net_mesh = min(net_mesh, 10.0)

        # === 派生尺寸 ===
        inner_W = max(W - 2 * fw, 10.0)
        inner_H = max(H - 2 * fw, 10.0)

        # === V型夹角计算(随滤芯折数自适应, 不碰撞) ===
        # 滤芯Y范围避开进出风端密封胶: y in [sealant_t, D-sealant_t]
        # 有效深度 D_eff = D - 2*sealant_t
        D_eff = max(D - 2.0 * sealant_t, 10.0)
        # 碰撞约束: 2*hw + fold_h <= spacing
        #   hw = D_eff*tan(v_angle/2), spacing = inner_W/n_v
        #   => v_angle = 2*atan((spacing - fold_h) / (2*D_eff))
        # 上限30度(GB/T 17939典型值), 折数少时取上限, 折数多时自动缩减
        spacing = inner_W / n_v
        avail = max(spacing - fold_h, 1.0)
        v_angle = 2.0 * math.degrees(math.atan(avail / (2.0 * D_eff)))
        v_angle = min(v_angle, 30.0)
        if v_angle < 5.0:
            # 夹角不足5度, 减少折数至不碰撞上限
            n_v = max(int(inner_W / (2.0 * D_eff * tan(5.0 * pi / 360.0) + fold_h)), 1)
            spacing = inner_W / n_v
            avail = max(spacing - fold_h, 1.0)
            v_angle = 2.0 * math.degrees(math.atan(avail / (2.0 * D_eff)))
            v_angle = min(v_angle, 30.0)
            print('[密褶过滤器] 滤芯折数缩减至 %d 以避免碰撞' % n_v)
        print('[密褶过滤器] V型夹角=%.1f 度 (折数=%d)' % (v_angle, n_v))

        # V型结构: hw = D_eff * tan(V型夹角/2)
        hw = D_eff * tan(v_angle * pi / 360.0)
        # V型顶点偏移: 短边水平, 左右板在顶点处X间距 = 2*apex_offset >= fold_h
        apex_offset = min(fold_h / 2.0, hw * 0.9)

        parts = []

        # ------------------------------------------------------------
        # 1. 边框: 矩形管, 四面围合, 前后(y=0, y=D)开放
        # ------------------------------------------------------------
        if self['显示边框']:
            left = translate(0, 0, 0) * scale(fw, D, H) * Cube()
            right = translate(W - fw, 0, 0) * scale(fw, D, H) * Cube()
            bottom = translate(fw, 0, 0) * scale(inner_W, D, fw) * Cube()
            top = translate(fw, 0, H - fw) * scale(inner_W, D, fw) * Cube()
            parts.append(combine(left, right, bottom, top).color(0.65, 0.67, 0.70, 1.0))

        # ------------------------------------------------------------
        # 2. 滤芯: 若干单片板式密褶滤芯(平行四边形大板)装配成V型结构
        #    滤芯Y范围 [sealant_t, D-sealant_t], 避开进出风端密封胶和防护网
        #    俯视: 长边沿板方向(斜), 短边沿X(水平)=褶幅高度(板厚)
        #    每个V单元含2片滤芯, 夹角=V型夹角
        #    V开口朝向进风面(y=sealant_t), 顶点在出风面(y=D-sealant_t)
        #    左滤芯: 从(cx-hw, sealant_t)斜穿到(cx-apex_offset, D-sealant_t)
        #    右滤芯: 从(cx+hw, sealant_t)斜穿到(cx+apex_offset, D-sealant_t)
        #    apex_offset=fold_h/2 分离顶点, 避免左右板板厚重叠
        # ------------------------------------------------------------
        if self['显示滤芯']:
            spacing = inner_W / n_v
            v_parts = []
            for i in range(n_v):
                cx = fw + (i + 0.5) * spacing
                left_board = make_filter_board(cx - hw, sealant_t,
                                               cx - apex_offset, D - sealant_t,
                                               fold_h, inner_H, fw)
                right_board = make_filter_board(cx + hw, sealant_t,
                                                cx + apex_offset, D - sealant_t,
                                                fold_h, inner_H, fw)
                if left_board is not None:
                    v_parts.append(left_board)
                if right_board is not None:
                    v_parts.append(right_board)
            if len(v_parts) > 0:
                parts.append(combine(*v_parts).color(0.85, 0.82, 0.72, 1.0))

        # ------------------------------------------------------------
        # 3. 防护网: 进风面(y=0)和出风面(y=D)的网格栅
        # ------------------------------------------------------------
        if self['显示防护网']:
            net_parts = []
            for face_y in [0, D - net_wire]:
                n_h = max(int(inner_W / (net_mesh * 3)), 3)
                for i in range(n_h):
                    xi = fw + inner_W * (i + 1) / (n_h + 1) - net_wire / 2
                    net_parts.append(translate(xi, face_y, fw) * scale(net_wire, net_wire, inner_H) * Cube())
                n_v_net = max(int(inner_H / (net_mesh * 3)), 3)
                for i in range(n_v_net):
                    zi = fw + inner_H * (i + 1) / (n_v_net + 1) - net_wire / 2
                    net_parts.append(translate(fw, face_y, zi) * scale(inner_W, net_wire, net_wire) * Cube())
            if len(net_parts) > 0:
                parts.append(combine(*net_parts).color(0.40, 0.42, 0.45, 1.0))

        # ------------------------------------------------------------
        # 4. 密封垫: 进风端面(y=0)外侧, 沿周长环绕
        # ------------------------------------------------------------
        if self['显示密封垫']:
            g_parts = []
            g_parts.append(translate(0, -gasket_t, 0) * scale(W, gasket_t, gasket_w) * Cube())
            g_parts.append(translate(0, -gasket_t, H - gasket_w) * scale(W, gasket_t, gasket_w) * Cube())
            g_parts.append(translate(0, -gasket_t, gasket_w) * scale(gasket_w, gasket_t, H - 2 * gasket_w) * Cube())
            g_parts.append(translate(W - gasket_w, -gasket_t, gasket_w) * scale(gasket_w, gasket_t, H - 2 * gasket_w) * Cube())
            parts.append(combine(*g_parts).color(0.20, 0.20, 0.22, 1.0))

        # ------------------------------------------------------------
        # 5. 密封胶: 滤芯与边框之间的密封, 位于滤芯前后端面周边
        # ------------------------------------------------------------
        if self['显示密封胶']:
            s_parts = []
            for sy in [0, D - sealant_t]:
                s_parts.append(translate(fw, sy, fw) * scale(inner_W, sealant_t, sealant_t) * Cube())
                s_parts.append(translate(fw, sy, H - fw - sealant_t) * scale(inner_W, sealant_t, sealant_t) * Cube())
                s_parts.append(translate(fw, sy, fw) * scale(sealant_t, sealant_t, inner_H) * Cube())
                s_parts.append(translate(W - fw - sealant_t, sy, fw) * scale(sealant_t, sealant_t, inner_H) * Cube())
            if len(s_parts) > 0:
                parts.append(combine(*s_parts).color(0.50, 0.48, 0.45, 1.0))

        # === 组合所有部件输出 ===
        if len(parts) > 0:
            self['过滤器'] = translate(0, -D, 0) * combine(*parts)
        else:
            self['过滤器'] = None


# === 主程序 ===
if __name__ == "__main__":
    FinalGeometry = 密褶核级高效空气过滤器()
    FinalGeometry.replace()
    place(FinalGeometry)
