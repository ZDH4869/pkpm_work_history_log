from pyp3d import *
import math


class 椭底面半椭球(Component):
    def __init__(self):
        Component.__init__(self)
        self['构件名称'] = Attr('椭底面半椭球', obvious=True, readonly=True)
        self['半长轴'] = Attr(1000.0, obvious=True)
        self['半短轴'] = Attr(700.0, obvious=True)
        self['椭球高度'] = Attr(500.0, obvious=True)
        self['椭底面半椭球'] = Attr(None, show=True)
        self.replace()

    @export
    def replace(self):
        # ========== 读取参数 ==========
        ax = max(float(self['半长轴']), 1e-3)
        by = max(float(self['半短轴']), 1e-3)
        cz = max(float(self['椭球高度']), 1e-3)

        # ========== 半椭球：底面椭圆截面（XOY面），沿+Z方向拉伸 ==========
        n = 25
        if n % 2 == 0:
            n += 1
        sections = []
        eps = 1e-3
        for i in range(n):
            t = 1.0 * i / (n - 1)                # t ∈ [0, 1]，底面→顶点
            z_local = cz * t                      # 当前截面高度
            scale_xy = math.sqrt(max(0.0, 1.0 - t * t))  # 椭球方程缩放因子
            rx = max(ax * scale_xy, eps)          # X方向截面半径
            ry = max(by * scale_xy, eps)          # Y方向截面半径
            sections.append(
                translate(0, 0, z_local) * scale(rx, ry) * Section(Arc(2 * math.pi))
            )
        half_ellipsoid = Loft(*sections)
        half_ellipsoid.smooth = True

        self['椭底面半椭球'] = half_ellipsoid


if __name__ == "__main__":
    FinalGeometry = 椭底面半椭球()
    place(FinalGeometry)