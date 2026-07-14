from pyp3d import *

class 长方台体(Component):
    def __init__(self):
        Component.__init__(self)
        # 定义参数
        self['顶部长度'] = Attr(2500.0, obvious=True, readonly=False)
        self['顶部宽度'] = Attr(1500.0, obvious=True, readonly=False)
        self['底部长度'] = Attr(1500.0, obvious=True, readonly=False)
        self['底部宽度'] = Attr(900.0, obvious=True, readonly=False)
        self['高度'] = Attr(1200.0, obvious=True, readonly=False)
        self['长方台体'] = Attr(None, show=True)
        
        self.replace()
    
    @export
    def replace(self):
        # 获取参数值
        top_length = self['顶部长度']
        top_width = self['顶部宽度']
        bottom_length = self['底部长度']
        bottom_width = self['底部宽度']
        height = self['高度']
        
        # 创建长方台体
        # Box(baseOrigin, topOrigin, vectorX, vectorY, baseX, baseY, topX, topY)
        frustum = Box(
            Vec3(0, 0, -height/2),  # 底部原点
            Vec3(0, 0, height/2),   # 顶部原点
            Vec3(1, 0, 0),          # 局部坐标系基矢X
            Vec3(0, 1, 0),          # 局部坐标系基矢Y
            bottom_length,          # 底部长度
            bottom_width,           # 底部宽度
            top_length,             # 顶部长度
            top_width               # 顶部宽度
        )
        
        # 赋值给组件
        self['长方台体'] = frustum

if __name__ == "__main__":
    FinalGeometry = 长方台体()
    place(FinalGeometry)