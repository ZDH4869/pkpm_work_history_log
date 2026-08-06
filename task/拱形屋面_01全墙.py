from pyp3d import *
class 拱形屋面_单拱(Component):
    def __init__(self):
        Component.__init__(self)
        self['构件名称']=Attr('拱形屋面_单拱', obvious = True, readonly = False)
        self['拱形半径']=Attr(1360.0, obvious = True, readonly = False)
        self['弦长']=Attr(1800.0, obvious = True)
        self['屋面长度'] = Attr(3000.0, obvious = True)
        self['屋面厚度']=Attr(60.0, obvious = True)

        # 分组：布尔位置
        self['布尔位置']=Attr("无", obvious = True, readonly = False, combo= ["无","前左","前右","后左","后右"], group='布尔位置')
        self['布尔长']=Attr(900.0, obvious = True, group='布尔位置') 
        self['布尔宽']=Attr(400.0, obvious = True, group='布尔位置') 

        # 分组：墙体
        self['墙体开关']=Attr("无", obvious = True, readonly = False, combo= ["无","有"], group='布尔位置')
        self['拱顶底墙高']=Attr(900.0, obvious = True, group='布尔位置') 
        self['墙体厚度']=Attr(300, obvious = True, group='布尔位置') 
       
        self['拱形屋面_单拱'] = Attr(None, show = True)
        
        self.replace()
    @export
    def replace(self): 
        L = self['弦长']
        R = self['拱形半径']
        H  = self['屋面厚度']
        W  = self['屋面长度']
        W_y = self['布尔长']
        L_x = self['布尔宽']
        布尔位置 = self['布尔位置']
        
        # ================================================================
        # 公共计算：扫掠路径的旋转角度
        # 旋转角度为 L/2 到 R 的角度
        # 扫略体如果直接用弦长两侧的切割体布尔，会导致放置点与几何受到弧线拟合影响错位
        # 错位导致了放置点坐标轴，与几何不在一起，所以需要旋转扫略体后再布尔
        # ================================================================
        x = L/2
        z = -math.sqrt(R**2 - (L/2)**2)
        angle_rad = math.atan2(z, x)
        angle_deg = math.degrees(angle_rad)
        z0 = math.sqrt(R**2 - (L/2)**2)  # 拱矢高(正值) = 1019.6
        
        # ================================================================
        # 第一部分：原有拱形屋面壳体 (Sweep + 布尔裁剪)
        # 半圆环截面沿拱弧路径扫掠 → 三个立方体裁剪 → 定位
        # ================================================================
        扫掠路径 = roty(-angle_rad)*rotx(pi/2)*scale(R,R)*Line(Arc(pi))
        扫掠平面 = Section(Vec2(R,0),Vec2(R,W),Vec2(R-H,W),Vec2(R-H,0))
        # 圆弧精度的控制是对单个扫略体生效，拟合数为32的360度扫略就会导致布尔后精度不够
        # 所以拆分为两个180度先合成一个再做布尔差
        扫掠体_1 = Sweep(扫掠平面,扫掠路径)
        扫掠体_2 = roty(pi)*Sweep(扫掠平面,扫掠路径)
        切割体1 = translate(Vec3(L/2,-W/2,-R))*scale(R-L/2,W*2,R*2.5)*Cube()
        切割体2 = translate(Vec3(-R,-W/2,-R))*scale(R-L/2,W*2,R*2.5)*Cube()
        切割体3 = translate(Vec3(-R*1.5,-W/2,-R*1.5))*scale(R*3,W*2,R*1.5)*Cube()
        body = 扫掠体_1+扫掠体_2-切割体1-切割体2-切割体3
        最终模型 = translate(L/2,0,-z0)*body

        # ================================================================
        # 第二部分：新增拱形矩形壳体 (Section + Sweep 拉伸)
        #
        # 四个节点 (基于最终模型 translate(L/2,0,-z0)*body 后的拱顶曲线):
        #   [最终模型] 弦两端在 (0,0,0) 和 (L,0,0), 弧圆心位于 (L/2, -z0), 半径 R
        #   A  = 拱顶曲线起点 = (0, 0, 0)
        #   B  = 拱顶曲线终点 = (L, 0, 0)
        #   A1 = A 沿 Z 偏移 -2000 = (0, 0, -2000)
        #   B1 = B 沿 Z 偏移 -2000 = (L, 0, -2000)
        #
        # 封闭截面 (顺时针):  A →(弧线CW)→ B →(直线)→ B1 →(直线)→ A1 →(直线)→ A
        # 拉伸方向: Y轴, 起点0 → 终点W (与原有拱壳Y范围一致)
        # 注意: 新壳体基于最终坐标系构建, 无需额外 translate 定位
        # ================================================================
        Z_OFFSET = 2000.0  # A1/B1 沿 Z 轴的偏移量(mm)

        # 拱弧在2D截面(XOY→rotx后映射为XOZ)中的参数:
        # 圆心在 (L/2, -z0), 半径 R
        # A_2d=(0,0), 顶点_2d=(L/2, R-z0), B_2d=(L,0)
        angle_pos = math.atan2(z0, L/2)       # B 相对圆心的角度 ≈ 0.847 rad
        angle_start = math.pi - angle_pos      # A 相对圆心的角度 ≈ 2.295 rad
        span = angle_start - angle_pos         # 顺时针弧跨度 = π - 2*angle_pos ≈ 1.448 rad

        # 顺时针弧线 A→B (经拱顶):
        # Arc(-span): 单位弧顺时针走 span 弧度;rotate(angle_start)使起点对准A方向
        弧线_cw = translate(L/2, -z0) * rotate(angle_start) * scale(R, R) * Arc(-span)

        # 拆为"弓形"(弧+弦)和"矩形"(下墙体)两个独立截面 → 截面布尔并
        # 弓形截面: A →(弧线CW)→ B, Section 自动补全弦 B→A
        # 矩形截面: B→B1→A1→A→B (闭合多边形)
        弓形截面 = Section(Vec2(0, 0), 弧线_cw, Vec2(L, 0))
        矩形截面 = Section(Vec2(L, 0), Vec2(L, -Z_OFFSET), Vec2(0, -Z_OFFSET), Vec2(0, 0), Vec2(L, 0))
        截面_矩形拱 = 弓形截面 + 矩形截面

        # 将截面从 XOY 旋转到 XOZ 平面，沿 Y 轴拉伸
        截面_XOZ = rotx(pi/2) * 截面_矩形拱
        拉伸路径 = Line(Vec3(0, 0, 0), Vec3(0, W, 0))
        拱形矩形壳体 = Sweep(截面_XOZ, 拉伸路径)

        # 新壳体已基于最终模型坐标系构建, 直接与原有拱壳合并
        完整模型 = 最终模型 + 拱形矩形壳体

        # ================================================================
        # 第三部分：布尔开口
        # ================================================================
        if 布尔位置 == "前左":
            布尔体 = translate(0,0,-H*2)*scale(L_x,W_y,R)*Cube()
            self['拱形屋面_单拱'] = 完整模型-布尔体
        elif 布尔位置 == "前右":
            布尔体 = translate(L-L_x,0,-H*2)*scale(L_x,W_y,R)*Cube()
            self['拱形屋面_单拱'] = 完整模型-布尔体
        elif 布尔位置 == "后左":
            布尔体 = translate(0,W-W_y,-H*2)*scale(L_x,W_y,R)*Cube()
            self['拱形屋面_单拱'] = 完整模型-布尔体
        elif 布尔位置 == "后右":
            布尔体 = translate(L-L_x,W-W_y,-H*2)*scale(L_x,W_y,R)*Cube()
            self['拱形屋面_单拱'] = 完整模型-布尔体
        else:
            self['拱形屋面_单拱'] = 完整模型
               

       
# 输出模型
if __name__ == "__main__":
    FinalGeometry = 拱形屋面_单拱()
    place(FinalGeometry)
