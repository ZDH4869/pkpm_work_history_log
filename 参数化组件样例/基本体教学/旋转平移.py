from pyp3d import *
# 定义参数化模型
class 立方体(Component):
    # 定义各个参数及其默认值
    def __init__(self):
        Component.__init__(self)
        self['长'] = Attr(1000.0, obvious = True, readonly = True)
        # obvious 属性的可见性 True时可见，False为不可见。默认为False
        # readonly 属性的只读性 True时不可调，为置灰状态，False为可调状态。默认为False
        self['宽'] = Attr(300.0, obvious = True)
        self['高'] = Attr(500, obvious = True)
        self['立方体'] = Attr(None, show = True)
        self.replace()
    @export
    # 模型造型
    def replace(self): 
        # 设置变量，同时调用参数(简化书写过程)
        L = self['长']
        W = self['宽']
        H = self['宽']
        # 绘制模型

        # 平移
        TestCube = translate(Vec3(1000,1000,1000)) * scale(L,W,H) * Cube()
        # TestCube = translate(1000,1000,1000) * scale(L,W,H) * Cube()
        # TestCube = translate(1000,1000) * scale(L,W,H) * Cube()

        # 旋转
        TestCube = rotate(0.5*pi) * scale(L,W,H) * Cube()
        # TestCube = rotate(Vec3(0,0,1),0.5*pi) * scale(L,W,H) * Cube()

        # 平移+旋转 就近原则
        TestCube = translate(1000,0,0) * rotate(Vec3(0,0,1),0.5*pi) * scale(L,W,H) * Cube()
        TestCube = rotate(Vec3(0,0,1),0.5*pi) * translate(1000,0,0) * scale(L,W,H) * Cube()
        
        self['立方体'] = TestCube
# 输出模型
if __name__ == "__main__":
    FinalGeometry = 立方体()
    place(FinalGeometry)
