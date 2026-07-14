from pyp3d import *

class 直角梯形拉伸体(Component):
    def __init__(self):
        Component.__init__(self)
        # 定义参数
        self['侧面梯形底边长'] = Attr(2500.0, obvious=True, readonly=False)
        self['侧面梯形顶边长'] = Attr(1500.0, obvious=True, readonly=False)
        self['侧面梯形高'] = Attr(800.0, obvious=True, readonly=False)
        self['拉伸长度'] = Attr(1500.0, obvious=True, readonly=False)
        self['直角梯形拉伸体'] = Attr(None, show=True)
        
        self.replace()
    
    @export
    def replace(self):
        # 获取参数值
        base_length = self['侧面梯形底边长']
        top_length = self['侧面梯形顶边长']
        height = self['侧面梯形高']
        extrude_length = self['拉伸长度']
        
        # 创建直角梯形截面（放在XZ平面）
        # 直角梯形的四个顶点：(0,0,0), (base_length,0,0), (top_length,0,height), (0,0,height)
        section = Section(
            Vec3(0, 0, 0),
            Vec3(base_length, 0, 0),
            Vec3(top_length, 0, height),
            Vec3(0, 0, height)
        )
        
        # 创建拉伸轨迹（Y方向）
        path = Line(Vec3(0, 0, 0), Vec3(0, extrude_length, 0))
        
        # 执行拉伸操作
        extrude = Sweep(section, path)
        
        # 赋值给组件
        self['直角梯形拉伸体'] = extrude
        
        # 设置驱动点
        # 左侧面（Y=0）的四个角点
        self.setDrivenFeaturePoint('left_front_bottom', SnapMode.EndPoint, '[X]', '[Y]', '[Z]')
        self.setDrivenFeaturePoint('left_back_bottom', SnapMode.EndPoint, '[侧面梯形底边长]', '[Y]', '[Z]')
        self.setDrivenFeaturePoint('left_back_top', SnapMode.EndPoint, '[侧面梯形顶边长]', '[Y]', '[侧面梯形高]')
        self.setDrivenFeaturePoint('left_front_top', SnapMode.EndPoint, '[X]', '[Y]', '[侧面梯形高]')
        
        # 右侧面（Y=拉伸长度）的四个角点
        self.setDrivenFeaturePoint('right_front_bottom', SnapMode.EndPoint, '0', '[拉伸长度]', '0')
        self.setDrivenFeaturePoint('right_back_bottom', SnapMode.EndPoint, '[侧面梯形底边长]', '[拉伸长度]', '0')
        self.setDrivenFeaturePoint('right_back_top', SnapMode.EndPoint, '[侧面梯形顶边长]', '[拉伸长度]', '[侧面梯形高]')
        self.setDrivenFeaturePoint('right_front_top', SnapMode.EndPoint, '0', '[拉伸长度]', '[侧面梯形高]')

if __name__ == "__main__":
    FinalGeometry = 直角梯形拉伸体()
    place(FinalGeometry)