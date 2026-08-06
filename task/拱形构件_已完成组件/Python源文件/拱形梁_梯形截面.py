from pyp3d import *
# 定义参数化模型
class 拱形梁_梯形截面(Component):
    # 定义各个参数及其默认值
    def __init__(self):
        Component.__init__(self)
        self['构件名称']=Attr('拱形梁_梯形截面', obvious = True, readonly = False)
        self['拱形半径']=Attr(13000, obvious = True, readonly = False)
        self['弦长']=Attr(18000, obvious = True)
        self['上底宽'] = Attr(600.0, obvious = True)
        self['下底宽'] = Attr(400.0, obvious = True)
        self['截面高']=Attr(900.0, obvious = True) 
        
        # obvious 属性的可见性 True时可见，False为不可见。默认为False
        # readonly 属性的只读性 True时不可调，为置灰状态，False为可调状态。默认为False
        self['拱形梁_梯形截面'] = Attr(None, show = True)
        
        self.replace()
    @export
    # 模型造型
    def replace(self): 
        # 设置变量，同时调用参数(简化书写过程)
        R = self['拱形半径']
        L = self['弦长']
        H  = self['截面高']
        W1  = self['上底宽']
        W2  = self['下底宽']
        
        # 计算扫掠路径的旋转角度
        # 旋转角度为 L/2 到 R 的角度
        # 扫略体如果直接用弦长两侧的切割体布尔，会导致放置点与几何受到弧线拟合影响错位
        # 错位导致了放置点坐标轴，与几何不在一起，所以需要旋转扫略体后再布尔
        x = L/2
        z = -math.sqrt(R**2 - (L/2)**2)
        angle_rad = math.atan2(z, x)
        angle_deg = math.degrees(angle_rad)
       
        # 绘制模型    
        扫掠路径 = roty(-angle_rad)*rotx(pi/2)*scale(R,R)*Line(Arc(pi))
        扫掠平面 = Section(Vec2(R,0),Vec2(R,W1),Vec2(R-H,(W1+W2)/2),Vec2(R-H,(W1-W2)/2))        
        扫掠体_1 = Sweep(扫掠平面,扫掠路径)
        扫掠体_2 = roty(pi)*Sweep(扫掠平面,扫掠路径)
        切割体1 = translate(Vec3(L/2,0,0))*scale(R-L/2,W1,R)*Cube()        
        切割体2 = translate(Vec3(-R,0,0))*scale(R-L/2,W1,R)*Cube() 
        切割体3 = translate(Vec3(-R*1.5,-W1/2,-R*1.5))*scale(R*3,W1*2,R*1.5)*Cube() 
        body = 扫掠体_1+扫掠体_2-切割体1-切割体2-切割体3 
        # body = combine(扫掠体,切割体1,切割体2,切割体3) 
        最终模型 = translate(L/2,-W1/2,-sqrt(R**2-(L/2)**2))*body
        self['拱形梁_梯形截面'] = 最终模型
        

       
# 输出模型
if __name__ == "__main__":
    FinalGeometry = 拱形梁_梯形截面()
    place(FinalGeometry)
