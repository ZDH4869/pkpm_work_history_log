from pyp3d import *
import math

class 拱形屋面_三点坐标(Component):
    def __init__(self):
        Component.__init__(self)
        self['构件名称']=Attr('拱形屋面_三点坐标', obvious = True, readonly = False)
        self['拱形半径']=Attr(1360.0, obvious = True, readonly = False)
        self['弦长']=Attr(1800.0, obvious = True)
        self['屋面厚度']=Attr(60.0, obvious = True)
        self['路径倒角']=Attr(2000.0, obvious = True)
        self['显示路径线']=Attr('否', obvious = True, combo = ['否', '是'])

        # 起点A坐标
        self['A点x值']=Attr(0.0, obvious = True, group='起点A坐标') 
        self['A点y值']=Attr(0.0, obvious = True, group='起点A坐标') 
        self['A点z值']=Attr(0.0, obvious = True, group='起点A坐标') 

        # 中间点B坐标
        self['B点x值']=Attr(5000.0, obvious = True, group='中间点B坐标')
        self['B点y值']=Attr(2000.0, obvious = True, group='中间点B坐标') 
        self['B点z值']=Attr(0.0, obvious = True, group='中间点B坐标') 

        # 终点C坐标
        self['C点x值']=Attr(10000.0, obvious = True, group='终点C坐标') 
        self['C点y值']=Attr(5000.0, obvious = True, group='终点C坐标') 
        self['C点z值']=Attr(0.0, obvious = True, group='终点C坐标') 
       
        self['拱形屋面_三点坐标'] = Attr(None, show = True)
        self['路径线'] = Attr(None, show = True)
        
        self.replace()

    @export
    def replace(self):
        # 获取参数
        L = self['弦长']
        R = self['拱形半径']
        H = self['屋面厚度']
        R_fillet = self['路径倒角']

        # 获取三点坐标
        A = Vec3(self['A点x值'], self['A点y值'], self['A点z值'])
        B = Vec3(self['B点x值'], self['B点y值'], self['B点z值'])
        C = Vec3(self['C点x值'], self['C点y值'], self['C点z值'])

        # ========== 1. 构建扫掠路径 (A-B-C折线, 可选B点倒角) ==========
        # 计算向量 AB(A→B) 和 BC(B→C)
        vec_AB = Vec3(B.x - A.x, B.y - A.y, B.z - A.z)
        vec_BC = Vec3(C.x - B.x, C.y - B.y, C.z - B.z)
        len_AB = math.sqrt(vec_AB.x**2 + vec_AB.y**2 + vec_AB.z**2)
        len_BC = math.sqrt(vec_BC.x**2 + vec_BC.y**2 + vec_BC.z**2)
        unit_AB = Vec3(vec_AB.x/len_AB, vec_AB.y/len_AB, vec_AB.z/len_AB)
        unit_BC = Vec3(vec_BC.x/len_BC, vec_BC.y/len_BC, vec_BC.z/len_BC)

        # 倒角为0时退化为折线(A-B-C); 倒角>0时为"直线+倒角弧+直线"整体路径
        use_fillet = R_fillet > 1e-6
        if use_fillet:
            # 倒角切点 P1(AB段, 距B为R_fillet, 沿B→A), P2(BC段, 距B为R_fillet, 沿B→C)
            P1 = Vec3(B.x - unit_AB.x * R_fillet, B.y - unit_AB.y * R_fillet, B.z - unit_AB.z * R_fillet)
            P2 = Vec3(B.x + unit_BC.x * R_fillet, B.y + unit_BC.y * R_fillet, B.z + unit_BC.z * R_fillet)
            # 精确倒角弧(与AB、BC相切): 内角α=BA与BC夹角
            cos_alpha = (-unit_AB.x)*unit_BC.x + (-unit_AB.y)*unit_BC.y + (-unit_AB.z)*unit_BC.z
            cos_alpha = max(-1.0, min(1.0, cos_alpha))  # 钳制防止数值误差
            alpha = math.acos(cos_alpha)
            half_alpha = alpha / 2
            # 角平分线方向(B指向角内) = normalize(-unit_AB + unit_BC)
            bisect = Vec3(-unit_AB.x + unit_BC.x, -unit_AB.y + unit_BC.y, -unit_AB.z + unit_BC.z)
            len_bisect = math.sqrt(bisect.x**2 + bisect.y**2 + bisect.z**2)
            if len_bisect > 1e-6:
                bisect_unit = Vec3(bisect.x/len_bisect, bisect.y/len_bisect, bisect.z/len_bisect)
                # 圆弧半径 r=t*tan(α/2), 圆心到B距离=t/cos(α/2), t=R_fillet(切点距离)
                r_arc = R_fillet * math.tan(half_alpha)
                dist_B_center = R_fillet / math.cos(half_alpha)
                O_arc = Vec3(B.x + bisect_unit.x * dist_B_center, B.y + bisect_unit.y * dist_B_center, B.z + bisect_unit.z * dist_B_center)
                # 弧顶M = 圆心朝B方向r_arc处(角平分线上, 弧的中点)
                M = Vec3(O_arc.x - bisect_unit.x * r_arc, O_arc.y - bisect_unit.y * r_arc, O_arc.z - bisect_unit.z * r_arc)
                # 整体路径: A→(直线)→P1→(倒角弧过M)→P2→(直线)→C, 单次Sweep连续扫掠
                path_whole = Line(A, Arc(P1, M, P2), C)
            else:
                use_fillet = False  # A-B-C共线, 退化为直线
        if not use_fillet:
            # 折线模式: A-B-C作为完整折线路径, 单次Sweep扫掠, B点处连续不断开
            path_whole = Line(A, B, C)

        # ========== 2. 构建局部2D拱形截面 (原点在外弧顶点, 竖直端面) ==========
        # 外弧: 圆心(0,-R), 半径R, 顶点(0,0), 端点(±L/2, d-R), d=√(R²-(L/2)²)
        # 内弧: 圆心(0,-R), 半径R-H, 顶点(0,-H)
        # 竖直端面: 外弧端点x=±L/2向下, 与内弧圆相交于上半圆交点
        d = math.sqrt(R**2 - (L/2)**2)
        y_outer_end = d - R                                    # 外弧端点y(负值)
        inner_half = math.sqrt((R - H)**2 - (L/2)**2)          # 内弧端点到圆心垂距
        y_inner_end = -R + inner_half                          # 内弧端点y(负值, 比外弧端点高)
        # 外弧: 左端→顶点(0,0)→右端
        arc_outer = Arc(Vec2(-L/2, y_outer_end), Vec2(0, 0), Vec2(L/2, y_outer_end))
        # 内弧: 右端→顶点(0,-H)→左端 (逆时针封闭, 反向)
        arc_inner = Arc(Vec2(L/2, y_inner_end), Vec2(0, -H), Vec2(-L/2, y_inner_end))
        # 封闭截面: 外弧左端→外弧→外弧右端→右竖直线下→内弧右端→内弧→内弧左端
        section_local = Section(
            Vec2(-L/2, y_outer_end),
            arc_outer,
            Vec2(L/2, y_outer_end),
            Vec2(L/2, y_inner_end),
            arc_inner,
            Vec2(-L/2, y_inner_end)
        )

        # ========== 3. 截面坐标变换: 法线对齐路径切线, 拱顶(原点)位于路径上 ==========
        # 变换顺序(就近原则, 从右到左生效):
        #   rotx(pi/2): XY平面→XZ平面, 法线Z→-Y, 拱起Y→Z(向上)
        #   rotz(pi/2+theta): 绕Z轴旋转, 使法线(-Y)对齐路径切线方向
        #   translate(origin): 平移到路径起点(拱顶落在路径上)
        def build_section_transform(origin, tangent):
            theta = math.atan2(tangent.y, tangent.x)
            return translate(origin) * rotz(math.pi/2 + theta) * rotx(math.pi/2) * section_local

        # 截面在A, 切线=A→B方向(整体路径起始切线)
        sec_1 = build_section_transform(A, unit_AB)

        # ========== 4. 执行单次整体扫掠 ==========
        # 倒角模式: 路径A→P1→(倒角弧)→P2→C, Sweep沿弧线自动旋转截面法线
        # 折线模式: 路径A→B→C, Sweep在B点处自动转向BC方向
        self['拱形屋面_三点坐标'] = Sweep(sec_1, path_whole)

        # ========== 5. 路径线显隐 ==========
        # path_whole即扫掠路径线, 截面顶点(外弧顶点,原点)经变换后映射到路径起点,
        # 扫掠时拱顶轨迹就是path_whole本身, 故直接输出该路径线即为截面顶点位置的路径线
        if self['显示路径线'] == '是':
            self['路径线'] = path_whole
        else:
            self['路径线'] = None
               
       
# 输出模型
if __name__ == "__main__":
    FinalGeometry = 拱形屋面_三点坐标()
    place(FinalGeometry)
