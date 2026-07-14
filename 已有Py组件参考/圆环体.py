from pyp3d import *

class 圆环体(Component):
    def __init__(self):
        Component.__init__(self)
        # 定义参数
        self['内环直径'] = Attr(1800.0, obvious=True, readonly=False)
        self['外环直径'] = Attr(2000.0, obvious=True, readonly=False)
        self['圆环高度'] = Attr(500.0, obvious=True, readonly=False)
        self['圆环体'] = Attr(None, show=True)
        
        # 设置驱动点
        self.setDrivenFeaturePoint('top_center', SnapMode.GeometricCenter, '[定位点X]', '[定位点Y]', '[定位点Z]+[圆环高度]/2')
        self.setDrivenFeaturePoint('bottom_center', SnapMode.GeometricCenter, '[定位点X]', '[定位点Y]', '[定位点Z]-[圆环高度]/2')
        
        self.replace()
    
    @export
    def replace(self):
        # 获取参数值
        inner_diameter = self['内环直径']
        outer_diameter = self['外环直径']
        height = self['圆环高度']
        
        # 计算半径
        inner_radius = inner_diameter / 2
        outer_radius = outer_diameter / 2
        
        # 创建外环圆柱（被减体）
        outer_cylinder = Cone(Vec3(0, 0, -height/2), Vec3(0, 0, height/2), outer_radius, outer_radius)
        
        # 创建内环圆柱（减体）
        inner_cylinder = Cone(Vec3(0, 0, -height/2), Vec3(0, 0, height/2), inner_radius, inner_radius)
        
        # 布尔相减得到圆环体
        torus = outer_cylinder - inner_cylinder
        
        # 赋值给组件
        self['圆环体'] = torus

if __name__ == "__main__":
    FinalGeometry = 圆环体()
    place(FinalGeometry)