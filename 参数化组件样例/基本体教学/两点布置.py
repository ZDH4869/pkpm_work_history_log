from pyp3d import *
# 定义参数化模型
class 立方体(Component):
    # 定义各个参数及其默认值
    def __init__(self):
        Component.__init__(self)
        self['长'] = Attr(1000.0, obvious = True)
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
        H = self['高']
        # 绘制模型
        TestCube = scale(L,W,H) * Cube()
        # TestCube = rotate(Vec3(0,1,0),0.5*pi) * scale(L,W,H) * Cube()
        self['立方体'] = TestCube
# 输出模型
if __name__ == "__main__":
    # 只需加上下面两行即可实现两点布置
    # 第一行 对【立方体】这个class进行装饰
    FinalGeometry = 立方体()
    # 第二行 实现旋转布置
    TwoPointPlace.linearize(FinalGeometry,'长')
    place(FinalGeometry)
