from pyp3d import *

# 测试4（核心假说 ★ 已证实）：验证非 obvious 的隐藏 Attr 导致驱动点引用失败
# 对照实验已证实：椭圆球 copy.py 中 [椭球体长度] 设为 obvious=False 后，
# point2 和 point3（引用该参数）消失，point1 和 point4（未引用）正常显示。
# 本测试在长方体上重现此验证。
#
# 预期（插入后点"点锁定"）：
#   center_obvious  → 显示在几何中心 (500, 750, 250)  ← 应该正常
#   center_hidden   → 不显示，或显示在错误位置        ← 隐藏参数导致失败
#   center_mixed    → 不显示，或显示在错误位置        ← 混入隐藏参数导致整体失败

class Attr引用测试(Component):
    def __init__(self):
        Component.__init__(self)
        self['长方体长度'] = Attr(1000.0, obvious=True)   # 可见
        self['长方体宽度'] = Attr(1500.0, obvious=True)   # 可见
        self['长方体高度'] = Attr(500.0)                   # 隐藏！
        self['长方体'] = Attr(None, show=True)

        # center_obvious：只引用 obvious 参数，Z 用常数
        self.setDrivenFeaturePoint('center_obvious', SnapMode.GeometricCenter,
            '[定位点X]+[长方体长度]/2',
            '[定位点Y]+[长方体宽度]/2',
            '[定位点Z]+250')

        # center_hidden：只引用隐藏参数 [长方体高度]
        self.setDrivenFeaturePoint('center_hidden', SnapMode.GeometricCenter,
            '[定位点X]+500',
            '[定位点Y]+750',
            '[定位点Z]+[长方体高度]/2')

        # center_mixed：同时引用 obvious 和隐藏参数
        self.setDrivenFeaturePoint('center_mixed', SnapMode.GeometricCenter,
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
    place(Attr引用测试())
