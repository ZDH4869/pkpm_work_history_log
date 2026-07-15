from pyp3d import *

# 测试2：括号 () vs 展开 — 验证括号是否真的导致驱动点失效
# 结果：椭圆球.py 使用嵌套括号工作正常 → 括号不是问题
# 预期：两个驱动点都应显示在长方体右上角 (1000, 1500, 500)

class 括号vs展开测试(Component):
    def __init__(self):
        Component.__init__(self)
        self['长方体长度'] = Attr(1000.0, obvious=True)
        self['长方体宽度'] = Attr(1500.0, obvious=True)
        self['长方体高度'] = Attr(500.0, obvious=True)
        self['长方体'] = Attr(None, show=True)

        # point_括号：使用括号 () 分组
        self.setDrivenFeaturePoint('point_括号', SnapMode.EndPoint,
            '[定位点X]+([长方体长度]+[长方体宽度]-[长方体宽度])',
            '[定位点Y]+[长方体宽度]',
            '[定位点Z]+([长方体高度]+[长方体高度]-[长方体高度])')
        # point_展开：不使用括号，等效表达式
        self.setDrivenFeaturePoint('point_展开', SnapMode.EndPoint,
            '[定位点X]+[长方体长度]+[长方体宽度]-[长方体宽度]',
            '[定位点Y]+[长方体宽度]',
            '[定位点Z]+[长方体高度]+[长方体高度]-[长方体高度]')

        self.replace()

    @export
    def replace(self):
        L = self['长方体长度']
        W = self['长方体宽度']
        H = self['长方体高度']
        self['长方体'] = translate(L/2, W/2, H/2) * scale(L, W, H) * Cube()


if __name__ == "__main__":
    place(括号vs展开测试())
