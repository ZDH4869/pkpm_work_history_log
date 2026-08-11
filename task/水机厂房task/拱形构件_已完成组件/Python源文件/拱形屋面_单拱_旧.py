from pyp3d import *
class 拱形屋面_单拱(Component):
    def __init__(self):
        Component.__init__(self)
        self['构件名称']=Attr('拱形屋面_单拱', obvious = True, readonly = False)
        self['拱形半径']=Attr(13600, obvious = True, readonly = False)
        self['弦长']=Attr(18000, obvious = True)
        self['屋面长度'] = Attr(30000, obvious = True)
        self['屋面厚度']=Attr(600, obvious = True) 
        
        self['拱形屋面_单拱'] = Attr(None, show = True)
        
        self.replace()
    @export
    def replace(self): 
        L = self['弦长']
        R = self['拱形半径']
        H  = self['屋面厚度']
        W  = self['屋面长度']
        
        # 计算扫掠路径的旋转角度
        # 旋转角度为 L/2 到 R 的角度
        # 扫略体如果直接用弦长两侧的切割体布尔，会导致放置点与几何受到弧线拟合影响错位
        # 错位导致了放置点坐标轴，与几何不在一起，所以需要旋转扫略体后再布尔
        x = L/2
        z = -math.sqrt(R**2 - (L/2)**2)
        angle_rad = math.atan2(z, x)
        angle_deg = math.degrees(angle_rad)
        
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
        # body = combine(扫掠体,切割体1,切割体2,切割体3)
        最终模型 = translate(L/2,0,-sqrt(R**2-(L/2)**2))*body
        self['拱形屋面_单拱'] = 最终模型
        

       
# 输出模型
if __name__ == "__main__":
    FinalGeometry = 拱形屋面_单拱()
    place(FinalGeometry)
