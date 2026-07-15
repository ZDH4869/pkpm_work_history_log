from pyp3d import *

# 测试1：*0.5 vs /2 — 验证小数乘法是否真的导致驱动点失效
# 结果：椭圆球.py 大量使用 * 和 **，证明 *0.5 不是问题根源
# 预期：两个驱动点都应显示在几何中心 (500, 750, 250)

class 乘05vs除2测试(Component):
    def __init__(self):
        Component.__init__(self)
        self['长方体长度'] = Attr(1000.0, obvious=True)
        self['长方体宽度'] = Attr(1500.0, obvious=True)
        self['长方体高度'] = Attr(500.0, obvious=True)
        self['长方体'] = Attr(None, show=True)

        # center_乘05：使用 *0.5 语法 → 预期正常显示
        self.setDrivenFeaturePoint('center_乘05', SnapMode.GeometricCenter,
            '[定位点X]+[长方体长度]*0.5',
            '[定位点Y]+[长方体宽度]*0.5',
            '[定位点Z]+[长方体高度]*0.5')
        # center_除2：使用 /2 语法 → 对照
        self.setDrivenFeaturePoint('center_除2', SnapMode.GeometricCenter,
            '[定位点X]+[长方体长度]/2',
            '[定位点Y]+[长方体宽度]/2',
            '[定位点Z]+[长方体高度]/2')

        self.replace()

    @export
    def replace(self):
        L = self['长方体长度']
        W = self['长方体宽度']
        H = self['长方体高度']
        self['长方体'] = translate(L/2, W/2, H/2) * scale(L, W, H) * Cube()


if __name__ == "__main__":
    place(乘05vs除2测试())
