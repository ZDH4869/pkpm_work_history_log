from pyp3d import *

# 测试3：含/不含 [定位点X/Y/Z] — 验证是否导致驱动点不跟随插入点
# 插入到 (100,100,0) 后观察两个点的世界坐标：
#   center_含定位点 → 应位于 (600, 850, 250) 跟随插入点
#   center_不含定位点 → 应位于 (500, 750, 250) 原地不动

class 定位点测试(Component):
    def __init__(self):
        Component.__init__(self)
        self['长方体长度'] = Attr(1000.0, obvious=True)
        self['长方体宽度'] = Attr(1500.0, obvious=True)
        self['长方体高度'] = Attr(500.0, obvious=True)
        self['长方体'] = Attr(None, show=True)

        # center_含定位点：三轴都含 [定位点X/Y/Z]
        self.setDrivenFeaturePoint('center_含定位点', SnapMode.GeometricCenter,
            '[定位点X]+[长方体长度]/2',
            '[定位点Y]+[长方体宽度]/2',
            '[定位点Z]+[长方体高度]/2')
        # center_不含定位点：三轴都不含 [定位点X/Y/Z]
        self.setDrivenFeaturePoint('center_不含定位点', SnapMode.GeometricCenter,
            '[长方体长度]/2',
            '[长方体宽度]/2',
            '[长方体高度]/2')

        self.replace()

    @export
    def replace(self):
        L = self['长方体长度']
        W = self['长方体宽度']
        H = self['长方体高度']
        self['长方体'] = translate(L/2, W/2, H/2) * scale(L, W, H) * Cube()


if __name__ == "__main__":
    place(定位点测试())
