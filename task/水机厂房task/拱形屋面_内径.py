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
        self['拱顶底墙高']=Attr(2000.0, obvious = True, group='墙体')
        self['墙体厚度']=Attr(300, obvious = True, group='墙体')
       
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
        bool_pos = self['布尔位置']
        wall_height = self['拱顶底墙高']
        
        # ================================================================
        # 公共计算：扫掠路径的旋转角度
        # 旋转角度为 L/2 到 R 的角度
        # 扫略体如果直接用弦长两侧的切割体布尔，会导致放置点与几何受到弧线拟合影响错位
        # 错位导致了放置点坐标轴，与几何不在一起，所以需要旋转扫略体后再布尔
        # ================================================================
        x = L/2
        z0 = math.sqrt(R**2 - (L/2)**2)  # 拱矢高(正值) = 1019.6
        angle_rad = math.atan2(-z0, x)
        
        # ================================================================
        # 第一部分：拱形屋面壳体 (Sweep + 布尔裁剪)
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
        拱形壳体 = translate(L/2,0,-z0)*body

        # ================================================================
        # 第二部分：拱形矩形壳体
        # 截面顶部使用拱形壳体底部内弧 (半径 = R-H, 圆心在 (L/2, -z0))
        # 内弧端点不落在弦线端点上，通过三角填充段连接到弦线端点，
        # 实现矩形壳体顶部与拱形壳体底部的精确贴合
        # ================================================================
        R_inner = R - H  # 拱形壳体内弧半径

        # 拱弧在2D截面(XOY→rotx后映射为XOZ)中的参数:
        # 圆心在 (L/2, -z0), 半径 R_inner
        angle_pos = math.atan2(z0, L/2)        # B 相对圆心的角度 ≈ 0.847 rad
        angle_start = math.pi - angle_pos       # A 相对圆心的角度 ≈ 2.295 rad
        span = angle_start - angle_pos          # 顺时针弧跨度 = π - 2*angle_pos ≈ 1.448 rad

        # 内弧两端在2D截面中的坐标 (与拱形壳体内弧端点精确一致)
        inner_A_x = H * L / (2 * R)
        inner_A_y = -H * z0 / R
        inner_B_x = L - inner_A_x
        inner_B_y = inner_A_y

        # 顺时针内弧线 A_inner→B_inner (经拱顶):
        # 使用与拱形壳体扫掠路径相同的Arc定义方式，保证拟合精度一致
        弧线_cw = translate(L/2, -z0) * rotate(angle_start) * scale(R_inner, R_inner) * Arc(-span)

        # 组合截面:
        #   (0,0) ──直线──→ A_inner ──内弧──→ B_inner ──直线──→ (L,0)
        #     ↑                                                       │
        #     └──────────── 墙体底面 ←────────────── 右侧墙 ──────────┘
        # Section 自动闭合从 (0,-wall_height) 回到 (0,0) 完成左侧墙
        截面_矩形拱 = Section(
            Vec2(0, 0),
            Vec2(inner_A_x, inner_A_y),
            弧线_cw,
            Vec2(L, 0),
            Vec2(L, -wall_height),
            Vec2(0, -wall_height),
        )

        # 将截面从 XOY 旋转到 XOZ 平面，沿 Y 轴拉伸 W
        截面_XOZ = rotx(pi/2) * 截面_矩形拱
        拉伸路径 = Line(Vec3(0, 0, 0), Vec3(0, W, 0))
        矩形壳体 = Sweep(截面_XOZ, 拉伸路径)

        # ================================================================
        # 第三部分：布尔开口 (分别作用于两个独立部件)
        # 布尔体 Z 向拉伸高度 = R + wall_height，贯穿拱形壳体+矩形壳体全高
        # ================================================================
        if bool_pos == "前左":
            布尔体 = translate(0,0,-H*2)*scale(L_x,W_y,R+wall_height)*Cube()
            拱形壳体_结果 = 拱形壳体 - 布尔体
            矩形壳体_结果 = 矩形壳体 - 布尔体
        elif bool_pos == "前右":
            布尔体 = translate(L-L_x,0,-H*2)*scale(L_x,W_y,R+wall_height)*Cube()
            拱形壳体_结果 = 拱形壳体 - 布尔体
            矩形壳体_结果 = 矩形壳体 - 布尔体
        elif bool_pos == "后左":
            布尔体 = translate(0,W-W_y,-H*2)*scale(L_x,W_y,R+wall_height)*Cube()
            拱形壳体_结果 = 拱形壳体 - 布尔体
            矩形壳体_结果 = 矩形壳体 - 布尔体
        elif bool_pos == "后右":
            布尔体 = translate(L-L_x,W-W_y,-H*2)*scale(L_x,W_y,R+wall_height)*Cube()
            拱形壳体_结果 = 拱形壳体 - 布尔体
            矩形壳体_结果 = 矩形壳体 - 布尔体
        else:
            拱形壳体_结果 = 拱形壳体
            矩形壳体_结果 = 矩形壳体

        # 两个独立部件合并输出
        self['拱形屋面_单拱'] = 拱形壳体_结果 + 矩形壳体_结果
               

       
# 输出模型
if __name__ == "__main__":
    FinalGeometry = 拱形屋面_单拱()
    place(FinalGeometry)
