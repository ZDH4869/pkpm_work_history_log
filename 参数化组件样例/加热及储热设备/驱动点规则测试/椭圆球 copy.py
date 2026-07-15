from pyp3d import *
# 定义参数化模型
class 椭圆球(Component):
    # 定义各个参数及其默认值
    def __init__(self):
        Component.__init__(self)
        self['椭球体直径']=Attr(600.0, obvious = True)
        self['椭球体长度']=Attr(700.0, obvious = False)
        self['空心圆内径']=Attr(400.0, obvious = True) 
        self['凸圆柱高'] = Attr(120.0, obvious = True)
        self['凸圆柱直径'] = Attr(400.0, obvious = True)
        # obvious 属性的可见性 True时可见，False为不可见。默认为False
        # readonly 属性的只读性 True时不可调，为置灰状态，False为可调状态。默认为False
        self['椭圆球'] = Attr(None, show = True)
        # 设置定位点
        self.setDrivenFeaturePoint('point1', SnapMode.EndPoint, '[定位点X]', '[定位点Y]', '[定位点Z]')
        self.setDrivenFeaturePoint('point2', SnapMode.EndPoint, '[定位点X]+(([椭球体长度]**2*[椭球体直径]**2-[椭球体长度]**2*[空心圆内径]**2)/(4*[椭球体直径]**2))**0.5', '[定位点Y]', '[定位点Z]')
        self.setDrivenFeaturePoint('point3', SnapMode.EndPoint, '[定位点X]-(([椭球体长度]**2*[椭球体直径]**2-[椭球体长度]**2*[空心圆内径]**2)/(4*[椭球体直径]**2))**0.5', '[定位点Y]', '[定位点Z]')
        self.setDrivenFeaturePoint('point4', SnapMode.GeometricCenter, '[定位点X]', '[定位点Y]', '[定位点Z]+[空心圆内径]/2+[凸圆柱高]')
        self.replace()
    @export
    # 模型造型
    def replace(self): 
        # 设置变量，同时调用参数(简化书写过程)
        Tb = self['椭球体直径']/2
        Ta = self['椭球体长度']/2
        r = self['空心圆内径']/2
        Ch = self['凸圆柱高']
        Cr = self['凸圆柱直径']/2 
        # 绘制模型
        # 绘制椭球体
        Line1 = roty(pi/2)*Line(scale(Tb)*Arc(pi*2))
        Section1 = scale(Ta,Tb)*Section(Arc(pi))
        FinalSphere = Sweep(Section1,Line1)
        # 绘制空心圆柱
        TestCone = Cone(Vec3(-Ta,0,0),Vec3(Ta,0,0),r)
        # 绘制凸圆柱
        TestCone1 = Cone(Vec3(0,0,r),Vec3(0,0,r+Ch),Cr)
        self['椭圆球'] = FinalSphere-TestCone+TestCone1
# 输出模型
if __name__ == "__main__":
    FinalGeometry = 椭圆球()
    place(FinalGeometry)
